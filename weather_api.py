# importing required modules
import requests
import json
from datetime import date

# city name and date
city_name = input("Please enter the city name : ")
date_input = input("Enter the date in(YYYY-MM-DD): ")

# rapidapi Url
url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

# apikey and host
headers = {"X-RapidAPI-Key": "65c9213e55mshbdd24dff0a55013p19ca0djsn174af0375cd5",
           "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}

today = {"q": city_name, "dt": date.today()}
future = {"q": city_name, "dt": date_input}

resp_today = requests.request("GET", url, headers=headers, params=today)
resp_future = requests.request("GET", url, headers=headers, params=future)

# json responses
final_resp_today = resp_today.json()
final_resp_future = resp_future.json()

# printing the conditions
if (final_resp_today["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"] == 1):
    print("It is raining today in " + city_name)
else:
    print("It is not raining today in " + city_name)

if (final_resp_future["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"] == 1):
    print("It is going to rain in " + city_name + " on " + str(date_input))
else:
    print("It is not going to rain in " + city_name + "on " + str(date_input))
