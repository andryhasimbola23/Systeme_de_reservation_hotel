from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import Clock

from api.api_client import api_client
from utils.validators import validators
from config import COLORS

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'register'
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal avec ScrollView pour les petits écrans
        scroll_view = ScrollView()
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(15),
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Logo
        logo = Label(
            text='[size=48]🏨[/size]\n[size=20]Créer un compte[/size]',
            markup=True,
            font_name='Roboto',
            halign='center',
            size_hint_y=None,
            height=dp(120)
        )
        
        # Formulaire
        form_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Prénom
        self.first_name_input = TextInput(
            hint_text='Prénom',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS['dark']
        )
        
        # Nom
        self.last_name_input = TextInput(
            hint_text='Nom',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS['dark']
        )
        
        # Nom d'utilisateur
        self.username_input = TextInput(
            hint_text='Nom d\'utilisateur *',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS['dark']
        )
        
        # Email
        self.email_input = TextInput(
            hint_text='Email *',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS['dark']
        )
        
        # Mot de passe
        self.password_input = TextInput(
            hint_text='Mot de passe *',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            password=True,
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS['dark']
        )
        
        # Confirmation mot de passe
        self.password_confirm_input = TextInput(
            hint_text='Confirmer le mot de passe *',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            password=True,
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS['dark']
        )
        
        # Message d'erreur
        self.error_label = Label(
            text='',
            font_size=dp(14),
            color=COLORS['danger'],
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        # Indicateur de force du mot de passe
        self.password_strength = Label(
            text='',
            font_size=dp(12),
            halign='center',
            size_hint_y=None,
            height=dp(20)
        )
        
        # Lier l'événement de saisie du mot de passe
        self.password_input.bind(text=self._check_password_strength)
        
        # Bouton d'inscription
        register_button = Button(
            text='S\'inscrire',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(55),
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1),
            bold=True
        )
        register_button.bind(on_press=self.on_register)
        
        # Lien vers connexion
        login_link = Label(
            text='[ref=login]Déjà un compte ? Se connecter[/ref]',
            markup=True,
            font_size=dp(14),
            color=COLORS['primary'],
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        login_link.bind(on_ref_press=self.on_login_link)
        
        # Mention champs obligatoires
        required_note = Label(
            text='* Champs obligatoires',
            font_size=dp(12),
            color=COLORS['gray'],
            halign='center',
            size_hint_y=None,
            height=dp(20)
        )
        
        # Ajout des widgets
        form_layout.add_widget(self.first_name_input)
        form_layout.add_widget(self.last_name_input)
        form_layout.add_widget(self.username_input)
        form_layout.add_widget(self.email_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(self.password_strength)
        form_layout.add_widget(self.password_confirm_input)
        form_layout.add_widget(self.error_label)
        form_layout.add_widget(register_button)
        form_layout.add_widget(login_link)
        form_layout.add_widget(required_note)
        
        main_layout.add_widget(logo)
        main_layout.add_widget(form_layout)
        
        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)
    
    def _check_password_strength(self, instance, value):
        """Vérifie la force du mot de passe"""
        if not value:
            self.password_strength.text = ''
            self.password_strength.color = COLORS['gray']
            return
        
        score = 0
        if len(value) >= 8:
            score += 1
        if any(c.isupper() for c in value):
            score += 1
        if any(c.islower() for c in value):
            score += 1
        if any(c.isdigit() for c in value):
            score += 1
        if any(c in '!@#$%^&*' for c in value):
            score += 1
        
        if score < 2:
            self.password_strength.text = 'Faible'
            self.password_strength.color = COLORS['danger']
        elif score < 4:
            self.password_strength.text = 'Moyen'
            self.password_strength.color = '#f59e0b'
        else:
            self.password_strength.text = 'Fort'
            self.password_strength.color = COLORS['success']
    
    def on_register(self, instance):
        """Gère l'inscription"""
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text
        password_confirm = self.password_confirm_input.text
        first_name = self.first_name_input.text.strip()
        last_name = self.last_name_input.text.strip()
        
        # Validation
        errors = []
        
        # Validation username
        valid, msg = validators.validate_username(username)
        if not valid:
            errors.append(msg)
        
        # Validation email
        valid, msg = validators.validate_email(email)
        if not valid:
            errors.append(msg)
        
        # Validation password
        valid, msg = validators.validate_password(password)
        if not valid:
            errors.append(msg)
        
        # Vérification correspondance
        if password != password_confirm:
            errors.append("Les mots de passe ne correspondent pas")
        
        if errors:
            self.show_error("\n".join(errors))
            return
        
        # Désactiver le bouton
        instance.disabled = True
        instance.text = "Inscription en cours..."
        
        # Tentative d'inscription
        Clock.schedule_once(
            lambda dt: self._perform_register(
                username, email, password, first_name, last_name, instance
            ), 0.1
        )
    
    def _perform_register(self, username, email, password, first_name, last_name, button):
        """Effectue l'inscription via l'API"""
        user = api_client.register(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        if user:
            self.show_error("")
            button.text = "Inscription réussie!"
            Clock.schedule_once(lambda dt: self.go_to_home(), 1)
        else:
            self.show_error("Erreur lors de l'inscription. L'utilisateur existe peut-être déjà.")
            button.disabled = False
            button.text = "S'inscrire"
    
    def go_to_home(self):
        """Navigation vers l'accueil"""
        self.manager.current = 'home'
    
    def on_login_link(self, instance, value):
        """Navigation vers la page de connexion"""
        self.manager.current = 'login'
    
    def show_error(self, message):
        """Affiche un message d'erreur"""
        self.error_label.text = message
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        # Effacer les champs
        self.first_name_input.text = ""
        self.last_name_input.text = ""
        self.username_input.text = ""
        self.email_input.text = ""
        self.password_input.text = ""
        self.password_confirm_input.text = ""
        self.show_error("")
        self.password_strength.text = ""