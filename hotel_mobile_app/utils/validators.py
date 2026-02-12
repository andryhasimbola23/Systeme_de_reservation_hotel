import re
from datetime import datetime, date

class Validators:
    """Validateurs pour les formulaires"""
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """Valide une adresse email"""
        if not email:
            return False, "L'email est obligatoire"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Format d'email invalide"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """Valide un mot de passe"""
        if not password:
            return False, "Le mot de passe est obligatoire"
        
        if len(password) < 8:
            return False, "Le mot de passe doit faire au moins 8 caractères"
        
        # Vérifier la complexité
        if not any(c.isupper() for c in password):
            return False, "Le mot de passe doit contenir au moins une majuscule"
        
        if not any(c.isdigit() for c in password):
            return False, "Le mot de passe doit contenir au moins un chiffre"
        
        return True, ""
    
    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """Valide un nom d'utilisateur"""
        if not username:
            return False, "Le nom d'utilisateur est obligatoire"
        
        if len(username) < 3:
            return False, "Le nom d'utilisateur doit faire au moins 3 caractères"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscores"
        
        return True, ""
    
    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, str]:
        """Valide un numéro de téléphone"""
        if not phone:
            return True, ""  # Optionnel
        
        # Supprimer les espaces et caractères spéciaux
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        # Format français
        if re.match(r'^(\+33|0)[1-9]\d{8}$', clean_phone):
            return True, ""
        
        # Format international
        if re.match(r'^\+\d{10,15}$', clean_phone):
            return True, ""
        
        return False, "Format de téléphone invalide"
    
    @staticmethod
    def validate_date(date_str: str, min_date: date = None) -> tuple[bool, str]:
        """Valide une date"""
        if not date_str:
            return False, "La date est obligatoire"
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            if min_date and date_obj < min_date:
                return False, f"La date doit être après le {min_date.strftime('%d/%m/%Y')}"
            
            return True, ""
        except ValueError:
            return False, "Format de date invalide. Utilisez JJ/MM/AAAA"
    
    @staticmethod
    def validate_date_range(check_in: str, check_out: str) -> tuple[bool, str]:
        """Valide une plage de dates"""
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            if check_in_date >= check_out_date:
                return False, "La date de départ doit être après la date d'arrivée"
            
            # Limiter à 30 nuits maximum
            if (check_out_date - check_in_date).days > 30:
                return False, "La réservation ne peut pas dépasser 30 nuits"
            
            return True, ""
        except:
            return False, "Dates invalides"
    
    @staticmethod
    def validate_number(value: str, min_val: int = None, max_val: int = None) -> tuple[bool, str]:
        """Valide un nombre"""
        if not value:
            return False, "Cette valeur est obligatoire"
        
        try:
            num = int(value)
            
            if min_val is not None and num < min_val:
                return False, f"La valeur doit être au moins {min_val}"
            
            if max_val is not None and num > max_val:
                return False, f"La valeur ne peut pas dépasser {max_val}"
            
            return True, ""
        except ValueError:
            return False, "Veuillez entrer un nombre valide"

validators = Validators()