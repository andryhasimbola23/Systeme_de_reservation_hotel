# Dans hotel_app.py, assurez-vous que tous les écrans ont le bon nom

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform

# Import des écrans
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.home_screen import HomeScreen
from screens.hotels_screen import HotelsScreen
from screens.hotel_detail_screen import HotelDetailScreen
from screens.search_screen import SearchScreen
from screens.booking_screen import BookingsScreen
from screens.booking_detail_screen import BookingDetailScreen
from screens.create_booking_screen import CreateBookingScreen
from screens.profile_screen import ProfileScreen

from api.api_client import api_client
from config import COLORS

class HotelApp(App):
    def build(self):
        # Configuration de la fenêtre
        if platform == 'android':
            Window.fullscreen = 'auto'
        else:
            Window.size = (360, 640)
            Window.top = 50
            Window.left = 50
        
        Window.clearcolor = (0.97, 0.97, 0.97, 1)
        
        # Créer le gestionnaire d'écrans
        self.sm = ScreenManager(transition=FadeTransition(duration=0.3))
        
        # ✅ AJOUTER LES ÉCRANS AVEC LEURS NOMS CORRECTS
        screens = [
            LoginScreen(name='login'),
            RegisterScreen(name='register'),
            HomeScreen(name='home'),           # Vérifiez que c'est bien 'home'
            HotelsScreen(name='hotels'),
            HotelDetailScreen(name='hotel_detail'),
            SearchScreen(name='search'),
            BookingsScreen(name='bookings'),
            BookingDetailScreen(name='booking_detail'),
            CreateBookingScreen(name='create_booking'),
            ProfileScreen(name='profile'),
        ]
        
        for screen in screens:
            self.sm.add_widget(screen)
            print(f"✅ Écran ajouté: {screen.name}")  # Debug
        
        # Déterminer l'écran de démarrage
        if api_client.is_authenticated():
            print("🔐 Utilisateur authentifié -> home")
            self.sm.current = 'home'
        else:
            print("🔐 Utilisateur non authentifié -> login")
            self.sm.current = 'login'
        
        return self.sm