from django.contrib.auth.models import User
from rest_framework import serializers
from weather_app.models import City,Weather
from accounts.models import Profile


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class CustomCitySerializer(serializers.ModelSerializer):
    weather = WeatherSerializer()

    class Meta:
        model = City
        fields = ['city_name', 'country_code', 'weather']


class ProfileSerializer(serializers.ModelSerializer):
    cities = CustomCitySerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['url', 'user', 'activated', 'token', 'cities']
