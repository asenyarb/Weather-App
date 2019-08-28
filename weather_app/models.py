from django.db import models
from accounts.models import Profile


# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2, blank=True)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name
