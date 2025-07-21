import falcon
import requests


# TODO: Logik Zeitzonen herausfinden

standard_url = "http://php/index.php?action="

class Hello:
    def on_get(self, req, resp):
        resp.media = requests.get(standard_url + "hello").json()

class HowAreYou:
    def on_get(self, req, resp):
        resp.media = requests.get(standard_url + "howareyou").json()

class WhatTimeIsIt:
    def on_get(self, req, resp):
        resp.media = {"n/a": "TODO"}

# Get und Post mit /in
class InByCityGet:
    def on_get(self, req, resp, city):
        resp.media = {"n/a": "TODO"}

class InByCityPost:
    def on_get(self, req, resp):
        resp.media = {"n/a": "TODO"}