from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.clock import Clock

from api.api_client import api_client
from components.hotel_card import HotelCard
from config import COLORS

class HotelsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'hotels'
        self.hotels = []
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Barre de recherche et filtres
        filter_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Champ de recherche
        self.search_input = TextInput(
            hint_text='Rechercher un hôtel...',
            font_size=dp(14),
            size_hint_x=0.6,
            multiline=False
        )
        self.search_input.bind(on_text_validate=lambda x: self.search_hotels())
        
        # Filtre par ville
        self.city_spinner = Spinner(
            text='Toutes villes',
            values=['Toutes villes', 'Paris', 'Lyon', 'Marseille', 'Nice'],
            size_hint_x=0.2,
            font_size=dp(14)
        )
        
        # Filtre par étoiles
        self.stars_spinner = Spinner(
            text='Toutes étoiles',
            values=['Toutes étoiles', '1', '2', '3', '4', '5'],
            size_hint_x=0.2,
            font_size=dp(14)
        )
        
        filter_layout.add_widget(self.search_input)
        filter_layout.add_widget(self.city_spinner)
        filter_layout.add_widget(self.stars_spinner)
        
        # Bouton recherche
        search_button = Button(
            text='🔍',
            size_hint_x=0.1,
            font_size=dp(18),
            background_color=COLORS['primary']
        )
        search_button.bind(on_press=lambda x: self.search_hotels())
        filter_layout.add_widget(search_button)
        
        # Container pour les hôtels avec ScrollView
        scroll_view = ScrollView()
        self.hotels_container = GridLayout(
            cols=1,
            spacing=dp(15),
            padding=dp(15),
            size_hint_y=None
        )
        self.hotels_container.bind(minimum_height=self.hotels_container.setter('height'))
        
        scroll_view.add_widget(self.hotels_container)
        
        # Ajouter au layout principal
        main_layout.add_widget(filter_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
        
        # Charger les hôtels au démarrage
        Clock.schedule_once(lambda dt: self.load_hotels(), 0.5)
    
    def load_hotels(self, filters=None):
        """Charge la liste des hôtels"""
        self.hotels_container.clear_widgets()
        
        # Afficher un indicateur de chargement
        loading_label = Label(
            text='Chargement des hôtels...',
            font_size=dp(16),
            color=COLORS['gray'],
            size_hint_y=None,
            height=dp(100)
        )
        self.hotels_container.add_widget(loading_label)
        
        # Récupérer les hôtels
        Clock.schedule_once(lambda dt: self._fetch_hotels(filters), 0.1)
    
    def _fetch_hotels(self, filters):
        """Récupère les hôtels depuis l'API"""
        self.hotels_container.clear_widgets()
        
        # Préparer les filtres
        api_filters = {}
        if filters:
            api_filters = filters
        else:
            if self.city_spinner.text != 'Toutes villes':
                api_filters['city'] = self.city_spinner.text
            if self.stars_spinner.text != 'Toutes étoiles':
                api_filters['stars'] = int(self.stars_spinner.text)
        
        # Appel API
        hotels = api_client.get_hotels(api_filters)
        
        if hotels:
            self.hotels = hotels
            self.display_hotels()
        else:
            self.show_error("Aucun hôtel trouvé")
    
    def display_hotels(self):
        """Affiche les hôtels"""
        self.hotels_container.clear_widgets()
        
        if not self.hotels:
            self.show_error("Aucun hôtel disponible")
            return
        
        for hotel in self.hotels:
            # Préparer les features
            features = []
            if hotel.has_wifi:
                features.append('WiFi')
            if hotel.has_parking:
                features.append('Parking')
            if hotel.has_pool:
                features.append('Piscine')
            if hotel.has_restaurant:
                features.append('Restaurant')
            
            # Créer la carte
            card = HotelCard(
                hotel_id=hotel.id,
                name=hotel.name,
                city=hotel.city,
                country=hotel.country,
                stars=hotel.stars,
                description=hotel.description,
                price=100,  # Prix moyen, à ajuster
                features=features
            )
            
            # Lier l'événement de clic
            card.children[0].children[0].bind(
                on_press=lambda instance, h_id=hotel.id: self.view_hotel(h_id)
            )
            
            self.hotels_container.add_widget(card)
    
    def search_hotels(self):
        """Recherche d'hôtels avec les filtres"""
        filters = {}
        
        if self.search_input.text:
            filters['search'] = self.search_input.text
        
        if self.city_spinner.text != 'Toutes villes':
            filters['city'] = self.city_spinner.text
        
        if self.stars_spinner.text != 'Toutes étoiles':
            filters['stars'] = int(self.stars_spinner.text)
        
        self.load_hotels(filters)
    
    def view_hotel(self, hotel_id):
        """Voir les détails d'un hôtel"""
        print(f"Voir hôtel {hotel_id}")
        # Naviguer vers l'écran de détail
        # self.manager.get_screen('hotel_detail').set_hotel_id(hotel_id)
        # self.manager.current = 'hotel_detail'
    
    def show_error(self, message):
        """Affiche un message d'erreur"""
        self.hotels_container.clear_widgets()
        self.hotels_container.add_widget(Label(
            text=message,
            font_size=dp(16),
            color=COLORS['gray'],
            size_hint_y=None,
            height=dp(100)
        ))
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'