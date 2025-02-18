import requests
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import WeatherData
from .serializers import WeatherDataSerializer
import json
from django.conf import settings

def get_city_id(city_name):
    """Ищем ID города по названию"""
    with open(settings.CITY_LIST_PATH, encoding="utf-8") as f:
        cities = json.load(f)

    for city in cities:
        if city["name"].lower() == city_name.lower():
            return city["id"]
    
    return None

API_KEY = "2634504740ffcea2b39bbff31b6f0f52"  #ApiKey from OpenWeatherMap


class WeatherView(APIView):
    def get(self, request, city):
        city_id = get_city_id(city)
        if not city_id:
            return Response({"error": "Город не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, есть ли свежие данные в базе
        weather = WeatherData.objects.filter(city=city).first()
        if weather and (now() - weather.updated_at).total_seconds() < 600:
            serializer = WeatherDataSerializer(weather)
            return Response(serializer.data)

        # Делаем запрос к OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
            }
            
            # Обновляем или создаем запись в базе данных
            if weather:
                for key, value in weather_data.items():
                    setattr(weather, key, value)
                weather.save()
            else:
                weather = WeatherData.objects.create(**weather_data)

            serializer = WeatherDataSerializer(weather)
            return Response(serializer.data)

        return Response({"error": "Ошибка при получении данных"}, status=status.HTTP_400_BAD_REQUEST)