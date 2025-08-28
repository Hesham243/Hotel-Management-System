from datetime import timezone
from tkinter import CASCADE
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    timezone = models.CharField(max_length=50)
    checkin_time = models.TimeField()
    checkout_time = models.TimeField()