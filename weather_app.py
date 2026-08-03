import requests

WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates():
    city = input(f"Enter City, type 'Exit' to leave: ").title()
    city_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    if city.lower() == "exit":
        return "exit"

    response = requests.get(city_url)
    data = response.json()

    if not data.get("results"):
        return None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    city_name = data["results"][0]["name"]


    return latitude, longitude, city_name

WEATHER_CODES = {
    0: "☀️ Clear Sky",
    1: "🌤️ Mainly Clear",
    2: "⛅ Partly Cloudy",
    3: "☁️ Overcast",
    45: "🌫️ Fog",
    61: "🌧️ Rain",
    71: "❄️ Snow",
    95: "⛈️ Thunderstorm"
}

def get_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,weather_code,apparent_temperature,relative_humidity_2m,is_day",
        "timezone": "auto"

    }
    weather_response = requests.get(WEATHER_BASE_URL, params = params)
    weather_data = weather_response.json()


    weather_code = weather_data["current"]["weather_code"]

    weather = WEATHER_CODES.get(weather_code, "Unknown Weather")

    return weather_data, weather


def print_weather(city_name, weather_data,weather):
    print("================================")
    print("           WEATHER APP")
    print("================================")

    print(f"📍 City: {city_name}\n")

    print(f"🌡️ Current Temperature: {weather_data['current']['temperature_2m']}°C")
    print(f"🍃 Current Wind Speed: {weather_data['current']['wind_speed_10m']} km/h")
    print(f"🌤️ Weather: {weather}")
    print(f"☀️ Apparent Temperature: {weather_data['current']['apparent_temperature']} °C")
    print(f"💧 Humidity: {weather_data['current']['relative_humidity_2m']}%")
    print(f"🕛 Local Time: {weather_data['current']['time']}")
    if weather_data["current"]["is_day"] == 1:
        print("☀️ Day")
    else:
        print("🌙 Night")

    print("================================")

while True:
    coordinates = get_coordinates()

    if coordinates == "exit":
        print("Exiting...")
        break
    elif coordinates is None:
        print("City not found.")
        continue



    latitude, longitude, city_name = coordinates

    weather_data, weather = get_weather(latitude, longitude)

    print_weather(city_name, weather_data, weather)

