# core/forms.py
from django import forms
from .models import CustomUser, Reservation

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'full_name', 'password']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user_id','space_id','reservation_date','start_time','end_time']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),  # Para una fecha
            'start_time': forms.TimeInput(attrs={'type': 'time'}),  # Para una hora
            'end_time': forms.TimeInput(attrs={'type': 'time'}),  # Para una hora
            'space_id': forms.HiddenInput(),
            'user_id': forms.HiddenInput(),
        }