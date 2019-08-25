from django.contrib import admin
from django.contrib.auth.models import Group
from .models import City

# Register your models here.
admin.site.unregister(Group)
admin.site.register(City)