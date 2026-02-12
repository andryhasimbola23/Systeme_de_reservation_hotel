import os
from kivy.utils import platform

# Configuration de l'API Django
API_BASE_URL = "http://127.0.0.1:8000"  # Pour développement local
# API_BASE_URL = "http://192.168.1.100:8000"  # Remplacez par l'IP de votre serveur Django

# Endpoints API
API_ENDPOINTS = {
    'login': '/api/auth/login/',
    'register': '/api/auth/register/',
    'profile': '/api/auth/profile/',
    'hotels': '/api/hotels/',
    'hotel_detail': '/api/hotels/{id}/',
    'search': '/api/hotels/search/',
    'bookings': '/api/bookings/',
    'my_bookings': '/api/bookings/my-bookings/',
    'booking_detail': '/api/bookings/{id}/',
    'process_payment': '/api/bookings/{id}/pay/',
    'cancellation_policies': '/api/bookings/hotel/{id}/cancellation-policies/',
}

# Configuration de l'application
APP_CONFIG = {
    'app_name': 'Hotel Reservation',
    'version': '1.0.0',
    'company': 'HotelReservation Inc.',
    'support_email': 'support@hotelreservation.com',
}

# Chemins des ressources
if platform == 'android':
    ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
else:
    ASSETS_PATH = 'assets'

# ✅ Configuration des couleurs - CORRIGÉE
COLORS = {
    'primary': '#2563eb',
    'primary_dark': '#1d4ed8',
    'secondary': '#64748b',
    'accent': '#0ea5e9',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'light': '#f8fafc',
    'dark': '#1e293b',
    'gray': '#94a3b8',
    'gray_light': '#e2e8f0',      # Ajouté
    'gray_dark': '#475569',       # ✅ Ajouté - c'est celui qui manquait
    'white': '#ffffff',
    'black': '#000000',
    'transparent': (0, 0, 0, 0),
}

# Configuration du stockage
if platform == 'android':
    try:
        from android.storage import app_storage_path
        STORAGE_PATH = app_storage_path()
    except:
        STORAGE_PATH = os.path.join(os.path.expanduser('~'), '.hotel_reservation')
else:
    STORAGE_PATH = os.path.join(os.path.expanduser('~'), '.hotel_reservation')

# Créer le dossier de stockage s'il n'existe pas
os.makedirs(STORAGE_PATH, exist_ok=True)