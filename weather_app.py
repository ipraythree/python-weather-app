import requests

WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates():
    city = input("Enter City: ").title()
    city_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    response = requests.get(city_url)
    data = response.json()

    if not data.get("results"):
        print("City not found.")
        return None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    city_name = data["results"][0]["name"]


    return latitude, longitude, city_name

coordinates = get_coordinates()

if coordinates is None:
    exit()

latitude, longitude, city_name = coordinates

def get_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m"
    }
    weather_response = requests.get(WEATHER_BASE_URL, params = params)
    weather_data = weather_response.json()

    return weather_data

weather_data = get_weather(latitude, longitude)

def print_weather(city_name, weather_data):
    print(f"City: {city_name}")
    print(f"Current Temperature: {weather_data['current']['temperature_2m']}°C")
    print(f"Current Wind Speed: {weather_data['current']['wind_speed_10m']}km/h")

print_weather(city_name, weather_data)
