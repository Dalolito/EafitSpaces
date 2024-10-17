from django.shortcuts import render, redirect
from .models import Space, Reservation, CustomUser, SpaceType, Resource, SpaceXResource
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ReservationForm, SpacesForm, resourcesForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from django.utils import timezone
from datetime import timedelta
from collections import Counter
from django.db.models import Count

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


def get_available_hours(request):
    selected_space_id = request.GET.get('space_id')
    reservation_date = request.GET.get('reservation_date')
    print(selected_space_id)
    print(reservation_date)

    available_hours = []

    if selected_space_id and reservation_date:
        # Convertir la fecha de reserva a un objeto datetime
        reservation_date = datetime.strptime(reservation_date, '%Y-%m-%d').date()

        # Filtrar reservas por espacio y fecha
        reservas = Reservation.objects.filter(space_id=selected_space_id, reservation_date=reservation_date)

        all_times = [
            ('06:00', '06:00 AM'), ('06:30', '06:30 AM'), 
            ('07:00', '07:00 AM'), ('07:30', '07:30 AM'), 
            ('08:00', '08:00 AM'), ('08:30', '08:30 AM'),
            ('09:00', '09:00 AM'), ('09:30', '09:30 AM'),
            ('10:00', '10:00 AM'), ('10:30', '10:30 AM'),
            ('11:00', '11:00 AM'), ('11:30', '11:30 AM'),
            ('12:00', '12:00 PM'), ('12:30', '12:30 PM'),
            ('13:00', '01:00 PM'), ('13:30', '01:30 PM'),
            ('14:00', '02:00 PM'), ('14:30', '02:30 PM'),
            ('15:00', '03:00 PM'), ('15:30', '03:30 PM'),
            ('16:00', '04:00 PM'), ('16:30', '04:30 PM'),
            ('17:00', '05:00 PM'), ('17:30', '05:30 PM'),
            ('18:00', '06:00 PM'), ('18:30', '06:30 PM'),
            ('19:00', '07:00 PM'), ('19:30', '07:30 PM'),
            ('20:00', '08:00 PM'), ('20:30', '08:30 PM'),
            ('21:00', '09:00 PM'), ('21:30', '09:30 PM'),
            ('22:00', '10:00 PM')
        ]

        # Filtrar las horas disponibles según las reservas
        for hour, display in all_times:
            hour_time = datetime.strptime(hour, '%H:%M').time()
            print(hour_time)
            is_available = True
            
            print(":::::::::::::")
            for reserva in reservas:
                print(reserva)
                print("________________________")
                if reserva.start_time <= hour_time < reserva.end_time:
                    is_available = False
                    break

            if is_available:
                available_hours.append((hour, display))

    return JsonResponse({'available_hours': available_hours})

