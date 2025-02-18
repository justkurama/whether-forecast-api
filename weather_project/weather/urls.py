from django.urls import path
from .views import register_user_view, register_manager_view, CityView, WeatherView, custom_login_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', register_user_view, name='register_user'),
    path('register/manager/', register_manager_view, name='register_manager'),
    path('cities/', CityView.as_view(), name='cities'),
    path('weather/', WeatherView.as_view(), name='weather'),
    path('login/', custom_login_view, name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
