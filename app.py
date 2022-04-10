import boto3
from flask import Flask, render_template, request, send_file, Response
import requests
from datetime import datetime
from datetime import timedelta
import calendar
import dynodb

KYE_N = "77d7d62a02bf7662f5406c63c27ee0e2&units=metric"
KYE_A = "b39af7bbff0f462a017788d2efdde3d3"
app = Flask(__name__)
weather_dict = {}


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


@app.route('/download')
def download():
    # return send_file("/home/alex/Downloads/sky.jpg", as_attachment=True)
    AWS_S3_CREDS = {
        "aws_access_key_id": "AKIAZ4MRP27HURL2X4ZV",  # os.getenv("AWS_ACCESS_KEY")
        "aws_secret_access_key": "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"  # os.getenv("AWS_SECRET_KEY")
    }
    s3_client = boto3.client('s3', **AWS_S3_CREDS)

    # s3 = boto3.client('s3')
    s3_client.download_file('alexeyindex.com', 'download/sky.jpg', '/home/alex/Desktop/downtest/client_sky.jpg')
    return render_template("index.html")


@app.route('/save_info')
def save_info():
    dynodb.adding_item_db(weather_dict['daily'], weather_dict['city_name'], weather_dict['country'])
    return render_template("index.html", daily=weather_dict['daily'], name=weather_dict['city_name'],
                           country=weather_dict['country'])


@app.route("/", methods=["GET", "POST"])
def get_coordinates():
    if request.method == "POST":
        location = request.form.get('location')
        if location:
            cities = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={KYE_A}")
            if len(cities.json()) > 0:
                coords = cities.json()[0]
                print("coords:",coords)
                daily = get_dict_7_days(coords["lat"], coords["lon"])
                global weather_dict
                weather_dict = {
                    'daily': daily,
                    'city_name': coords["name"],
                    'country': coords["country"]
                }
                return render_template("index.html", daily=daily, name=coords["name"], country=coords["country"])
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
