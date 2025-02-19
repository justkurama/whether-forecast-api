from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterUserView,
    RegisterManagerView,
    CityView,
    UserWeatherView,
    UpdateWeatherView,
    LogoutView,
    LoginView,
    ProfileView
)

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("register/manager/", RegisterManagerView.as_view(), name="register_manager"),

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("cities/", CityView.as_view(), name="city_list_create"),
    
    path("weather/", UserWeatherView.as_view(), name="user_weather"),
    path("weather/update/<int:city_id>/", UpdateWeatherView.as_view(), name="update_weather"),
    
    path("profile/", ProfileView.as_view(), name="profile"),
]
