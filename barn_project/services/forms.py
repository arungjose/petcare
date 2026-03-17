from django import forms
from .models import ServiceBooking


class ServiceBookingForm(forms.ModelForm):
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = ServiceBooking
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'pet_name', 'pet_type', 'pet_breed',
            'appointment_date', 'appointment_time', 'special_requests',
        ]
        widgets = {
            'special_requests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requirements or medical conditions...'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'customer_email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'customer_phone': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}),
            'pet_name': forms.TextInput(attrs={'placeholder': "Your pet's name"}),
            'pet_type': forms.TextInput(attrs={'placeholder': 'Dog, Cat, Bird, etc.'}),
            'pet_breed': forms.TextInput(attrs={'placeholder': 'Breed (optional)'}),
        }
