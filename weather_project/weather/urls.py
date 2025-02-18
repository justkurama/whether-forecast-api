from django.urls import path
from .views import WeatherView, CityView, register_user_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', register_user_view, name='register'),
    path('weather/', WeatherView.as_view(), name='weather'),
    path('cities/', CityView.as_view(), name='cities'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
