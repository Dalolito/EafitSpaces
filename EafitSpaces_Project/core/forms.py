# core/forms.py
from django import forms
from .models import CustomUser, Reservation, Space

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
