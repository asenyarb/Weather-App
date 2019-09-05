from django.shortcuts import render
from django.template import RequestContext
from django.views import View
import requests
from .models import City, Weather
from accounts.models import Profile
from django.contrib.auth.models import User
from .forms import CityForm
from .utils import response_to_map, create_warning_message


# Create your views here.


class CityViewer(View):

    def get(self, request, id=0):
        warning_message = create_warning_message(request.user)
        form = CityForm()
        city_message = ""
        if id:      # city-list.html
            user = User.objects.get(id=id)
            current_profile = Profile.objects.get_or_create(user=user)[0]  # User is authorised
            cities_list = current_profile.cities.all()
            available = True if cities_list.count() else False    # False if empty
            info = {
                'available': available,
                'cities_list': cities_list,
            }
            template_name = 'city_list.html'

        else:       # weather_info.html
            city = City()
            info = {
                'available': False,
                'city': city,
            }
            template_name = 'weather_in_city.html'
        result = render(
            request,
            template_name,
            {
                'info': info,
                'form': form,
                'user': request.user,
                'city_message': city_message,
                'warning_message': warning_message,
            }
        )
        return result

    def post(self, request, id=0):
        app_id = '&units=metric&appid=d5690ce2c8cf4f332eb7788636e9bc69'
        template_name = "city_list.html" if id else "weather_in_city.html"
        city_message = ""
        warning_message = create_warning_message(request.user)

        if id and not request.POST.get("send"):     # Sent by delete button for city
            current_profile = Profile.objects.get(user=request.user)
            for city in current_profile.cities.all():
                if ('delete_' + city.city_name) in request.POST:  # Searching for button name
                    City.objects.get(city_name=city.city_name, country_code=city.country_code, profile=current_profile).delete()
            city_list = current_profile.cities.all()
            available = True if city_list.count() else False
            info = {
                'available': available,
                'cities_list': city_list,
            }
            form = CityForm()
            return render(request, template_name, {
                'info': info,
                'form': form,
                'user': request.user,
                'city_message': city_message,
                'warning_message': warning_message,
            })
        form = CityForm(request.POST)
        if not form.is_valid():
            city_message = r"The city wasn't accepted because the form isn't valid!"
            info = {
                'available': False
            }
            form = CityForm()
            return render(request, template_name, {
                'info': info,
                'form': form,
                'user': request.user,
                'city_message': city_message,
                'warning_message': warning_message,
            })
        city = form.save(commit=False)
        form = CityForm()
        if city.country_code:
            app_id = ',' + city.country_code + app_id
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}' + app_id
        response = requests.get(url.format(city.city_name)).json()
        if response['cod'] == '404':  # Request error
            city_message = r"The city wasn't found!"
            if id:
                current_profile = Profile.objects.get(user=request.user)
                cities = current_profile.cities.all()
                available = True if cities.count() else False
                info = {
                    'available': available,
                    'cities_list': cities,
                }
            else:
                info = {
                    'available': False
                }
            form = CityForm()
            return render(request, template_name, {
                'info': info,
                'form': form,
                'user': request.user,
                'city_message': city_message,
                'warning_message': warning_message,
            })
        weather = Weather()
        weather.save(weather_dict=response_to_map(response))
        city.country_code = response['sys']['country']
        if id:
            current_profile = Profile.objects.get(user=request.user)
            if current_profile.cities.all().count() > 5:
                city_message = r"Too many cities in list! Delete some of to continue."
            # Check if city already exists in profile cities list
            elif current_profile.cities.filter(city_name=city.city_name).count():
                city_message = r"The city is already in list!"
            else:
                city_message=""
                city.profile = current_profile
                city.weather = weather
                city.save()

            form = CityForm()
            cities = current_profile.cities.all()
            available = True if cities.count() else False
            info = {
                'available': available,
                'cities_list': cities,
            }
        else:
            template_name = "weather_in_city.html"
            city.weather = weather
            info = {
                'available': True,
                'city': city,
            }
        return render(request, template_name, {
                                            'info': info,
                                            'form': form,
                                            'user': request.user,
                                            'city_message': city_message,
                                            'warning_message': warning_message,
                                        }
               )
