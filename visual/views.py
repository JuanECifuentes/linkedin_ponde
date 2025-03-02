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
from .bots import computrabajo,elempleo 

# Create your views here.
User = get_user_model()

class LoginUsuario(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True
    success_url = '/page/'

    def form_invalid(self, form):

        try:
            self.usuario = User.objects.get(username=self.request.POST['username'])
        except User.DoesNotExist:
            return super().form_invalid(form)

        return super().form_invalid(form)

    def form_valid(self, form):
        try:
            self.usuario = form.get_user()
        except Exception:
            return super().form_invalid(form)

        login(self.request, self.usuario)

        next_url = self.request.GET.get('next', None)

        if not next_url:
            next_url = self.success_url

        return redirect(next_url)

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        return self.success_url


class ButtonsView(LoginRequiredMixin,  generic.TemplateView):

    template_name = 'pages/page.html'

    def post(self, request, *args, **kwargs):
        accion = request.POST.get('accion')
        
        if 'iniciar_' in accion:
            print('accion',accion)
            bot = accion.split('_')[1]
            return self.ejecutar_inicio(request,bot)
        
        elif 'detener_' in accion:
            print('accion',accion)
            bot = accion.split('_')[1]
            return self.ejecutar_detener(request,bot)
        
        else:
            print('else accion',accion)
        
    def ejecutar_inicio(self, request, bot):
        if 'computrabajo' in bot:
            computrabajo.computrabajo_source(cantidad_ofertas=10)
        if 'elempleo' in bot:
            elempleo.elempleo_source(cantidad_ofertas=10)

        print(f"Se Inicio {bot}")
        return render(request, self.template_name)

    def ejecutar_detener(self, request, bot):
        print(f"Se Detuvo {bot}")
        return render(request, self.template_name)
class DashBoard(LoginRequiredMixin,  generic.TemplateView):

    template_name = 'pages/index.html'

def obtener_datos(request):
    datos = Ofertas.objects.all().values()  # Ajusta la consulta según tus necesidades
    return JsonResponse({'datos': list(datos)})  # Convertimos el queryset a lista para poderlo enviar

def user_logout_view(request):
  logout(request)
  return redirect('/accounts/login/')