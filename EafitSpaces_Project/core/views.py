from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ReservationForm, SpacesForm, resourcesForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from datetime import timedelta
from collections import Counter
from django.db.models import Count
from reportlab.pdfgen import canvas
import io
import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from django.conf import settings
import tempfile
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Count
from django.utils import timezone

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
        data = request.POST.get('data')
        if data == "reservation":
            form = ReservationForm(space_id=selected_space_id, data=request.POST)
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
            form = ReservationForm(space_id=selected_space_id, initial={
                'space_id': selected_space_id,
                'user_id': user.user_id
            })
        else:
            form = SpacesForm(initial={
                'user_id': user.user_id,
                'available': True
            })

    # Obtener datos del espacio seleccionado
    peticion_data = Space.objects.get(space_id=selected_space_id) if selected_space_id else None

    return render(request, 'spacesAdmin.html', {
        'spaces': spaces,
        'space_types': space_types,
        'is_superuser': is_superuser,
        'space_id': selected_space_id,
        'form': form,
        'peticion_data': peticion_data,
        'available_hours': available_hours_json,  # Pasar las horas disponibles como JSON al template
        'available_resources': available_resources,
        'errors': form.errors  
    })

@login_required
def statisticsAdmin(request):
    user = request.user 
    id_user = user.user_id
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

    # Agrupar las reservas por el número de edificio (building_number) y contar cuántas hay para cada uno
    reservations_count = (
        reservations.values('space_id__building_number')
        .annotate(total=Count('reservation_id'))
        .order_by('space_id__building_number')
    )

    # Preparar los datos para el gráfico
    blocks = [item['space_id__building_number'] for item in reservations_count]
    counts2 = [item['total'] for item in reservations_count]

    # Obtener los reportes generados por el usuario
    user_reports = Reports.objects.filter(user_id=request.user).order_by('-report_date')
    print(user_reports)

    # Verificar si el usuario está autenticado
    user = request.user  # Obtiene el usuario autenticado
    is_superuser = user.is_superuser  # Verifica si el usuario es un superusuario

    return render(request, 'statisticsAdmin.html', {
        'hours': hours,
        'counts': counts,
        'is_superuser': is_superuser,
        'blocks': blocks,
        'counts2': counts2,
        'user_reports': user_reports,
    })

@login_required
def reservationHistory(request):
    user = request.user 
    id_user = user.user_id
    reservations = Reservation.objects.all().order_by('-reservation_id')
    reservations = reservations.filter(user_id=id_user)
    return render(request,'reservationHistory.html',{
    'reservations': reservations
    })

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
    reservation.delete()
    messages.success(request, 'Reservation deleted successfully.')
    return redirect('reservationsAdmin')

@csrf_exempt
def cancel_reservation(request):
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        
        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
            reservation.status = 'Cancel'
            reservation.save()
            return JsonResponse({'success': True})
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reservation not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

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

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user_id = request.user
            reservation.save()

            # Crear una notificación cuando se crea una reserva
            Notifications.objects.create(
                user_id=request.user,
                message=f"A new reservation has been created for the space {reservation.space_id}",
                reservation=reservation
            )
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form})

@login_required
def notifications(request):
    user_notifications = Notifications.objects.filter(user_id=request.user).order_by('-date_time')

    # Marcar todas las notificaciones como leídas
    user_notifications.update(is_read=True)

    return render(request, 'notifications.html', {'notifications': user_notifications})


# Vista para modificar un espacio
@login_required
def modify_space(request, space_id):
    space = get_object_or_404(Space, space_id=space_id)
    user = request.user
    is_superuser = user.is_superuser
    
    if request.method == 'POST':
        form = SpacesForm(request.POST, request.FILES, instance=space)
        if form.is_valid():
            form.save()
            messages.success(request, 'Space modified successfully!')
            return redirect('spacesAdmin')  # Ajusta esto según la URL que uses para la página de administración
    else:
        form = SpacesForm(instance=space)
    
    return render(request, 'modify_space.html', {
        'form': form,
        'is_superuser': is_superuser,
        'space': space,

    })

# Vista para eliminar un espacio
@login_required
def delete_space(request, space_id):
    space = get_object_or_404(Space, space_id=space_id)
    space.delete()
    messages.success(request, 'Space deleted successfully!')
    return redirect('spacesAdmin')  # Redirigir a la vista de administración de espacios

