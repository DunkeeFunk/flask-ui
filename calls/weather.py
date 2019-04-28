import requests
from datetime import datetime


def get_weather():
    weather_endpoint = 'http://api.openweathermap.org/data/2.5/weather?lat=55.0198978&lon=-7.3185895&appid=26fac9ce320917802e0dc0b6f10137ca'
    r = requests.get(weather_endpoint)
    weather = r.json()
    return_me = {
        'air_pressure': weather['main']['pressure'],
        'sunrise': str(datetime.utcfromtimestamp(weather['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')),
        'sunset': str(datetime.utcfromtimestamp(weather['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')),
        'wind_speed': weather['wind']['speed']
    }
    return return_me
















