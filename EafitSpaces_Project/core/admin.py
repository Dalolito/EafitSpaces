from django.contrib import admin
from .models import CustomUser, Space, Reservation, Resource, SpaceType, Notifications, Reports


admin.site.register(CustomUser)
admin.site.register(Space)
admin.site.register(Reservation)
admin.site.register(Resource)
admin.site.register(SpaceType)
admin.site.register(Notifications)
admin.site.register(Reports)



# Register your models here.
#username : administrator
#email:dein4267@gmail.com
#password: neosistemas