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
from . import selectors as sel

# Create your views here.
User = get_user_model()

class LoginUsuario(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True
    success_url = '/page/dashboard/'

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Nombre de la URL de dashboard
    return redirect('login1')  # Nombre de la URL de login

def user_logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class DashBoard(LoginRequiredMixin,  generic.TemplateView):

    template_name = 'pages/index.html'

class PonderadoView(LoginRequiredMixin,  generic.TemplateView):
    template_name = 'pages/ponderado.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'ofertas': sel.get_all_ofertas(),
        })
        return super().get_context_data(**kwargs)