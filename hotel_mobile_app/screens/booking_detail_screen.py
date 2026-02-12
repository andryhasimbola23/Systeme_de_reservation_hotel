from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.popup import Popup

from api.api_client import api_client
from utils.helpers import helpers
from config import COLORS

class BookingDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'booking_detail'
        self.booking_id = None
        self.booking = None
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
    
    def set_booking_id(self, booking_id):
        """Définit l'ID de la réservation à afficher"""
        self.booking_id = booking_id
        self.load_booking_data()
    
    def load_booking_data(self):
        """Charge les données de la réservation"""
        if not self.booking_id:
            return
        
        self.content_layout.clear_widgets()
        
        # Afficher chargement
        loading_label = Label(
            text='Chargement de la réservation...',
            font_size=dp(16),
            color=COLORS['gray'],
            size_hint_y=None,
            height=dp(100)
        )
        self.content_layout.add_widget(loading_label)
        
        Clock.schedule_once(lambda dt: self._fetch_booking_data(), 0.1)
    
    def _fetch_booking_data(self):
        """Récupère les données de la réservation depuis l'API"""
        self.content_layout.clear_widgets()
        
        self.booking = api_client.get_booking(self.booking_id)
        
        if self.booking:
            self.display_booking_data()
        else:
            self.content_layout.add_widget(Label(
                text='Réservation introuvable',
                font_size=dp(16),
                color=COLORS['danger'],
                size_hint_y=None,
                height=dp(100)
            ))
    
    def display_booking_data(self):
        """Affiche les données de la réservation"""
        self.content_layout.clear_widgets()
        
        # En-tête avec statut
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )
        
        header.add_widget(Label(
            text=f'Réservation #{self.booking.id}',
            font_size=dp(18),
            bold=True,
            color=COLORS['dark'],
            halign='left',
            size_hint_x=0.6
        ))
        
        status_color = helpers.get_booking_status_color(self.booking.status)
        status_label = Label(
            text=self.booking.get_status_display(),
            font_size=dp(14),
            color=status_color,
            halign='center',
            size_hint_x=0.4
        )
        status_label.canvas.before.add(Color(rgba=self._hex_to_rgb(status_color, 0.2)))
        status_label.canvas.before.add(RoundedRectangle(
            pos=status_label.pos,
            size=status_label.size,
            radius=[dp(12),]
        ))
        header.add_widget(status_label)
        
        self.content_layout.add_widget(header)
        
        # Hôtel
        hotel_section = self.create_section(
            '🏨 Hôtel',
            [
                ('Nom', self.booking.room_type.hotel_name if self.booking.room_type else 'N/A'),
                ('Adresse', self.booking.room_type.hotel.address if self.booking.room_type and hasattr(self.booking.room_type, 'hotel') else 'N/A'),
                ('Téléphone', self.booking.room_type.hotel.phone if self.booking.room_type and hasattr(self.booking.room_type, 'hotel') else 'N/A'),
            ]
        )
        self.content_layout.add_widget(hotel_section)
        
        # Chambre
        room_section = self.create_section(
            '🛏️ Chambre',
            [
                ('Type', self.booking.room_type.name if self.booking.room_type else 'N/A'),
                ('Capacité', f"{self.booking.number_of_guests} personnes"),
                ('Nombre', f"{self.booking.number_of_rooms} chambre(s)"),
            ]
        )
        self.content_layout.add_widget(room_section)
        
        # Dates
        dates_section = self.create_section(
            '📅 Dates',
            [
                ('Arrivée', helpers.format_date(self.booking.check_in_date)),
                ('Départ', helpers.format_date(self.booking.check_out_date)),
                ('Nuits', f"{self.booking.number_of_nights} nuit(s)"),
            ]
        )
        self.content_layout.add_widget(dates_section)
        
        # Paiement
        if self.booking.payment:
            payment_status = self.booking.payment.get_payment_status_display()
            payment_color = COLORS['success'] if self.booking.payment.payment_status == 'completed' else COLORS['warning']
            
            payment_section = self.create_section(
                '💳 Paiement',
                [
                    ('Montant', helpers.format_price(self.booking.total_price)),
                    ('Statut', payment_status),
                    ('Transaction', self.booking.payment.transaction_id),
                ]
            )
            self.content_layout.add_widget(payment_section)
        
        # Demandes spéciales
        if self.booking.special_requests:
            requests_section = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(100),
                spacing=dp(5),
                padding=dp(10)
            )
            
            requests_section.add_widget(Label(
                text='📝 Demandes spéciales',
                font_size=dp(16),
                bold=True,
                color=COLORS['dark'],
                halign='left',
                size_hint_y=None,
                height=dp(30)
            ))
            
            requests_section.add_widget(Label(
                text=self.booking.special_requests,
                font_size=dp(14),
                color=COLORS['gray_dark'],
                halign='left',
                valign='top',
                size_hint_y=None,
                height=dp(60)
            ))
            
            self.content_layout.add_widget(requests_section)
        
        # Actions
        actions_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120),
            padding=dp(10)
        )
        
        if self.booking.status == 'pending' and self.booking.payment:
            pay_button = Button(
                text='✅ Procéder au paiement',
                font_size=dp(16),
                size_hint_y=None,
                height=dp(50),
                background_color=COLORS['success'],
                color=(1, 1, 1, 1)
            )
            pay_button.bind(on_press=self.process_payment)
            actions_layout.add_widget(pay_button)
        
        if self.booking.can_cancel:
            cancel_button = Button(
                text='❌ Annuler la réservation',
                font_size=dp(16),
                size_hint_y=None,
                height=dp(50),
                background_color=COLORS['danger'],
                color=(1, 1, 1, 1)
            )
            cancel_button.bind(on_press=self.confirm_cancel)
            actions_layout.add_widget(cancel_button)
        
        back_button = Button(
            text='← Retour aux réservations',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['gray'],
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=lambda x: self.go_back())
        actions_layout.add_widget(back_button)
        
        self.content_layout.add_widget(actions_layout)
    
    def create_section(self, title, items):
        """Crée une section d'information"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(5),
            padding=dp(10)
        )
        section.bind(minimum_height=section.setter('height'))
        
        # Titre
        section.add_widget(Label(
            text=title,
            font_size=dp(16),
            bold=True,
            color=COLORS['dark'],
            halign='left',
            size_hint_y=None,
            height=dp(30)
        ))
        
        # Ligne de séparation
        separator = BoxLayout(size_hint_y=None, height=dp(1))
        separator.canvas.before.add(Color(rgba=(0.8, 0.8, 0.8, 1)))
        separator.canvas.before.add(RoundedRectangle(pos=separator.pos, size=separator.size))
        section.add_widget(separator)
        
        # Items
        for label, value in items:
            item_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(30),
                spacing=dp(10)
            )
            
            item_layout.add_widget(Label(
                text=f"{label}:",
                font_size=dp(14),
                color=COLORS['gray'],
                halign='left',
                size_hint_x=0.4
            ))
            
            item_layout.add_widget(Label(
                text=value,
                font_size=dp(14),
                color=COLORS['dark'],
                bold=True,
                halign='right',
                size_hint_x=0.6
            ))
            
            section.add_widget(item_layout)
        
        section.height = len(items) * 35 + 60
        return section
    
    def process_payment(self, instance):
        """Traite le paiement"""
        instance.disabled = True
        instance.text = "Traitement..."
        
        success = api_client.process_payment(self.booking_id)
        
        if success:
            instance.text = "✅ Paiement réussi!"
            Clock.schedule_once(lambda dt: self.load_booking_data(), 1)
        else:
            instance.text = "❌ Erreur de paiement"
            instance.disabled = False
    
    def confirm_cancel(self, instance):
        """Confirme l'annulation"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        content.add_widget(Label(
            text='Voulez-vous vraiment annuler cette réservation ?',
            font_size=dp(14)
        ))
        
        buttons = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        confirm_btn = Button(
            text='Confirmer',
            background_color=COLORS['danger'],
            color=(1, 1, 1, 1)
        )
        cancel_btn = Button(
            text='Annuler',
            background_color=COLORS['gray'],
            color=(1, 1, 1, 1)
        )
        
        buttons.add_widget(confirm_btn)
        buttons.add_widget(cancel_btn)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Confirmation',
            content=content,
            size_hint=(0.8, 0.4),
            separator_color=COLORS['danger']
        )
        
        confirm_btn.bind(on_press=lambda x: self._do_cancel(popup))
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def _do_cancel(self, popup):
        """Effectue l'annulation"""
        popup.dismiss()
        success = api_client.cancel_booking(self.booking_id)
        if success:
            self.load_booking_data()
    
    def go_back(self):
        """Retour à la liste des réservations"""
        self.manager.current = 'bookings'
    
    def _hex_to_rgb(self, hex_color, alpha=1):
        """Convertit une couleur hexadécimale en RGB"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        return (r, g, b, alpha)
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'