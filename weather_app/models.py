from django.db import models
from accounts.models import Profile


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

    def save(self, weather_dict=None, *args, **kwargs):
        self.temp = weather_dict['temp']
        self.temp_min = weather_dict['temp_min']
        self.temp_max = weather_dict['temp_max']
        self.humidity = weather_dict['humidity']
        self.pressure = weather_dict['pressure']
        self.description = weather_dict['description']
        self.wind_speed = weather_dict['wind_speed']
        self.weather = weather_dict['weather']
        self.icon_id = weather_dict['icon_id']
        self.sunrise = weather_dict['sunrise']
        self.sunset = weather_dict['sunset']
        super(Weather, self).save(*args, *kwargs)

    class Meta:
        verbose_name = "Weather"

    def _str_(self):
        return "weather in " + self.city.city_name + self.city.country_code


class City(models.Model):
    city_name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2, blank=True)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='cities')
    weather = models.OneToOneField(Weather, null=True, on_delete=models.CASCADE, related_name="city")

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name
