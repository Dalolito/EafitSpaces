from django.shortcuts import render, redirect
from .models import Space, Reservation, CustomUser, SpaceType
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ReservationForm, SpacesForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

                # Saber si es admin o no el usuario que ingresa
                request.session['is_admin'] = user.is_superuser
                
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
    space_types = SpaceType.objects.all()
    spaces = Space.objects.all()
    selected_space_id = request.GET.get('space_id')
    space_type_id = request.GET.get('space_type')
    
    if space_type_id:
        spaces = spaces.filter(type_id=space_type_id)
    
    # Verificar si el usuario está autenticado
    user = request.user  # Obtiene el usuario autenticado
    is_superuser = user.is_superuser  # Verifica si el usuario es un superusuario
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReservationForm(initial={
            'space_id': selected_space_id,
            'user_id': user.user_id
            })

    # Obtener datos del espacio seleccionado
    peticion_data = None
    if selected_space_id:
        try:
            peticion_data = Space.objects.get(space_id=selected_space_id)
        except Space.DoesNotExist:
            peticion_data = None

    return render(request, 'home.html', {
        'spaces': spaces,
        'space_types': space_types, 
        'is_superuser': is_superuser,
        'space_id': selected_space_id,
        'form': form,
        'peticion_data': peticion_data
        })

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('register')

def reservationsAdmin(request):
    # Verificar si el usuario está autenticado
    user = request.user  # Obtiene el usuario autenticado
    is_superuser = user.is_superuser  # Verifica si el usuario es un superusuario
    
    reservations = Reservation.objects.all()
    
    return render(request, 'reservationsAdmin.html', {
        'is_superuser': is_superuser, 
        'reservations': reservations
        }
    )
def spacesAdmin(request):

    space_types = SpaceType.objects.all()
    spaces = Space.objects.all()
    selected_space_id = request.GET.get('space_id')
    space_type_id = request.GET.get('space_type')
    type_form = request.GET.get('type_form')
    print("Formulario válido. Guardando datos...") 
    if space_type_id:
        spaces = spaces.filter(type_id=space_type_id)
    
    # Verificar si el usuario está autenticado
    user = request.user  # Obtiene el usuario autenticado
    is_superuser = user.is_superuser  # Verifica si el usuario es un superusuario
    
    if request.method == 'POST':
        
        data = request.POST.get('data')
        if data == "reservation":
            form = ReservationForm(request.POST)
            if form.is_valid():
                form.save()

        else:
            form = SpacesForm(request.POST, request.FILES)  
            if form.is_valid():
                form.save()
            else:
                print(form.errors) 
    else:
        if type_form == "reservation_form":
            form = ReservationForm(initial={
                'space_id': selected_space_id,
                'user_id': user.user_id
                 })
        else:
            form = SpacesForm(initial={
                'user_id': user.user_id,
                'available':True
                 })

    # Obtener datos del espacio seleccionado
    peticion_data = None
    if selected_space_id:
        try:
            peticion_data = Space.objects.get(space_id=selected_space_id)
        except Space.DoesNotExist:
            peticion_data = None

    return render(request, 'spacesAdmin.html', {
        'spaces': spaces,
        'space_types': space_types, 
        'is_superuser': is_superuser,
        'space_id': selected_space_id,
        'form': form,
        'peticion_data': peticion_data,
        'errors': form.errors  
        })



def reservationHistory(request):
    user = request.user 
    id_user = user.user_id
    reservations = Reservation.objects.all()
    reservations = reservations.filter(user_id=id_user)
    return render(request,'reservationHistory.html',{
    'reservations': reservations
    })

def prueba(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirige a una URL de éxito después de guardar
    else:
        form = ReservationForm()
    
    return render(request, 'prueba.html', {'form': form})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
    reservation.delete()
    messages.success(request, 'Reservation cancelled successfully.')
    return redirect('reservationsAdmin')

@csrf_exempt
def update_reservation_date(request):
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        reservation_date = request.POST.get('reservation_date')

        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
            reservation.reservation_date = reservation_date
            reservation.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Reservation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Reservation not found.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)