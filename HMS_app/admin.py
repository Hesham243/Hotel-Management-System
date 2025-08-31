from django.contrib import admin
from .models import Hotel,Room,Booking

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)