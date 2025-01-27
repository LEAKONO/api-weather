from django.shortcuts import render
import requests

def weather_view(request):
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city", "").strip()  # Remove leading/trailing spaces
        if not city:
            error = "City name cannot be empty."
        else:
            api_key = "29fcc3d7b5d1b7314360d96e56039d50"

            
            # Step 1: Get latitude and longitude from the city name using OpenWeatherMap Geocoding API
            geocoding_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            geocode_response = requests.get(geocoding_url)

            # Print the raw response for debugging
            print(f"Geocoding URL: {geocoding_url}")
            print(f"Geocoding Response: {geocode_response.json()}")  # Print the response from geocoding API
            
            if geocode_response.status_code == 200:
                geocode_data = geocode_response.json()
                
                # Check if 'coord' exists in the response
                if "coord" in geocode_data:
                    lat = geocode_data["coord"]["lat"]
                    lon = geocode_data["coord"]["lon"]

                    # Step 2: Use One Call API with the obtained lat and lon
                    onecall_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&units=metric&appid={api_key}"

                    try:
                        response = requests.get(onecall_url, timeout=10)  # Timeout added for safety
                        response.raise_for_status()  # Raise an error for 4xx/5xx responses
                        data = response.json()

                        if "current" in data:
                            # Extract weather data from the One Call API response
                            weather_data = {
                                "city": city,
                                "temperature": data["current"].get("temp", "Data not available"),  # Temperature in Celsius
                                "description": data["current"]["weather"][0].get("description", "No description"),  # Weather description
                                "icon": data["current"]["weather"][0].get("icon", "No icon"),  # Weather icon
                            }

                    except requests.exceptions.Timeout:
                        error = "The request timed out. Please try again later."
                    except requests.exceptions.RequestException as e:
                        error = f"An error occurred: {str(e)}"
                else:
                    error = f"City '{city}' could not be found. Please try another city."
            else:
                error = f"Error: Unable to retrieve data for the city '{city}'. Response code: {geocode_response.status_code}"

    return render(request, "weather/index.html", {"weather_data": weather_data, "error": error})
