"""
URL configuration for EafitSpaces project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views as Views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Views.home, name='home'),
    path('register/', Views.register, name='register'),
    path('login/', Views.login, name='login'),
    path('logout/', Views.logout, name='logout'),
    path('reservationsAdmin/', Views.reservationsAdmin, name='reservationsAdmin'),
    path('spacesAdmin/', Views.spacesAdmin, name='spacesAdmin'),
    path('reservationHistory/', Views.reservationHistory, name='reservationHistory'),
    path('delete_reservation/<int:reservation_id>/', Views.delete_reservation, name='delete_reservation'),
    path('update_reservation_date/', Views.update_reservation_date, name='update_reservation_date'),
    path('get-available-hours/', Views.get_available_hours, name='get_available_hours'),
    path('statisticsAdmin/', Views.statisticsAdmin, name='statisticsAdmin'),
    path('resourcesAdmin/', Views.resourcesAdmin, name='resourcesAdmin'),
    path('cancel_reservation/', Views.cancel_reservation, name='cancel_reservation'),
    path('notifications/', Views.notifications, name='notifications'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#prueba de push para github
