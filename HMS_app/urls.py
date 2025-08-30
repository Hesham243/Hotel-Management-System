from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name="About"),

    path('bookings/', views.booking_index, name='booking-index'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking-detail'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking-delete'),
]

