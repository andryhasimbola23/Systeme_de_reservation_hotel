from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, BooleanProperty, ColorProperty, ListProperty
from kivy.animation import Animation
from kivy.utils import get_color_from_hex

from config import COLORS, BORDER_RADIUS, SPACING, ANIMATION

class ModernNavItem(BoxLayout):
    """
    Élément de navigation individuel
    """
    icon = StringProperty('')
    text = StringProperty('')
    active = BooleanProperty(False)
    active_color = ColorProperty(COLORS['primary'])
    inactive_color = ColorProperty(COLORS['text_disabled'])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = SPACING['xs']
        self.padding = [SPACING['md'], SPACING['sm']]
        
        # Déterminer la couleur initiale
        initial_color = self.active_color if self.active else self.inactive_color
        
        # Icône
        self.icon_label = Label(
            text=self.icon,
            font_size=sp(24),
            color=initial_color,
            size_hint_y=None,
            height=dp(24)
        )
        
        # Texte
        self.text_label = Label(
            text=self.text,
            font_size=sp(12),
            color=initial_color,
            size_hint_y=None,
            height=dp(16)
        )
        
        self.add_widget(self.icon_label)
        self.add_widget(self.text_label)
    
    def set_active(self, active):
        """Active ou désactive l'élément"""
        self.active = active
        color = self.active_color if active else self.inactive_color
        self.icon_label.color = color
        self.text_label.color = color


class ModernNavBar(BoxLayout):
    """
    Barre de navigation moderne avec indicateur actif
    """
    current = StringProperty('home')
    items = ListProperty([
        {'screen': 'home', 'icon': '🏠', 'text': 'Accueil'},
        {'screen': 'hotels', 'icon': '🏨', 'text': 'Hôtels'},
        {'screen': 'search', 'icon': '🔍', 'text': 'Recherche'},
        {'screen': 'bookings', 'icon': '📅', 'text': 'Réservations'},
        {'screen': 'profile', 'icon': '👤', 'text': 'Profil'},
    ])
    
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = [SPACING['md'], SPACING['sm']]
        self.spacing = SPACING['xs']
        
        # Fond de la barre de navigation
        with self.canvas.before:
            # Ombre
            Color(rgba=(0, 0, 0, 0.05))
            self.shadow = RoundedRectangle(
                pos=(self.x, self.y + self.height - dp(2)),
                size=(self.size[0], dp(2)),
                radius=[0, 0, 0, 0]
            )
            # Fond blanc
            Color(rgba=(1, 1, 1, 1))
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[BORDER_RADIUS['lg'], BORDER_RADIUS['lg'], 0, 0]
            )
        
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(current=self._on_current_changed)
        self._build_nav_items()
    
    def _update_rect(self, *args):
        """Met à jour les rectangles"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.shadow.pos = (self.x, self.y + self.height - dp(2))
        self.shadow.size = (self.size[0], dp(2))
    
    def _on_current_changed(self, *args):
        """Quand l'écran courant change"""
        self._build_nav_items()
    
    def _build_nav_items(self):
        """Construit les éléments de navigation"""
        self.nav_items = []
        self.clear_widgets()
        
        for item in self.items:
            nav_item = ModernNavItem(
                icon=item['icon'],
                text=item['text'],
                active=(self.current == item['screen']),
                size_hint_x=1.0 / len(self.items)
            )
            
            # Rendre cliquable
            nav_item.bind(on_touch_down=lambda x, touch, s=item['screen']: self.on_nav_click(s, touch))
            
            self.nav_items.append(nav_item)
            self.add_widget(nav_item)
    
    def on_nav_click(self, screen, touch):
        """Gère le clic sur un élément de navigation"""
        for i, item in enumerate(self.items):
            if item['screen'] == screen:
                if self.nav_items[i].collide_point(*touch.pos):
                    self.set_current(screen)
                    if self.sm and screen in self.sm.screen_names:
                        self.sm.current = screen
                break
    
    def set_current(self, screen):
        """Définit l'écran actif"""
        self.current = screen
        for i, item in enumerate(self.nav_items):
            item.set_active(self.items[i]['screen'] == screen)