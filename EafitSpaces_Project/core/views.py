from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from .models import Space
from .models import Reservation
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
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
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    # Log in the user
                    auth_login(request, user)
                    spaces = Space.objects.all()
                    return render(request, 'home.html', {'spaces': spaces})
                else:
                    form.add_error('password', 'Contraseña incorrecta')
            except User.DoesNotExist:
                form.add_error('email', 'Correo electrónico no registrado')
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
        user = User.objects.get(email=request.user.email)
        space_id = Space.objects.get(space_id=reserve_confirmation_id)
        Reservation.objects.create(user_id=user, space_id=space_id, reservation_date=reserve_date, start_time=reserve_start_time, end_time=reserve_end_time)
        spaces = Space.objects.all()
        return render(request, 'home.html', {'spaces': spaces, 'space_id': reserve_confirmation_id})
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

def home(request):
    reserve_peticion = request.GET.get('space_id')
    reserve_confirmation_id = request.GET.get('space_id_reservation')
    reserve_date = request.GET.get('date_reserve')
    reserve_start_time = request.GET.get('start_time')
    reserve_end_time = request.GET.get('end_time')
    
    if(reserve_confirmation_id):
        user = User.objects.get(email="dein4267@gmail.com")
        space_id = Space.objects.get(space_id =reserve_confirmation_id )
        Reservation.objects.create(user_id = user, space_id =space_id,  reservation_date = reserve_date, start_time= reserve_start_time,end_time = reserve_end_time )
        spaces = Space.objects.all()
        return render(request, 'home.html',{'spaces':spaces,'space_id':reserve_confirmation_id})

    elif reserve_peticion:
        peticion_data = Space.objects.get(space_id=reserve_peticion)
        spaces = Space.objects.all()
        return render(request, 'home.html',{'spaces':spaces,'space_id':reserve_peticion, 'peticion_data': peticion_data})
    else:
        spaces = Space.objects.all()
        return render(request, 'home.html',{'spaces':spaces})