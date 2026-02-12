import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from kivy.storage.jsonstore import JsonStore

from config import STORAGE_PATH

class StorageManager:
    """Gestionnaire de stockage local"""
    
    def __init__(self):
        self.store = JsonStore(f'{STORAGE_PATH}/app_storage.json')
        self.cache_store = JsonStore(f'{STORAGE_PATH}/cache.json')
    
    # ===== DONNEES UTILISATEUR =====
    
    def save_user_data(self, user_data: dict):
        """Sauvegarde les données utilisateur"""
        self.store.put('user', **user_data)
    
    def get_user_data(self) -> dict:
        """Récupère les données utilisateur"""
        try:
            return self.store.get('user')
        except:
            return {}
    
    def clear_user_data(self):
        """Efface les données utilisateur"""
        try:
            self.store.delete('user')
        except:
            pass
    
    # ===== CACHE =====
    
    def cache_data(self, key: str, data: dict, ttl: int = 300):
        """Cache des données avec temps d'expiration (en secondes)"""
        cache_item = {
            'data': data,
            'expires_at': datetime.now().timestamp() + ttl
        }
        self.cache_store.put(key, **cache_item)
    
    def get_cached_data(self, key: str) -> Optional[dict]:
        """Récupère des données du cache"""
        try:
            cache_item = self.cache_store.get(key)
            if cache_item['expires_at'] > datetime.now().timestamp():
                return cache_item['data']
            else:
                self.cache_store.delete(key)
                return None
        except:
            return None
    
    def clear_cache(self):
        """Vide tout le cache"""
        try:
            self.cache_store.clear()
        except:
            pass
    
    # ===== PREFERENCES =====
    
    def save_preference(self, key: str, value):
        """Sauvegarde une préférence"""
        try:
            preferences = self.store.get('preferences')
        except:
            preferences = {}
        
        preferences[key] = value
        self.store.put('preferences', **preferences)
    
    def get_preference(self, key: str, default=None):
        """Récupère une préférence"""
        try:
            preferences = self.store.get('preferences')
            return preferences.get(key, default)
        except:
            return default
    
    def save_search_filters(self, filters: dict):
        """Sauvegarde les derniers filtres de recherche"""
        self.save_preference('last_search_filters', filters)
    
    def get_search_filters(self) -> dict:
        """Récupère les derniers filtres de recherche"""
        return self.get_preference('last_search_filters', {})
    
    # ===== HISTORIQUE =====
    
    def add_to_history(self, item_type: str, item_id: int, item_data: dict):
        """Ajoute un élément à l'historique"""
        try:
            history = self.store.get('history')
        except:
            history = {'hotels': [], 'searches': []}
        
        item = {
            'type': item_type,
            'id': item_id,
            'data': item_data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Limiter l'historique à 50 éléments
        history_list = history.get(item_type, [])
        history_list.insert(0, item)
        history_list = history_list[:50]
        history[item_type] = history_list
        
        self.store.put('history', **history)
    
    def get_history(self, item_type: str) -> list:
        """Récupère l'historique"""
        try:
            history = self.store.get('history')
            return history.get(item_type, [])
        except:
            return []
    
    # ===== FAVORIS =====
    
    def toggle_favorite(self, item_type: str, item_id: int, item_data: dict) -> bool:
        """Ajoute ou retire un favori"""
        try:
            favorites = self.store.get('favorites')
        except:
            favorites = {'hotels': {}}
        
        item_type_favorites = favorites.get(item_type, {})
        
        if str(item_id) in item_type_favorites:
            # Retirer des favoris
            del item_type_favorites[str(item_id)]
            is_favorite = False
        else:
            # Ajouter aux favoris
            item_type_favorites[str(item_id)] = {
                'data': item_data,
                'added_at': datetime.now().isoformat()
            }
            is_favorite = True
        
        favorites[item_type] = item_type_favorites
        self.store.put('favorites', **favorites)
        
        return is_favorite
    
    def is_favorite(self, item_type: str, item_id: int) -> bool:
        """Vérifie si un élément est en favori"""
        try:
            favorites = self.store.get('favorites')
            item_type_favorites = favorites.get(item_type, {})
            return str(item_id) in item_type_favorites
        except:
            return False
    
    def get_favorites(self, item_type: str) -> list:
        """Récupère la liste des favoris"""
        try:
            favorites = self.store.get('favorites')
            item_type_favorites = favorites.get(item_type, {})
            
            result = []
            for item_id, item_data in item_type_favorites.items():
                result.append({
                    'id': int(item_id),
                    **item_data['data']
                })
            
            return result
        except:
            return []

# Instance globale du gestionnaire de stockage
storage = StorageManager()