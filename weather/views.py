from django.shortcuts import render
import requests

def weather_view(request):
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city")
        api_key = "YOUR_API_KEY"  # Replace with your actual OpenWeatherMap API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        else:
            error = f"Could not retrieve weather for {city}. Please check the city name."

    return render(request, "weather/index.html", {"weather_data": weather_data, "error": error})
