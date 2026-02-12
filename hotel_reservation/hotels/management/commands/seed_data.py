import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hotels.models import Hotel, HotelImage, RoomType, RoomImage
from bookings.models import Booking, Payment, CancellationPolicy
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Peuple la base de données avec des données de test'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Début du peuplement des données...'))
        
        # 1. Créer des utilisateurs
        self.create_users()
        
        # 2. Créer des hôtels avec images
        hotels = self.create_hotels()
        
        # 3. Créer des types de chambres pour chaque hôtel
        for hotel in hotels:
            self.create_rooms_for_hotel(hotel)
        
        # 4. Créer des politiques d'annulation
        self.create_cancellation_policies(hotels)
        
        # 5. Créer des réservations de test
        self.create_bookings()
        
        self.stdout.write(self.style.SUCCESS('Données créées avec succès!'))
    
    def create_users(self):
        """Crée des utilisateurs de test"""
        users_data = [
            {'username': 'client1', 'email': 'client1@test.com', 'password': 'password123', 'user_type': 'client'},
            {'username': 'client2', 'email': 'client2@test.com', 'password': 'password123', 'user_type': 'client'},
            {'username': 'hotel_manager', 'email': 'manager@test.com', 'password': 'password123', 'user_type': 'hotel_manager'},
            {'username': 'admin_user', 'email': 'admin@test.com', 'password': 'password123', 'user_type': 'admin'},
        ]
        
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    user_type=user_data['user_type']
                )
                user.first_name = user_data['username'].capitalize()
                user.last_name = 'Test'
                user.save()
                self.stdout.write(f'Utilisateur créé: {user.username}')
    
    def create_hotels(self):
        """Crée des hôtels de test"""
        hotels_data = [
            {
                'name': 'Hôtel Plaza Paris',
                'city': 'Paris',
                'country': 'France',
                'stars': 5,
                'address': '25 Avenue Montaigne, 75008 Paris',
                'description': 'Un hôtel de luxe au cœur de Paris avec vue sur la Tour Eiffel.',
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_spa': True,
                'has_restaurant': True,
                'has_gym': True,
            },
            {
                'name': 'Hôtel Central Lyon',
                'city': 'Lyon',
                'country': 'France',
                'stars': 4,
                'address': '12 Rue de la République, 69002 Lyon',
                'description': 'Hôtel moderne au centre-ville de Lyon, proche du Vieux Lyon.',
                'has_wifi': True,
                'has_parking': False,
                'has_pool': True,
                'has_spa': False,
                'has_restaurant': True,
                'has_gym': True,
            },
            {
                'name': 'Hôtel Méditerranée Marseille',
                'city': 'Marseille',
                'country': 'France',
                'stars': 3,
                'address': '45 Corniche Kennedy, 13007 Marseille',
                'description': 'Hôtel avec vue sur la mer Méditerranée, proche du Vieux-Port.',
                'has_wifi': True,
                'has_parking': True,
                'has_pool': False,
                'has_spa': False,
                'has_restaurant': True,
                'has_gym': False,
            },
            {
                'name': 'Hôtel Montagne Chamonix',
                'city': 'Chamonix',
                'country': 'France',
                'stars': 4,
                'address': 'Route des Aiguilles du Midi, 74400 Chamonix',
                'description': 'Hôtel de montagne avec accès direct aux pistes de ski.',
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_spa': True,
                'has_restaurant': True,
                'has_gym': True,
            },
            {
                'name': 'Hôtel Plage Nice',
                'city': 'Nice',
                'country': 'France',
                'stars': 3,
                'address': 'Promenade des Anglais, 06000 Nice',
                'description': 'Hôtel face à la mer sur la célèbre Promenade des Anglais.',
                'has_wifi': True,
                'has_parking': False,
                'has_pool': False,
                'has_spa': False,
                'has_restaurant': True,
                'has_gym': False,
            },
        ]
        
        hotels = []
        for hotel_data in hotels_data:
            hotel = Hotel.objects.create(**hotel_data)
            hotels.append(hotel)
            self.stdout.write(f'Hôtel créé: {hotel.name} à {hotel.city}')
        
        return hotels
    
    def create_rooms_for_hotel(self, hotel):
        """Crée des chambres pour un hôtel"""
        rooms_data = [
            {
                'name': 'Chambre Simple Standard',
                'room_type': 'single',
                'description': 'Chambre simple avec lit simple, salle de bain privée.',
                'capacity': 1,
                'price_per_night': 80.00,
                'size': 18,
                'quantity_available': 10,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': False,
                'has_safe': True,
                'has_balcony': False,
            },
            {
                'name': 'Chambre Double Supérieure',
                'room_type': 'double',
                'description': 'Chambre double spacieuse avec lit queen size.',
                'capacity': 2,
                'price_per_night': 120.00,
                'size': 25,
                'quantity_available': 15,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': True,
                'has_safe': True,
                'has_balcony': True,
            },
            {
                'name': 'Suite Familiale',
                'room_type': 'family',
                'description': 'Suite avec chambre séparée et salon, idéale pour familles.',
                'capacity': 4,
                'price_per_night': 200.00,
                'size': 45,
                'quantity_available': 5,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': True,
                'has_safe': True,
                'has_balcony': True,
            },
            {
                'name': 'Suite Présidentielle',
                'room_type': 'presidential',
                'description': 'Suite de luxe avec vue panoramique et tous les services.',
                'capacity': 2,
                'price_per_night': 500.00,
                'size': 80,
                'quantity_available': 2,
                'has_tv': True,
                'has_ac': True,
                'has_minibar': True,
                'has_safe': True,
                'has_balcony': True,
            },
        ]
        
        for room_data in rooms_data:
            # Ajuster les prix selon le nombre d'étoiles
            price_multiplier = 1 + (hotel.stars - 3) * 0.2  # +20% par étoile au-dessus de 3
            room_data['price_per_night'] = round(room_data['price_per_night'] * price_multiplier, 2)
            
            room = RoomType.objects.create(hotel=hotel, **room_data)
            self.stdout.write(f'  Chambre créée: {room.name} - {room.price_per_night}€/nuit')
    
    def create_cancellation_policies(self, hotels):
        """Crée des politiques d'annulation pour chaque hôtel"""
        policies_data = [
            {'days_before_checkin': 30, 'penalty_percentage': 0, 'description': 'Annulation gratuite jusqu\'à 30 jours avant'},
            {'days_before_checkin': 14, 'penalty_percentage': 20, 'description': '20% de pénalité entre 14 et 30 jours'},
            {'days_before_checkin': 7, 'penalty_percentage': 50, 'description': '50% de pénalité entre 7 et 14 jours'},
            {'days_before_checkin': 0, 'penalty_percentage': 100, 'description': '100% de pénalité moins de 7 jours avant'},
        ]
        
        for hotel in hotels:
            for policy_data in policies_data:
                CancellationPolicy.objects.create(hotel=hotel, **policy_data)
            self.stdout.write(f'Politiques créées pour: {hotel.name}')
    
    def create_bookings(self):
        """Crée des réservations de test"""
        try:
            client = User.objects.get(username='client1')
            rooms = RoomType.objects.all()[:3]  # Prendre 3 premières chambres
            
            for i, room in enumerate(rooms):
                check_in = timezone.now().date() + timedelta(days=10 + i*7)
                check_out = check_in + timedelta(days=3 + i)
                
                booking = Booking.objects.create(
                    user=client,
                    room_type=room,
                    check_in_date=check_in,
                    check_out_date=check_out,
                    number_of_rooms=1 + (i % 2),  # 1 ou 2 chambres
                    number_of_guests=room.capacity,
                    total_price=room.price_per_night * (check_out - check_in).days * (1 + (i % 2)),
                    status=random.choice(['pending', 'confirmed', 'completed']),
                    special_requests=f'Test booking {i+1}'
                )
                
                # Créer un paiement associé
                Payment.objects.create(
                    booking=booking,
                    amount=booking.total_price,
                    payment_method=random.choice(['credit_card', 'paypal']),
                    payment_status='completed' if booking.status == 'confirmed' else 'pending',
                    transaction_id=f'TXN{booking.id:06d}',
                    payment_date=timezone.now() if booking.status == 'confirmed' else None
                )
                
                self.stdout.write(f'Réservation créée: #{booking.id} pour {room.hotel.name}')
        
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('Utilisateur client1 non trouvé, skip des réservations'))