from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
      return self.full_name



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

  def get_available_count(self, check_in, check_out):
    overlapping = self.bookings.filter(
      status='confirmed',
      check_in_date__lt=check_out,
      check_out_date__gt=check_in
    ).count()
    return self.total - overlapping

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
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="bookings")
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
    """Custom validation: check_in must be before check_out, no overbooking, and guests <= max occupancy."""
    from django.core.exceptions import ValidationError
    # Date ordering
    if self.check_in_date and self.check_out_date and self.check_in_date >= self.check_out_date:
      raise ValidationError("Check-in date must be before check-out date.")
    # No past dates
    today = timezone.now().date()
    if self.check_in_date and self.check_in_date < today:
      raise ValidationError("Check-in date cannot be in the past.")
    if self.check_out_date and self.check_out_date < today:
      raise ValidationError("Check-out date cannot be in the past.")
    # Overbooking check
    if self.room and self.check_in_date and self.check_out_date:
      available = self.room.get_available_count(self.check_in_date, self.check_out_date)
      # If updating an existing booking, exclude itself
      if self.pk:
        overlapping = self.room.bookings.filter(
          status='confirmed',
          check_in_date__lt=self.check_out_date,
          check_out_date__gt=self.check_in_date
        ).exclude(pk=self.pk).count()
        available = self.room.total - overlapping
      if available <= 0:
        raise ValidationError("All rooms of this type are fully booked for the selected dates.")
    # Max occupancy check
    if self.num_guests is not None:
      if self.num_guests < 1:
        raise ValidationError("Number of guests must be at least 1.")
      if self.room and self.num_guests > self.room.max_occupancy:
        raise ValidationError(f"Number of guests ({self.num_guests}) exceeds the maximum occupancy ({self.room.max_occupancy}) for this room.")
  
  

class Services(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="BHD")
    
    def __str__(self):
      return self.name
