import requests
from flask import Flask, request, render_template


app = Flask(__name__)

API_KEY = ""

def get_weather_data(api_key, city):
    url_for_location = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city.strip().lower()}"

    try:
        r = requests.get(url_for_location).json()
        if len(r) == 0:
            raise Exception(f"Не найден город: {city}")

        location_key = r[0]["Key"]

        url_for_weather = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}&details=true"

        response = requests.get(url_for_weather).json()[0]

    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return

    data = {
        "temperature": response["Temperature"]["Metric"]["Value"],
        "humidity": response["RelativeHumidity"],
        "wind_speed": response["Wind"]["Speed"]["Metric"]["Value"],
        # так как у AccuWeather нет отдельного поля под вероятность дождя, пусть будет так
        "precipitation_prob": response["PrecipitationSummary"]["PastHour"]["Metric"]["Value"]
    }

    return data


def check_weather(temperature, wind_speed, precipitation_probability, humidity):
    if temperature < -5 or temperature > 35 or wind_speed > 50 or precipitation_probability > 70 or humidity > 70:
        return "Плохая погода"
    return "Хорошая погода"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_location = request.form['start']
        end_location = request.form['end']

        city1_weather_data = get_weather_data(API_KEY, start_location)
        city2_weather_data = get_weather_data(API_KEY, end_location)

        if not city1_weather_data or not city2_weather_data:
            return render_template('exception.html')

        result1 = check_weather(city1_weather_data['temperature'], city1_weather_data['wind_speed'], city1_weather_data['precipitation_prob'], city1_weather_data['humidity'])
        result2 = check_weather(city2_weather_data['temperature'], city2_weather_data['wind_speed'], city2_weather_data['precipitation_prob'], city2_weather_data['humidity'])

        if result1 == result2 and result1 == 'Хорошая погода':
            return render_template('result.html', result="Погода хороша, приятного путешествия!")
        else:
            return render_template('result.html', result="Погода не очень, советую посидеть дома(")

    return render_template('index.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
