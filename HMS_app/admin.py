from django.contrib import admin
from .models import Hotel,Room,Booking,RoomImage,RoomNumber

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(RoomNumber)
admin.site.register(RoomImage)
# admin.site.register(Customer)
