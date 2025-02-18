from django.urls import path
from weather.views import home_view, weather_view, custom_login_view, register_user_view

urlpatterns = [
    path('', home_view, name='home'),
    path('weather/', weather_view, name='weather'),
    path('login/', custom_login_view, name='login'),   
    path('register/', register_user_view, name='register'),
]
