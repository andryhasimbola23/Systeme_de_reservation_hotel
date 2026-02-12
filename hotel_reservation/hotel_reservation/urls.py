# hotel_reservation/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Pages templates
    path('', views.home, name='home'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('search/', views.search_hotels, name='search_hotels'),
    path('contact/', views.contact, name='contact'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Réservations
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/pay/', views.process_payment, name='process_payment'),
    path('book-room/<int:room_id>/', views.create_booking, name='create_booking'),
    
    # API
    path('api/status/', views.api_status, name='api_status'),
    path('api/search/', views.api_search_hotels, name='api_search'),
    
    # API REST (existant)
    path('api/auth/', include('accounts.urls')),
    path('api/hotels/', include('hotels.urls')),
    path('api/bookings/', include('bookings.urls')),
    
    # Admin
    path('admin/', admin.site.urls),
]

# Page 404 personnalisée
handler404 = 'hotel_reservation.views.custom_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)