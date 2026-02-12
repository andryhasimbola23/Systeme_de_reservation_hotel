import requests
import json
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from kivy.storage.jsonstore import JsonStore

from config import API_BASE_URL, API_ENDPOINTS, STORAGE_PATH
from .models import User, Hotel, RoomType, Booking, Payment, CancellationPolicy, SearchFilters

class APIClient:
    """Client pour communiquer avec l'API Django"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.endpoints = API_ENDPOINTS
        self.token = None
        self.user = None
        self.store = JsonStore(f'{STORAGE_PATH}/app_data.json')
        
        # Charger le token et les données utilisateur depuis le stockage local
        self._load_auth_data()
    
    def _load_auth_data(self):
        """Charge les données d'authentification depuis le stockage local"""
        try:
            if 'auth' in self.store:
                auth_data = self.store.get('auth')
                self.token = auth_data.get('token')
                user_data = auth_data.get('user')
                if user_data:
                    self.user = User(**user_data)
        except:
            self.token = None
            self.user = None
    
    def _save_auth_data(self, token: str, user_data: dict):
        """Sauvegarde les données d'authentification"""
        self.token = token
        self.user = User(**user_data)
        self.store.put('auth', token=token, user=user_data)
    
    def _clear_auth_data(self):
        """Efface les données d'authentification"""
        self.token = None
        self.user = None
        try:
            self.store.delete('auth')
        except:
            pass
    
    def _get_headers(self) -> Dict[str, str]:
        """Retourne les headers pour les requêtes API"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Effectue une requête à l'API"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                timeout=10,
                **kwargs
            )
            
            if response.status_code == 401:
                # Token expiré ou invalide
                self._clear_auth_data()
                return None
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"API Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
    
    # ===== AUTHENTIFICATION =====
    
    def login(self, username: str, password: str) -> Optional[User]:
        """Connexion utilisateur"""
        data = {
            'username': username,
            'password': password
        }
        
        result = self._make_request('POST', self.endpoints['login'], json=data)
        
        if result and 'access' in result:
            token = result['access']
            user_data = result.get('user', {})
            self._save_auth_data(token, user_data)
            return self.user
        
        return None
    
    def register(self, username: str, email: str, password: str, 
                 first_name: str = '', last_name: str = '') -> Optional[User]:
        """Inscription utilisateur"""
        data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password,
            'first_name': first_name,
            'last_name': last_name,
        }
        
        result = self._make_request('POST', self.endpoints['register'], json=data)
        
        if result:
            # Après inscription, on se connecte automatiquement
            return self.login(username, password)
        
        return None
    
    def logout(self):
        """Déconnexion utilisateur"""
        self._clear_auth_data()
    
    def get_profile(self) -> Optional[User]:
        """Récupère le profil utilisateur"""
        result = self._make_request('GET', self.endpoints['profile'])
        
        if result:
            self.user = User(**result)
            # Mettre à jour le stockage local
            if self.token:
                self._save_auth_data(self.token, result)
            return self.user
        
        return None
    
    # ===== HOTELS =====
    
    def get_hotels(self, filters: Optional[Dict] = None) -> Optional[List[Hotel]]:
        params = filters or {}
        result = self._make_request('GET', self.endpoints['hotels'], params=params)
    
        if result:
            hotels = []
        
            # ✅ Vérifier le type de résultat
            if isinstance(result, list):
                for hotel_data in result:
                    # Si hotel_data est déjà un dictionnaire
                    if isinstance(hotel_data, dict):
                        try:
                            hotel = Hotel(**hotel_data)
                        
                        # Gérer les images
                            if 'images' in hotel_data:
                                hotel.images = [img['image'] for img in hotel_data['images'] if isinstance(img, dict)]
                        
                            hotels.append(hotel)
                        except Exception as e:
                            print(f"❌ Erreur création hôtel: {e}")
                            print(f"   Données: {hotel_data}")
                    else:
                        # Si c'est une string ou autre, on ignore ou on crée un objet minimal
                        print(f"⚠️ Format de données non valide pour hôtel: {hotel_data}")
        
            return hotels
    
        return None
    
    def get_hotel(self, hotel_id: int) -> Optional[Hotel]:
        """Récupère les détails d'un hôtel"""
        endpoint = self.endpoints['hotel_detail'].format(id=hotel_id)
        result = self._make_request('GET', endpoint)
        
        if result:
            hotel = Hotel(**result)
            
            # Gérer les images
            if 'images' in result:
                hotel.images = [img['image'] for img in result['images']]
            
            return hotel
        
        return None
    
    def search_hotels(self, filters: SearchFilters) -> Optional[List[RoomType]]:
        """Recherche d'hôtels avec filtres"""
        data = filters.to_dict()
        result = self._make_request('POST', self.endpoints['search'], json=data)
        
        if result:
            rooms = []
            for room_data in result:
                room = RoomType(**room_data)
                
                # Gérer les images
                if 'images' in room_data:
                    room.images = [img['image'] for img in room_data['images']]
                
                rooms.append(room)
            return rooms
        
        return None
    
    def get_hotel_rooms(self, hotel_id: int) -> Optional[List[RoomType]]:
        """Récupère les chambres d'un hôtel"""
        # Note: Cet endpoint doit être ajouté à votre API Django
        endpoint = f"/api/hotels/{hotel_id}/rooms/"
        result = self._make_request('GET', endpoint)
        
        if result:
            rooms = []
            for room_data in result:
                room = RoomType(**room_data)
                
                # Gérer les images
                if 'images' in room_data:
                    room.images = [img['image'] for img in room_data['images']]
                
                rooms.append(room)
            return rooms
        
        return None
    
    # ===== RESERVATIONS =====
    
    def get_my_bookings(self) -> Optional[List[Booking]]:
        """Récupère les réservations de l'utilisateur"""
        result = self._make_request('GET', self.endpoints['my_bookings'])
        
        if result:
            bookings = []
            for booking_data in result:
                # Convertir les données de la chambre
                room_type_data = booking_data.pop('room_type_details', {})
                if room_type_data:
                    room_type = RoomType(**room_type_data)
                    booking_data['room_type'] = room_type
                
                # Convertir les données de paiement
                payment_data = booking_data.pop('payment', None)
                if payment_data:
                    payment = Payment(**payment_data)
                    booking_data['payment'] = payment
                
                booking = Booking(**booking_data)
                bookings.append(booking)
            
            return bookings
        
        return None
    
    def get_booking(self, booking_id: int) -> Optional[Booking]:
        """Récupère les détails d'une réservation"""
        endpoint = self.endpoints['booking_detail'].format(id=booking_id)
        result = self._make_request('GET', endpoint)
        
        if result:
            # Convertir les données de la chambre
            room_type_data = result.pop('room_type_details', {})
            if room_type_data:
                room_type = RoomType(**room_type_data)
                result['room_type'] = room_type
            
            # Convertir les données de paiement
            payment_data = result.pop('payment', None)
            if payment_data:
                payment = Payment(**payment_data)
                result['payment'] = payment
            
            booking = Booking(**result)
            return booking
        
        return None
    
    def create_booking(self, room_type_id: int, check_in: str, check_out: str,
                      number_of_rooms: int = 1, number_of_guests: int = 2,
                      special_requests: str = '') -> Optional[Booking]:
        """Crée une nouvelle réservation"""
        data = {
            'room_type': room_type_id,
            'check_in_date': check_in,
            'check_out_date': check_out,
            'number_of_rooms': number_of_rooms,
            'number_of_guests': number_of_guests,
            'special_requests': special_requests,
        }
        
        result = self._make_request('POST', self.endpoints['bookings'], json=data)
        
        if result:
            # Récupérer les détails complets
            booking_id = result.get('id')
            if booking_id:
                return self.get_booking(booking_id)
        
        return None
    
    def cancel_booking(self, booking_id: int) -> bool:
        """Annule une réservation"""
        endpoint = self.endpoints['booking_detail'].format(id=booking_id)
        data = {'status': 'cancelled'}
        
        result = self._make_request('PATCH', endpoint, json=data)
        return result is not None
    
    def process_payment(self, booking_id: int) -> bool:
        """Simule un paiement"""
        endpoint = self.endpoints['process_payment'].format(id=booking_id)
        
        result = self._make_request('POST', endpoint)
        return result is not None
    
    def get_cancellation_policies(self, hotel_id: int) -> Optional[List[CancellationPolicy]]:
        """Récupère les politiques d'annulation d'un hôtel"""
        endpoint = self.endpoints['cancellation_policies'].format(id=hotel_id)
        result = self._make_request('GET', endpoint)
        
        if result:
            policies = [CancellationPolicy(**policy_data) for policy_data in result]
            return policies
        
        return None
    
    # ===== UTILITAIRES =====
    
    def is_authenticated(self) -> bool:
        """Vérifie si l'utilisateur est authentifié"""
        return self.token is not None and self.user is not None
    
    def check_connection(self) -> bool:
        """Vérifie la connexion à l'API"""
        try:
            response = requests.get(f"{self.base_url}/api/status/", timeout=5)
            return response.status_code == 200
        except:
            return False

# Instance globale du client API
api_client = APIClient()