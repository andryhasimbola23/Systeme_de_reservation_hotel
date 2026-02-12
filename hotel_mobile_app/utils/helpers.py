from datetime import datetime, date
from typing import Optional
import math

class Helpers:
    """Fonctions utilitaires"""
    
    @staticmethod
    def format_date(date_str: str, format_str: str = "%d/%m/%Y") -> str:
        """Formate une date"""
        try:
            if isinstance(date_str, str):
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date_obj = date_str
            
            return date_obj.strftime(format_str)
        except:
            return date_str
    
    @staticmethod
    def format_price(price: float) -> str:
        """Formate un prix"""
        try:
            return f"{price:.2f}€".replace('.', ',')
        except:
            return str(price)
    
    @staticmethod
    def format_date_range(check_in: str, check_out: str) -> str:
        """Formate une plage de dates"""
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            
            nights = (check_out_date - check_in_date).days
            
            if check_in_date.year == check_out_date.year:
                if check_in_date.month == check_out_date.month:
                    return f"{check_in_date.day}-{check_out_date.day} {check_in_date.strftime('%b %Y')} ({nights} nuits)"
                else:
                    return f"{check_in_date.strftime('%d %b')} - {check_out_date.strftime('%d %b %Y')} ({nights} nuits)"
            else:
                return f"{check_in_date.strftime('%d/%m/%Y')} - {check_out_date.strftime('%d/%m/%Y')} ({nights} nuits)"
        except:
            return f"{check_in} - {check_out}"
    
    @staticmethod
    def calculate_price(price_per_night: float, check_in: str, check_out: str, rooms: int = 1) -> float:
        """Calcule le prix total"""
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            
            nights = (check_out_date - check_in_date).days
            return price_per_night * nights * rooms
        except:
            return 0.0
    
    @staticmethod
    def get_stars_rating(stars: int) -> str:
        """Retourne la représentation des étoiles"""
        return '★' * stars + '☆' * (5 - stars)
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Tronque un texte"""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."
    
    @staticmethod
    def format_duration(minutes: int) -> str:
        """Formate une durée"""
        if minutes < 60:
            return f"{minutes}min"
        
        hours = minutes // 60
        mins = minutes % 60
        
        if mins == 0:
            return f"{hours}h"
        return f"{hours}h{mins:02d}"
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> Optional[float]:
        """Calcule la distance entre deux points (en km)"""
        try:
            # Rayon de la Terre en km
            R = 6371.0
            
            # Conversion en radians
            lat1_rad = math.radians(lat1)
            lon1_rad = math.radians(lon1)
            lat2_rad = math.radians(lat2)
            lon2_rad = math.radians(lon2)
            
            # Différences
            dlon = lon2_rad - lon1_rad
            dlat = lat2_rad - lat1_rad
            
            # Formule de Haversine
            a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            distance = R * c
            return round(distance, 1)
        except:
            return None
    
    @staticmethod
    def get_room_type_icon(room_type: str) -> str:
        """Retourne l'icône pour un type de chambre"""
        icons = {
            'single': 'bed',
            'double': 'bed-double',
            'twin': 'bed-queen',
            'suite': 'sofa',
            'family': 'home-group',
            'presidential': 'crown',
        }
        return icons.get(room_type, 'bed')
    
    @staticmethod
    def get_booking_status_color(status: str) -> str:
        """Retourne la couleur pour un statut de réservation"""
        colors = {
            'pending': '#f59e0b',    # orange
            'confirmed': '#10b981',   # vert
            'cancelled': '#ef4444',   # rouge
            'completed': '#64748b',   # gris
        }
        return colors.get(status, '#64748b')

helpers = Helpers()