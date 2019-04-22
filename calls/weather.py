import requests


def get_weather():
    weather_endpoint = 'http://api.openweathermap.org/data/2.5/weather?lat=55.0198978&lon=-7.3185895&appid=26fac9ce320917802e0dc0b6f10137ca'
    r = requests.get(weather_endpoint)
    weather = r.json()
    return_me = {
        'air_pressure': weather['main']['pressure'],
        'sunrise': weather['sys']['sunrise'],
        'sunset': weather['sys']['sunset'],
        'wind_speed': weather['wind']['speed']
    }
    return return_me
















