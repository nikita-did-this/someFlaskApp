from flask import current_app
import requests


def weather_by_city(city_name):
    geo_data = {
        "key": current_app.config['WEATHER_API_KEY'],
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }
    weather_url = current_app.config['WEATHER_URL']
    try:
        result = requests.get(weather_url, params=geo_data)
        result.raise_for_status()
        weather = result.json()
        if "data" in weather:
            if "current_condition" in weather['data']:
                try:
                    return weather["data"]["current_condition"][0]
                except(IndexError, TypeError):
                    return False
    except (requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
    return False
