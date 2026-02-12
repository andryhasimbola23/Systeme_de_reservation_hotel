from django.contrib import admin
from .models import Hotel, HotelImage, RoomType, RoomImage

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'stars', 'has_wifi', 'has_parking')
    list_filter = ('stars', 'city', 'country')
    search_fields = ('name', 'city', 'country')
    inlines = [HotelImageInline]

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'room_type', 'price_per_night', 'capacity', 'quantity_available')
    list_filter = ('room_type', 'hotel')
    search_fields = ('name', 'hotel__name')
    inlines = [RoomImageInline]