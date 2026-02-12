from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import StringProperty

class LoadingIndicator(BoxLayout):
    """Indicateur de chargement animé"""
    
    message = StringProperty("Chargement...")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(100)
        self.spacing = dp(10)
        self.padding = dp(20)
        
        self._build_ui()
        self._animate()
    
    def _build_ui(self):
        # Points animés
        self.dots_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(10)
        )
        
        self.dots = []
        for i in range(3):
            dot = Label(
                text='●',
                font_size=dp(20),
                color=(0.2, 0.4, 0.8, 1)
            )
            self.dots.append(dot)
            self.dots_layout.add_widget(dot)
        
        # Message
        message_label = Label(
            text=self.message,
            font_size=dp(14),
            color=(0.4, 0.4, 0.4, 1)
        )
        
        self.add_widget(self.dots_layout)
        self.add_widget(message_label)
    
    def _animate(self):
        """Animation des points"""
        for i, dot in enumerate(self.dots):
            anim = Animation(
                opacity=0.2,
                duration=0.5
            ) + Animation(
                opacity=1,
                duration=0.5
            )
            anim.repeat = True
            anim.start(dot)
            
            # Décaler le démarrage
            Clock.schedule_once(lambda dt, a=anim: a, i * 0.2)
    
    def stop_animation(self):
        """Arrête l'animation"""
        for dot in self.dots:
            Animation.cancel_all(dot)
            dot.opacity = 1