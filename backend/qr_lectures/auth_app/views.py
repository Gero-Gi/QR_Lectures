from django.http import response
from django.shortcuts import render
from django.urls.base import set_urlconf
from django.views.generic import FormView
from django.contrib.auth.views import LoginView as LoginBase
from django.contrib.auth.views import LogoutView as LogoutBase
from django.urls import reverse


class LoginView(LoginBase):
    template_name = 'auth_app/login_view.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous and request.user.is_authenticated:
            return response.HttpResponseRedirect(reverse('dashboard'))
        else:
            return super().get(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse('dashboard')

    def get_success_url(self):
        return reverse('dashboard')


class LogoutView(LogoutBase):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return response.HttpResponseRedirect(reverse('login_view'))

  

    def get_success_url(self):
        return reverse('login_view')

    def get_redirect_url(self):
        return reverse('login_view')
