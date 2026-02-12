from django.db import models
from django.conf import settings
from hotels.models import RoomType

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
        ('completed', 'Terminée'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_rooms = models.IntegerField(default=1)
    number_of_guests = models.IntegerField()
    
    # Détails de la réservation
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Informations supplémentaires
    special_requests = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Réservation {self.id} - {self.user.username}"
    
    @property
    def number_of_nights(self):
        return (self.check_out_date - self.check_in_date).days

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Carte de crédit'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Virement bancaire'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Paiement {self.transaction_id} - {self.amount}€"

class CancellationPolicy(models.Model):
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE, related_name='cancellation_policies')
    days_before_checkin = models.IntegerField(help_text="Nombre de jours avant l'arrivée")
    penalty_percentage = models.IntegerField(help_text="Pourcentage de pénalité")
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "Cancellation policies"
        ordering = ['days_before_checkin']
    
    def __str__(self):
        return f"{self.hotel.name} - {self.days_before_checkin} jours: {self.penalty_percentage}%"