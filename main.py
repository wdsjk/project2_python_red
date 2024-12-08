from pprint import pprint

import requests


API_KEY = ""

def get_weather_data(latitude, longitude, api_key):
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{latitude},{longitude}?apikey={api_key}"

    response = requests.get(url).json()

    data = {
        "temperature": response["Temperature"]["Metric"]["Value"],
        "humidity": response["RelativeHumidity"],
        "wind_speed": response["Wind"]["Speed"]["Metric"]["Value"],
        # так как у AccuWeather нет отдельного поля под вероятность дождя, пусть будет так
        "precipitation_prob": response["PrecipitationSummary"]["PastHour"]["Metric"]["Value"] / response["PrecipitationSummary"]["Past24Hours"]["Metric"]["Value"]
    }

    return data


def main():
    pprint(get_weather_data(55.751244, 37.618423, API_KEY))


if __name__ == '__main__':
    main()