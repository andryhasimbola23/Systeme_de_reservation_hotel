from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime, timedelta

from api.api_client import api_client
from api.models import SearchFilters
from components.hotel_card import HotelCard
from utils.validators import validators
from utils.helpers import helpers
from utils.storage import storage
from config import COLORS

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'search'
        self.search_results = []
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Layout des filtres (fixe en haut)
        filter_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(400),
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Titre
        filter_layout.add_widget(Label(
            text='[size=18][b]Rechercher un hôtel[/b][/size]',
            markup=True,
            font_size=dp(18),
            color=COLORS['dark'],
            size_hint_y=None,
            height=dp(30)
        ))
        
        # Destination/Ville
        self.city_input = TextInput(
            hint_text='Destination (ville)',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            background_color=(1, 1, 1, 0.9)
        )
        filter_layout.add_widget(self.city_input)
        
        # Dates
        date_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        self.check_in_input = TextInput(
            hint_text='Arrivée',
            font_size=dp(14),
            size_hint_x=0.5,
            multiline=False
        )
        self.check_in_input.text = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        self.check_out_input = TextInput(
            hint_text='Départ',
            font_size=dp(14),
            size_hint_x=0.5,
            multiline=False
        )
        self.check_out_input.text = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        date_layout.add_widget(self.check_in_input)
        date_layout.add_widget(self.check_out_input)
        filter_layout.add_widget(date_layout)
        
        # Nombre de personnes et chambres
        guests_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        self.rooms_spinner = Spinner(
            text='1 chambre',
            values=['1 chambre', '2 chambres', '3 chambres', '4+ chambres'],
            size_hint_x=0.5,
            font_size=dp(14)
        )
        
        self.guests_spinner = Spinner(
            text='2 personnes',
            values=['1 personne', '2 personnes', '3 personnes', '4 personnes', '5+ personnes'],
            size_hint_x=0.5,
            font_size=dp(14)
        )
        
        guests_layout.add_widget(self.rooms_spinner)
        guests_layout.add_widget(self.guests_spinner)
        filter_layout.add_widget(guests_layout)
        
        # Prix
        price_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        self.min_price_input = TextInput(
            hint_text='Prix min',
            font_size=dp(14),
            size_hint_x=0.5,
            multiline=False,
            input_filter='int'
        )
        
        self.max_price_input = TextInput(
            hint_text='Prix max',
            font_size=dp(14),
            size_hint_x=0.5,
            multiline=False,
            input_filter='int'
        )
        
        price_layout.add_widget(self.min_price_input)
        price_layout.add_widget(self.max_price_input)
        filter_layout.add_widget(price_layout)
        
        # Étoiles
        stars_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        stars_layout.add_widget(Label(
            text='Étoiles:',
            font_size=dp(14),
            color=COLORS['dark'],
            size_hint_x=0.3
        ))
        
        self.stars_spinner = Spinner(
            text='Toutes',
            values=['Toutes', '5★', '4★', '3★', '2★', '1★'],
            size_hint_x=0.7,
            font_size=dp(14)
        )
        
        stars_layout.add_widget(self.stars_spinner)
        filter_layout.add_widget(stars_layout)
        
        # Boutons
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        search_button = Button(
            text='Rechercher',
            font_size=dp(16),
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_x=0.7
        )
        search_button.bind(on_press=self.search_hotels)
        
        reset_button = Button(
            text='Réinitialiser',
            font_size=dp(14),
            background_color=COLORS['gray'],
            color=(1, 1, 1, 1),
            size_hint_x=0.3
        )
        reset_button.bind(on_press=self.reset_filters)
        
        buttons_layout.add_widget(search_button)
        buttons_layout.add_widget(reset_button)
        filter_layout.add_widget(buttons_layout)
        
        # Résultats
        results_label = Label(
            text='[size=16][b]Résultats[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=dp(30),
            halign='left'
        )
        results_label.bind(size=results_label.setter('text_size'))
        
        # Container pour les résultats avec ScrollView
        scroll_view = ScrollView()
        self.results_container = GridLayout(
            cols=1,
            spacing=dp(15),
            padding=dp(15),
            size_hint_y=None
        )
        self.results_container.bind(minimum_height=self.results_container.setter('height'))
        
        scroll_view.add_widget(self.results_container)
        
        # Ajout au layout principal
        main_layout.add_widget(filter_layout)
        main_layout.add_widget(results_label)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def search_hotels(self, instance):
        """Recherche des hôtels avec les filtres"""
        # Désactiver le bouton
        instance.disabled = True
        instance.text = "Recherche..."
        
        # Afficher chargement
        self.results_container.clear_widgets()
        loading_label = Label(
            text='Recherche en cours...',
            font_size=dp(16),
            color=COLORS['gray'],
            size_hint_y=None,
            height=dp(100)
        )
        self.results_container.add_widget(loading_label)
        
        Clock.schedule_once(lambda dt: self._perform_search(instance), 0.1)
    
    def _perform_search(self, button):
        """Effectue la recherche via l'API"""
        # Créer les filtres
        filters = SearchFilters()
        
        # Ville
        if self.city_input.text:
            filters.city = self.city_input.text.strip()
        
        # Dates
        filters.check_in = self.check_in_input.text
        filters.check_out = self.check_out_input.text
        
        # Nombre de chambres
        rooms_map = {
            '1 chambre': 1,
            '2 chambres': 2,
            '3 chambres': 3,
            '4+ chambres': 4
        }
        filters.number_of_rooms = rooms_map.get(self.rooms_spinner.text, 1)
        
        # Nombre de personnes
        guests_map = {
            '1 personne': 1,
            '2 personnes': 2,
            '3 personnes': 3,
            '4 personnes': 4,
            '5+ personnes': 5
        }
        filters.number_of_guests = guests_map.get(self.guests_spinner.text, 2)
        
        # Prix
        if self.min_price_input.text:
            filters.min_price = float(self.min_price_input.text)
        if self.max_price_input.text:
            filters.max_price = float(self.max_price_input.text)
        
        # Étoiles
        stars_map = {
            '5★': 5,
            '4★': 4,
            '3★': 3,
            '2★': 2,
            '1★': 1
        }
        filters.stars = stars_map.get(self.stars_spinner.text)
        
        # Sauvegarder les filtres
        storage.save_search_filters(filters.to_dict())
        
        # Appel API
        results = api_client.search_hotels(filters)
        
        self.results_container.clear_widgets()
        
        if results:
            self.search_results = results
            self.display_results()
        else:
            self.results_container.add_widget(Label(
                text='Aucun hôtel trouvé',
                font_size=dp(16),
                color=COLORS['gray'],
                size_hint_y=None,
                height=dp(100)
            ))
        
        # Réactiver le bouton
        button.disabled = False
        button.text = "Rechercher"
    
    def display_results(self):
        """Affiche les résultats de recherche"""
        self.results_container.clear_widgets()
        
        for room in self.search_results[:20]:  # Limiter à 20 résultats
            # Créer une carte d'hôtel
            card = HotelCard(
                hotel_id=room.hotel_id,
                name=room.hotel_name,
                city=room.hotel_city,
                country='France',
                stars=5,  # À récupérer depuis l'API
                description=room.description,
                price=room.price_per_night,
                features=[]
            )
            
            # Lier l'événement de clic
            # card.bind(on_press=lambda x, h_id=room.hotel_id: self.view_hotel(h_id))
            
            self.results_container.add_widget(card)
    
    def reset_filters(self, instance):
        """Réinitialise tous les filtres"""
        self.city_input.text = ""
        self.check_in_input.text = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        self.check_out_input.text = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        self.rooms_spinner.text = '1 chambre'
        self.guests_spinner.text = '2 personnes'
        self.min_price_input.text = ""
        self.max_price_input.text = ""
        self.stars_spinner.text = 'Toutes'
    
    def view_hotel(self, hotel_id):
        """Voir les détails d'un hôtel"""
        detail_screen = self.manager.get_screen('hotel_detail')
        detail_screen.set_hotel_id(hotel_id)
        self.manager.current = 'hotel_detail'
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'
        
        # Charger les derniers filtres
        last_filters = storage.get_search_filters()
        if last_filters:
            if 'city' in last_filters:
                self.city_input.text = last_filters['city']
            if 'min_price' in last_filters:
                self.min_price_input.text = str(last_filters['min_price'])
            if 'max_price' in last_filters:
                self.max_price_input.text = str(last_filters['max_price'])