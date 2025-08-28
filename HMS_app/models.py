from datetime import timezone
from tkinter import CASCADE
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    timezone = models.CharField(max_length=50)
    checkin_time = models.TimeField()
    checkout_time = models.TimeField()
    
    
    
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
    

    
class Booking(models.Model):
  ##customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")
  room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
  check_in_date = models.DateField()
  check_out_date = models.DateField()
  status = models.CharField(max_length=20, choices=[("confirmed","Confirmed"),("cancelled","Cancelled")])
  num_guests = models.IntegerField(default=1)
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)
  currency = models.CharField(max_length=10, default="USD")
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f"Booking {self.id} - {self.customer.full_name}"
  
  def clean(self):
    """Custom validation: check_in must be before check_out."""
    from django.core.exceptions import ValidationError
    if self.check_in_date >= self.check_out_date:
        raise ValidationError("Check-in date must be before check-out date.")
  

