from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking, Payment, CancellationPolicy
from .serializers import BookingSerializer, PaymentSerializer, CancellationPolicySerializer 
from hotels.models import RoomType

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        room_type = serializer.validated_data['room_type']
        nights = (serializer.validated_data['check_out_date'] - 
                 serializer.validated_data['check_in_date']).days
        
        total_price = room_type.price_per_night * nights * serializer.validated_data['number_of_rooms']
        
        booking = serializer.save(
            user=self.request.user,
            total_price=total_price,
            status='pending'
        )
        
        # Créer un paiement simulé
        Payment.objects.create(
            booking=booking,
            amount=total_price,
            payment_method='credit_card',
            payment_status='pending',
            transaction_id=f"TXN{booking.id:06d}"
        )
        
        # Envoyer l'email de confirmation
        self.send_confirmation_email(booking)
    
    def send_confirmation_email(self, booking):
        subject = f'Confirmation de réservation #{booking.id}'
        message = f"""
        Bonjour {booking.user.get_full_name()},
        
        Votre réservation a été enregistrée avec succès.
        
        Détails de la réservation:
        - Hôtel: {booking.room_type.hotel.name}
        - Type de chambre: {booking.room_type.name}
        - Date d'arrivée: {booking.check_in_date}
        - Date de départ: {booking.check_out_date}
        - Nombre de nuits: {booking.number_of_nights}
        - Nombre de chambres: {booking.number_of_rooms}
        - Prix total: {booking.total_price}€
        
        Votre numéro de réservation: {booking.id}
        
        Cordialement,
        L'équipe de réservation
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [booking.user.email],
            fail_silently=False,
        )

class UserBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        # Mise à jour du statut de la réservation
        if 'status' in serializer.validated_data:
            if serializer.validated_data['status'] == 'cancelled':
                # Appliquer la politique d'annulation
                booking = self.get_object()
                days_before = (booking.check_in_date - timezone.now().date()).days
                
                # Trouver la politique applicable
                policies = CancellationPolicy.objects.filter(
                    hotel=booking.room_type.hotel,
                    days_before_checkin__lte=days_before
                ).order_by('-days_before_checkin')
                
                if policies.exists():
                    penalty = policies.first().penalty_percentage
                    refund_amount = booking.total_price * (100 - penalty) / 100
                    
                    # Mettre à jour le paiement
                    payment = booking.payment
                    payment.payment_status = 'refunded'
                    payment.save()
                    
                    # Envoyer email d'annulation
                    self.send_cancellation_email(booking, penalty, refund_amount)
        
        serializer.save()

class ProcessPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            payment = booking.payment
            
            # Simulation de paiement
            payment.payment_status = 'completed'
            payment.payment_date = timezone.now()
            payment.save()
            
            # Mettre à jour le statut de la réservation
            booking.status = 'confirmed'
            booking.save()
            
            return Response({"message": "Paiement effectué avec succès"})
        
        except Booking.DoesNotExist:
            return Response({"error": "Réservation non trouvée"}, status=status.HTTP_404_NOT_FOUND)

class CancellationPolicyView(generics.ListAPIView):
    serializer_class = CancellationPolicySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return CancellationPolicy.objects.filter(hotel_id=hotel_id).order_by('days_before_checkin')

# Ajoutez ces méthodes manquantes à la classe BookingDetailView
def send_cancellation_email(self, booking, penalty, refund_amount):
    subject = f'Annulation de réservation #{booking.id}'
    message = f"""
    Bonjour {booking.user.get_full_name()},
    
    Votre réservation #{booking.id} a été annulée.
    
    Détails de l'annulation:
    - Hôtel: {booking.room_type.hotel.name}
    - Type de chambre: {booking.room_type.name}
    - Date d'arrivée: {booking.check_in_date}
    - Pénalité appliquée: {penalty}%
    - Montant remboursé: {refund_amount}€
    
    Cordialement,
    L'équipe de réservation
    """
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [booking.user.email],
        fail_silently=False,
    )