@login_required
def generate_report(request):
    if request.method == 'POST':
        user = request.user
        # Obtener el rango seleccionado por el usuario
        report_range = request.POST.get('report_range')
        today = timezone.now().date()
        
        # Definir la fecha inicial en función del rango seleccionado
        if report_range == '1':  # Últimos 30 días
            start_date = today - timedelta(days=30)
        elif report_range == '2':  # Últimos 3 meses
            start_date = today - timedelta(days=90)
        elif report_range == '3':  # Último año
            start_date = today - timedelta(days=365)
        else:
            start_date = today - timedelta(days=30)  # Valor por defecto

        # Hacer que la fecha de inicio sea "aware" (con zona horaria)
        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))

        # Filtrar las reservas de acuerdo con el rango de fechas seleccionado
        reservations = Reservation.objects.filter(reservation_date__gte=start_date)

        # Número total de reservas
        total_reservations = reservations.count()

        # Contar el número de reservas por bloque
        reservations_by_block = reservations.values('space_id__building_number').annotate(count=Count('space_id')).order_by('-count')

        # Contar el número de reservas por hora (6 AM a 10 PM)
        reservations_by_hour = {hour: 0 for hour in range(6, 23)}
        for reservation in reservations:
            start_hour = reservation.start_time.hour
            end_hour = reservation.end_time.hour
            for hour in range(max(6, start_hour), min(23, end_hour) + 1):
                reservations_by_hour[hour] += 1

        # Salones más pedidos
        most_requested_spaces = reservations.values('space_id__room_number').annotate(count=Count('space_id')).order_by('-count')[:5]

        # Horas de más reservas
        most_reserved_hours = sorted(reservations_by_hour.items(), key=lambda x: x[1], reverse=True)[:3]

        # Bloques de más reservas
        most_reserved_blocks = sorted(reservations_by_block, key=lambda x: x['count'], reverse=True)[:3]

        # Recomendación del sistema (basada en la hora más concurrida)
        recommendation = ""
        if most_reserved_hours:
            recommendation = f"Recommendation: Increase cleaning frequency at {most_reserved_hours[0][0]}:00 due to high demand."

        # Crear un buffer para almacenar el contenido del PDF
        buffer = io.BytesIO()

        # Crear un objeto canvas con reportlab
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y_position = height - 50

        # Añadir el logo al PDF (centrado)
        logo_path = os.path.join(settings.BASE_DIR, 'core/static/img/logo.png')
        if os.path.exists(logo_path):
            try:
                logo_width, logo_height = 100, 100
                x_position = (width - logo_width) / 2  # Centrar el logo horizontalmente
                pdf.drawImage(logo_path, x=x_position, y=height - 150, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
                y_position -= 120
            except Exception as e:
                print(f"Error al añadir el logo: {e}")

        # Añadir el título del reporte
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(200, y_position, "Reservation Report")
        y_position -= 40

        # Añadir el número total de reservas
        pdf.setFont("Helvetica", 14)
        pdf.drawString(50, y_position, f"Total Reservations for Selected Period: {total_reservations}")
        y_position -= 20
        pdf.drawString(50, y_position, f"Generated on: {today}")
        y_position -= 40

        # Añadir el título de la sección: Número de reservas por bloque
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position, "Reservations by Block:")
        y_position -= 20

        # Añadir los datos de reservas por bloque
        pdf.setFont("Helvetica", 12)
        for block in reservations_by_block:
            pdf.drawString(50, y_position, f"Block {block['space_id__building_number']}: {block['count']} reservations")
            y_position -= 20
            if y_position < 50:
                pdf.showPage()
                y_position = height - 50

        # Añadir el título de la sección: Reservas por hora
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position, "Reservations by Hour:")
        y_position -= 20

        # Añadir los datos de reservas por hora
        pdf.setFont("Helvetica", 12)
        for hour, count in reservations_by_hour.items():
            pdf.drawString(50, y_position, f"{hour}:00 - {count} reservations")
            y_position -= 20
            if y_position < 50:
                pdf.showPage()
                y_position = height - 50

        # Añadir el título de la sección: Salones más pedidos
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position, "Most Requested Rooms:")
        y_position -= 20

        # Añadir los datos de los salones más pedidos
        pdf.setFont("Helvetica", 12)
        for space in most_requested_spaces:
            pdf.drawString(50, y_position, f"Room {space['space_id__room_number']}: {space['count']} reservations")
            y_position -= 20
            if y_position < 50:
                pdf.showPage()
                y_position = height - 50

        # Añadir el título de la sección: Horas con más reservas
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position, "Most Reserved Hours:")
        y_position -= 20

        # Añadir los datos de las horas con más reservas
        pdf.setFont("Helvetica", 12)
        for hour, count in most_reserved_hours:
            pdf.drawString(50, y_position, f"{hour}:00 - {count} reservations")
            y_position -= 20
            if y_position < 50:
                pdf.showPage()
                y_position = height - 50

        # Añadir el título de la sección: Bloques con más reservas
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position, "Most Reserved Blocks:")
        y_position -= 20

        # Añadir los datos de los bloques con más reservas
        pdf.setFont("Helvetica", 12)
        for block in most_reserved_blocks:
            pdf.drawString(50, y_position, f"Block {block['space_id__building_number']}: {block['count']} reservations")
            y_position -= 20
            if y_position < 50:
                pdf.showPage()
                y_position = height - 50

        # Añadir la recomendación del sistema
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position, "System Recommendation:")
        y_position -= 20
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y_position, recommendation)
        y_position -= 40
        if y_position < 50:
            pdf.showPage()
            y_position = height - 50

        # Crear gráficos adicionales para el reporte
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            # Generar el gráfico de reservas por hora
            fig, ax = plt.subplots()
            ax.bar(reservations_by_hour.keys(), reservations_by_hour.values(), color='skyblue')
            ax.set_title('Reservations by Hour')
            ax.set_xlabel('Hour of the Day')
            ax.set_ylabel('Number of Reservations')
            ax.set_xticks(list(reservations_by_hour.keys()))
            plt.savefig(tmpfile.name, format='png')
            plt.close(fig)

            # Añadir el gráfico al PDF
            if y_position < 300:
                pdf.showPage()
                y_position = height - 50

            pdf.drawImage(tmpfile.name, x=50, y=y_position - 300, width=500, height=250)
            y_position -= 350

        # Crear gráfico de tipo pastel de reservas por bloque
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile_pie:
            fig, ax = plt.subplots()
            labels = [f"Block {block['space_id__building_number']}" for block in reservations_by_block]
            sizes = [block['count'] for block in reservations_by_block]
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Para asegurar que el gráfico sea un círculo.
            plt.title("Reservations by Block")
            plt.savefig(tmpfile_pie.name, format='png')
            plt.close(fig)

            # Añadir el gráfico de pastel al PDF
            if y_position < 300:
                pdf.showPage()
                y_position = height - 50

            pdf.drawImage(tmpfile_pie.name, x=50, y=y_position - 300, width=500, height=250)
            y_position -= 350

        # Guardar el PDF y cerrar el objeto canvas
        pdf.save()

        # Obtener el archivo PDF desde el buffer
        buffer.seek(0)

        # Crear un objeto Report para almacenar el reporte en la base de datos
        report = Reports(
            user_id=request.user,  # Utilizando la instancia del usuario autenticado
            report_date=today,
            range_type=int(report_range)
        )
        
        # Guardar el archivo PDF en el campo report_pdf del modelo
        report.report_pdf.save(f"reservation_report_{today}.pdf", buffer, save=True)

        # Eliminar los archivos temporales después de usarlos
        os.remove(tmpfile.name)
        os.remove(tmpfile_pie.name)

        # Redirigir a la página de estadísticas con un mensaje de éxito (puede personalizarse)
        return redirect('statisticsAdmin')

    # Si no es POST, redirigir a la página de estadísticas
    return redirect('statisticsAdmin')

