from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm
from .models import Profile
from django.contrib.auth.models import User
from weather_app.forms import CityForm

# Email
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_token


def index(request, warning_message=''):
    return render(request, 'weather_in_city.html', {'user': request.user,
                                                    'warning_message': warning_message,
                                                    'form': CityForm(),
                                                    'info': {'available': False}
                                                    })


def login(request):
    return render(request, 'log_in.html', {'user': request.user})


def confirm(request, id, token):

    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)

    form = CityForm()

    if profile.token == token:
        profile.activated = True
        profile.save()
        message = 'Your registration is now complete, ' + user.username + '!'

    else:
        message = 'Invalid token.'

    return render(
        request,
        'weather_in_city.html',
        {
            'user': request.user,
            'warning_message': message,
            'form': form,
            'info': {'available': False}
        }
    )


def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(
            request,
            'sign_up.html',
            {
                'form': form,
                'user': request.user
            }
        )

    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user, token=generate_token())
            profile.save()

            # Email
            subject = 'Weather by asenya_rb'
            URL = '127.0.0.1:8000/account/confirm/'
            link = URL + str(user.id) + '/' + profile.token
            message = 'Hello, ' + user.first_name + '!  Thanks for registration in weather_app ' \
                      'under the username ' + user.username + '.\nPlease, follow' \
                      ' this link to proceed: \n' + link
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, 'dimoniss00@gmail.com']
            send_mail(subject, message, from_email, to_list, fail_silently=False)

            message = 'Thank you for registration! We have sent a confirmation link to your email.'

            return render(
                request,
                'weather_in_city.html',
                {
                    'user': request.user,
                    'warning_message': message,
                    'form': CityForm(),
                    'info': {'available': False}
                }
            )
        else:
            print(form.errors)
            return render(
                request,
                'sign_up.html',
                {
                    'form': form,
                    'user': request.user
                }
            )

