from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from .models import City, WeatherData
from .serializers import UserSerializer, CitySerializer, WeatherDataSerializer
from django.conf import settings
import requests

api_key = settings.API_KEY

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        city_name = request.data.get("city")

        city = City.objects.filter(name=city_name).first()
        if not city:
            return Response({"error": "Указанный город не найден"}, status=400)

        user = User.objects.create_user(
            username=request.data["username"],
            password=request.data["password"],
            role=request.data["role"],
            city=city
        )

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterManagerView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(role='manager', is_staff=True)
        user.save()

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "city": user.city.name if user.city else None
                }
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh-токен обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CityView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [permissions.AllowAny()]

class UserWeatherView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(f"🔍 Пользователь {user.username} ищет погоду для города: {user.city}")

        if not user.city:
            return Response({"error": "У пользователя не указан город"}, status=400)

        try:
            city = City.objects.get(name=user.city)
        except City.DoesNotExist:
            return Response({"error": "Город не найден"}, status=404)

        weather = WeatherData.objects.filter(city=city).first()
        if not weather:
            return Response({"error": "Нет данных о погоде"}, status=404)

        serializer = WeatherDataSerializer(weather)
        return Response(serializer.data)

class UpdateWeatherView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, city_id):
        try:
            city = City.objects.get(city_id=city_id)
        except City.DoesNotExist:
            return Response({"error": "Город не найден"}, status=404)

        url = f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={api_key}&units=metric"
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Ошибка получения данных с OpenWeatherMap"}, status=500)

        data = response.json()

        if "list" not in data or not data["list"]:
            return Response({"error": "Неверный формат данных OpenWeatherMap"}, status=500)

        forecast = data["list"][0]

        if "main" not in forecast or "weather" not in forecast or "wind" not in forecast:
            return Response({"error": "Отсутствуют необходимые данные в OpenWeatherMap"}, status=500)

        weather, created = WeatherData.objects.update_or_create(
            city=city,
            defaults={
                "temperature": forecast["main"]["temp"],
                "description": forecast["weather"][0]["description"],
                "humidity": forecast["main"]["humidity"],
                "wind_speed": forecast["wind"]["speed"]
            }
        )

        return Response({"message": "Погода обновлена", "data": WeatherDataSerializer(weather).data})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "role": user.role,
            "city": user.city.name if user.city else None
        }
        if user.role == "manager":
            data["added_cities"] = CitySerializer(City.objects.filter(manager=user), many=True).data
        return Response(data)
