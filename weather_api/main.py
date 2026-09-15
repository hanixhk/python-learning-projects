import os
import dotenv
import requests

dotenv.load_dotenv()

def get_weather(city):
    api_key = os.environ["API_KEY"]
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        data = response.json()
        raise Exception(f"Error fetching weather data: {data.get('message', 'Unknown error')}")

    data = response.json()

    temperature = data['main']['temp']

    humidity = data['main']['humidity']

    description = data['weather'][0]['description']
    
    return {
        "temperature": temperature,
        "humidity": humidity,
        "description": description,
        "city": city

    }

# Example usage
# get_weather("London", "your_api_key")
def menu():
    while True:
        print("Welcome to the Weather API!")
        print("1. Get weather for a city")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            city = input("Enter the city name: ")
            return city
        elif choice == "2":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please try again.")
            
city = menu()   
try:
    weather_data = get_weather(city)
    print(f"Weather in {city}:")
    print(f"Temperature: {weather_data['temperature']:.2f}°C")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Description: {weather_data['description']}")
except Exception as e:
    print(e)