@login_required
def analyze_data(request):
    # Calcular la fecha de hace 6 meses desde hoy
    six_months_ago = timezone.now() - timedelta(days=180)
    
    # Filtrar las reservas de los últimos 6 meses
    reservations = Reservation.objects.filter(reservation_date__gte=six_months_ago)

    # Contadores de las horas de inicio y fin
    start_times_count = Counter()
    end_times_count = Counter()

    # Contar las reservas para cada hora de inicio y fin
    for reservation in reservations:
        start_hour = reservation.start_time.hour
        end_hour = reservation.end_time.hour
        start_times_count[start_hour] += 1
        end_times_count[end_hour] += 1

    # Obtener la hora de inicio y fin con más reservas
    most_common_start_hour = max(start_times_count, key=start_times_count.get)
    most_common_end_hour = max(end_times_count, key=end_times_count.get)

    # Convertir horas al formato 12 horas con AM/PM
    def format_hour(hour):
        if hour == 0:
            return "12 AM"
        elif hour < 12:
            return f"{hour} AM"
        elif hour == 12:
            return "12 PM"
        else:
            return f"{hour - 12} PM"

    # Crear el mensaje con el formato de 12 horas
    response_data = {
        'message': (
            f"The hour with the most reservations starts at {format_hour(most_common_start_hour)} "
            f"with {start_times_count[most_common_start_hour]} reservations, "
            f"and the most common end time is at {format_hour(most_common_end_hour)} "
            f"with {end_times_count[most_common_end_hour]} reservations."
        )
    }

    return JsonResponse(response_data)

@login_required
def analyze_block_data(request):
    # Calcular la fecha de hace 6 meses desde hoy
    six_months_ago = timezone.now() - timedelta(days=180)
    
    # Filtrar las reservas de los últimos 6 meses
    reservations = Reservation.objects.filter(reservation_date__gte=six_months_ago)

    # Contador para las reservas por bloque
    block_counts = Counter()
    for reservation in reservations:
        block_number = reservation.space_id.building_number
        block_counts[block_number] += 1

    # Obtener el bloque con más reservas
    if block_counts:
        most_common_block = max(block_counts, key=block_counts.get)
        most_common_block_count = block_counts[most_common_block]
        response_data = {
            'message': (
                f"The block with the most reservations is Block {most_common_block} "
                f"with {most_common_block_count} reservations."
            )
        }
    else:
        response_data = {
            'message': "No reservation data available for the selected period."
        }

    return JsonResponse(response_data)
