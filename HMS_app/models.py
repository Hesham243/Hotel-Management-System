from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
#     full_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)

#     def __str__(self):
#       return self.full_name

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    rating = models.DecimalField(
    max_digits=2,
    decimal_places=1,
    default=0.0,
    validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    timezone = models.CharField(max_length=64, default="Asia/Bahrain")
    checkin_time = models.TimeField(default="15:00")
    checkout_time = models.TimeField(default="11:00")
    # created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.rating}:star:)"
    
    
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("available", "Available"), ("booked", "Booked")])
    max_occupancy = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
      return f"{self.type} - {self.hotel.name}"


class RoomNumber(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_numbers")
    number = models.IntegerField()
    
    def __str__(self):
      return f"Room Number {self.number} in {self.room.type}"


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image_url = models.CharField()

    def __str__(self):
      return f"Image for {self.room.type} - {self.image_url}"


class Booking(models.Model):
  # customer= models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings", null=True)
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
  check_in_date = models.DateField()
  check_out_date = models.DateField()
  status = models.CharField(max_length=20, choices=[("confirmed","Confirmed"),("cancelled","Cancelled")])
  num_guests = models.IntegerField(default=1)
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)
  currency = models.CharField(max_length=10, default="USD")
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f"Booking {self.id} "
  
  def clean(self):
    """Custom validation: check_in must be before check_out."""
    from django.core.exceptions import ValidationError
    if self.check_in_date >= self.check_out_date:
        raise ValidationError("Check-in date must be before check-out date.")
  

