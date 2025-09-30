# weather.py
import requests


# Function to fetch weather data
def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Construct the full URL for the API request
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"

    # Send the GET request to the OpenWeatherMap API
    response = requests.get(complete_url)

    # Convert the response JSON to a dictionary
    data = response.json()

    # If the response contains valid data, display it
    if data["cod"] == 200:
        main = data["main"]
        wind = data["wind"]
        weather_description = data["weather"][0]["description"]

        print(f"City: {city_name}")
        print(f"Temperature: {main['temp']}°C")
        print(f"Humidity: {main['humidity']}%")
        print(f"Pressure: {main['pressure']} hPa")
        print(f"Weather: {weather_description.capitalize()}")
        print(f"Wind Speed: {wind['speed']} m/s")
    else:
        print("City not found.")


# Main part of the script
if __name__ == "__main__":
    # User inputs the city and API key
    city = input("Enter city name: ")
    api_key = "bf8e23c795088c0b305fef853a43af6b"  # Replace with your OpenWeatherMap API key

    get_weather(city, api_key)
