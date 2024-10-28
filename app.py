from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from weather_data import fetch_weather  
from models import init_db
import sqlite3
import requests
import pandas as pd

app = Flask(__name__)
app.config.from_object("config.Config")

#initialize the database
init_db()

# Schedule data fetching every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_weather, trigger="interval", minutes=app.config["FETCH_INTERVAL"])
scheduler.start()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = fetch_weather(city)
        return render_template('summary.html', weather_data=weather_data)
    return render_template("index.html")

@app.route("/summary", methods=['GET', 'POST'])
def summary():
    if request.method == 'POST':
        city = request.form['city']  # Retrieve the city from the submitted form
        weather_data = fetch_weather(city)  # Fetch weather for the city
        return render_template("summary.html", weather_data=weather_data)
    
    # If it's a GET request, display the summary
    conn = sqlite3.connect(app.config["DATABASE"])
    query = "SELECT * FROM weather"
    df = pd.read_sql(query, conn)
    daily_summary = df.groupby('city').agg(
        avg_temp=('temp', 'mean'),
        max_temp=('temp', 'max'),
        min_temp=('temp', 'min'),
        dominant_weather=('main', lambda x: x.mode()[0])
    )
    conn.close()
    return render_template("summary.html", daily_summary=daily_summary)


@app.route("/alerts")
def alerts():
    conn = sqlite3.connect(app.config["DATABASE"])
    df = pd.read_sql("SELECT * FROM weather", conn)
    alerts = df[(df['temp'] > 35)]
    conn.close()
    return render_template("alerts.html", alerts=alerts)

# OpenWeatherMap API Configuration
API_KEY = "2ae9bd609aa084fec4d1e35ec1244b22"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "main_weather": data["weather"][0]["main"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "timestamp": data["dt"]
        }
    else:
        return None  

if __name__ == "__main__":
    app.run(debug=True)
