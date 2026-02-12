from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

from api.api_client import api_client
from utils.validators import validators
from utils.helpers import helpers
from config import COLORS

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'profile'
        self.user = None
        self._build_ui()
    
    def _build_ui(self):
        # Layout principal avec ScrollView
        scroll_view = ScrollView()
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        self.content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        main_layout.add_widget(self.content_layout)
        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)
    
    def load_profile(self):
        """Charge le profil utilisateur"""
        self.content_layout.clear_widgets()
        
        # Afficher chargement
        loading_label = Label(
            text='Chargement du profil...',
            font_size=dp(16),
            color=COLORS['gray'],
            size_hint_y=None,
            height=dp(100)
        )
        self.content_layout.add_widget(loading_label)
        
        Clock.schedule_once(lambda dt: self._fetch_profile(), 0.1)
    
    def _fetch_profile(self):
        """Récupère le profil depuis l'API"""
        self.content_layout.clear_widgets()
        
        self.user = api_client.user
        
        if self.user:
            self.display_profile()
        else:
            self.user = api_client.get_profile()
            if self.user:
                self.display_profile()
            else:
                self.show_error()
    
    def display_profile(self):
        """Affiche le profil utilisateur"""
        self.content_layout.clear_widgets()
        
        # Avatar
        avatar_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )
        
        avatar = Label(
            text='👤',
            font_size=dp(60),
            color=COLORS['primary'],
            size_hint_y=None,
            height=dp(80)
        )
        avatar_layout.add_widget(avatar)
        
        avatar_layout.add_widget(Label(
            text=f'[size=20][b]{self.user.full_name}[/b][/size]',
            markup=True,
            font_size=dp(20),
            color=COLORS['dark'],
            halign='center'
        ))
        
        self.content_layout.add_widget(avatar_layout)
        
        # Informations
        info_section = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(15)
        )
        info_section.canvas.before.add(Color(rgba=(0.95, 0.95, 0.95, 1)))
        info_section.canvas.before.add(RoundedRectangle(
            pos=info_section.pos,
            size=info_section.size,
            radius=[dp(10),]
        ))
        info_section.bind(minimum_height=info_section.setter('height'))
        
        info_section.add_widget(Label(
            text='[size=16][b]Informations personnelles[/b][/size]',
            markup=True,
            font_size=dp(16),
            color=COLORS['dark'],
            halign='left',
            size_hint_y=None,
            height=dp(30)
        ))
        
        info_items = [
            ('Nom d\'utilisateur', self.user.username),
            ('Email', self.user.email),
            ('Membre depuis', helpers.format_date(self.user.date_joined) if self.user.date_joined else 'N/A'),
            ('Type de compte', self.user.user_type),
        ]
        
        if self.user.phone_number:
            info_items.append(('Téléphone', self.user.phone_number))
        
        for label, value in info_items:
            item_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(40),
                spacing=dp(10)
            )
            
            item_layout.add_widget(Label(
                text=f"{label}:",
                font_size=dp(14),
                color=COLORS['gray'],
                halign='left',
                size_hint_x=0.4
            ))
            
            item_layout.add_widget(Label(
                text=value,
                font_size=dp(14),
                color=COLORS['dark'],
                bold=True,
                halign='right',
                size_hint_x=0.6
            ))
            
            info_section.add_widget(item_layout)
        
        info_section.height = len(info_items) * 45 + 50
        self.content_layout.add_widget(info_section)
        
        # Formulaire de modification
        edit_section = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            padding=dp(15)
        )
        edit_section.bind(minimum_height=edit_section.setter('height'))
        
        edit_section.add_widget(Label(
            text='[size=16][b]Modifier mes informations[/b][/size]',
            markup=True,
            font_size=dp(16),
            color=COLORS['dark'],
            halign='left',
            size_hint_y=None,
            height=dp(30)
        ))
        
        # Prénom
        self.first_name_input = TextInput(
            text=self.user.first_name or '',
            hint_text='Prénom',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(50),
            multiline=False
        )
        edit_section.add_widget(self.first_name_input)
        
        # Nom
        self.last_name_input = TextInput(
            text=self.user.last_name or '',
            hint_text='Nom',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(50),
            multiline=False
        )
        edit_section.add_widget(self.last_name_input)
        
        # Email
        self.email_input = TextInput(
            text=self.user.email or '',
            hint_text='Email',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(50),
            multiline=False
        )
        edit_section.add_widget(self.email_input)
        
        # Téléphone
        self.phone_input = TextInput(
            text=self.user.phone_number or '',
            hint_text='Téléphone',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(50),
            multiline=False
        )
        edit_section.add_widget(self.phone_input)
        
        # Bouton de mise à jour
        update_button = Button(
            text='💾 Mettre à jour',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1)
        )
        update_button.bind(on_press=self.update_profile)
        edit_section.add_widget(update_button)
        
        edit_section.height = 250
        self.content_layout.add_widget(edit_section)
        
        # Actions
        actions_section = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120),
            padding=dp(15)
        )
        
        logout_button = Button(
            text='🚪 Déconnexion',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['danger'],
            color=(1, 1, 1, 1)
        )
        logout_button.bind(on_press=self.logout)
        
        back_button = Button(
            text='← Retour',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['gray'],
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=lambda x: self.go_back())
        
        actions_section.add_widget(logout_button)
        actions_section.add_widget(back_button)
        
        self.content_layout.add_widget(actions_section)
    
    def update_profile(self, instance):
        """Met à jour le profil utilisateur"""
        # Validation
        email = self.email_input.text.strip()
        valid, msg = validators.validate_email(email)
        if not valid:
            self.show_error(msg)
            return
        
        phone = self.phone_input.text.strip()
        if phone:
            valid, msg = validators.validate_phone(phone)
            if not valid:
                self.show_error(msg)
                return
        
        # Désactiver le bouton
        instance.disabled = True
        instance.text = "Mise à jour..."
        
        # Simuler la mise à jour (à remplacer par appel API)
        Clock.schedule_once(lambda dt: self._update_success(instance), 1)
    
    def _update_success(self, button):
        """Succès de la mise à jour"""
        # Mettre à jour l'objet utilisateur localement
        if self.user:
            self.user.first_name = self.first_name_input.text
            self.user.last_name = self.last_name_input.text
            self.user.email = self.email_input.text
            self.user.phone_number = self.phone_input.text
        
        button.text = "✅ Mise à jour réussie!"
        Clock.schedule_once(lambda dt: self.load_profile(), 1)
    
    def logout(self, instance):
        """Déconnexion"""
        api_client.logout()
        self.manager.current = 'login'
    
    def go_back(self):
        """Retour à l'accueil"""
        self.manager.current = 'home'
    
    def show_error(self, message):
        """Affiche une erreur"""
        from kivy.uix.popup import Popup
        popup = Popup(
            title='Erreur',
            content=Label(text=message, font_size=dp(14)),
            size_hint=(0.8, 0.3),
            separator_color=COLORS['danger']
        )
        popup.open()
    
    def show_error_state(self):
        """Affiche un état d'erreur"""
        self.content_layout.clear_widgets()
        
        error_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(40),
            size_hint_y=None,
            height=dp(300)
        )
        
        error_layout.add_widget(Label(
            text='❌',
            font_size=dp(60)
        ))
        
        error_layout.add_widget(Label(
            text='[size=18][b]Erreur de chargement[/b][/size]',
            markup=True,
            font_size=dp(18),
            color=COLORS['danger']
        ))
        
        error_layout.add_widget(Label(
            text='Impossible de charger le profil',
            font_size=dp(14),
            color=COLORS['gray']
        ))
        
        retry_button = Button(
            text='Réessayer',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['primary'],
            color=(1, 1, 1, 1)
        )
        retry_button.bind(on_press=lambda x: self.load_profile())
        
        back_button = Button(
            text='Retour à l\'accueil',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=COLORS['gray'],
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=lambda x: self.go_back())
        
        error_layout.add_widget(retry_button)
        error_layout.add_widget(back_button)
        
        self.content_layout.add_widget(error_layout)
    
    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        if not api_client.is_authenticated():
            self.manager.current = 'login'
        else:
            self.load_profile()