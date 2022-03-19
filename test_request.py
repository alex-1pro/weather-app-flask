# import requests
# from datetime import date
# import calendar


#
# if __name__ == '__main__':
#     # x = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=32.08088&lon=34.78057&exclude=minutely,hourly&appid=77d7d62a02bf7662f5406c63c27ee0e2&units=metric")
#     # # print(x.json()['coord']['lon'])
#     # days = x.json()['daily']
#     # day_current = days[0]
#     #
#     # print(day_current["temp"]["day"])
#     my_date = date.today()
#     print(calendar.day_name[my_date.weekday()])
#
#     # print(x.json())


from datetime import datetime
from datetime import timedelta

# Add 1 day
print(datetime.now() + timedelta(days=1))

# Subtract 60 seconds
print(datetime.now() - timedelta(seconds=60))

# Add 2 years
print(datetime.now() + timedelta(days=730))

# Other Parameters you can pass in to timedelta:
# days, seconds, microseconds,
# milliseconds, minutes, hours, weeks

# Pass multiple parameters (1 day and 5 minutes)
print(datetime.now() + timedelta(days=1, minutes=5))