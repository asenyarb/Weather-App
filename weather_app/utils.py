import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder
from accounts.models import Profile
from django.contrib.auth.models import User


def unix_time_to_local(coord, unix_time):
    # Timezone defining
    tf = TimezoneFinder()
    # Unix to UTC
    dt_object = datetime.fromtimestamp(unix_time)
    timezone = pytz.timezone(tf.timezone_at(lat=coord['lat'], lng=coord['lon']))
    # UTC to local time
    result = dt_object.replace(tzinfo=None).astimezone(timezone).strftime("%m/%d/%Y, %H:%M:%S")
    return result[12:17]


def create_warning_message(user: User):
    if user.is_anonymous:
        message = 'Log in for more features'
    else:
        profile = Profile.objects.get(user=user)
        if not profile.activated and not user.is_superuser:
            message = "Hello, " + user.username + "! Activate your profile to get access to your cities list"
        else:
            message = "Hello, " + user.username + "!"
    return message
