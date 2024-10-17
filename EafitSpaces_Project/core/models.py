from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, full_name=None, role=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, full_name=None, role=False):
        user = self.create_user(email, password, username, full_name, role=role)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email

#Space Type
class SpaceType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.type_name
# Resource
class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    availability = models.BooleanField()

    def __str__(self):
        return self.name
    
class Space(models.Model):
    space_id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()
    building_number = models.IntegerField()
    room_number = models.CharField(max_length=255)
    image = models.ImageField(upload_to='core/images/')
    type_id = models.ForeignKey(SpaceType, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    resources = models.ManyToManyField(Resource, through='SpaceXResource', related_name='spaces')
    
    def __str__(self):
        return str(self.building_number) + " - " +str(self.room_number)

class SpaceXResource(models.Model):
    space_id = models.ForeignKey(Space, on_delete=models.CASCADE)  # Llave foránea a Space
    resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE)  # Llave foránea a Resource
    quantity = models.IntegerField()  
    
    class Meta:
        unique_together = ('space_id', 'resource_id')  # Para evitar duplicaciones en la combinación espacio-recurso
    
    def __str__(self):
        return f"Space: {self.space_id} - Resource: {self.resource_id} - Quantity: {self.quantity}"    
# Space

# Reservation
class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    space_id = models.ForeignKey(Space, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    STATUS_CHOICES = [
        ('Close', 'Close'),
        ('Available', 'Available'),
        ('Cancel', 'Cancel')
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

    # Variable interna para almacenar el estado anterior
    _previous_status = None

    def __str__(self):
        return f"Reserva desde {self.start_time} hasta {self.end_time}"

    def save(self, *args, **kwargs):
        # Si la instancia ya existe (no es una nueva) obtenemos el estado previo
        if self.pk:
            previous_reservation = Reservation.objects.get(pk=self.pk)
            self._previous_status = previous_reservation.status
        
        super().save(*args, **kwargs)  # Guardamos la instancia

        # Verificar si el estado ha cambiado
        if self._previous_status and self._previous_status != self.status:
            # Crear una nueva notificación con el ID del espacio
            Notifications.objects.create(
                user_id=self.user_id,
                message=f"The status of your reservation for space ID {self.space_id} has changed to {self.status}.",
                reservation=self
            )

class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Notification for {self.user_id}"

# Reports
class Reports(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_pdf = models.FileField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    report_date = models.DateField()