@login_required
def home(request):
    space_types = SpaceType.objects.all()
    spaces = Space.objects.all()
    
    selected_space_id = request.GET.get('space_id')
    space_type_id = request.GET.get('space_type')
    
    if space_type_id:
        spaces = spaces.filter(type_id=space_type_id)
    
    user = request.user
    is_superuser = user.is_superuser
    available_hours = []
    peticion_data = None
    available_resources = None

    if selected_space_id:
        # Obtener todas las horas reservadas para el espacio seleccionado
        peticion_data = Space.objects.get(space_id=selected_space_id)
        reservas = Reservation.objects.filter(space_id=selected_space_id)
        resources = SpaceXResource.objects.filter(space_id=selected_space_id)
        available_resources = [
            f"{resource.resource_id.name} (Cantidad: {resource.quantity})"
            for resource in resources
        ]
        # Todas las horas posibles
        all_times = [
            ('06:00', '06:00 AM'), ('06:30', '06:30 AM'), 
            ('07:00', '07:00 AM'), ('07:30', '07:30 AM'), 
            ('08:00', '08:00 AM'), ('08:30', '08:30 AM'),
            ('09:00', '09:00 AM'), ('09:30', '09:30 AM'),
            ('10:00', '10:00 AM'), ('10:30', '10:30 AM'),
            ('11:00', '11:00 AM'), ('11:30', '11:30 AM'),
            ('12:00', '12:00 PM'), ('12:30', '12:30 PM'),
            ('13:00', '01:00 PM'), ('13:30', '01:30 PM'),
            ('14:00', '02:00 PM'), ('14:30', '02:30 PM'),
            ('15:00', '03:00 PM'), ('15:30', '03:30 PM'),
            ('16:00', '04:00 PM'), ('16:30', '04:30 PM'),
            ('17:00', '05:00 PM'), ('17:30', '05:30 PM'),
            ('18:00', '06:00 PM'), ('18:30', '06:30 PM'),
            ('19:00', '07:00 PM'), ('19:30', '07:30 PM'),
            ('20:00', '08:00 PM'), ('20:30', '08:30 PM'),
            ('21:00', '09:00 PM'), ('21:30', '09:30 PM'),
            ('22:00', '10:00 PM')
        ]
        
        # Convertir las horas posibles a objetos datetime para facilitar comparaciones
        from datetime import datetime

        # Filtrar las horas disponibles para que no estén en el rango de ninguna reserva
        available_hours = []

        for hour, display in all_times:
            # Convertir la hora a un objeto datetime para comparar
            hour_time = datetime.strptime(hour, '%H:%M').time()
            is_available = True

            # Verificar si la hora cae dentro de algún rango de reserva
            for reserva in reservas:
                start_time = reserva.start_time
                end_time = reserva.end_time

                # Si la hora está entre la hora de inicio y fin de la reserva, marcarla como no disponible
                if start_time <= hour_time < end_time:
                    is_available = False
                    break

            # Si la hora no está dentro de ningún rango reservado, agregarla a las horas disponibles
            if is_available:
                available_hours.append((hour, display))


    # Convertir available_hours a JSON
    available_hours_json = json.dumps(available_hours)

    if request.method == 'POST':
        form = ReservationForm(space_id=selected_space_id, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReservationForm(space_id=selected_space_id, initial={
            'space_id': selected_space_id,
            'user_id': user.user_id
        })

    peticion_data = Space.objects.get(space_id=selected_space_id) if selected_space_id else None

    return render(request, 'home.html', {
        'spaces': spaces,
        'space_types': space_types,
        'is_superuser': is_superuser,
        'space_id': selected_space_id,
        'form': form,
        'peticion_data': peticion_data,
        'available_hours': available_hours_json,  # Pasar las horas disponibles como JSON al template
        'available_resources': available_resources
    })


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('register')

@login_required
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
@login_required
def spacesAdmin(request):

    space_types = SpaceType.objects.all()
    spaces = Space.objects.all()
    selected_space_id = request.GET.get('space_id')
    space_type_id = request.GET.get('space_type')
    type_form = request.GET.get('type_form')

    if space_type_id:
        spaces = spaces.filter(type_id=space_type_id)

    # Verificar si el usuario está autenticado
    user = request.user
    is_superuser = user.is_superuser

    if request.method == 'POST':
        data = request.POST.get('data')
        if data == "reservation":
            form = ReservationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Reservation added successfully!')
        else:
            form = SpacesForm(request.POST, request.FILES)
            if form.is_valid():
                space = form.save(commit=False)  # No guardar todavía para manejar los recursos
                space.save()  # Guarda el espacio

                # Manejar la relación SpaceXResource
                resources = form.cleaned_data.get('resources')
                for resource in resources:
                    # Asignar la cantidad según lo que necesites (en este caso por defecto es 1)
                    SpaceXResource.objects.create(space_id=space, resource_id=resource, quantity=1)
                
                messages.success(request, 'Space added successfully!')
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
                'available': True
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



@login_required
def statisticsAdmin(request):
    # Calcular la fecha de hace 6 meses desde hoy
    six_months_ago = timezone.now() - timedelta(days=180)
    
    # Filtrar las reservas de los últimos 6 meses
    reservations = Reservation.objects.filter(reservation_date__gte=six_months_ago)
    
    # Inicializar un contador para cada hora del día de 6 AM a 10 PM (22:00)
    hours_count = Counter({hour: 0 for hour in range(6, 23)})  # De 6 a 22 (6 AM a 10 PM)

    # Iterar sobre cada reserva y contar todas las horas que abarca
    for reservation in reservations:
        # Obtener la hora de inicio y fin de la reserva (en formato datetime.time)
        start_hour = reservation.start_time.hour
        end_hour = reservation.end_time.hour

        # Asegurarnos de que solo contemos horas dentro del rango de 6 AM a 10 PM
        for hour in range(max(start_hour, 6), min(end_hour, 22) + 1):
            hours_count[hour] += 1

    # Extraer las listas de horas y sus respectivos conteos
    hours = list(hours_count.keys())
    counts = list(hours_count.values())


    reservations = Reservation.objects.filter(reservation_date__gte=six_months_ago)

    # Agrupar las reservas por el número de edificio (building_number) y contar cuántas hay para cada uno
    reservations_count = (
        reservations.values('space_id__building_number')
        .annotate(total=Count('reservation_id'))
        .order_by('space_id__building_number')
    )

    # Preparar los datos para el gráfico
    blocks = [item['space_id__building_number'] for item in reservations_count]
    counts2 = [item['total'] for item in reservations_count]

    # Verificar si el usuario está autenticado
    user = request.user  # Obtiene el usuario autenticado
    is_superuser = user.is_superuser  # Verifica si el usuario es un superusuario
    return render(request, 'statisticsAdmin.html', {
        'hours': hours,
        'counts': counts,
        'is_superuser': is_superuser,
        'blocks': blocks,
        'counts2': counts2,
        })

@login_required
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


@login_required
def resourcesAdmin(request):
    resources = Resource.objects.all()  # Obtener todos los recursos
    user = request.user
    is_superuser = user.is_superuser  # Verificar si el usuario es superuser (administrador)

    # Manejar el formulario de creación de nuevos recursos
    if request.method == 'POST':
        form = resourcesForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)  # Guardar el nuevo recurso en la base de datos
            resource.availability = True
            resource.save()
            messages.success(request, 'Resource added successfully!')
            return redirect('resourcesAdmin')  # Redirigir a la página de administración de recursos
    else:
        form = resourcesForm()  # Formulario vacío para agregar un nuevo recurso
    
    return render(request, 'resourcesAdmin.html', {
        'resources': resources,
        'is_superuser': is_superuser,
        'form': form  # Pasar el formulario a la plantilla
    })
