from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_in_city, name='index'),
    path('city-list/<int:id>', views.city_list, name='city-list')
]
