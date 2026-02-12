from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, ColorProperty, BooleanProperty

from config import COLORS, BORDER_RADIUS, ANIMATION

class ModernButton(Button):
    """
    Bouton moderne avec animation de toucher et design élégant
    """
    background_color = ColorProperty(COLORS['primary'])
    text_color = ColorProperty(COLORS['text_white'])
    radius = NumericProperty(BORDER_RADIUS['md'])
    elevation = NumericProperty(2)
    outlined = BooleanProperty(False)
    icon = StringProperty('')
    icon_size = NumericProperty(sp(18))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = sp(16)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(52)
        self.color = self.text_color
        self.pressed = False
        
        self.bind(background_color=self._update_color)
        self.bind(text_color=self._update_text_color)
    
    def _update_color(self, *args):
        self.canvas.ask_update()
    
    def _update_text_color(self, *args):
        self.color = self.text_color
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = True
            anim = Animation(
                scale=0.95, 
                duration=ANIMATION['duration']/2, 
                t=ANIMATION['transition']
            )
            anim.start(self)
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if self.pressed:
            anim = Animation(
                scale=1, 
                duration=ANIMATION['duration']/2, 
                t=ANIMATION['transition']
            )
            anim.start(self)
            self.pressed = False
        return super().on_touch_up(touch)


class ModernButtonIcon(BoxLayout):
    """
    Bouton avec icône et texte
    """
    text = StringProperty('')
    icon = StringProperty('')
    background_color = ColorProperty(COLORS['primary'])
    text_color = ColorProperty(COLORS['text_white'])
    outlined = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(8)
        self.padding = [dp(16), dp(12)]
        self.size_hint_y = None
        self.height = dp(52)
        
        # Fond du bouton
        with self.canvas.before:
            if self.outlined:
                Color(rgba=(1, 1, 1, 1))
                self.bg_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[BORDER_RADIUS['md']]
                )
                Color(rgba=self.background_color)
                self.border_rect = RoundedRectangle(
                    pos=(self.x + 1, self.y + 1),
                    size=(self.width - 2, self.height - 2),
                    radius=[BORDER_RADIUS['md'] - 1]
                )
            else:
                Color(rgba=self.background_color)
                self.bg_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[BORDER_RADIUS['md']]
                )
        
        # Icône
        if self.icon:
            icon_label = Label(
                text=self.icon,
                font_size=sp(20),
                color=self.text_color,
                size_hint_x=0.2
            )
            self.add_widget(icon_label)
        
        # Texte
        text_label = Label(
            text=self.text,
            font_size=sp(16),
            color=self.text_color,
            bold=True,
            size_hint_x=0.8
        )
        self.add_widget(text_label)
        
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(background_color=self._update_color)
    
    def _update_rect(self, *args):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
        if hasattr(self, 'border_rect'):
            self.border_rect.pos = (self.x + 1, self.y + 1)
            self.border_rect.size = (self.width - 2, self.height - 2)
    
    def _update_color(self, *args):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.rgba = self.background_color
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            anim = Animation(
                scale=0.95,
                duration=ANIMATION['duration']/2,
                t=ANIMATION['transition']
            )
            anim.start(self)
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            anim = Animation(
                scale=1,
                duration=ANIMATION['duration']/2,
                t=ANIMATION['transition']
            )
            anim.start(self)
            if hasattr(self, 'on_press'):
                self.on_press()
        return super().on_touch_up(touch)
    
    def on_press(self):
        """Méthode à surcharger pour gérer le clic"""
        pass