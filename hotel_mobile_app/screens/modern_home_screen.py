from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

from components.modern_button import ModernButton, ModernButtonIcon
from components.modern_card import ModernCard, HotelCardModern
from components.modern_navbar import ModernNavBar
from api.api_client import api_client
from utils.helpers import helpers
from config import COLORS, SPACING, FONT_SIZES, BORDER_RADIUS

class ModernHomeScreen(Screen):
    """
    Écran d'accueil moderne avec tableau de bord
    """
    def __init__(self, **kwargs):
        # S'assurer que le nom est bien 'home'
        if 'name' not in kwargs:
            kwargs['name'] = 'home'
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal
        main = BoxLayout(orientation='vertical')
        
        # Header avec avatar et notifications
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            padding=[SPACING['lg'], SPACING['md']],
            spacing=SPACING['md']
        )
        
        with header.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            RoundedRectangle(
                pos=header.pos,
                size=header.size,
                radius=[0, 0, BORDER_RADIUS['lg'], BORDER_RADIUS['lg']]
            )
        
        # Greeting
        self.greeting_label = Label(
            text='Bonjour 👋',
            font_size=sp(FONT_SIZES['xl']),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            size_hint_x=0.6
        )
        self.greeting_label.bind(size=self.greeting_label.setter('text_size'))
        
        # Avatar
        avatar = BoxLayout(
            size_hint_x=0.2,
            size_hint_y=None,
            height=dp(50)
        )
        with avatar.canvas:
            Color(rgba=(0.2, 0.4, 0.8, 0.1))
            RoundedRectangle(
                pos=avatar.pos,
                size=avatar.size,
                radius=[BORDER_RADIUS['circle']]
            )
        avatar.add_widget(Label(
            text='👤',
            font_size=sp(24)
        ))
        
        # Notification
        notification = BoxLayout(
            size_hint_x=0.2,
            size_hint_y=None,
            height=dp(50)
        )
        with notification.canvas:
            Color(rgba=(0.95, 0.95, 0.95, 1))
            RoundedRectangle(
                pos=notification.pos,
                size=notification.size,
                radius=[BORDER_RADIUS['circle']]
            )
        notification.add_widget(Label(
            text='🔔',
            font_size=sp(20)
        ))
        
        header.add_widget(self.greeting_label)
        header.add_widget(avatar)
        header.add_widget(notification)
        
        # Content avec ScrollView
        scroll = ScrollView()
        content = BoxLayout(
            orientation='vertical',
            padding=SPACING['lg'],
            spacing=SPACING['lg'],
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Statistiques
        stats_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(100),
            spacing=SPACING['md']
        )
        
        stats = [
            {'value': '0', 'label': 'Hôtels', 'icon': '🏨'},
            {'value': '0', 'label': 'Réservations', 'icon': '📅'},
            {'value': '0€', 'label': 'Dépenses', 'icon': '💰'},
        ]
        
        self.stat_cards = []
        for stat in stats:
            card = ModernCard()
            card.padding = SPACING['md']
            card.size_hint_x = 1.0/3
            card.height = dp(100)
            
            stat_layout = BoxLayout(orientation='vertical')
            stat_layout.add_widget(Label(
                text=stat['icon'],
                font_size=sp(24),
                size_hint_y=None,
                height=dp(30)
            ))
            stat_layout.add_widget(Label(
                text=f'[b]{stat["value"]}[/b]',
                markup=True,
                font_size=sp(FONT_SIZES['lg']),
                color=(0.1, 0.1, 0.1, 1)
            ))
            stat_layout.add_widget(Label(
                text=stat['label'],
                font_size=sp(FONT_SIZES['xs']),
                color=(0.4, 0.4, 0.4, 1)
            ))
            
            card.add_widget(stat_layout)
            stats_layout.add_widget(card)
            self.stat_cards.append(card)
        
        # Menu rapide
        quick_actions = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            spacing=SPACING['md']
        )
        
        quick_actions.add_widget(Label(
            text='[b]Actions rapides[/b]',
            markup=True,
            font_size=sp(FONT_SIZES['md']),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            size_hint_y=None,
            height=dp(30)
        ))
        
        actions_grid = GridLayout(
            cols=2,
            spacing=SPACING['md'],
            size_hint_y=None,
            height=dp(150)
        )
        
        actions = [
            {'text': 'Rechercher', 'icon': '🔍', 'color': COLORS['primary'], 'screen': 'search'},
            {'text': 'Hôtels', 'icon': '🏨', 'color': COLORS['secondary'], 'screen': 'hotels'},
            {'text': 'Réservations', 'icon': '📅', 'color': COLORS['success'], 'screen': 'bookings'},
            {'text': 'Profil', 'icon': '👤', 'color': COLORS['accent'], 'screen': 'profile'},
        ]
        
        for action in actions:
            btn = ModernButtonIcon(
                text=action['text'],
                icon=action['icon'],
                background_color=action['color'],
                height=dp(60)
            )
            btn.on_press = lambda s=action['screen']: self.navigate(s)
            actions_grid.add_widget(btn)
        
        quick_actions.add_widget(actions_grid)
        
        # Recommandations
        recommendations = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(300),
            spacing=SPACING['md']
        )
        
        recommendations.add_widget(Label(
            text='[b]Recommandés pour vous[/b]',
            markup=True,
            font_size=sp(FONT_SIZES['md']),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            size_hint_y=None,
            height=dp(30)
        ))
        
        self.recommendations_container = BoxLayout(
            orientation='vertical',
            spacing=SPACING['md'],
            size_hint_y=None
        )
        self.recommendations_container.bind(minimum_height=self.recommendations_container.setter('height'))
        recommendations.add_widget(self.recommendations_container)
        
        # Dernières réservations
        recent_bookings = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            spacing=SPACING['md']
        )
        
        recent_bookings.add_widget(Label(
            text='[b]Dernières réservations[/b]',
            markup=True,
            font_size=sp(FONT_SIZES['md']),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            size_hint_y=None,
            height=dp(30)
        ))
        
        self.bookings_container = BoxLayout(
            orientation='vertical',
            spacing=SPACING['sm'],
            size_hint_y=None
        )
        self.bookings_container.bind(minimum_height=self.bookings_container.setter('height'))
        recent_bookings.add_widget(self.bookings_container)
        
        # Assemblage
        content.add_widget(stats_layout)
        content.add_widget(quick_actions)
        content.add_widget(recommendations)
        content.add_widget(recent_bookings)
        
        scroll.add_widget(content)
        
        # Barre de navigation
        self.navbar = ModernNavBar(self.manager)
        
        # Ajout au layout principal
        main.add_widget(header)
        main.add_widget(scroll)
        main.add_widget(self.navbar)
        
        self.add_widget(main)
    
    def load_user_data(self):
        """Charge les données utilisateur"""
        if api_client.user:
            name = api_client.user.first_name or api_client.user.username
            self.greeting_label.text = f'Bonjour {name} 👋'
    
    def load_stats(self):
        """Charge les statistiques"""
        # TODO: Implémenter le chargement des stats depuis l'API
        pass
    
    def load_recommendations(self):
        """Charge les recommandations"""
        self.recommendations_container.clear_widgets()
        
        # Exemple statique
        hotel_cards = [
            {'id': 1, 'name': 'Hôtel Plaza Paris', 'city': 'Paris', 'stars': 5, 'price': 180},
            {'id': 2, 'name': 'Hôtel Central Lyon', 'city': 'Lyon', 'stars': 4, 'price': 120},
            {'id': 3, 'name': 'Hôtel Méditerranée', 'city': 'Marseille', 'stars': 3, 'price': 90},
        ]
        
        for hotel in hotel_cards:
            card = HotelCardModern(
                hotel_id=hotel['id'],
                name=hotel['name'],
                city=hotel['city'],
                stars=hotel['stars'],
                price=hotel['price']
            )
            card.bind(on_book=lambda x, h_id: self.view_hotel(h_id))
            self.recommendations_container.add_widget(card)
    
    def load_recent_bookings(self):
        """Charge les dernières réservations"""
        self.bookings_container.clear_widgets()
        
        bookings = api_client.get_my_bookings()
        
        if bookings:
            for booking in bookings[:3]:
                # Créer une carte simple pour la réservation
                booking_card = ModernCard()
                booking_card.padding = SPACING['md']
                booking_card.size_hint_y = None
                booking_card.height = dp(60)
                
                booking_layout = BoxLayout(orientation='horizontal')
                
                hotel_name = booking.room_type.hotel_name if booking.room_type else "Hôtel"
                booking_layout.add_widget(Label(
                    text=f'🏨 {hotel_name}',
                    font_size=sp(FONT_SIZES['sm']),
                    color=(0.1, 0.1, 0.1, 1),
                    halign='left',
                    size_hint_x=0.6
                ))
                
                status_color = helpers.get_booking_status_color(booking.status)
                booking_layout.add_widget(Label(
                    text=booking.get_status_display(),
                    font_size=sp(FONT_SIZES['xs']),
                    color=status_color,
                    halign='right',
                    size_hint_x=0.4
                ))
                
                booking_card.add_widget(booking_layout)
                self.bookings_container.add_widget(booking_card)
        else:
            self.bookings_container.add_widget(Label(
                text='Aucune réservation',
                font_size=sp(FONT_SIZES['sm']),
                color=(0.4, 0.4, 0.4, 1),
                size_hint_y=None,
                height=dp(50)
            ))
    
    def navigate(self, screen_name):
        """Navigation vers un écran"""
        if screen_name in self.manager.screen_names:
            self.manager.current = screen_name
        else:
            print(f"Écran {screen_name} non trouvé")
    
    def view_hotel(self, hotel_id):
        """Voir les détails d'un hôtel"""
        hotel_detail = self.manager.get_screen('hotel_detail')
        hotel_detail.set_hotel_id(hotel_id)
        self.manager.current = 'hotel_detail'
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'
        else:
            self.load_user_data()
            self.load_stats()
            self.load_recommendations()
            self.load_recent_bookings()
            self.navbar.set_current('home')