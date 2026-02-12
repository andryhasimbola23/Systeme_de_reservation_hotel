from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

from api.api_client import api_client
from components.room_card import RoomCard
from utils.helpers import helpers
from utils.storage import storage
from config import COLORS

class HotelDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'hotel_detail'
        self.hotel_id = None
        self.hotel = None
        self.rooms = []
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal avec ScrollView
        scroll_view = ScrollView()
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(15),
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # En-tête avec image
        self.image_container = BoxLayout(
            size_hint_y=None,
            height=dp(200),
            padding=dp(0)
        )
        
        self.hotel_image = Label(
            text='🏨',
            font_size=dp(80),
            halign='center',
            valign='middle'
        )
        self.image_container.add_widget(self.hotel_image)
        
        # Informations principales
        self.info_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.info_layout.bind(minimum_height=self.info_layout.setter('height'))
        
        # Nom et étoiles
        self.name_stars_layout = BoxLayout(
            size_hint_y=None,
            height=dp(40)
        )
        
        self.hotel_name = Label(
            font_size=dp(20),
            bold=True,
            color=COLORS['dark'],
            halign='left',
            valign='middle',
            size_hint_x=0.7
        )
        self.hotel_name.bind(size=self.hotel_name.setter('text_size'))
        
        self.stars_label = Label(
            font_size=dp(16),
            color='#FFD700',
            halign='right',
            valign='middle',
            size_hint_x=0.3
        )
        self.stars_label.bind(size=self.stars_label.setter('text_size'))
        
        self.name_stars_layout.add_widget(self.hotel_name)
        self.name_stars_layout.add_widget(self.stars_label)
        
        # Localisation
        self.location_label = Label(
            font_size=dp(14),
            color=COLORS['secondary'],
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(25)
        )
        self.location_label.bind(size=self.location_label.setter('text_size'))
        
        # Description
        self.description_label = Label(
            font_size=dp(14),
            color=COLORS['gray_dark'],
            halign='left',
            valign='top',
            size_hint_y=None
        )
        self.description_label.bind(size=self.description_label.setter('text_size'))
        
        # Bouton favoris
        self.favorite_button = Button(
            text='⭐ Ajouter aux favoris',
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['secondary'],
            color=(1, 1, 1, 1)
        )
        self.favorite_button.bind(on_press=self.toggle_favorite)
        
        # Tabbed Panel pour les détails
        self.tab_panel = TabbedPanel(
            do_default_tab=False,
            size_hint_y=None,
            height=dp(300)
        )
        
        # Onglet Chambres
        rooms_tab = TabbedPanelHeader(text='Chambres')
        self.rooms_container = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )
        rooms_scroll = ScrollView()
        rooms_scroll.add_widget(self.rooms_container)
        rooms_tab.content = rooms_scroll
        
        # Onglet Équipements
        amenities_tab = TabbedPanelHeader(text='Équipements')
        self.amenities_container = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        self.amenities_container.bind(minimum_height=self.amenities_container.setter('height'))
        amenities_scroll = ScrollView()
        amenities_scroll.add_widget(self.amenities_container)
        amenities_tab.content = amenities_scroll
        
        # Onglet Contact
        contact_tab = TabbedPanelHeader(text='Contact')
        self.contact_container = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        self.contact_container.bind(minimum_height=self.contact_container.setter('height'))
        contact_scroll = ScrollView()
        contact_scroll.add_widget(self.contact_container)
        contact_tab.content = contact_scroll
        
        self.tab_panel.add_widget(rooms_tab)
        self.tab_panel.add_widget(amenities_tab)
        self.tab_panel.add_widget(contact_tab)
        
        # Bouton retour
        back_button = Button(
            text='← Retour',
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['gray'],
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=lambda x: self.go_back())
        
        # Ajout des widgets
        self.info_layout.add_widget(self.name_stars_layout)
        self.info_layout.add_widget(self.location_label)
        self.info_layout.add_widget(self.description_label)
        self.info_layout.add_widget(self.favorite_button)
        
        main_layout.add_widget(self.image_container)
        main_layout.add_widget(self.info_layout)
        main_layout.add_widget(self.tab_panel)
        main_layout.add_widget(back_button)
        
        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)
    
    def set_hotel_id(self, hotel_id):
        """Définit l'ID de l'hôtel à afficher"""
        self.hotel_id = hotel_id
        self.load_hotel_data()
    
    def load_hotel_data(self):
        """Charge les données de l'hôtel"""
        if not self.hotel_id:
            return
        
        # Afficher le chargement
        self.hotel_name.text = "Chargement..."
        
        Clock.schedule_once(lambda dt: self._fetch_hotel_data(), 0.1)
    
    def _fetch_hotel_data(self):
        """Récupère les données de l'hôtel depuis l'API"""
        self.hotel = api_client.get_hotel(self.hotel_id)
        
        if self.hotel:
            self.display_hotel_data()
            self.load_rooms()
            self.load_amenities()
            self.load_contact_info()
            self.update_favorite_button()
    
    def display_hotel_data(self):
        """Affiche les données de l'hôtel"""
        if not self.hotel:
            return
        
        self.hotel_name.text = self.hotel.name
        self.stars_label.text = helpers.get_stars_rating(self.hotel.stars)
        self.location_label.text = f"📍 {self.hotel.city}, {self.hotel.country}"
        self.description_label.text = self.hotel.description
        
        # Image
        if self.hotel.images:
            self.image_container.clear_widgets()
            hotel_image = AsyncImage(
                source=self.hotel.images[0],
                allow_stretch=True,
                keep_ratio=True
            )
            self.image_container.add_widget(hotel_image)
    
    def load_rooms(self):
        """Charge les chambres de l'hôtel"""
        self.rooms_container.clear_widgets()
        
        rooms = api_client.get_hotel_rooms(self.hotel_id)
        
        if rooms:
            self.rooms = rooms
            for room in rooms:
                room_card = RoomCard(
                    room_id=room.id,
                    name=room.name,
                    room_type=room.get_room_type_display(),
                    capacity=room.capacity,
                    size=room.size,
                    price=room.price_per_night,
                    available=room.quantity_available,
                    features=[
                        '📺' if room.has_tv else None,
                        '❄️' if room.has_ac else None,
                        '🍸' if room.has_minibar else None,
                        '🔒' if room.has_safe else None,
                        '🚪' if room.has_balcony else None,
                    ]
                )
                room_card.bind(on_book=self.on_book_room)
                self.rooms_container.add_widget(room_card)
        else:
            self.rooms_container.add_widget(Label(
                text="Aucune chambre disponible",
                color=COLORS['gray'],
                size_hint_y=None,
                height=dp(50)
            ))
    
    def load_amenities(self):
        """Charge les équipements de l'hôtel"""
        self.amenities_container.clear_widgets()
        
        if not self.hotel:
            return
        
        amenities = [
            ('📶', 'WiFi', self.hotel.has_wifi),
            ('🅿️', 'Parking', self.hotel.has_parking),
            ('🏊', 'Piscine', self.hotel.has_pool),
            ('💆', 'Spa', self.hotel.has_spa),
            ('🍽️', 'Restaurant', self.hotel.has_restaurant),
            ('🏋️', 'Gym', self.hotel.has_gym),
        ]
        
        for icon, name, available in amenities:
            if available:
                amenity_box = BoxLayout(
                    orientation='horizontal',
                    spacing=dp(10),
                    size_hint_y=None,
                    height=dp(40)
                )
                
                amenity_box.add_widget(Label(
                    text=icon,
                    font_size=dp(20),
                    size_hint_x=0.2
                ))
                
                amenity_box.add_widget(Label(
                    text=name,
                    font_size=dp(14),
                    color=COLORS['dark'],
                    halign='left',
                    size_hint_x=0.8
                ))
                
                self.amenities_container.add_widget(amenity_box)
        
        if not self.amenities_container.children:
            self.amenities_container.add_widget(Label(
                text="Aucun équipement spécifié",
                color=COLORS['gray'],
                size_hint_y=None,
                height=dp(50)
            ))
    
    def load_contact_info(self):
        """Charge les informations de contact"""
        self.contact_container.clear_widgets()
        
        if not self.hotel:
            return
        
        contacts = [
            ('📞', 'Téléphone', self.hotel.phone),
            ('📧', 'Email', self.hotel.email),
            ('📍', 'Adresse', f"{self.hotel.address}\n{self.hotel.city}, {self.hotel.country}"),
        ]
        
        for icon, label, value in contacts:
            contact_box = BoxLayout(
                orientation='vertical',
                spacing=dp(5),
                size_hint_y=None,
                height=dp(60)
            )
            
            contact_box.add_widget(Label(
                text=f"{icon} {label}",
                font_size=dp(12),
                color=COLORS['gray'],
                halign='left',
                size_hint_y=None,
                height=dp(20)
            ))
            
            contact_box.add_widget(Label(
                text=value,
                font_size=dp(14),
                color=COLORS['dark'],
                halign='left',
                size_hint_y=None,
                height=dp(30)
            ))
            
            self.contact_container.add_widget(contact_box)
    
    def update_favorite_button(self):
        """Met à jour le bouton favori"""
        if not self.hotel_id:
            return
        
        is_favorite = storage.is_favorite('hotels', self.hotel_id)
        
        if is_favorite:
            self.favorite_button.text = '⭐ Retirer des favoris'
            self.favorite_button.background_color = COLORS['success']
        else:
            self.favorite_button.text = '⭐ Ajouter aux favoris'
            self.favorite_button.background_color = COLORS['secondary']
    
    def toggle_favorite(self, instance):
        """Ajoute ou retire des favoris"""
        if not self.hotel or not self.hotel_id:
            return
        
        hotel_data = {
            'name': self.hotel.name,
            'city': self.hotel.city,
            'stars': self.hotel.stars,
        }
        
        is_favorite = storage.toggle_favorite('hotels', self.hotel_id, hotel_data)
        self.update_favorite_button()
    
    def on_book_room(self, room_id, price, name):
        """Gère la réservation d'une chambre"""
        print(f"Réservation chambre {room_id}: {name}")
        # Naviguer vers l'écran de création de réservation
        booking_screen = self.manager.get_screen('create_booking')
        booking_screen.set_room_id(room_id)
        self.manager.current = 'create_booking'
    
    def go_back(self):
        """Retour à la liste des hôtels"""
        self.manager.current = 'hotels'
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'