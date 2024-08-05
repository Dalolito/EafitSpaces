from django.shortcuts import render
from .models import Space
from .models import Reservation
from .models import User

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