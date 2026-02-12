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
from datetime import datetime, timedelta

from api.api_client import api_client
from utils.validators import validators
from utils.helpers import helpers
from config import COLORS

class CreateBookingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'create_booking'
        self.room_id = None
        self.room = None
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal avec ScrollView
        scroll_view = ScrollView()
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        self.content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        main_layout.add_widget(self.content_layout)
        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)
    
    def set_room_id(self, room_id):
        """Définit l'ID de la chambre à réserver"""
        self.room_id = room_id
        self.load_room_data()
    
    def load_room_data(self):
        """Charge les données de la chambre"""
        if not self.room_id:
            return
        
        self.content_layout.clear_widgets()
        
        # Afficher chargement
        loading_label = Label(
            text='Chargement des informations...',
            font_size=dp(16),
            color=COLORS['gray'],
            size_hint_y=None,
            height=dp(100)
        )
        self.content_layout.add_widget(loading_label)
        
        # Simuler le chargement (à remplacer par un appel API réel)
        Clock.schedule_once(lambda dt: self._load_mock_data(), 0.5)
    
    def _load_mock_data(self):
        """Charge des données de test (à remplacer par API)"""
        self.content_layout.clear_widgets()
        
        # Simulation d'une chambre
        self.room = {
            'id': self.room_id,
            'name': 'Chambre Double Deluxe',
            'hotel_name': 'Hôtel Plaza Paris',
            'hotel_id': 1,
            'room_type': 'double',
            'capacity': 2,
            'size': 25,
            'price_per_night': 150.0,
            'quantity_available': 5
        }
        
        self.display_booking_form()
    
    def display_booking_form(self):
        """Affiche le formulaire de réservation"""
        self.content_layout.clear_widgets()
        
        # En-tête
        self.content_layout.add_widget(Label(
            text=f'[size=20][b]Réserver[/b][/size]\n{self.room["name"]}',
            markup=True,
            font_size=dp(20),
            color=COLORS['dark'],
            halign='center',
            size_hint_y=None,
            height=dp(80)
        ))
        
        # Récapitulatif chambre
        summary = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(150),
            spacing=dp(10),
            padding=dp(15)
        )
        summary.canvas.before.add(Color(rgba=(0.95, 0.95, 0.95, 1)))
        summary.canvas.before.add(RoundedRectangle(pos=summary.pos, size=summary.size, radius=[dp(10),]))
        
        summary.add_widget(Label(
            text=f'🏨 {self.room["hotel_name"]}',
            font_size=dp(16),
            bold=True,
            color=COLORS['dark'],
            halign='left'
        ))
        
        summary.add_widget(Label(
            text=f'👥 Capacité: {self.room["capacity"]} personnes • 📏 {self.room["size"]}m²',
            font_size=dp(14),
            color=COLORS['gray'],
            halign='left'
        ))
        
        summary.add_widget(Label(
            text=f'💰 {self.room["price_per_night"]}€ / nuit',
            font_size=dp(16),
            color=COLORS['primary'],
            bold=True,
            halign='left'
        ))
        
        self.content_layout.add_widget(summary)
        
        # Formulaire
        form = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None
        )
        form.bind(minimum_height=form.setter('height'))
        
        # Dates
        form.add_widget(Label(
            text='📅 Dates du séjour',
            font_size=dp(16),
            bold=True,
            color=COLORS['dark'],
            halign='left',
            size_hint_y=None,
            height=dp(30)
        ))
        
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
        self.check_in_input.bind(text=self.calculate_price)
        
        self.check_out_input = TextInput(
            hint_text='Départ',
            font_size=dp(14),
            size_hint_x=0.5,
            multiline=False
        )
        self.check_out_input.text = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        self.check_out_input.bind(text=self.calculate_price)
        
        date_layout.add_widget(self.check_in_input)
        date_layout.add_widget(self.check_out_input)
        form.add_widget(date_layout)
        
        # Nombre de chambres et personnes
        details_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        self.rooms_spinner = Spinner(
            text='1 chambre',
            values=['1 chambre', '2 chambres', '3 chambres', '4 chambres'],
            size_hint_x=0.5,
            font_size=dp(14)
        )
        self.rooms_spinner.bind(text=self.calculate_price)
        
        self.guests_spinner = Spinner(
            text='2 personnes',
            values=['1 personne', '2 personnes', '3 personnes', '4 personnes'],
            size_hint_x=0.5,
            font_size=dp(14)
        )
        self.guests_spinner.bind(text=self.calculate_price)
        
        details_layout.add_widget(self.rooms_spinner)
        details_layout.add_widget(self.guests_spinner)
        form.add_widget(details_layout)
        
        # Demandes spéciales
        form.add_widget(Label(
            text='📝 Demandes spéciales (optionnel)',
            font_size=dp(14),
            color=COLORS['dark'],
            halign='left',
            size_hint_y=None,
            height=dp(30)
        ))
        
        self.special_requests_input = TextInput(
            hint_text='Chambre calme, vue, etc...',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(80),
            multiline=True
        )
        form.add_widget(self.special_requests_input)
        
        # Calcul du prix
        self.price_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(10),
            padding=dp(15)
        )
        self.price_layout.canvas.before.add(Color(rgba=(0.95, 0.95, 0.95, 1)))
        self.price_layout.canvas.before.add(RoundedRectangle(pos=self.price_layout.pos, size=self.price_layout.size, radius=[dp(10),]))
        
        self.price_label = Label(
            text='Prix total: 0€',
            font_size=dp(18),
            bold=True,
            color=COLORS['primary'],
            halign='center'
        )
        self.price_layout.add_widget(self.price_label)
        
        self.nights_label = Label(
            text='0 nuits',
            font_size=dp(14),
            color=COLORS['gray'],
            halign='center'
        )
        self.price_layout.add_widget(self.nights_label)
        
        form.add_widget(self.price_layout)
        
        # Boutons
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120),
            padding=dp(10)
        )
        
        confirm_button = Button(
            text='✅ Confirmer la réservation',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['success'],
            color=(1, 1, 1, 1)
        )
        confirm_button.bind(on_press=self.confirm_booking)
        
        cancel_button = Button(
            text='❌ Annuler',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['danger'],
            color=(1, 1, 1, 1)
        )
        cancel_button.bind(on_press=self.cancel_booking)
        
        buttons_layout.add_widget(confirm_button)
        buttons_layout.add_widget(cancel_button)
        
        form.add_widget(buttons_layout)
        self.content_layout.add_widget(form)
        
        # Calcul initial du prix
        self.calculate_price()
    
    def calculate_price(self, *args):
        """Calcule le prix total"""
        try:
            check_in = self.check_in_input.text
            check_out = self.check_out_input.text
            
            # Extraire le nombre de chambres
            rooms_text = self.rooms_spinner.text
            rooms = int(rooms_text.split()[0]) if rooms_text else 1
            
            nights = 0
            total = 0
            
            if check_in and check_out:
                try:
                    check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
                    check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
                    nights = (check_out_date - check_in_date).days
                    if nights > 0 and self.room:
                        total = self.room['price_per_night'] * nights * rooms
                except:
                    pass
            
            self.price_label.text = f'Prix total: {helpers.format_price(total)}'
            self.nights_label.text = f'{nights} nuits • {rooms} chambre(s)'
        except Exception as e:
            print(f"Erreur calcul prix: {e}")
    
    def confirm_booking(self, instance):
        """Confirme la réservation"""
        # Validation des dates
        check_in = self.check_in_input.text
        check_out = self.check_out_input.text
        
        valid, error = validators.validate_date_range(check_in, check_out)
        if not valid:
            self.show_error(error)
            return
        
        # Validation nombre de personnes
        guests_text = self.guests_spinner.text
        guests = int(guests_text.split()[0]) if guests_text else 2
        
        rooms_text = self.rooms_spinner.text
        rooms = int(rooms_text.split()[0]) if rooms_text else 1
        
        if guests > self.room['capacity'] * rooms:
            self.show_error(f"Maximum {self.room['capacity'] * rooms} personnes pour {rooms} chambre(s)")
            return
        
        # Désactiver le bouton
        instance.disabled = True
        instance.text = "Création en cours..."
        
        # Simuler la création (à remplacer par appel API)
        Clock.schedule_once(lambda dt: self._create_booking_success(instance), 1)
    
    def _create_booking_success(self, button):
        """Succès de la création de réservation"""
        # Créer la réservation via API
        # booking = api_client.create_booking(
        #     room_type_id=self.room_id,
        #     check_in=self.check_in_input.text,
        #     check_out=self.check_out_input.text,
        #     number_of_rooms=int(self.rooms_spinner.text.split()[0]),
        #     number_of_guests=int(self.guests_spinner.text.split()[0]),
        #     special_requests=self.special_requests_input.text
        # )
        
        # Simulation
        booking_id = 12345
        
        button.text = "✅ Réservation créée!"
        Clock.schedule_once(lambda dt: self.go_to_booking_detail(booking_id), 1)
    
    def go_to_booking_detail(self, booking_id):
        """Navigation vers le détail de la réservation"""
        detail_screen = self.manager.get_screen('booking_detail')
        detail_screen.set_booking_id(booking_id)
        self.manager.current = 'booking_detail'
    
    def cancel_booking(self, instance):
        """Annule la création de réservation"""
        self.manager.current = 'hotel_detail'
    
    def show_error(self, message):
        """Affiche une erreur"""
        from kivy.uix.popup import Popup
        popup = Popup(
            title='Erreur',
            content=Label(text=message, font_size=dp(14)),
            size_hint=(0.8, 0.3),
            separator_color=COLORS['danger']
        )
        popup.open()
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'