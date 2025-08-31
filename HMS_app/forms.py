from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date', 'num_guests']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide room field if initial is set (for booking a specific room)
        if self.initial.get('room'):
            self.fields['room'].widget = forms.HiddenInput()
        import datetime
        today = datetime.date.today().isoformat()
        self.fields['check_in_date'].widget = forms.DateInput(attrs={'type': 'date', 'min': today})
        self.fields['check_out_date'].widget = forms.DateInput(attrs={'type': 'date', 'min': today})
