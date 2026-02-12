from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty

from config import COLORS

class RoomCard(BoxLayout):
    """Carte de chambre pour le détail d'hôtel"""
    
    room_id = NumericProperty(0)
    name = StringProperty("")
    room_type = StringProperty("")
    capacity = NumericProperty(0)
    size = NumericProperty(0)
    price = NumericProperty(0)
    available = NumericProperty(0)
    features = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(200)
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
        
        name_label = Label(
            text=f"[b]{self.name}[/b]",
            markup=True,
            font_size=dp(16),
            color=COLORS['dark'],
            halign='left',
            valign='middle',
            size_hint_x=0.7
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        type_label = Label(
            text=self.room_type,
            font_size=dp(12),
            color=COLORS['gray'],
            halign='right',
            valign='middle',
            size_hint_x=0.3
        )
        type_label.bind(size=type_label.setter('text_size'))
        
        header.add_widget(name_label)
        header.add_widget(type_label)
        
        # Détails
        details = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(10))
        
        details.add_widget(Label(
            text=f"👥 {self.capacity} pers.",
            font_size=dp(12),
            color=COLORS['gray']
        ))
        
        details.add_widget(Label(
            text=f"📏 {self.size}m²",
            font_size=dp(12),
            color=COLORS['gray']
        ))
        
        # Équipements
        features_layout = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(5))
        
        for feature in self.features:
            if feature:
                feature_label = Label(
                    text=feature,
                    font_size=dp(14),
                    color=COLORS['primary']
                )
                features_layout.add_widget(feature_label)
        
        # Pied
        footer = BoxLayout(size_hint_y=None, height=dp(50))
        
        price_label = Label(
            text=f"[size=18][b]{self.price}€[/b][/size][size=12] /nuit[/size]",
            markup=True,
            font_size=dp(12),
            color=COLORS['primary'],
            halign='left',
            valign='middle',
            size_hint_x=0.5
        )
        price_label.bind(size=price_label.setter('text_size'))
        
        availability_label = Label(
            text=f"{self.available} disponible(s)",
            font_size=dp(12),
            color=COLORS['success'] if self.available > 0 else COLORS['danger'],
            halign='center',
            valign='middle',
            size_hint_x=0.3
        )
        availability_label.bind(size=availability_label.setter('text_size'))
        
        book_button = Button(
            text='Réserver',
            font_size=dp(14),
            background_color=COLORS['primary'] if self.available > 0 else COLORS['gray'],
            color=(1, 1, 1, 1),
            size_hint_x=0.2,
            disabled=self.available <= 0
        )
        book_button.bind(on_press=lambda x: self.on_book())
        
        footer.add_widget(price_label)
        footer.add_widget(availability_label)
        footer.add_widget(book_button)
        
        # Ajouter tous les widgets
        self.add_widget(header)
        self.add_widget(details)
        self.add_widget(features_layout)
        self.add_widget(footer)
    
    def on_book(self):
        """Gère le clic sur le bouton Réserver"""
        self.dispatch('on_book', self.room_id, self.price, self.name)
    
    def on_book(self, room_id, price, name):
        """Événement déclenché lors du clic sur Réserver"""
        pass

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

class RoomCard(BoxLayout, EventDispatcher):
    __events__ = ('on_book',)
    
    def on_book(self, room_id, price, name):
        pass