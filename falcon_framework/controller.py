import falcon
import requests
from geopy.geocoders import Nominatim                               #city -> coordinates
from timezonefinder import TimezoneFinder                           #coordinates -> timezone

standard_url = "http://php/index.php?action="

def find_timezone_ip() -> str | None:
    try:
        info = requests.get("https://ipapi.co/json/").json()
        b_grad = info.get("latitude")
        l_grad = info.get("longitude")
        if b_grad and l_grad:
            return TimezoneFinder().timezone_at(lng=l_grad, lat=b_grad)
    except Exception:
        return None

def find_timezone_city(cityname: str) -> str | None:
        geolocator = Nominatim(user_agent="timezone_city")
        location = geolocator.geocode(cityname)
        if not location:
            return None
        b_grad = location.latitude
        l_grad = location.langitude
        return TimezoneFinder().timezone_at(lng=l_grad, lat=b_grad)



class Hello:
    def on_get(self, req, resp):
        resp.media = requests.get(standard_url + "hello").json()

class HowAreYou:
    def on_get(self, req, resp):
        resp.media = requests.get(standard_url + "howareyou").json()

class WhatTimeIsIt:
    def on_get(self, req, resp):
        time_zone = find_timezone_ip()
        if not time_zone:
            resp.media = {"Error": "Unable to identify timezone"}
            return
        php_response = requests.get(standard_url + "whattimeisit", params={"timezone": time_zone})
        resp.media = php_response.json()

class InByCityGet:
    def on_get(self, req, resp, city):
        time_zone = find_timezone_city(city)
        if time_zone is None:
            resp.media = {"Error": "City not found."}
        else:
            response = requests.get(standard_url + "in", params={"timezone": time_zone})
            resp.media = response.json()

class InByCityPost:
    def on_get(self, req, resp):
        data = req.media
        city = data.get("city", "").strip()

        if not city:
            resp.media = {"Error": "The name of the city has to be in JSON e.g. {'city': 'London'}"}
            return
        time_zone = find_timezone_city(city)
        if time_zone is None:
            resp.media = {"Error": "City not found."}
        else:
                response = requests.get(standard_url + "in", params={"timezone": time_zone})
                resp.media = response.json()            
