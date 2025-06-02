from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger_name', 'passenger_email']

class BookingSearchForm(forms.Form):
    passenger_email = forms.EmailField(label="Your Email Address")

class CancelBookingForm(forms.Form):
    passenger_email = forms.EmailField()
    booking_id = forms.IntegerField(widget=forms.HiddenInput())
