from django import forms
from .models import Booking, Profile

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date', 'status', 'num_guests', 'total_amount', 'currency']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'email','phone_number']
