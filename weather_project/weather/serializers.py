from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import City, WeatherData

User = get_user_model()

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'city_id']

class WeatherDataSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    
    class Meta:
        model = WeatherData
        fields = ['city', 'temperature', 'description', 'humidity', 'wind_speed', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'city', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user