import requests
import time
from config import Config
from models import save_weather_data

def fetch_weather():
    for city in Config.METROS:
        params = {
            "q": city,
            "appid": Config.API_KEY,
            "units": "metric"  # Metric to get Celsius directly
        }
        response = requests.get(Config.BASE_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            main = data["weather"][0]["main"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            dt = data["dt"]
            save_weather_data(city, main, temp, feels_like, dt)
        time.sleep(1)  # Avoid hitting API rate limits
