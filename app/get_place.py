from geopy.geocoders import Nominatim
from flask import request
import requests
import os


def get_location():
    """Gets the langitude and longitude of location entered
    (or located from IP using http://ipinfo.io )
    using GeoPy, if no city is found returns error message"""

    geolocator = Nominatim(user_agent="the_weather")
    if request.method == "POST":
        city = request.form.get("query", default="New Delhi")
    if request.method == "GET":
        city = "New Delhi"
    location = geolocator.geocode(city, language="en_US")
    return location


def get_location_data(location_name):
    """Accepts the longitude and latitude which are used as parameters
    for requesting weather data
    from OpenWeatherMap , returns weather data in JSON"""
    # try:
    api_key = os.environ.get("MY_OPEN_WEATHER_API_KEY")
    lat = location_name.latitude
    lon = location_name.longitude
    url = (
        "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=hourly,minutely&appid=%s&units=metric"
        % (lat, lon, api_key)
    )

    result = requests.get(url)
    # data is the json file
    data = result.json()
    return data
