from flask import Flask, render_template, request
import requests
import configparser
from datetime import datetime

app = Flask(__name__)
app.debug = True


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = get_api_key()
    if temp_units == 'F':
        data = get_weather_results_imperial(zip_code, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    else:
        data = get_weather_results_metric(zip_code, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])

    data = get_weather_results(zip_code, api_key)
    icon = data["weather"][0]["icon"]
    iconurl = "http://openweathermap.org/img/w/" + icon + ".png"
    weather = data["weather"][0]["main"]
    location = data["name"]
    sunrise = data["sys"]["sunrise"]
    dt_obj = datetime.fromtimestamp(int(sunrise))
    return render_template('results.html',
                           location=location, temp=temp, iconurl=iconurl, dt_obj=dt_obj,
                           feels_like=feels_like, weather=weather, sunrise=sunrise)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_forecast(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/forecast?zip={}&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run()

print(get_weather_results("95129", get_api_key()))
