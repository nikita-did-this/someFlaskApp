from dotenv import load_dotenv
import os
import requests

load_dotenv()


class Config(object):
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_DEFAULT_CITY = os.getenv("WEATHER_DEFAULT_CITY")
    WEATHER_URL = os.getenv("WEATHER_URL")


def weather_by_city(city_name=Config.WEATHER_DEFAULT_CITY):
    geo_data = {
        "key": Config.WEATHER_API_KEY,
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }
    weather_url = Config.WEATHER_URL
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


if __name__ == "__main__":
    print(weather_by_city())

