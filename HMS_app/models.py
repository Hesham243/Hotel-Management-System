from django.db import models

# Create your models here.
class Hotel(model.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    timezone = models.CharField(max_length=50)
    checkin_time = models.TimeField()
    checkout_time = models.TimeField()