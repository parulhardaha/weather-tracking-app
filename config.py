import os

class Config:
    API_KEY = os.getenv("OPENWEATHER_API_KEY", "2ae9bd609aa084fec4d1e35ec1244b22")
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    DATABASE = "weather_data.db"
    METROS = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
    FETCH_INTERVAL = 5  # Minutes
