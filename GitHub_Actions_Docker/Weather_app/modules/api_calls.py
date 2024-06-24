from flask import json
import requests


def api_request(location):
    # API key  
    api_key = "26ETMDQDCHSH573U2N5CCFF5L"
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + location + "?unitGroup=metric&key=" + api_key
    resp = requests.get(url)
    status_code = resp.status_code
    if status_code == 200:
        return resp.json()
    else:
        False




    