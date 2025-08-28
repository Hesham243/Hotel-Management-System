from django.db import models


# Create your models here.
















#======================= haider
class Room(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=CASCADE, related_name="rooms")
    number = models.IntegerField(max_length=1200)
    type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20, choices=[("available","Available")("booked","Booked")])
    max_occupancy = models.IntegerField()
    images = models.CharField()
    
    def __str__(self):
        return self.name
    
