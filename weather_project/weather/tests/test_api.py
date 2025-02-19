import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def manager_data():
    return {"username": "manager", "password": "password123", "role": "manager"}

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "password123", "role": "user", "city": "City 1"}

@pytest.fixture
def create_manager(api_client, manager_data):
    print(f"📝 Регистрируем менеджера с данными: {manager_data}")
    response = api_client.post("/api/register/manager/", manager_data)
    print(f"📩 Ответ от сервера: {response.status_code}, {response.json()}")
    return response

@pytest.fixture
def obtain_tokens(api_client, manager_data):
    print(f"🔑 Получаем токены для менеджера: {manager_data}")
    response = api_client.post("/api/token/", manager_data)
    print(f"📩 Токены получены: {response.json()}")
    return response.data

@pytest.fixture
def refresh_token(api_client, obtain_tokens):
    print(f"♻️ Обновляем токен: {obtain_tokens['refresh']}")
    response = api_client.post("/api/token/refresh/", {"refresh": obtain_tokens["refresh"]})
    print(f"📩 Новый токен: {response.json()}")
    return response.data

@pytest.fixture
def create_cities(api_client, obtain_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {obtain_tokens['access']}")
    cities = [f"City {i}" for i in range(1, 11)]
    
    print("🏙️ Создаём города:")
    for i, city_name in enumerate(cities, start=1):
        response = api_client.post("/api/cities/", {"name": city_name, "city_id": 524900 + i})
        print(f"📩 Город {city_name} создан: {response.status_code}, {response.json()}")
    
    return cities

@pytest.fixture
def list_cities(api_client, obtain_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {obtain_tokens['access']}")
    response = api_client.get("/api/cities/")
    print(f"📜 Список городов получен: {response.status_code}, {response.json()}")
    return response

@pytest.fixture
def update_weather(api_client, obtain_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {obtain_tokens['access']}")
    response = api_client.post("/api/weather/update/524901/")
    print(f"⛅ Обновление погоды для города 524901: {response.status_code}, {response.json()}")
    return response

@pytest.fixture
def logout_manager(api_client, obtain_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {obtain_tokens['access']}")
    response = api_client.post("/api/logout/", data={"refresh": obtain_tokens["refresh"]})
    print(f"🚪 Логаут менеджера: {response.status_code}, {response.json()}")
    return response

@pytest.fixture
def register_user(api_client, user_data, create_cities):
    user_data["city"] = create_cities[0]
    print(f"📝 Регистрируем пользователя с данными: {user_data}")
    response = api_client.post("/api/register/", user_data)
    print(f"📩 Ответ от сервера: {response.status_code}, {response.json()}")
    return response

@pytest.fixture
def obtain_user_tokens(api_client, user_data):
    print(f"🔑 Получаем токены для пользователя: {user_data}")
    response = api_client.post("/api/token/", user_data)
    print(f"📩 Токены пользователя: {response.json()}")
    return response.data

@pytest.fixture
def user_weather(api_client, obtain_user_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {obtain_user_tokens['access']}")
    response = api_client.get("/api/weather/")
    print(f"🌤️ Запрос погоды: {response.status_code}, {response.json()}")
    return response

@pytest.fixture
def logout_user(api_client, obtain_user_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {obtain_user_tokens['access']}")
    response = api_client.post("/api/logout/", data={"refresh": obtain_user_tokens["refresh"]})
    print(f"🚪 Логаут пользователя: {response.status_code}, {response.json()}")
    return response

@pytest.mark.django_db
def test_full_api_flow(create_manager, obtain_tokens, refresh_token, create_cities, list_cities, update_weather, logout_manager, register_user, obtain_user_tokens, user_weather, logout_user):
    print("\n🚀 **Начинаем полный тест API** 🚀\n")
    
    assert create_manager.status_code == 201
    assert "access" in obtain_tokens
    assert "access" in refresh_token
    assert len(create_cities) == 10
    assert list_cities.status_code == 200
    assert update_weather.status_code in [200, 404]
    assert logout_manager.status_code == 205 
    assert register_user.status_code == 201
    assert "access" in obtain_user_tokens
    assert user_weather.status_code in [200, 404]
    assert logout_user.status_code == 205 

    print("\n✅ **Все тесты успешно пройдены!** ✅\n")
