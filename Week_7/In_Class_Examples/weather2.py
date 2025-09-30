# weather2.py
import requests


# Function to fetch current weather data
def get_current_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:
        main = data["main"]
        weather_description = data["weather"][0]["description"]
        print(f"\nCurrent weather in {city_name}:")
        print(f"Temperature: {main['temp']}°C")
        print(f"Humidity: {main['humidity']}%")
        print(f"Weather: {weather_description.capitalize()}\n")
    else:
        print("City not found.")


# Function to fetch 5-day/3-hour weather forecast data
def get_weather_forecast(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == "200":
        print(f"5-Day Weather Forecast for {city_name}:")
        for forecast in data["list"]:
            dt_txt = forecast["dt_txt"]
            main = forecast["main"]
            weather_description = forecast["weather"][0]["description"]
            temp = main["temp"]
            print(f"{dt_txt} | Temp: {temp}°C | {weather_description.capitalize()}")
    else:
        print("City not found.")


# Main function to fetch current weather and forecast
if __name__ == "__main__":
    city = input("Enter city name: ")
    api_key = "bf8e23c795088c0b305fef853a43af6b"  # Replace with your OpenWeatherMap API key

    get_current_weather(city, api_key)
    get_weather_forecast(city, api_key)
