from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    activated = models.BooleanField(default=False)
    token = models.CharField(primary_key=True, unique=True, max_length=30)

    def __str__(self):
        return str(self.user) + ' - ' + ('Activated' if self.activated else 'Not activated')