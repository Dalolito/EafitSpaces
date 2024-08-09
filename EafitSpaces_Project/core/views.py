from django.shortcuts import render, redirect
from .models import Space
from .models import Reservation
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser

def register(request):
    if request.user.is_authenticated:
        auth_logout(request)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)

                return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def home(request):
    
    reserve_peticion = request.GET.get('space_id')
    reserve_confirmation_id = request.GET.get('space_id_reservation')
    reserve_date = request.GET.get('date_reserve')
    reserve_start_time = request.GET.get('start_time')
    reserve_end_time = request.GET.get('end_time')
    
    if reserve_confirmation_id:
        user_id = request.user.user_id
        user = CustomUser.objects.get(user_id=user_id)
        space_id = Space.objects.get(space_id=reserve_confirmation_id)
        peticion_data = Space.objects.get(space_id=reserve_confirmation_id)
        Reservation.objects.create(user=user, space=space_id, reservation_date=reserve_date, start_time=reserve_start_time, end_time=reserve_end_time)
        Space.objects.filter(space_id=reserve_confirmation_id).update(available=False)
        spaces = Space.objects.all()
        return render(request, 'home.html', {'spaces': spaces, 'space_id': reserve_confirmation_id,'peticion_data':peticion_data})
    elif reserve_peticion:
        peticion_data = Space.objects.get(space_id=reserve_peticion)
        spaces = Space.objects.all()
        return render(request, 'home.html', {'spaces': spaces, 'space_id': reserve_peticion, 'peticion_data': peticion_data})
    else:
        spaces = Space.objects.all()
        return render(request, 'home.html', {'spaces': spaces})

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('register')

