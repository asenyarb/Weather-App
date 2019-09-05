from django.urls import path
from . import views

urlpatterns = [
    path('', views.CityViewer.as_view(), name='index'),
    path('city-list/<int:id>', views.CityViewer.as_view(), name='city-list')
]
