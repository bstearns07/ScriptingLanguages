# Using flask
from flask import Flask, render_template, request
import requests
import webbrowser

app = Flask(__name__)


# Function to fetch current weather data
def get_current_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    return response.json()


# Function to fetch 5-day/3-hour weather forecast
def get_weather_forecast(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    return response.json()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = "bf8e23c795088c0b305fef853a43af6b"  # Replace with your OpenWeatherMap API key

    current_weather = get_current_weather(city, api_key)
    forecast = get_weather_forecast(city, api_key)

    if current_weather["cod"] != "404" and forecast["cod"] == "200":
        return render_template('weather.html', current_weather=current_weather, forecast=forecast)
    else:
        return render_template('error.html', city=city)


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    app.run(debug=True)
