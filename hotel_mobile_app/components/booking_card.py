from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

from utils.helpers import helpers
from config import COLORS

class BookingCard(BoxLayout):
    """Carte de réservation pour la liste"""
    
    booking_id = NumericProperty(0)
    hotel_name = StringProperty("")
    room_name = StringProperty("")
    check_in = StringProperty("")
    check_out = StringProperty("")
    nights = NumericProperty(0)
    guests = NumericProperty(0)
    total_price = NumericProperty(0)
    status = StringProperty("")
    status_display = StringProperty("")
    can_cancel = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(180)
        self.spacing = dp(8)
        self.padding = dp(15)
        
        with self.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(8),]
            )
        
        self.bind(pos=self._update_rect, size=self._update_rect)
        self._build_ui()
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def _build_ui(self):
        # En-tête
        header = BoxLayout(size_hint_y=None, height=dp(30))
        
        hotel_label = Label(
            text=f"[b]{self.hotel_name}[/b]",
            markup=True,
            font_size=dp(16),
            color=COLORS['dark'],
            halign='left',
            valign='middle',
            size_hint_x=0.6
        )
        hotel_label.bind(size=hotel_label.setter('text_size'))
        
        status_color = helpers.get_booking_status_color(self.status)
        status_label = Label(
            text=self.status_display,
            font_size=dp(12),
            color=status_color,
            halign='right',
            valign='middle',
            size_hint_x=0.4
        )
        status_label.bind(size=status_label.setter('text_size'))
        
        header.add_widget(hotel_label)
        header.add_widget(status_label)
        
        # Détails chambre
        room_label = Label(
            text=f"🛏️ {self.room_name}",
            font_size=dp(14),
            color=COLORS['gray'],
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(25)
        )
        room_label.bind(size=room_label.setter('text_size'))
        
        # Dates
        dates = helpers.format_date_range(self.check_in, self.check_out)
        dates_label = Label(
            text=f"📅 {dates}",
            font_size=dp(14),
            color=COLORS['gray'],
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(25)
        )
        dates_label.bind(size=dates_label.setter('text_size'))
        
        # Personnes
        guests_label = Label(
            text=f"👥 {self.guests} personne(s)",
            font_size=dp(14),
            color=COLORS['gray'],
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(25)
        )
        guests_label.bind(size=guests_label.setter('text_size'))
        
        # Pied
        footer = BoxLayout(size_hint_y=None, height=dp(50))
        
        price_label = Label(
            text=f"[size=18][b]{helpers.format_price(self.total_price)}[/b][/size]",
            markup=True,
            font_size=dp(18),
            color=COLORS['primary'],
            halign='left',
            valign='middle',
            size_hint_x=0.5
        )
        price_label.bind(size=price_label.setter('text_size'))
        
        actions = BoxLayout(spacing=dp(10), size_hint_x=0.5)
        
        view_button = Button(
            text='Voir',
            font_size=dp(14),
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1),
            size_hint_x=0.5
        )
        view_button.bind(on_press=lambda x: self.on_view())
        
        actions.add_widget(view_button)
        
        if self.can_cancel:
            cancel_button = Button(
                text='Annuler',
                font_size=dp(14),
                background_color=COLORS['danger'],
                color=(1, 1, 1, 1),
                size_hint_x=0.5
            )
            cancel_button.bind(on_press=lambda x: self.on_cancel())
            actions.add_widget(cancel_button)
        
        footer.add_widget(price_label)
        footer.add_widget(actions)
        
        # Ajouter tous les widgets
        self.add_widget(header)
        self.add_widget(room_label)
        self.add_widget(dates_label)
        self.add_widget(guests_label)
        self.add_widget(footer)
    
    def on_view(self):
        """Gère le clic sur le bouton Voir"""
        self.dispatch('on_view', self.booking_id)
    
    def on_cancel(self):
        """Gère le clic sur le bouton Annuler"""
        self.dispatch('on_cancel', self.booking_id)
    
    def on_view(self, booking_id):
        """Événement déclenché lors du clic sur Voir"""
        pass
    
    def on_cancel(self, booking_id):
        """Événement déclenché lors du clic sur Annuler"""
        pass

from kivy.event import EventDispatcher

class BookingCard(BoxLayout, EventDispatcher):
    __events__ = ('on_view', 'on_cancel')
    
    def on_view(self, booking_id):
        pass
    
    def on_cancel(self, booking_id):
        pass