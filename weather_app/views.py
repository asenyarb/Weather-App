from django.shortcuts import render
import requests
from .models import City
from accounts.models import Profile
from django.contrib.auth.models import User
from .forms import CityForm
from .utils import utc_to_local_time, create_warning_message
from django.shortcuts import redirect

# Create your views here.


def weather_in_city(request):
    if request.user.is_anonymous:
        activated = True
    else:
        activated = Profile.objects.get(user=request.user).activated
    warning_message = create_warning_message(request.user)
    if request.method == 'POST':
        city_info = {}
        form = CityForm(request.POST)
        city_message = ""
        if not form.is_valid():
            city_message = r"The city wasn't saved because the form isn't valid!"
        else:
            model = form.save(commit=False)
            if model.country_code:
                country_code = ',' + model.country_code + '&units=metric&appid='
            else:
                country_code = '&units=metric&appid='
            app_id = 'd5690ce2c8cf4f332eb7788636e9bc69'
            url = 'https://api.openweathermap.org/data/2.5/weather?q=' + model.city_name + country_code + app_id
            if requests.get(url).json()['cod'] == '404':  # Request error
                city_message = r"The city wasn't found!"
            else:
                response = requests.get(url).json()
                city_info = {
                    'available': True,
                    'city_name': response['name'],
                    'country': response['sys']['country'],
                    'temp': response['main']['temp'],
                    'temp_min': response['main']['temp_min'],
                    'temp_max': response['main']['temp_max'],
                    'humidity': response['main']['humidity'],
                    'pressure': response['main']['pressure'],
                    'description': response['weather'][0]['description'],
                    'icon_id': response['weather'][0]['icon'],
                    'wind': {
                        'speed': response['wind']['speed'],
                    },
                    'sunrise': utc_to_local_time(lng=response['coord']['lon'], lat=response['coord']['lat'], unix_time=response['sys']['sunrise'])[12:17],
                    'sunset': utc_to_local_time(lng=response['coord']['lon'], lat=response['coord']['lat'], unix_time=response['sys']['sunset'])[12:17],
                }
        form = CityForm()
        return render(
                request,
                'weather_in_city.html',
                {
                    'info': city_info,
                    'form': form,
                    'user': request.user,
                    'profile_activated': activated,
                    'city_message': city_message,
                    'warning_message': warning_message,
                }
            )
    if request.method == "GET":
        city_info = {'available': False}
        form = CityForm()
        return render(
            request,
            'weather_in_city.html',
            {
                'info': city_info,
                'form': form,
                'user': request.user,
                'profile_activated': activated,
                'warning_message': warning_message
            }
        )


def city_list(request, id):
    app_id = 'd5690ce2c8cf4f332eb7788636e9bc69'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

    user = User.objects.get(id=id)
    current_profile = Profile.objects.get_or_create(user=user)[0]   # User is authorised

    city_message = ""
    if request.method == 'POST':
        if request.POST.get("city_name"):
            # POST message from add-city form
            form = CityForm(request.POST)
            model = form.save(commit=False)  # Save form into temporary model
            if not form.is_valid():
                city_message = r"The city wasn't saved because the form isn't valid!"
            elif current_profile.cities.all().count() > 5:
                city_message = r"Too many cities in list! Delete some of to continue."
            elif current_profile.cities.filter(city_name=model.city_name).count():  # Check if city already exists in profile cities list
                city_message = r"The city is already in list!"
            elif requests.get(url.format(model.city_name)).json()['cod'] == '404':  # Request error
                city_message = r"The city wasn't found!"
            else:
                model.profile = current_profile
                model.save()
        else:
            # POST message from delete button
            string = 'delete_{}'
            for city in current_profile.cities.all():
                if string.format(city.city_name) in request.POST:  # Searching for button name
                    City.objects.get(city_name=city.city_name, profile=current_profile).delete()
    form = CityForm()
    cities = current_profile.cities.all()
    info = []
    for city in cities:
        response = requests.get(url.format(city.city_name)).json()
        city_info = {
            'city_name': response['name'],
            'country': response['sys']['country'],
            'temp': response['main']['temp'],
            'temp_min': response['main']['temp_min'],
            'temp_max': response['main']['temp_max'],
            'humidity': response['main']['humidity'],
            'weather': response['weather'][0]['main'],
            'icon_id': response['weather'][0]['icon'],
        }
        info.append(city_info)
    result = render(
        request,
        'city_list.html',
        {
            'all_info': info,
            'form': form,
            'user': request.user,
            'city_message': city_message,
        }
    )
    return result
