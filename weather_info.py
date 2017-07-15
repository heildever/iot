import json
import urllib


class Weather(object):
    def __init__(self):
        self.url = 'http://api.openweathermap.org/data/2.5/weather?q=Turin,it,uk&APPID=89b0d25b5372053b338f9bf0689921fd'
        self.urlout = urllib.urlopen(self.url)
        self.weather_info = json.loads(self.urlout.read())

    def getweather(self):
        weather_detailed = self.weather_info['weather']
        weather_simplified = weather_detailed[0]['main']
        return weather_simplified

    def getsunrise(self):
        sunrise = self.weather_info['sys']['sunrise']
        return sunrise

    def getsunset(self):
        sunset = self.weather_info['sys']['sunset']
        return sunset
