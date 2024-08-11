from django.contrib import admin
from .models import CustomUser, Space, Reservation, Resource, SpaceType


admin.site.register(CustomUser)
admin.site.register(Space)
admin.site.register(Reservation)
admin.site.register(Resource)
admin.site.register(SpaceType)



# Register your models here.
#username : administrator
#email:dein4267@gmail.com
#password: neosistemas