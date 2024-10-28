import sqlite3

def init_db():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY,
            city TEXT,
            main TEXT,
            temp REAL,
            feels_like REAL,
            dt INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_weather_data(city, main, temp, feels_like, dt):
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weather (city, main, temp, feels_like, dt) VALUES (?, ?, ?, ?, ?)",
                   (city, main, temp, feels_like, dt))
    conn.commit()
    conn.close()
