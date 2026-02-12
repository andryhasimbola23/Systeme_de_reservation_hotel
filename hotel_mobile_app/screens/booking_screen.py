from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock

from api.api_client import api_client
from components.booking_card import BookingCard
from utils.helpers import helpers
from config import COLORS

class BookingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'bookings'
        self.bookings = []
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # En-tête
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=dp(15),
            spacing=dp(10)
        )
        
        header.add_widget(Label(
            text='[size=20][b]Mes réservations[/b][/size]',
            markup=True,
            font_size=dp(20),
            color=COLORS['dark'],
            halign='left',
            size_hint_x=0.7
        ))
        
        refresh_button = Button(
            text='↻',
            font_size=dp(20),
            size_hint_x=0.3,
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1)
        )
        refresh_button.bind(on_press=self.refresh_bookings)
        header.add_widget(refresh_button)
        
        # Container pour les réservations avec ScrollView
        scroll_view = ScrollView()
        self.bookings_container = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(15),
            size_hint_y=None
        )
        self.bookings_container.bind(minimum_height=self.bookings_container.setter('height'))
        
        scroll_view.add_widget(self.bookings_container)
        
        # Ajout au layout principal
        main_layout.add_widget(header)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def refresh_bookings(self, instance):
        """Rafraîchit la liste des réservations"""
        instance.disabled = True
        self.load_bookings()
        Clock.schedule_once(lambda dt: self._reenable_button(instance), 1)
    
    def _reenable_button(self, button):
        button.disabled = False
    
    def load_bookings(self):
        """Charge les réservations depuis l'API"""
        self.bookings_container.clear_widgets()
        
        # Afficher chargement
        loading_label = Label(
            text='Chargement des réservations...',
            font_size=dp(16),
            color=COLORS['gray'],
            size_hint_y=None,
            height=dp(100)
        )
        self.bookings_container.add_widget(loading_label)
        
        Clock.schedule_once(lambda dt: self._fetch_bookings(), 0.1)
    
    def _fetch_bookings(self):
        """Récupère les réservations depuis l'API"""
        self.bookings_container.clear_widgets()
        
        bookings = api_client.get_my_bookings()
        
        if bookings:
            self.bookings = bookings
            self.display_bookings()
        else:
            self.show_empty_state()
    
    def display_bookings(self):
        """Affiche la liste des réservations"""
        self.bookings_container.clear_widgets()
        
        # Trier par date (plus récent en premier)
        sorted_bookings = sorted(
            self.bookings,
            key=lambda x: x.created_at,
            reverse=True
        )
        
        for booking in sorted_bookings:
            booking_card = BookingCard(
                booking_id=booking.id,
                hotel_name=booking.room_type.hotel_name if booking.room_type else 'Hôtel',
                room_name=booking.room_type.name if booking.room_type else 'Chambre',
                check_in=booking.check_in_date,
                check_out=booking.check_out_date,
                nights=booking.number_of_nights,
                guests=booking.number_of_guests,
                total_price=booking.total_price,
                status=booking.status,
                status_display=booking.get_status_display(),
                can_cancel=booking.can_cancel
            )
            booking_card.bind(on_view=self.view_booking)
            booking_card.bind(on_cancel=self.cancel_booking)
            
            self.bookings_container.add_widget(booking_card)
    
    def show_empty_state(self):
        """Affiche l'état vide"""
        self.bookings_container.clear_widgets()
        
        empty_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(40),
            size_hint_y=None,
            height=dp(300)
        )
        
        empty_layout.add_widget(Label(
            text='📅',
            font_size=dp(60)
        ))
        
        empty_layout.add_widget(Label(
            text='[size=18][b]Aucune réservation[/b][/size]',
            markup=True,
            font_size=dp(18),
            color=COLORS['dark']
        ))
        
        empty_layout.add_widget(Label(
            text='Vous n\'avez pas encore effectué de réservation',
            font_size=dp(14),
            color=COLORS['gray']
        ))
        
        search_button = Button(
            text='Rechercher un hôtel',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1)
        )
        search_button.bind(on_press=lambda x: self.go_to_search())
        
        empty_layout.add_widget(search_button)
        self.bookings_container.add_widget(empty_layout)
    
    def view_booking(self, booking_id):
        """Voir les détails d'une réservation"""
        detail_screen = self.manager.get_screen('booking_detail')
        detail_screen.set_booking_id(booking_id)
        self.manager.current = 'booking_detail'
    
    def cancel_booking(self, booking_id):
        """Annuler une réservation"""
        success = api_client.cancel_booking(booking_id)
        if success:
            self.load_bookings()
    
    def go_to_search(self):
        """Navigation vers la recherche"""
        self.manager.current = 'search'
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'
        else:
            self.load_bookings()