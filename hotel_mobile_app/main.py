#!/usr/bin/env python3
"""
Application mobile Hotel Reservation
Connexion à l'API Django REST Framework
"""

import os
import sys
from kivy.config import Config

# Configuration de la fenêtre
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)
Config.set('kivy', 'window_icon', 'assets/icons/app_icon.png')

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hotel_app import HotelApp

if __name__ == '__main__':
    # Vérifier la connexion à l'API
    from api.api_client import api_client
    
    print("=" * 50)
    print("Hotel Reservation Mobile App v1.0.0")
    print("=" * 50)
    print()
    
    if api_client.check_connection():
        print("✅ Connexion à l'API établie")
        print(f"   URL: {api_client.base_url}")
    else:
        print("❌ Impossible de se connecter à l'API")
        print(f"   URL: {api_client.base_url}")
        print()
        print("Vérifiez que le serveur Django est en cours d'exécution :")
        print("   python manage.py runserver 0.0.0.0:8000")
        print()
        print("Vérifiez la configuration CORS dans Django :")
        print("   CORS_ALLOW_ALL_ORIGINS = True")
        print()
    
    print("\nDémarrage de l'application...\n")
    
    # Lancer l'application
    HotelApp().run()