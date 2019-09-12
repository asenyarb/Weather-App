from django.db import models
from accounts.models import Profile
from weather_app.utils import unix_time_to_local
from datetime import datetime, timedelta
import requests
from copy import deepcopy


class Weather(models.Model):
    temp = models.DecimalField(max_digits=2, decimal_places=0)
    temp_min = models.DecimalField(max_digits=2, decimal_places=0)
    temp_max = models.DecimalField(max_digits=2, decimal_places=0)
    humidity = models.DecimalField(max_digits=3, decimal_places=0)
    pressure = models.DecimalField(max_digits=4, decimal_places=0)
    description = models.CharField(max_length=20)
    wind_speed = models.FloatField()
    weather = models.CharField(max_length=20)
    icon_id = models.CharField(max_length=20)
    sunrise = models.CharField(max_length=6)
    sunset = models.CharField(max_length=6)
    update_time = models.DateTimeField(null=True)

    def save(self, response=None, *args, **kwargs):
        if response:
            self.temp = response['main']['temp']
            self.temp_min = response['main']['temp_min']
            self.temp_max = response['main']['temp_max']
            self.humidity = response['main']['humidity']
            self.pressure = response['main']['pressure']
            self.description = response['weather'][0]['description']
            self.wind_speed = response['wind']['speed']
            self.weather = response['weather'][0]['main']
            self.icon_id = response['weather'][0]['icon']
            self.sunrise = unix_time_to_local(response['coord'], response['sys']['sunrise'])
            self.sunset = unix_time_to_local(response['coord'], response['sys']['sunset'])
            self.update_time = datetime.utcnow()
            super(Weather, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Weather"

    def _str_(self):
        return "weather in " + self.city.city_name + self.city.country_code


class City(models.Model):
    id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2, blank=True)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='cities')
    weather = models.OneToOneField(Weather, null=True, on_delete=models.CASCADE, related_name="city")

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name


def update_weather_if_needed(city: City):
    if (city.weather.update_time).replace(tzinfo=None)-datetime.utcnow() > timedelta(minutes=20):
        app_id = '&units=metric&appid=d5690ce2c8cf4f332eb7788636e9bc69'
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city.city_name + ',' + city.country_code + app_id
        response = requests.get(url.format(city.city_name)).json()
        weather = Weather()
        weather.save(response=response)
        new_city = City()
        id = new_city.id
        new_city = deepcopy(city)
        new_city.id = id
        new_city.weather = weather
        city.delete()
        new_city.save()

