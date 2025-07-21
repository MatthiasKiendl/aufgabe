"""
controller.py
This module implements a Falcon-based web API that interacts with a PHP backend and provides endpoints for time-related queries based on city names or IP geolocation.
Functions:
----------
- city_to_timezone(city_name: str) -> str | None:
    Converts a city name to its corresponding timezone using geopy and timezonefinder.
    Returns the timezone string or None if the city is not found.
- find_timezone_by_ip() -> str | None:
    Determines the timezone based on the client's IP address using ipapi.co and timezonefinder.
    Returns the timezone string or None if the location cannot be determined.
Classes:
--------
- Hello:
    GET endpoint that proxies a "hello" request to the PHP backend.
- HowAreYou:
    GET endpoint that proxies a "howareyou" request to the PHP backend.
- WhatTimeIsIt:
    GET endpoint that determines the user's timezone by IP and requests the current time from the PHP backend.
    Returns an error if the timezone cannot be determined.
- InByCity:
    GET endpoint that accepts a city name as a URL parameter, determines its timezone, and requests the current time from the PHP backend.
    Returns an error if the city is not found.
- InByCityPost:
    POST endpoint that accepts a city name in JSON, determines its timezone, and requests the current time from the PHP backend.
    Returns an error if the city is not found or if the request is malformed.
- IndexRedirect:
    GET endpoint that redirects requests to '/index.html'.
App Setup:
----------
- Registers static route for frontend assets.
- Adds all defined routes to the Falcon app.
"""
import falcon
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import os

standard_url = "http://php/index.php?action="


def city_to_timezone(city_name: str) -> str | None:
    geolocator = Nominatim(user_agent="city_to_timezone")
    location = geolocator.geocode(city_name)

    if not location:
        return None

    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=location.longitude, lat=location.latitude)

    return timezone

def find_timezone_by_ip() -> str | None:
    try:
        ip_info = requests.get("https://ipapi.co/json/").json()
        lat = ip_info.get("latitude")
        lon = ip_info.get("longitude")
        if lat and lon:
            tf = TimezoneFinder()
            return tf.timezone_at(lat=lat, lng=lon)
    except Exception:
        return None

class Hello: 
    def on_get(self, req, resp):
        resp.media = requests.get(standard_url + "hello").json()


class HowAreYou:
    def on_get(self, req, resp):
        resp.media = requests.get(standard_url + "howareyou").json()

class WhatTimeIsIt:
    def on_get(self, req, resp):
        tz = find_timezone_by_ip()
        if not tz:
            resp.status = falcon.HTTP_400
            resp.media = {"Error": "Unable to identify timezone"}
            return

        php_response = requests.get(standard_url + "whattimeisit", params={"timezone": tz})
        resp.media = php_response.json()

class InByCity:
    def on_get(self, req, resp, city):
        tz = city_to_timezone(city)
        if tz is None:
            resp.status = falcon.HTTP_404
            resp.media = {"Error": "City not found."}
        else:
            response = requests.get(standard_url + "in", params={"timezone": tz})
            resp.media = response.json()

class InByCityPost:
    def on_post(self, req, resp):
        try:
            data = req.media
            city = data.get("city", "").strip()

            if not city:
                resp.status = falcon.HTTP_400
                resp.media = {"Error": "The name of the city has to be in JSON e.g. {'city': 'London'}"}
                return

            tz = city_to_timezone(city)
            if tz is None:
                resp.status = falcon.HTTP_404
                resp.media = {"Error": "City not found."}
            else:
                response = requests.get(standard_url + "in", params={"timezone": tz})
                resp.media = response.json()

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"Error": f"Internal Error: {str(e)}"}


class IndexRedirect:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_302
        resp.set_header('Location', '/index.html')

app = falcon.App()

frontend_path = os.path.dirname(os.path.abspath(__file__))

app.add_static_route("/", frontend_path)
app.add_route("/", IndexRedirect())
app.add_route("/hello", Hello())
app.add_route("/howareyou", HowAreYou())
app.add_route("/whattimeisit", WhatTimeIsIt())
app.add_route("/in/{city}", InByCity())
app.add_route("/in", InByCityPost())


