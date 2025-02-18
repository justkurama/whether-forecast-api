import requests
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import WeatherData, City
from .serializers import WeatherDataSerializer, CitySerializer, UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home_view(request):
    return render(request, "weather/home.html")

@login_required
def weather_view(request):
    return render(request, "weather/weather.html")

User = get_user_model()

API_KEY = "6d8e495ca73d5bbc1d6bf8ebd52c4"  # API-ключ OpenWeatherMap

@csrf_exempt
def register_user_view(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST.dict()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

        data['role'] = 'user'  # Default role for user registration
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # Create JWT tokens immediately after registration
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    cities = City.objects.all()
    return render(request, 'weather/register.html', {'cities': cities})

@csrf_exempt
def register_manager_view(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST.dict()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

        data['role'] = 'manager'  # Role for manager registration
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # Create JWT tokens immediately after registration
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    cities = City.objects.all()
    return render(request, 'weather/register_manager.html', {'cities': cities})

class CityView(APIView):
    """Менеджер может добавлять города"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'manager':
            return Response({"error": "Только менеджер может добавлять города."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            city_name = serializer.validated_data['name']
            country = serializer.validated_data['country']
            url = f"http://api.openweathermap.org/data/2.5/find?q={city_name},{country}&type=like&APPID={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['count'] > 0:
                    city_data = data['list'][0]
                    serializer.save(city_id=city_data['id'])
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "City not found in OpenWeatherMap"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Error fetching data from OpenWeatherMap"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeatherView(APIView):
    """Пользователь получает погоду только для своего города"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.city:
            return Response({"error": "Вы не выбрали город при регистрации"}, status=status.HTTP_400_BAD_REQUEST)

        city = request.user.city  # Берем город пользователя
        weather = WeatherData.objects.filter(city=city).first()

        # Проверяем, есть ли свежие данные (менее 10 минут)
        if weather and (now() - weather.updated_at).total_seconds() < 600:
            serializer = WeatherDataSerializer(weather)
            return Response(serializer.data)

        # Запрос к OpenWeatherMap по city_id
        url = f"http://api.openweathermap.org/data/2.5/weather?id={city.city_id}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
            }

            # Обновляем или создаем запись в базе
            if weather:
                weather.temperature = weather_data["temperature"]
                weather.description = weather_data["description"]
                weather.updated_at = now()
                weather.save()
            else:
                weather = WeatherData.objects.create(**weather_data)

            serializer = WeatherDataSerializer(weather)
            return Response(serializer.data)

        return Response({"error": "Ошибка при получении данных"}, status=status.HTTP_400_BAD_REQUEST)

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Неверное имя пользователя или пароль"}, status=status.HTTP_400_BAD_REQUEST)

    return render(request, 'weather/login.html')