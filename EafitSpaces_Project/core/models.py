from django.db import models


# Create your models here.

# Users 
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

# Space 
class Space(models.Model):
    space_id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()
    available_resources = models.CharField(max_length=255)
    building_number = models.IntegerField()
    room_number = models.CharField(max_length=255)
    image = models.ImageField(upload_to='core/images/')
    type = models.CharField(max_length=50)
    available = models.BooleanField(default=True)


# Reservation
class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    space_id = models.ForeignKey(Space, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

# Resource
class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    availability = models.BooleanField()
