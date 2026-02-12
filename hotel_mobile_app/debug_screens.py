# debug_screens.py
import os
import sys
import inspect

print("=" * 60)
print("🔍 DIAGNOSTIC DES ÉCRANS HOTEL RESERVATION")
print("=" * 60)

# 1. Vérifier la structure des fichiers
print("\n📁 VÉRIFICATION DES FICHIERS:")
print("-" * 40)

required_files = [
    "screens/modern_login_screen.py",
    "screens/modern_home_screen.py",
    "screens/hotels_screen.py",
    "components/modern_button.py",
    "components/modern_card.py",
    "components/modern_navbar.py",
    "components/modern_input.py",
    "api/api_client.py",
    "config.py"
]

for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file:35} - OK")
    else:
        print(f"❌ {file:35} - MANQUANT")

# 2. Vérifier les imports
print("\n📦 VÉRIFICATION DES IMPORTS:")
print("-" * 40)

try:
    from screens.modern_home_screen import ModernHomeScreen
    print("✅ ModernHomeScreen importé avec succès")
except Exception as e:
    print(f"❌ Erreur import ModernHomeScreen: {e}")

try:
    from screens.hotels_screen import HotelsScreen
    print("✅ HotelsScreen importé avec succès")
except Exception as e:
    print(f"❌ Erreur import HotelsScreen: {e}")

# 3. Tester le ScreenManager
print("\n🎯 TEST DU SCREENMANAGER:")
print("-" * 40)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.clock import Clock

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text=f"Écran: {self.name}"))

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        
        # Ajouter les écrans de test
        test_screens = [
            TestScreen(name='login'),
            TestScreen(name='register'),
            TestScreen(name='home'),
            TestScreen(name='hotels'),
        ]
        
        for screen in test_screens:
            sm.add_widget(screen)
            print(f"✅ Écran ajouté: {screen.name}")
        
        print(f"\n📱 Écrans dans le manager: {sm.screen_names}")
        
        if 'home' in sm.screen_names:
            sm.current = 'home'
            print("✅ Écran 'home' défini comme courant")
        else:
            print("❌ Écran 'home' non trouvé!")
        
        return sm

print("\n🚀 Lancement du test...")
TestApp().run()