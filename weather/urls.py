"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from rest_framework import routers
from accounts.views import ProfileViewSet
from weather_app.views import CityViewSet, AddCityApi, DeleteCityApi, ApiHelp

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'cities', CityViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/add-city/', AddCityApi.as_view(), name='profile-delete'),
    path('api/delete-city/', DeleteCityApi.as_view(), name='profile-delete'),
    path('api/help', ApiHelp.as_view(), name='api-help'),
    path('admin/', admin.site.urls),
    path('', include('weather_app.urls')),
    path('', include('accounts.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
]
