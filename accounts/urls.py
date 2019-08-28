from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import LogInForm

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('account/confirm/<int:id>/<str:token>', views.confirm, name='confirm'),
    path('login/', auth_views.LoginView.as_view(template_name='log_in.html', authentication_form=LogInForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
