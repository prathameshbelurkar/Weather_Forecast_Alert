import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# 4Y--K9cqPMFhTj94EbQAYmVsHi87NPz03ztSLiAr
account_sid = "ACea172c704ff2313dc6001192b5efbe71"
auth_token = "4e9bd57a5acbb271a49d5af95c249330"
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "f183ede7ab41ccfc4486a144cf997eb7"

weather_params = {
    "lat": 18.582890,
    "lon": 73.809799,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(url=OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

# print(weather_data["hourly"][0]["weather"][0]["id"])
weather_slice = weather_data["hourly"][:12]

will_rain = True
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
        # print("Bring a umbrella")

if will_rain:
    # print("Bring an umbrella.")
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"https": os.environ["https_proxy"]}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's goint to rain today. Remember to bring the ☔",
        from_='+12017203693',
        to='+919579195742'
    )
    print(message.status)