from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API Configuration
API_KEY = "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"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()
  
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/current-weather", methods=["GET", "POST"])
def current_weather():
    weather_data = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            data = fetch_weather(city)
            if data.get("cod") == 200:
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                }
            else:
                error = data.get("message", "City not found.")
        else:
            error = "Please enter a city name."
    return render_template("current_weather.html", weather_data=weather_data, error=error)

@app.route("/forecast")
def forecast():
    return render_template("forecast.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
