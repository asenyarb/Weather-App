from django.forms import ModelForm, TextInput
from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['city_name']
        widgets = {'city_name': TextInput(attrs={'class': "form-control", 'name': "city", 'id': "city", 'placeholder': "Enter the city"})}