from django.urls import path
from .views import HotelListCreateView, HotelDetailView, RoomTypeListView, SearchHotelsView

urlpatterns = [
    path('', HotelListCreateView.as_view(), name='hotel-list'),
    path('<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('<int:hotel_id>/rooms/', RoomTypeListView.as_view(), name='room-list'),
    path('search/', SearchHotelsView.as_view(), name='hotel-search'),
]