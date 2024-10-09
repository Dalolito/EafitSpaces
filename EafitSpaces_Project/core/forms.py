# core/forms.py
from django import forms
from .models import CustomUser, Reservation, Space
from datetime import date, timedelta


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
        fields = ['user_id', 'space_id', 'reservation_date', 'start_time', 'end_time']
        widgets = {
            'reservation_date': forms.DateInput(attrs={
                'type': 'date',
                'id': 'id_reservation_date',
                'class': 'reservation_input',
                'min': date.today().strftime('%Y-%m-%d'),
                'max': (date.today() + timedelta(days=365)).strftime('%Y-%m-%d') 
                }),
            'start_time': forms.Select(attrs={
                'class': 'reservation_input',
                'id': 'id_start_time'  # Asegúrate de que el ID sea consistente
            }),
            'end_time': forms.Select(attrs={
                'type': 'time',
                'min': '06:00',
                'max': '22:00',
                'step': 1800,
                'class': 'reservation_input',
                'id': 'id_end_time',  # Asegúrate de que el ID sea consistente
            }),
            'space_id': forms.HiddenInput(),
            'user_id': forms.HiddenInput(),
        }
    
    def __init__(self, space_id, *args, **kwargs):
        available_times = kwargs.pop('available_times', [])
        super().__init__(*args, **kwargs)
        self.fields['start_time'].choices = available_times
     


class SpacesForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['capacity', 'building_number', 'room_number', 'image', 'type_id', 'available', 'available_resources']
        widgets = {
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Capacity',
                'id': 'capacity_input',
            }),
            'building_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Building Number',
                'id': 'building_input',
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Room Number',
                'id': 'room_input',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
                'id': 'id_image',  
                'onchange': 'handleImageChange(event)',
            }),
            'type_id':  forms.Select(attrs={'class': 'form-control', 'id': 'type_input',}),
            'available': forms.HiddenInput(),
            'available_resources': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Available Resources',
                'rows': 3
            }),
        }
