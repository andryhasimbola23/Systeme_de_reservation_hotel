# screens/modern_login_screen.py - VERSION CORRIGÉE
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.clock import Clock

from components.modern_button import ModernButton
from components.modern_input import ModernInputField
from api.api_client import api_client
from config import COLORS, SPACING, FONT_SIZES, ANIMATION

class ModernLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self._build_ui()
        print(f"🔐 Écran 'login' initialisé")
    
    def _build_ui(self):
        # Layout principal
        scroll = ScrollView()
        main = BoxLayout(
            orientation='vertical',
            padding=[SPACING['xl'], SPACING['xxl']],
            spacing=SPACING['lg'],
            size_hint_y=None
        )
        main.bind(minimum_height=main.setter('height'))
        
        # Logo
        logo_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            spacing=SPACING['md']
        )
        
        self.logo = Label(
            text='🏨',
            font_size=sp(80),
            color=(0.2, 0.4, 0.8, 1)
        )
        
        title = Label(
            text='[b]HotelReservation[/b]',
            markup=True,
            font_size=sp(FONT_SIZES['xxl']),
            color=(0.1, 0.1, 0.1, 1)
        )
        
        subtitle = Label(
            text='Connectez-vous pour continuer',
            font_size=sp(FONT_SIZES['md']),
            color=(0.4, 0.4, 0.4, 1)
        )
        
        logo_layout.add_widget(self.logo)
        logo_layout.add_widget(title)
        logo_layout.add_widget(subtitle)
        
        # Formulaire
        form_layout = BoxLayout(
            orientation='vertical',
            spacing=SPACING['md'],
            size_hint_y=None,
            height=dp(200)
        )
        
        self.username_field = ModernInputField(
            label_text='Nom d\'utilisateur',
            hint_text='Entrez votre nom d\'utilisateur'
        )
        
        self.password_field = ModernInputField(
            label_text='Mot de passe',
            hint_text='Entrez votre mot de passe',
            password=True
        )
        
        form_layout.add_widget(self.username_field)
        form_layout.add_widget(self.password_field)
        
        # Boutons
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=SPACING['md'],
            size_hint_y=None,
            height=dp(120)
        )
        
        self.login_button = ModernButton(
            text='Se connecter',
            background_color=COLORS['primary'],
            height=dp(52)
        )
        self.login_button.bind(on_press=self.on_login)
        
        register_button = ModernButton(
            text='Créer un compte',
            outlined=True,
            background_color=COLORS['primary'],
            height=dp(52)
        )
        register_button.bind(on_press=self.go_to_register)
        
        buttons_layout.add_widget(self.login_button)
        buttons_layout.add_widget(register_button)
        
        # Message d'erreur
        self.error_label = Label(
            text='',
            font_size=sp(FONT_SIZES['sm']),
            color=(0.9, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        # Assemblage
        main.add_widget(logo_layout)
        main.add_widget(form_layout)
        main.add_widget(buttons_layout)
        main.add_widget(self.error_label)
        
        scroll.add_widget(main)
        self.add_widget(scroll)
    
    def on_login(self, instance):
        """Gère la connexion"""
        username = self.username_field.value
        password = self.password_field.value
        
        # Validation
        self.username_field.set_error('')
        self.password_field.set_error('')
        
        has_error = False
        
        if not username:
            self.username_field.set_error('Nom d\'utilisateur requis')
            has_error = True
        
        if not password:
            self.password_field.set_error('Mot de passe requis')
            has_error = True
        
        if has_error:
            return
        
        # Animation de chargement
        instance.disabled = True
        instance.text = 'Connexion...'
        
        Clock.schedule_once(lambda dt: self._perform_login(instance), 0.1)
    
    def _perform_login(self, button):
        """Effectue la connexion API"""
        user = api_client.login(
            self.username_field.value,
            self.password_field.value
        )
        
        if user:
            self.error_label.text = ''
            button.text = '✅ Connecté!'
            Clock.schedule_once(lambda dt: self.go_to_home(), 0.5)
        else:
            self.error_label.text = '❌ Identifiants incorrects'
            button.disabled = False
            button.text = 'Se connecter'
    
    def go_to_home(self):
        """Navigation vers l'accueil"""
        print("🔄 Tentative de redirection vers 'home'")
        if self.manager and 'home' in self.manager.screen_names:
            self.manager.current = 'home'
            print("✅ Redirection vers 'home' réussie")
        else:
            print("❌ Écran 'home' non disponible")
    
    def go_to_register(self, instance):
        """Navigation vers l'inscription"""
        if self.manager and 'register' in self.manager.screen_names:
            self.manager.current = 'register'
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        # Réinitialiser les champs
        self.username_field.input.text = ''
        self.password_field.input.text = ''
        self.error_label.text = ''
        self.login_button.disabled = False
        self.login_button.text = 'Se connecter'
        
        # NE PAS REDIRIGER AUTOMATIQUEMENT ICI !
        # La redirection est gérée par hotel_app.py
        pass

