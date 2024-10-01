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
from .models import Interacao
from .forms import InteracaoForm
from django.http import HttpResponseForbidden


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
        usuario = Usuario.objects.create(
            nome=nome,
            sobrenome=sobrenome,
            data_nasc=data_nasc,
            sexo=sexo,
            peso=peso,
            altura=altura,
            email=email,
            senha=senha, 
            imagem_perfil=imagem_perfil
        )

        login(request, user)

        return redirect(reverse('index'))
    
class PerfilView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        
        usuario_logado = None
        for usuario in Usuario.objects.all():
            if usuario.email == request.user.username:
                usuario_logado = usuario
                break  

        if usuario_logado:  
            return render(request, 'perfil.html', {
                'nome': usuario_logado.nome,
                'sobrenome': usuario_logado.sobrenome,
                'email': usuario_logado.email,
                'senha': usuario_logado.senha,  
                'data_nasc': usuario_logado.data_nasc,
                'sexo': usuario_logado.sexo,
                'peso': usuario_logado.peso,
                'altura': usuario_logado.altura,
                'imagem_perfil': usuario_logado.imagem_perfil,
            })
        else:
            return render(request, 'perfil.html', {
                'error': 'Perfil não encontrado.'
            })
    def post(self, request):
        pass

class TreinosProntosView(View):
    def get(self, request, *args, **kwargs):
        fichas = FichaTreino.objects.prefetch_related('exercicio_set').all()
        return render(request, 'treinosprontos.html', {'fichas': fichas})
    def post(self, request):
        pass

class TreinarView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'treinar.html')
    def post(self, request):
        pass

class InteracaoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        interacoes = Interacao.objects.all().order_by('-data_comentario')
        form = InteracaoForm()
        lista = [1,2,3,4,5]
        return render(request, 'interacao.html', {'interacoes': interacoes, 'lista': lista, 'form': form})

    def post(self, request, *args, **kwargs):
        form = InteracaoForm(request.POST)
        if form.is_valid():
            interacao = form.save(commit=False)
            interacao.nome_usuario = Usuario.objects.get(email=request.user.email)
            interacao.save()
            form.save()
            lista = [1,2,3,4,5]
            return redirect('interacao')
        interacoes = Interacao.objects.all().order_by('-data_comentario')
        return render(request, 'interacao.html', {'interacoes': interacoes, 'lista': lista, 'form': form})
    
class EditarInteracaoView(LoginRequiredMixin, View):
    model = Interacao
    fields = ['texto', 'nota']

    def dispatch(self, request, *args, **kwargs):
        interacao = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk):
        interacao = get_object_or_404(Interacao, pk=pk)
        form = InteracaoForm(instance=interacao)
        return render(request, 'editar_interacao.html', {'form': form, 'interacao': interacao})

    def post(self, request, pk):
        interacao = get_object_or_404(Interacao, pk=pk)
        form = InteracaoForm(request.POST, instance=interacao)
        if form.is_valid():
            form.save()
            return redirect('interacao')
        return render(request, 'editar_interacao.html', {'form': form, 'interacao': interacao})

class ExcluirInteracaoView(LoginRequiredMixin, View):
    def post(self, pk):
        interacao = Interacao.objects.get(pk=pk)
        interacao.delete()
        return redirect('interacao')

class VolumeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'volume.html')
    def post(self, request):
        pass
