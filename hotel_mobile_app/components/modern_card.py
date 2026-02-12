from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ColorProperty, ObjectProperty
from kivy.event import EventDispatcher
from kivy.utils import get_color_from_hex

from config import COLORS, BORDER_RADIUS, SPACING, FONT_SIZES

class ModernCard(BoxLayout):
    """
    Carte moderne avec ombre, coins arrondis
    """
    elevation = NumericProperty(2)
    radius = NumericProperty(BORDER_RADIUS['md'])
    padding_card = NumericProperty(SPACING['md'])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Fond et ombre
        with self.canvas.before:
            # Ombre
            Color(rgba=(0, 0, 0, 0.1))
            self.shadow = RoundedRectangle(
                pos=(self.x, self.y - dp(2)),
                size=self.size,
                radius=[self.radius]
            )
            # Fond blanc
            Color(rgba=(1, 1, 1, 1))
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius]
            )
        
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_rect(self, *args):
        """Met à jour les rectangles"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.shadow.pos = (self.x, self.y - dp(2))
        self.shadow.size = self.size


class HotelCardModern(ModernCard, EventDispatcher):
    """
    Carte d'hôtel moderne
    """
    __events__ = ('on_book',)
    
    hotel_id = NumericProperty(0)
    name = StringProperty('')
    city = StringProperty('')
    stars = NumericProperty(0)
    price = NumericProperty(0)
    image_url = StringProperty('')
    is_favorite = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = SPACING['md']
        self.spacing = SPACING['sm']
        self._build_ui()
    
    def _build_ui(self):
        """Construit l'interface de la carte"""
        # Conteneur principal
        content = BoxLayout(
            orientation='horizontal',
            spacing=SPACING['md'],
            size_hint_y=None,
            height=dp(120)
        )
        
        # Zone d'image
        image_container = BoxLayout(
            size_hint_x=0.3,
            size_hint_y=None,
            height=dp(100)
        )
        
        with image_container.canvas:
            Color(rgba=(0.2, 0.4, 0.8, 0.1))
            RoundedRectangle(
                pos=image_container.pos,
                size=image_container.size,
                radius=[BORDER_RADIUS['sm']]
            )
        
        image_container.add_widget(Label(
            text='🏨',
            font_size=sp(32)
        ))
        
        # Zone d'information
        info = BoxLayout(
            orientation='vertical',
            size_hint_x=0.7,
            spacing=SPACING['xs']
        )
        
        # Nom de l'hôtel
        name_label = Label(
            text=f'[b]{self.name}[/b]',
            markup=True,
            font_size=sp(FONT_SIZES['md']),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            size_hint_y=None,
            height=dp(25)
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        # Localisation
        location_label = Label(
            text=f'📍 {self.city}',
            font_size=sp(FONT_SIZES['sm']),
            color=(0.4, 0.4, 0.4, 1),
            halign='left',
            size_hint_y=None,
            height=dp(20)
        )
        location_label.bind(size=location_label.setter('text_size'))
        
        # Étoiles
        stars_text = '★' * self.stars + '☆' * (5 - self.stars)
        stars_label = Label(
            text=stars_text,
            font_size=sp(FONT_SIZES['sm']),
            color=(1, 0.8, 0, 1),  # Or
            halign='left',
            size_hint_y=None,
            height=dp(20)
        )
        stars_label.bind(size=stars_label.setter('text_size'))
        
        # Prix et bouton
        footer = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40)
        )
        
        price_label = Label(
            text=f'[size={sp(FONT_SIZES["lg"])}][b]{self.price}€[/b][/size][size={sp(FONT_SIZES["xs"])}] /nuit[/size]',
            markup=True,
            color=(0.2, 0.4, 0.8, 1),
            halign='left',
            size_hint_x=0.6
        )
        price_label.bind(size=price_label.setter('text_size'))
        
        from components.modern_button import ModernButton
        book_button = ModernButton(
            text='Réserver',
            font_size=sp(FONT_SIZES['sm']),
            height=dp(36),
            size_hint_x=0.4
        )
        book_button.bind(on_press=lambda x: self.dispatch('on_book', self.hotel_id))
        
        footer.add_widget(price_label)
        footer.add_widget(book_button)
        
        # Assemblage
        info.add_widget(name_label)
        info.add_widget(location_label)
        info.add_widget(stars_label)
        info.add_widget(footer)
        
        content.add_widget(image_container)
        content.add_widget(info)
        
        self.add_widget(content)
    
    def on_book(self, hotel_id):
        """Événement déclenché lors du clic sur Réserver"""
        pass