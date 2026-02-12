from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty

from config import COLORS

class HotelCard(BoxLayout):
    """Carte d'hôtel pour la liste"""
    
    # Propriétés
    hotel_id = NumericProperty(0)
    name = StringProperty("")
    city = StringProperty("")
    country = StringProperty("")
    stars = NumericProperty(0)
    description = StringProperty("")
    price = NumericProperty(0)
    image_url = StringProperty("")
    is_favorite = BooleanProperty(False)
    features = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(300)
        self.spacing = dp(8)
        self.padding = dp(12)
        
        with self.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12),]
            )
            
            Color(rgba=(0.9, 0.9, 0.9, 1))
            self.border = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12),]
            )
        
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Construire l'interface
        self._build_ui()
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.pos = (self.pos[0] - 1, self.pos[1] - 1)
        self.border.size = (self.size[0] + 2, self.size[1] + 2)
    
    def _build_ui(self):
        # En-tête avec nom et étoiles
        header = BoxLayout(size_hint_y=None, height=dp(40))
        
        # Nom de l'hôtel
        name_label = Label(
            text=self.name,
            font_size=dp(16),
            font_name='Roboto',
            bold=True,
            color=COLORS['dark'],
            halign='left',
            valign='middle',
            size_hint_x=0.7
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        # Étoiles
        stars_box = BoxLayout(size_hint_x=0.3, spacing=dp(2))
        for i in range(5):
            star_label = Label(
                text='★' if i < self.stars else '☆',
                font_size=dp(14),
                color='#FFD700' if i < self.stars else COLORS['gray'],
                size_hint_x=0.2
            )
            stars_box.add_widget(star_label)
        
        header.add_widget(name_label)
        header.add_widget(stars_box)
        
        # Localisation
        location_label = Label(
            text=f"[size=12]{self.city}, {self.country}[/size]",
            markup=True,
            font_name='Roboto',
            color=COLORS['secondary'],
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(20)
        )
        location_label.bind(size=location_label.setter('text_size'))
        
        # Image (placeholder si pas d'image)
        image_container = BoxLayout(size_hint_y=None, height=dp(150))
        if self.image_url:
            image = AsyncImage(
                source=self.image_url,
                allow_stretch=True,
                keep_ratio=True
            )
        else:
            image = Label(
                text='[size=48]🏨[/size]',
                markup=True,
                font_name='Roboto',
                color=COLORS['primary']
            )
        image_container.add_widget(image)
        
        # Description
        desc_label = Label(
            text=self.description[:100] + '...' if len(self.description) > 100 else self.description,
            font_size=dp(12),
            font_name='Roboto',
            color=COLORS['gray_dark'],
            halign='left',
            valign='top',
            size_hint_y=None,
            height=dp(40)
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        
        # Features
        features_box = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(4))
        for feature in self.features[:4]:  # Limiter à 4 features
            if feature:
                feature_label = Label(
                    text=feature,
                    font_size=dp(10),
                    font_name='Roboto',
                    color=COLORS['primary'],
                    size_hint_x=None,
                    width=dp(60)
                )
                feature_label.canvas.before.add(Color(rgba=(0.87, 0.92, 1, 1)))
                feature_label.canvas.before.add(RoundedRectangle(
                    pos=feature_label.pos,
                    size=feature_label.size,
                    radius=[dp(8),]
                ))
                features_box.add_widget(feature_label)
        
        # Pied avec prix et bouton
        footer = BoxLayout(size_hint_y=None, height=dp(40))
        
        price_label = Label(
            text=f"[size=18][b]{self.price}€[/b][/size]\n[size=10]/nuit[/size]",
            markup=True,
            font_name='Roboto',
            color=COLORS['primary'],
            halign='left',
            valign='middle',
            size_hint_x=0.6
        )
        price_label.bind(size=price_label.setter('text_size'))
        
        view_button = Button(
            text='Voir',
            size_hint_x=0.4,
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1),
            font_name='Roboto',
            font_size=dp(14),
            bold=True
        )
        view_button.bind(on_release=self.on_view)
        
        footer.add_widget(price_label)
        footer.add_widget(view_button)
        
        # Ajouter tous les widgets
        self.add_widget(header)
        self.add_widget(location_label)
        self.add_widget(image_container)
        self.add_widget(desc_label)
        self.add_widget(features_box)
        self.add_widget(footer)
    
    def on_view(self, instance):
        """Gère le clic sur le bouton Voir"""
        print(f"Voir l'hôtel {self.hotel_id}: {self.name}")
        # Cette méthode sera surchargée par l'écran parent