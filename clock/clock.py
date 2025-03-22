from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz
import requests
import os

def get_is_night(latitude, longitude):
    # Sunrise-Sunset API URL
    url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0"

    # Make the API request
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        # Get the UTC time for sunrise and sunset
        sunrise_utc = data["results"]["sunrise"]
        sunset_utc = data["results"]["sunset"]

        # Convert UTC times to local time (example: using UTC as the timezone)
        utc_zone = pytz.utc
        local_zone = pytz.timezone("America/New_York")  # Replace with your desired timezone

        sunrise_time = datetime.fromisoformat(sunrise_utc).astimezone(local_zone)
        sunset_time = datetime.fromisoformat(sunset_utc).astimezone(local_zone)

        # Get the current time in the same timezone
        current_time = datetime.now(local_zone)

        # Check if current time is after sunset or before sunrise
        if current_time > sunset_time or current_time < sunrise_time:
            return True
        else:
            return False
    else:
        print("Error: Could not retrieve data.")
        return False

def get_weather_data(latitude, longitude):
    api_key = "669076decd09031ac99ba76fbc479936"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric"  # Use 'imperial' for Fahrenheit
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        weather_info = {
            "location": f"{data['name']}, {data['sys']['country']}",
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "cloud_cover": data["clouds"]["all"]
        }
        return weather_info
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

def get_is_cloudy(latitude, longitude, threshold=50):
    weather_data = get_weather_data(latitude, longitude)
    
    if isinstance(weather_data, str):  # Error occurred
        return weather_data
    
    current_cloud_cover = weather_data['cloud_cover']
    
    return current_cloud_cover >= threshold

def save_clock_image(file_path, width=32, height=32, font_path=None, font_size=1, bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    """
    Generates an image displaying the current date and time and saves it to the specified path.
    """

    # set fonts using relative path
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "Pixolletta8px.ttf")

    # Create a blank image
    image = Image.new("RGB", (width, height), color=bg_color)

    # Initialize drawing context
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path,10)

    # Get the current date and etime
    current_day_of_week = datetime.now().strftime("%a.")
    current_date = datetime.now().strftime("%m/%d")
    current_time = datetime.now().strftime("%I:%M")

    # Draw the text on the image
    draw.text((0, 1), current_day_of_week, fill=text_color, font=font)
    draw.text((0, 12), current_date, fill=text_color, font=font)
    draw.text((0, 23), current_time, fill=text_color, font=font)

    # Load the sun or moon image using relative paths
    sun_image_path = os.path.join(os.path.dirname(__file__), "sun.png")
    moon_image_path = os.path.join(os.path.dirname(__file__), "moon.png")

    latitude = 40.036217
    longitude = -75.513809
    is_night = get_is_night(latitude, longitude)
    #is_cloudy = get_is_cloudy(latitude, longitude)

    if is_night:
        moon_image = Image.open(moon_image_path)
        moon_position = (22,1)
        image.paste(moon_image, moon_position, moon_image)
    else:
        sun_image = Image.open(sun_image_path)
        sun_position = (22,1)
        image.paste(sun_image, sun_position, sun_image)

    # Save the image to the specified path
    image.save(file_path)
