# Weather Forecast API

## 📌 Overview
The Weather Forecast API is a RESTful web service that provides weather information for specified cities. The project allows users to register, authenticate, and retrieve weather updates for their selected city. It is built with Django and Django REST Framework and integrates with the OpenWeatherMap API to fetch real-time weather data.

---
## 🛠️ Tech Stack
- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Authentication**: JWT (SimpleJWT)
- **External API**: OpenWeatherMap
- **Testing**: Pytest, Django Test Client

---
## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```sh
$ git clone https://github.com/justkurama/weather-forecast-api.git
$ cd weather-forecast-api
```

### 2️⃣ Create a Virtual Environment
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3️⃣ Install Dependencies
```sh
$ pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file and configure the following:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/weather_db
API_KEY=your_openweathermap_api_key
```

### 5️⃣ Apply Migrations & Create Superuser
```sh
$ python manage.py migrate
$ python manage.py createsuperuser
```

### 6️⃣ Run the Development Server
```sh
$ python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`

---
## 📌 Functional Requirements
### 🌍 User Roles
- **Manager**: Can register users, add cities, update weather.
- **User**: Can register, retrieve weather data for their city.

### 🔧 Core Features
- **User Authentication**: JWT-based authentication for security.
- **City Management**: Managers can add and list cities.
- **Weather Update**: Fetches weather data from OpenWeatherMap API.
- **Weather Retrieval**: Users can get the latest weather for their city.

---
## 🛠️ API Endpoints
### 🔑 Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/register/` | Register a new user |
| `POST` | `/api/register/manager/` | Register a new manager |
| `POST` | `/api/token/` | Obtain JWT access and refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh an access token |
| `POST` | `/api/logout/` | Logout a user (blacklist refresh token) |

### 🌆 City Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/cities/` | Add a new city (Manager only) |
| `GET`  | `/api/cities/` | List all available cities |

### ⛅ Weather
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/weather/update/<city_id>/` | Update weather for a city (Manager only) |
| `GET`  | `/api/weather/` | Retrieve weather data for the user's city |

### 🏠 User Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/profile/` | Retrieve the profile of the logged-in user |

---
## 🧪 Testing with Pytest

### 1️⃣ Run Tests
```sh
$ pytest -v -s
```
### 2️⃣ Test Flow
- Manager Registration
- Obtain JWT Token
- Refresh JWT Token
- Login
- Add 10 Cities
- Retrieve City List
- Update Weather
- Logout Manager
- Register User (Selecting a city)
- Obtain JWT Token
- Login
- Retrieve Weather Data
- Logout User

---
## 📌 Future Improvements
- **Docker support**: Add Docker for deployment.
- **GraphQL API**: Provide an alternative to REST.
- **WebSocket Notifications**: Real-time weather updates.
- **Admin Panel**: Web UI for managing users and cities.

---
## 💡 Contributing
Feel free to fork the repository and submit pull requests!
