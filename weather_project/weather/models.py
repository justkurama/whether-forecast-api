from django.contrib.auth.models import AbstractUser
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    city_id = models.IntegerField(unique=True) 

    def __str__(self):
        return self.name

class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField() 
    description = models.CharField(max_length=255)  
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.city.name} ({self.temperature}°C, {self.description})"

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Менеджер'),
        ('user', 'Пользователь'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
