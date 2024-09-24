from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import logout


class IndexView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    def post(self, request):
        pass
    
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('senha')

        # Autenticar o usuário pelo email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            if user.is_superuser:
                 return redirect('index') # Redireciona para a dashboard de admin se for superusuário
            else:
                 return redirect(reverse('index'))  # Redireciona para o dashboard de usuário comum
        else:
            messages.error(request, 'Email ou senha inválidos')
            return render(request, 'login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)  # Faz o logout do usuário
        return redirect('login')   

class PerfilView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'perfil.html')
    def post(self, request):
        pass

class TreinosProntosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'treinosprontos.html')
    def post(self, request):
        pass

class TreinarView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'treinar.html')
    def post(self, request):
        pass

class InteracaoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'interacao.html')
    def post(self, request):
        pass

class VolumeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'volume.html')
    def post(self, request):
        pass
