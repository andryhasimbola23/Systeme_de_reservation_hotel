from rest_framework import serializers
from .models import Hotel, HotelImage, RoomType, RoomImage

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'image', 'is_main']

class HotelSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'image']

class RoomTypeSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    hotel_city = serializers.CharField(source='hotel.city', read_only=True)
    
    class Meta:
        model = RoomType
        fields = '__all__'

class AvailableRoomSerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    number_of_rooms = serializers.IntegerField(min_value=1, default=1)
    number_of_guests = serializers.IntegerField(min_value=1, default=1)