from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from config import COLORS

class Navbar(BoxLayout):
    """Barre de navigation principale"""
    
    def __init__(self, sm: ScreenManager, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(5)
        self.padding = [dp(10), dp(5)]
        
        with self.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(0),]
            )
            Color(rgba=(0.9, 0.9, 0.9, 1))
            self.border = RoundedRectangle(
                pos=(self.pos[0], self.pos[1] + self.size[1]),
                size=(self.size[0], dp(1)),
                radius=[dp(0),]
            )
        
        self.bind(pos=self._update_rect, size=self._update_rect)
        self._build_ui()
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.pos = (self.pos[0], self.pos[1] + self.size[1] - dp(1))
        self.border.size = (self.size[0], dp(1))
    
    def _build_ui(self):
        # Bouton Accueil
        home_btn = Button(
            text='🏠\nAccueil',
            font_size=dp(12),
            background_color=COLORS['primary'] if self.sm.current == 'home' else COLORS['gray'],
            color=(1, 1, 1, 1),
            size_hint_x=0.25
        )
        home_btn.bind(on_press=lambda x: self.navigate('home'))
        
        # Bouton Hôtels
        hotels_btn = Button(
            text='🏨\nHôtels',
            font_size=dp(12),
            background_color=COLORS['primary'] if self.sm.current == 'hotels' else COLORS['gray'],
            color=(1, 1, 1, 1),
            size_hint_x=0.25
        )
        hotels_btn.bind(on_press=lambda x: self.navigate('hotels'))
        
        # Bouton Recherche
        search_btn = Button(
            text='🔍\nRecherche',
            font_size=dp(12),
            background_color=COLORS['primary'] if self.sm.current == 'search' else COLORS['gray'],
            color=(1, 1, 1, 1),
            size_hint_x=0.25
        )
        search_btn.bind(on_press=lambda x: self.navigate('search'))
        
        # Bouton Réservations
        bookings_btn = Button(
            text='📅\nRéservations',
            font_size=dp(12),
            background_color=COLORS['primary'] if self.sm.current == 'bookings' else COLORS['gray'],
            color=(1, 1, 1, 1),
            size_hint_x=0.25
        )
        bookings_btn.bind(on_press=lambda x: self.navigate('bookings'))
        
        self.add_widget(home_btn)
        self.add_widget(hotels_btn)
        self.add_widget(search_btn)
        self.add_widget(bookings_btn)
    
    def navigate(self, screen_name):
        """Navigation vers un écran"""
        if screen_name in self.sm.screen_names:
            self.sm.current = screen_name
            self._build_ui()  # Reconstruire pour mettre à jour les couleurs