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

# Space
class Space(models.Model):
    space_id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()
    building_number = models.IntegerField()
    room_number = models.CharField(max_length=255)
    image = models.ImageField(upload_to='core/images/')
    type_id = models.ForeignKey(SpaceType, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    available_resources = models.CharField(max_length=255)

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
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

# Resource
class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    availability = models.BooleanField()

# Notifications
class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    message = models.CharField(max_length=300)

# Reports
class Reports(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_pdf = models.FileField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    report_date = models.DateField()