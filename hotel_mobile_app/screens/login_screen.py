from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock

from api.api_client import api_client
from utils.validators import validators
from config import COLORS

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
        
        # Logo
        logo = Label(
            text='[size=48]🏨[/size]\n[size=24]Hotel Reservation[/size]',
            markup=True,
            font_name='Roboto',
            halign='center',
            size_hint_y=0.3
        )
        
        # Formulaire
        form_layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        # Champ nom d'utilisateur
        self.username_input = TextInput(
            hint_text='Nom d\'utilisateur',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS['dark']
        )
        
        # Champ mot de passe
        self.password_input = TextInput(
            hint_text='Mot de passe',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            password=True,
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS['dark']
        )
        
        # Bouton connexion
        login_button = Button(
            text='Se connecter',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(55),
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1),
            bold=True
        )
        login_button.bind(on_press=self.on_login)
        
        # Lien inscription
        register_label = Label(
            text='[ref=register]Pas encore de compte ? Inscrivez-vous[/ref]',
            markup=True,
            font_size=dp(14),
            color=COLORS['primary'],
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        register_label.bind(on_ref_press=self.on_register_link)
        
        # Message d'erreur
        self.error_label = Label(
            text='',
            font_size=dp(14),
            color=COLORS['danger'],
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        # Ajout des widgets
        form_layout.add_widget(self.username_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(login_button)
        form_layout.add_widget(register_label)
        form_layout.add_widget(self.error_label)
        
        main_layout.add_widget(logo)
        main_layout.add_widget(form_layout)
        
        self.add_widget(main_layout)
    
    def on_login(self, instance):
        """Gère la connexion"""
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        # Validation
        if not username or not password:
            self.show_error("Veuillez remplir tous les champs")
            return
        
        # Désactiver le bouton
        instance.disabled = True
        instance.text = "Connexion..."
        
        # Tentative de connexion
        Clock.schedule_once(lambda dt: self._perform_login(username, password, instance), 0.1)
    
    def _perform_login(self, username, password, button):
        """Effectue la connexion API"""
        user = api_client.login(username, password)
        
        if user:
            self.show_error("")  # Effacer les erreurs
            print(f"Connecté en tant que {user.username}")
            # Naviguer vers l'écran d'accueil
            self.manager.current = 'home'
        else:
            self.show_error("Identifiants incorrects")
        
        # Réactiver le bouton
        button.disabled = False
        button.text = "Se connecter"
    
    def on_register_link(self, instance, value):
        """Navigue vers l'écran d'inscription"""
        self.manager.current = 'register'
    
    def show_error(self, message):
        """Affiche un message d'erreur"""
        self.error_label.text = message
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        # Effacer les champs
        self.username_input.text = ""
        self.password_input.text = ""
        self.show_error("")
        
        # Vérifier si déjà connecté
        if api_client.is_authenticated():
            # ✅ Vérifier d'abord si l'écran home existe
            if self.manager and 'home' in self.manager.screen_names:
                self.manager.current = 'home'
            else:
                print("⚠️ Écran home non trouvé, redirection vers login")
                self.manager.current = 'login'