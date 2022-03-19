from flask import Flask, render_template, request
import requests
from datetime import datetime
from datetime import timedelta
import calendar


KYE_N = "77d7d62a02bf7662f5406c63c27ee0e2&units=metric"
KYE_A = "b39af7bbff0f462a017788d2efdde3d3"
app = Flask(__name__)


def get_dict_7_days(lat, lon):
    forecast = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={KYE_A}&units=metric")
    daily = forecast.json()["daily"]
    result = []
    for index, value in enumerate(daily):
        t_date = datetime.now() + timedelta(days=index)
        day_week = calendar.day_name[t_date.weekday()]
        day = int(value["temp"]["day"])
        night = int(value["temp"]["night"])
        humidity = value["humidity"]
        icon = f'http://openweathermap.org/img/wn/{value["weather"][0]["icon"]}@2x.png'
        description = value["weather"][0]["description"]
        wind_speed = value["wind_speed"]
        current_temp = int(forecast.json()["current"]["temp"])
        daily_dict = {
            "day_week": day_week, "t_date": t_date, "day": day,
            "night": night, "humidity": humidity, "icon": icon,
            "description": description, "wind_speed": wind_speed, "current_temp": current_temp
        }

        result.append(daily_dict)
    return result


@app.route("/", methods=["GET", "POST"])
def get_coordinates():
    if request.method == "POST":
        location = request.form.get('location')
        if location:
            cities = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={KYE_A}")
            if len(cities.json()) > 0:
                coords = cities.json()[0]
                daily = get_dict_7_days(coords["lat"], coords["lon"])
                return render_template("index.html", daily=daily, name=coords["name"], country=coords["country"])
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
