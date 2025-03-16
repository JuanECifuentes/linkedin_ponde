from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.conf import settings
from .models import *

# Create your views here.
User = get_user_model()

class LoginUsuario(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True
    success_url = '/page/dashboard/'

class DashBoard(LoginRequiredMixin,  generic.TemplateView):

    template_name = 'pages/index.html'

def user_logout_view(request):
  logout(request)
  return redirect('/accounts/login/')