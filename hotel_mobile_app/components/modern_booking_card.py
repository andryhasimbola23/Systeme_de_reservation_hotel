# components/modern_booking_card.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.event import EventDispatcher

from components.modern_card import ModernCard
from utils.helpers import helpers
from config import COLORS, SPACING, FONT_SIZES, BORDER_RADIUS

class ModernBookingCard(ModernCard, EventDispatcher):
    """
    Carte de réservation moderne
    """
    __events__ = ('on_view', 'on_cancel')
    
    booking_id = NumericProperty(0)
    hotel_name = StringProperty('')
    room_name = StringProperty('')
    check_in = StringProperty('')
    check_out = StringProperty('')
    nights = NumericProperty(0)
    guests = NumericProperty(0)
    total_price = NumericProperty(0)
    status = StringProperty('')
    status_display = StringProperty('')
    can_cancel = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = SPACING['lg']
        self.spacing = SPACING['md']
        self._build_ui()
    
    def _build_ui(self):
        # En-tête avec hôtel et statut
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30)
        )
        
        hotel_label = Label(
            text=f'[b]{self.hotel_name}[/b]',
            markup=True,
            font_size=sp(FONT_SIZES['md']),
            color=self._hex_to_rgba(COLORS['text_primary']),
            halign='left',
            size_hint_x=0.6
        )
        hotel_label.bind(size=hotel_label.setter('text_size'))
        
        status_color = helpers.get_booking_status_color(self.status)
        status_label = Label(
            text=self.status_display,
            font_size=sp(FONT_SIZES['sm']),
            color=self._hex_to_rgba(status_color),
            halign='right',
            size_hint_x=0.4
        )
        status_label.bind(size=status_label.setter('text_size'))
        
        header.add_widget(hotel_label)
        header.add_widget(status_label)
        
        # Détails de la chambre
        room_label = Label(
            text=f'🛏️ {self.room_name}',
            font_size=sp(FONT_SIZES['sm']),
            color=self._hex_to_rgba(COLORS['text_secondary']),
            halign='left',
            size_hint_y=None,
            height=dp(25)
        )
        room_label.bind(size=room_label.setter('text_size'))
        
        # Dates
        dates_text = f'📅 {helpers.format_date_range(self.check_in, self.check_out)}'
        dates_label = Label(
            text=dates_text,
            font_size=sp(FONT_SIZES['sm']),
            color=self._hex_to_rgba(COLORS['text_secondary']),
            halign='left',
            size_hint_y=None,
            height=dp(25)
        )
        dates_label.bind(size=dates_label.setter('text_size'))
        
        # Prix et actions
        footer = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=SPACING['md']
        )
        
        price_label = Label(
            text=f'[size={sp(FONT_SIZES["lg"])}][b]{helpers.format_price(self.total_price)}[/b][/size]',
            markup=True,
            font_size=sp(FONT_SIZES['lg']),
            color=self._hex_to_rgba(COLORS['primary']),
            halign='left',
            size_hint_x=0.5
        )
        price_label.bind(size=price_label.setter('text_size'))
        
        actions = BoxLayout(
            orientation='horizontal',
            spacing=SPACING['sm'],
            size_hint_x=0.5
        )
        
        view_btn = Button(
            text='Voir',
            font_size=sp(FONT_SIZES['sm']),
            background_color=self._hex_to_rgba(COLORS['primary']),
            color=(1, 1, 1, 1),
            size_hint_x=0.5
        )
        view_btn.bind(on_press=lambda x: self.dispatch('on_view', self.booking_id))
        
        actions.add_widget(view_btn)
        
        if self.can_cancel:
            cancel_btn = Button(
                text='Annuler',
                font_size=sp(FONT_SIZES['sm']),
                background_color=self._hex_to_rgba(COLORS['danger']),
                color=(1, 1, 1, 1),
                size_hint_x=0.5
            )
            cancel_btn.bind(on_press=lambda x: self.dispatch('on_cancel', self.booking_id))
            actions.add_widget(cancel_btn)
        
        footer.add_widget(price_label)
        footer.add_widget(actions)
        
        # Assemblage
        self.add_widget(header)
        self.add_widget(room_label)
        self.add_widget(dates_label)
        self.add_widget(footer)
    
    def on_view(self, booking_id):
        pass
    
    def on_cancel(self, booking_id):
        pass