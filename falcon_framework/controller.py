import falcon
import requests
from geopy.geocoders import Nominatim                               #city -> coordinates
from timezonefinder import TimezoneFinder                           #coordinates -> timezone
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


