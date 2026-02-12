from django.urls import path
from .views import (BookingCreateView, UserBookingsView, BookingDetailView, 
                   ProcessPaymentView, CancellationPolicyView)

urlpatterns = [
    path('', BookingCreateView.as_view(), name='booking-create'),
    path('my-bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<int:booking_id>/pay/', ProcessPaymentView.as_view(), name='process-payment'),
    path('hotel/<int:hotel_id>/cancellation-policies/', 
         CancellationPolicyView.as_view(), name='cancellation-policies'),
]