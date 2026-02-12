from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Hotel(models.Model):
    STAR_CHOICES = [
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    stars = models.IntegerField(choices=STAR_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Coordonnées GPS
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Équipements
    has_wifi = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.city}"

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')
    is_main = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class RoomType(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Chambre Simple'),
        ('double', 'Chambre Double'),
        ('twin', 'Chambre Twin'),
        ('suite', 'Suite'),
        ('family', 'Chambre Familiale'),
        ('presidential', 'Suite Présidentielle'),
    ]
    
    hotel = models.ForeignKey(Hotel, related_name='room_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    description = models.TextField()
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.IntegerField(help_text="Taille en m²")
    quantity_available = models.IntegerField()
    
    # Équipements de la chambre
    has_tv = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=True)
    has_minibar = models.BooleanField(default=False)
    has_safe = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    is_smoking = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

class RoomImage(models.Model):
    room_type = models.ForeignKey(RoomType, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)