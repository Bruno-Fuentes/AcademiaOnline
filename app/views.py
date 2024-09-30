from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import logout
from .models import Usuario


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

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            if user.is_superuser:
                 return redirect('index')
            else:
                 return redirect(reverse('index'))
        else:
            messages.error(request, 'Email ou senha inválidos')
            return render(request, 'login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')   


class CadastroView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cadastro.html')

    def post(self, request, *args, **kwargs):
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        data_nasc = request.POST.get('data_nasc')
        sexo = request.POST.get('sexo')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_confirmacao = request.POST.get('senha_confirmacao')
        imagem_perfil = request.POST.get('imagem_perfil')

        if not nome or not sobrenome or not data_nasc or not sexo or not peso or not altura or not email or not senha or not senha_confirmacao:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'cadastro.html')

        if senha != senha_confirmacao:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'O email já está cadastrado.')
            return render(request, 'cadastro.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome,
            last_name=sobrenome
        )
        
        login(request, user)

        return redirect(reverse('index'))
    
class PerfilView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        usuario = get_object_or_404(Usuario, email=request.user.email)
        return render(request, 'perfil.html', {
            'nome': usuario.nome,
            'sobrenome': usuario.sobrenome,
            'email': usuario.email,
            'data_nasc': usuario.data_nasc,
            'sexo': usuario.sexo,
            'peso': usuario.peso,
            'altura': usuario.altura,
            'imagem_perfil': usuario.imagem_perfil,
        })
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
