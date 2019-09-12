from rest_framework import serializers
from .models import Weather, City
from weather_app.models import Profile
from accounts.serializers import UserSerializer, WeatherSerializer


class CustomProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user']


class CitySerializer(serializers.ModelSerializer):
    weather = WeatherSerializer()
    profile = CustomProfileSerializer()

    class Meta:
        model = City
        fields = ['url', 'city_name', 'country_code', 'weather', 'profile']

