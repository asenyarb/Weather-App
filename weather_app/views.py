from django.shortcuts import render
import requests

# Create your views here.


def index(request):
    appid = 'd5690ce2c8cf4f332eb7788636e9bc69'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    cityname = 'London'
    response = requests.get(url.format(cityname)).json()
    dict = {
        'city_name': response['name'],
        'temp': response['main']['temp'],
        'temp_min': response['main']['temp_min'],
        'temp_max': response['main']['temp_max'],
        'humidity': response['main']['humidity'],
        'weather': response['weather'][0]['main'],
        'icon_id':response['weather'][0]['icon'],
    }
    return render(request, 'index.html', {'info': dict})