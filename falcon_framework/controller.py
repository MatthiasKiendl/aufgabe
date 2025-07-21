import falcon
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

# TODO: Logik Zeitzonen herausfinden
def find_timezone_ip() -> str | None:
    try:
        info = requests.get("https://ipapi.co/json/").json()
        b_grad = info.get("latitude")
        l_grad = info.get("longitude")
        if b_grad and l_grad:
            finder = TimezoneFinder()
            return finder.timezone_at(lat=b_grad, lng=l_grad)
    except Exception:
        return None

standard_url = "http://php/index.php?action="

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

# Get und Post mit /in
class InByCityGet:
    def on_get(self, req, resp, city):
        resp.media = {"n/a": "TODO"}

class InByCityPost:
    def on_get(self, req, resp):
        resp.media = {"n/a": "TODO"}