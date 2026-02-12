from rest_framework import generics, filters, status, permissions  # Ajoutez 'permissions' ici
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Hotel, RoomType
from .serializers import HotelSerializer, RoomTypeSerializer, AvailableRoomSerializer
from bookings.models import Booking

class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'country', 'stars', 'has_wifi', 'has_parking']
    search_fields = ['name', 'city', 'country', 'description']
    ordering_fields = ['stars', 'name']

class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RoomTypeListView(generics.ListAPIView):
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return RoomType.objects.filter(hotel_id=hotel_id)

class SearchHotelsView(APIView):
    permission_classes = [permissions.AllowAny]  # Ici permissions est maintenant défini
    
    def post(self, request):
        serializer = AvailableRoomSerializer(data=request.data)
        if serializer.is_valid():
            check_in = serializer.validated_data['check_in']
            check_out = serializer.validated_data['check_out']
            number_of_rooms = serializer.validated_data['number_of_rooms']
            number_of_guests = serializer.validated_data['number_of_guests']
            city = request.data.get('city', '')
            min_price = request.data.get('min_price')
            max_price = request.data.get('max_price')
            stars = request.data.get('stars')
            
            # Trouver les chambres disponibles
            booked_rooms = Booking.objects.filter(
                Q(check_in_date__lt=check_out) & Q(check_out_date__gt=check_in),
                status__in=['confirmed', 'pending']
            ).values_list('room_type_id', flat=True)
            
            # Filtrer les chambres
            rooms = RoomType.objects.filter(
                quantity_available__gte=number_of_rooms,
                capacity__gte=number_of_guests
            ).exclude(id__in=booked_rooms)
            
            # Appliquer les filtres supplémentaires
            if city:
                rooms = rooms.filter(hotel__city__icontains=city)
            if min_price:
                rooms = rooms.filter(price_per_night__gte=min_price)
            if max_price:
                rooms = rooms.filter(price_per_night__lte=max_price)
            if stars:
                rooms = rooms.filter(hotel__stars=stars)
            
            serializer = RoomTypeSerializer(rooms, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)