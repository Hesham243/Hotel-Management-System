from django.urls import path, include
from . import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name="About"),
    path('rooms/', views.rooms, name="Rooms"),
    path("rooms/<int:room_id>", views.room_detail, name="room-detail"),
    path('bookings/', views.booking_index, name='booking-index'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking-detail'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/create/<int:room_id>/', views.BookingCreateView.as_view(), name='booking-create-for-room'),
    path('bookings/<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking-delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('complete-profile/', views.complete_profile, name='complete-profile'),
]

