from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import Clock

from api.api_client import api_client
from utils.helpers import helpers
from config import COLORS

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal avec ScrollView
        scroll_view = ScrollView()
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Header avec nom utilisateur
        header = BoxLayout(size_hint_y=None, height=dp(80))
        
        user_info = Label(
            text=f"[size=24]👋 Bonjour[/size]\n[size=18]{api_client.user.first_name or api_client.user.username}[/size]" 
                 if api_client.user else "[size=24]Bienvenue[/size]",
            markup=True,
            font_name='Roboto',
            halign='left',
            valign='middle',
            size_hint_x=0.7
        )
        user_info.bind(size=user_info.setter('text_size'))
        
        logout_button = Button(
            text='Déconnexion',
            size_hint_x=0.3,
            background_color=COLORS['danger'],
            color=(1, 1, 1, 1),
            font_size=dp(14)
        )
        logout_button.bind(on_press=self.on_logout)
        
        header.add_widget(user_info)
        header.add_widget(logout_button)
        
        # Statistiques
        stats_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(100))
        
        stats_data = [
            ('🏨', 'Hôtels', '0'),
            ('📅', 'Réservations', '0'),
            ('💰', 'Dépenses', '0€'),
            ('⭐', 'Note moyenne', '0.0'),
        ]
        
        for icon, title, value in stats_data:
            stat_box = BoxLayout(orientation='vertical', spacing=dp(5))
            stat_box.add_widget(Label(
                text=f"[size=32]{icon}[/size]",
                markup=True,
                halign='center'
            ))
            stat_box.add_widget(Label(
                text=f"[size=18][b]{value}[/b][/size]\n[size=12]{title}[/size]",
                markup=True,
                halign='center'
            ))
            stats_grid.add_widget(stat_box)
        
        # Menu principal
        menu_grid = GridLayout(cols=2, spacing=dp(15), size_hint_y=None, height=dp(300))
        
        menu_items = [
            ('🏨', 'Hôtels', 'hotels'),
            ('🔍', 'Rechercher', 'search'),
            ('📅', 'Mes réservations', 'bookings'),
            ('👤', 'Mon profil', 'profile'),
            ('⭐', 'Favoris', 'favorites'),
            ('📞', 'Contact', 'contact'),
        ]
        
        for icon, title, screen in menu_items:
            menu_button = Button(
                text=f"[size=32]{icon}[/size]\n[size=14]{title}[/size]",
                markup=True,
                background_color=COLORS['primary'],
                color=(1, 1, 1, 1),
                font_name='Roboto'
            )
            menu_button.bind(on_press=lambda instance, s=screen: self.on_menu_click(s))
            menu_grid.add_widget(menu_button)
        
        # Dernières réservations
        bookings_label = Label(
            text='[size=18][b]Dernières réservations[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=dp(40),
            halign='left'
        )
        bookings_label.bind(size=bookings_label.setter('text_size'))
        
        self.bookings_container = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(150)
        )
        
        # Ajouter tous les widgets
        main_layout.add_widget(header)
        main_layout.add_widget(stats_grid)
        main_layout.add_widget(menu_grid)
        main_layout.add_widget(bookings_label)
        main_layout.add_widget(self.bookings_container)
        
        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)
        
        # Charger les données
        Clock.schedule_once(lambda dt: self.load_data(), 0.5)
    
    def load_data(self):
        """Charge les données utilisateur"""
        if api_client.is_authenticated():
            # Charger les statistiques
            # Charger les dernières réservations
            self.update_bookings()
    
    def update_bookings(self):
        """Met à jour la liste des réservations"""
        self.bookings_container.clear_widgets()
        
        # Récupérer les réservations
        bookings = api_client.get_my_bookings()
        
        if bookings:
            for booking in bookings[:3]:  # 3 dernières
                booking_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(40),
                    padding=dp(10)
                )
                
                booking_box.add_widget(Label(
                    text=f"[size=14]{booking.room_type.hotel_name if booking.room_type else 'Hôtel'}[/size]",
                    markup=True,
                    halign='left',
                    size_hint_x=0.6
                ))
                
                booking_box.add_widget(Label(
                    text=f"[size=12]{helpers.format_date(booking.check_in_date)}[/size]",
                    markup=True,
                    halign='right',
                    size_hint_x=0.4
                ))
                
                self.bookings_container.add_widget(booking_box)
        else:
            self.bookings_container.add_widget(Label(
                text='Aucune réservation',
                color=COLORS['gray'],
                halign='center'
            ))
    
    def on_menu_click(self, screen):
        """Gère les clics sur le menu"""
        if screen in self.manager.screen_names:
            self.manager.current = screen
        else:
            print(f"Écran {screen} non trouvé")
    
    def on_logout(self, instance):
        """Déconnexion"""
        api_client.logout()
        self.manager.current = 'login'
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'
        else:
            self.load_data()