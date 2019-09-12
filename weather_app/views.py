# Django
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
import requests

from weather_app.models import City, Weather, update_weather_if_needed
from accounts.models import Profile
from weather_app.forms import CityForm
from weather_app.utils import create_warning_message

# Rest
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from weather_app.serializers import CitySerializer


# Create your views here.


class CityViewer(View):

    def get(self, request, id=0):
        warning_message = create_warning_message(request.user)
        form = CityForm()
        city_message = ""
        if id:      # city-list.html
            user = User.objects.get(id=id)
            current_profile = Profile.objects.get_or_create(user=user)[0]  # User is authorised
            for city in current_profile.cities.all():
                update_weather_if_needed(city)
            cities_list = current_profile.cities.all()  # Get updated list of cities
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
                if ('delete_' + city.city_name + city.country_code) in request.POST:  # Searching for button name
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
        weather.save(response=response)
        city.country_code = response['sys']['country']
        if id:
            current_profile = Profile.objects.get(user=request.user)
            if current_profile.cities.all().count() > 5:
                city_message = r"Too many cities in list! Delete some of to continue."
            # Check if city already exists in profile cities list
            elif current_profile.cities.filter(city_name=city.city_name, country_code=city.country_code).count():
                city_message = r"The city is already in list!"
            else:
                city_message = ""
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


class CityViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def list(self, request, *args, **kwargs):
        for city in City.objects.all():
            update_weather_if_needed(city)
        return super(CityViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        for city in City.objects.all():
            update_weather_if_needed(city)
        return super(CityViewSet, self).retrieve(request, *args, **kwargs)


class AddCityApi(APIView):

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'message': "Profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        app_id = '&units=metric&appid=d5690ce2c8cf4f332eb7788636e9bc69'
        city_name = request.GET.get('city_name', None)
        country_code = request.GET.get('code', None)
        if not city_name:
            return Response({'message': "You should enter city_name!"}, status.HTTP_400_BAD_REQUEST)
        if country_code:
            app_id = ',' + country_code + app_id
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}' + app_id
        response = requests.get(url.format(city_name)).json()
        if response['cod'] == '404':  # Request error
            return Response({'message': "The city wasn't found!"}, status.HTTP_404_NOT_FOUND)
        if profile.cities.filter(city_name=city_name).count():
            return Response({'message': "The city wasn't found!"}, status.HTTP_400_BAD_REQUEST)
        weather = Weather()
        weather.save(response=response)
        country_code = response['sys']['country']
        city = City(profile=profile, city_name=city_name, country_code=country_code, weather=weather)
        city.save()

        return Response({'message': "Successfully added"}, status.HTTP_201_CREATED)


class DeleteCityApi(APIView):

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'message': "Profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        city_name = request.GET.get('city_name', None)
        country_code = request.GET.get('code', None)
        if not city_name:
            return Response({'message': "You should enter city_name!"}, status.HTTP_400_BAD_REQUEST)
        try:
            if country_code:
                city = profile.cities.get(city_name=city_name, country_code=country_code)
                city.delete()
            else:
                cities = profile.cities.filter(city_name=city_name)
                if not cities:
                    raise Exception("bad city_name")
                for city in cities:
                    city.delete()
        except:
            return Response({'message': "Profile doesn't have a city with that name!"}, status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Deleted successfully'}, status.HTTP_200_OK)


class ApiHelp(View):

    def get(self, request):
        return render(request, 'api_help.html')
