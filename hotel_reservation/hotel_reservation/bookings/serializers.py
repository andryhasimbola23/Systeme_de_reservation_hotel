from rest_framework import serializers
from django.utils import timezone
from .models import Booking, Payment, CancellationPolicy
from hotels.serializers import RoomTypeSerializer

class BookingSerializer(serializers.ModelSerializer):
    room_type_details = RoomTypeSerializer(source='room_type', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    hotel_name = serializers.CharField(source='room_type.hotel.name', read_only=True)
    can_cancel = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'total_price', 'status', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Validation des dates
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError("La date de départ doit être après la date d'arrivée")
        
        if data['check_in_date'] < timezone.now().date():
            raise serializers.ValidationError("La date d'arrivée ne peut pas être dans le passé")
        
        # Validation du nombre de personnes
        if data['number_of_guests'] > data['room_type'].capacity * data['number_of_rooms']:
            raise serializers.ValidationError("Le nombre de personnes dépasse la capacité des chambres")
        
        return data
    
    def get_can_cancel(self, obj):
        if obj.status in ['cancelled', 'completed']:
            return False
        days_before = (obj.check_in_date - timezone.now().date()).days
        return days_before > 1

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['booking', 'amount', 'payment_status', 'created_at']

class CancellationPolicySerializer(serializers.ModelSerializer): 
    class Meta:
        model = CancellationPolicy
        fields = '__all__'