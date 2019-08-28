from django.forms import ModelForm, TextInput, CharField
from weather_app.models import City


class CityForm(ModelForm):
    city_name = CharField(max_length=50, widget=TextInput(attrs={
                'class': "form-control",
                'name': "city-name",
                'id': "city-name",
                'placeholder': "Enter the city",
                'focus': True,
            }))
    country_code = CharField(label=("Country code(optional)"), max_length=2, required=False, widget=TextInput(attrs={
                'class': "form-control",
                'name': "country-code",
                'id': "country-code",
                'placeholder': "Use ISO 3166-2 standart"
            }))

    class Meta:
        model = City
        fields = ['city_name',
                  'country_code'
                  ]