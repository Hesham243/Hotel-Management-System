from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name="About"),
    path('rooms/', views.rooms, name="Rooms"),
    path("rooms/<int:room_id>", views.room_detail, name="room-detail")
]