from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    """Modèle utilisateur - Version complète avec tous les champs"""
    
    # Champs de base
    id: int = 0
    username: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    user_type: str = "client"
    
    # Champs optionnels
    phone_number: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    profile_picture: Optional[str] = None
    date_joined: Optional[str] = None
    last_login: Optional[str] = None
    
    # Statut
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False
    
    @property
    def full_name(self) -> str:
        """Retourne le nom complet"""
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username
    
    def __post_init__(self):
        """Conversion des types après initialisation"""
        # Convertir les IDs
        if isinstance(self.id, str):
            try:
                self.id = int(self.id)
            except:
                self.id = 0
        
        # Convertir les booléens
        for field in ['is_active', 'is_staff', 'is_superuser']:
            value = getattr(self, field)
            if isinstance(value, str):
                setattr(self, field, value.lower() == 'true')
        
        # Formater la date de naissance si présente
        if self.date_of_birth and isinstance(self.date_of_birth, str):
            try:
                # Garder le format original
                pass
            except:
                self.date_of_birth = None

@dataclass
class Hotel:
    """Modèle hôtel"""
    id: int = 0
    name: str = ""
    description: str = ""
    address: str = ""
    city: str = ""
    country: str = "France"
    stars: int = 3
    email: str = ""
    phone: str = ""
    created_at: str = ""
    updated_at: str = ""
    
    # Équipements
    has_wifi: bool = False
    has_parking: bool = False
    has_pool: bool = False
    has_spa: bool = False
    has_restaurant: bool = False
    has_gym: bool = False
    
    # Coordonnées
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Images
    images: List[str] = field(default_factory=list)
    
    def get_stars_display(self) -> str:
        """Retourne la représentation des étoiles"""
        return '★' * self.stars

@dataclass
class RoomType:
    """Modèle type de chambre"""
    id: int = 0
    hotel_id: int = 0
    name: str = ""
    room_type: str = "standard"
    description: str = ""
    capacity: int = 2
    price_per_night: float = 0.0
    size: int = 20
    quantity_available: int = 0
    
    # Équipements
    has_tv: bool = True
    has_ac: bool = True
    has_minibar: bool = False
    has_safe: bool = False
    has_balcony: bool = False
    is_smoking: bool = False
    
    # Informations liées
    hotel_name: Optional[str] = None
    hotel_city: Optional[str] = None
    images: List[str] = field(default_factory=list)
    
    def get_room_type_display(self) -> str:
        """Retourne le type de chambre en français"""
        types = {
            'single': 'Chambre Simple',
            'double': 'Chambre Double',
            'twin': 'Chambre Twin',
            'suite': 'Suite',
            'family': 'Chambre Familiale',
            'presidential': 'Suite Présidentielle',
            'standard': 'Chambre Standard',
        }
        return types.get(self.room_type, self.room_type)

@dataclass
class Booking:
    """Modèle réservation"""
    id: int = 0
    user_id: int = 0
    room_type_id: int = 0
    check_in_date: str = ""
    check_out_date: str = ""
    number_of_rooms: int = 1
    number_of_guests: int = 2
    total_price: float = 0.0
    status: str = "pending"
    created_at: str = ""
    updated_at: str = ""
    
    special_requests: Optional[str] = None
    cancellation_reason: Optional[str] = None
    
    # Relations
    room_type: Optional[RoomType] = None
    user: Optional[User] = None
    payment: Optional['Payment'] = None
    
    @property
    def number_of_nights(self) -> int:
        """Calcule le nombre de nuits"""
        try:
            check_in = datetime.strptime(self.check_in_date, '%Y-%m-%d').date()
            check_out = datetime.strptime(self.check_out_date, '%Y-%m-%d').date()
            return (check_out - check_in).days
        except:
            return 0
    
    def get_status_display(self) -> str:
        """Retourne le statut en français"""
        status_map = {
            'pending': 'En attente',
            'confirmed': 'Confirmée',
            'cancelled': 'Annulée',
            'completed': 'Terminée',
        }
        return status_map.get(self.status, self.status)
    
    @property
    def can_cancel(self) -> bool:
        """Vérifie si la réservation peut être annulée"""
        if self.status in ['cancelled', 'completed']:
            return False
        try:
            check_in = datetime.strptime(self.check_in_date, '%Y-%m-%d').date()
            days_before = (check_in - datetime.now().date()).days
            return days_before > 1
        except:
            return False

@dataclass
class Payment:
    """Modèle paiement"""
    id: int = 0
    booking_id: int = 0
    amount: float = 0.0
    payment_method: str = "credit_card"
    payment_status: str = "pending"
    transaction_id: str = ""
    created_at: str = ""
    payment_date: Optional[str] = None
    
    def get_payment_status_display(self) -> str:
        """Retourne le statut de paiement en français"""
        status_map = {
            'pending': 'En attente',
            'completed': 'Complété',
            'failed': 'Échoué',
            'refunded': 'Remboursé',
        }
        return status_map.get(self.payment_status, self.payment_status)
    
    def get_payment_method_display(self) -> str:
        """Retourne la méthode de paiement en français"""
        method_map = {
            'credit_card': 'Carte de crédit',
            'paypal': 'PayPal',
            'bank_transfer': 'Virement bancaire',
        }
        return method_map.get(self.payment_method, self.payment_method)

@dataclass
class CancellationPolicy:
    """Modèle politique d'annulation"""
    id: int = 0
    hotel_id: int = 0
    days_before_checkin: int = 0
    penalty_percentage: int = 0
    description: str = ""

@dataclass
class SearchFilters:
    """Filtres de recherche"""
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    city: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    stars: Optional[int] = None
    number_of_rooms: int = 1
    number_of_guests: int = 2
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire pour l'API"""
        data = {}
        if self.check_in:
            data['check_in'] = self.check_in
        if self.check_out:
            data['check_out'] = self.check_out
        if self.city:
            data['city'] = self.city
        if self.min_price:
            data['min_price'] = self.min_price
        if self.max_price:
            data['max_price'] = self.max_price
        if self.stars:
            data['stars'] = self.stars
        data['number_of_rooms'] = self.number_of_rooms
        data['number_of_guests'] = self.number_of_guests
        return data