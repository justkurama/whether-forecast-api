from django.db import models

# Create your models here.
class WeatherData(models.Model):
    city = models.CharField(max_length=100, unique=True)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city}: {self.temperature}°C, {self.description}"
