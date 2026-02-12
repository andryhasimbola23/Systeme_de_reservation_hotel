from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ColorProperty
from kivy.utils import get_color_from_hex

from config import COLORS, BORDER_RADIUS, SPACING, FONT_SIZES, ANIMATION

class ModernTextInput(TextInput):
    """
    Champ de texte moderne avec animation de focus
    """
    radius = NumericProperty(BORDER_RADIUS['sm'])
    focused_color = ColorProperty(COLORS['primary'])
    unfocused_color = ColorProperty(COLORS['border'])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = sp(FONT_SIZES['md'])
        self.size_hint_y = None
        self.height = dp(52)
        self.padding = [dp(16), dp(14)]
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (1, 1, 1, 1)
        self.foreground_color = (0.1, 0.1, 0.1, 1)
        self.hint_text_color = (0.6, 0.6, 0.6, 1)
        
        # Bordure
        self.border_color = self.unfocused_color
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(focus=self._on_focus)
    
    def _update_rect(self, *args):
        """Met à jour les rectangles"""
        pass
    
    def _on_focus(self, instance, value):
        """Animation lors du focus"""
        self.border_color = self.focused_color if value else self.unfocused_color


class ModernInputField(BoxLayout):
    """
    Champ de formulaire complet avec label et validation
    """
    label_text = StringProperty('')
    hint_text = StringProperty('')
    value = StringProperty('')
    error_message = StringProperty('')
    has_error = BooleanProperty(False)
    password = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = SPACING['xs']
        self.size_hint_y = None
        self.height = dp(80)
        
        # Label
        if self.label_text:
            label = Label(
                text=self.label_text,
                font_size=sp(FONT_SIZES['sm']),
                color=(0.4, 0.4, 0.4, 1),
                halign='left',
                size_hint_y=None,
                height=dp(20)
            )
            label.bind(size=label.setter('text_size'))
            self.add_widget(label)
        
        # Champ de saisie
        self.input = ModernTextInput(
            hint_text=self.hint_text,
            password=self.password,
            multiline=False
        )
        self.input.bind(text=self.on_text_change)
        self.add_widget(self.input)
        
        # Message d'erreur
        self.error_label = Label(
            text='',
            font_size=sp(FONT_SIZES['xs']),
            color=(0.9, 0.2, 0.2, 1),  # Rouge
            halign='left',
            size_hint_y=None,
            height=dp(16)
        )
        self.error_label.bind(size=self.error_label.setter('text_size'))
        self.add_widget(self.error_label)
    
    def on_text_change(self, instance, value):
        """Quand le texte change"""
        self.value = value
        if self.has_error:
            self.set_error('')
    
    def set_error(self, message):
        """Définit un message d'erreur"""
        self.error_message = message
        self.error_label.text = message
        self.has_error = bool(message)
        
        if message:
            self.input.focused_color = (0.9, 0.2, 0.2, 1)  # Rouge
        else:
            self.input.focused_color = (0.2, 0.4, 0.8, 1)  # Bleu