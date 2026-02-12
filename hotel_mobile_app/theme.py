from kivy.core.text import LabelBase
from kivy.utils import platform

# Police personnalisée
if platform == 'android':
    LabelBase.register(name='Roboto', fn_regular='assets/fonts/Roboto-Regular.ttf')
    LabelBase.register(name='Roboto-Bold', fn_regular='assets/fonts/Roboto-Bold.ttf')
else:
    LabelBase.register(name='Roboto', fn_regular='assets/fonts/Roboto-Regular.ttf')
    LabelBase.register(name='Roboto-Bold', fn_regular='assets/fonts/Roboto-Bold.ttf')

# Thème sombre/clair
THEME = {
    'light': {
        'bg_color': '#f8fafc',
        'surface_color': '#ffffff',
        'text_color': '#0f172a',
        'text_secondary': '#475569',
        'border_color': '#e2e8f0',
    },
    'dark': {
        'bg_color': '#0f172a',
        'surface_color': '#1e293b',
        'text_color': '#f1f5f9',
        'text_secondary': '#94a3b8',
        'border_color': '#334155',
    }
}

# Animations
ANIMATIONS = {
    'fast': 0.2,
    'normal': 0.3,
    'slow': 0.5,
}

# Dimensions
DIMENSIONS = {
    'card_radius': 16,
    'button_radius': 25,
    'input_radius': 25,
    'padding_small': 8,
    'padding_medium': 16,
    'padding_large': 24,
}