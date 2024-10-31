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
from .models import FichaTreino, Exercicio, Treino
from .forms import EditarInteracaoForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class IndexView(View):
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
    
class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'password_reset_form.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        sobrenome = request.POST.get('sobrenome')
        nova_senha = request.POST.get('nova_senha')

        try:
            user = User.objects.get(email=email)
            if user.last_name == sobrenome:
                user.set_password(nova_senha)
                user.save()
                messages.success(request, 'Senha redefinida com sucesso!')
                return redirect('login') 
            else:
                messages.error(request, 'Sobrenome incorreto.')
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

        return render(request, 'password_reset_form.html')

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
    template_name = 'perfil.html'
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
        
    def post(self, request, *args, **kwargs):
        if 'delete' in kwargs:  # Processa exclusão do perfil
            return self.delete(request)
        
        usuario_logado = self.get_usuario_logado(request)
        email = request.POST.get('email')
        
        if Usuario.objects.exclude(id=usuario_logado.id).filter(email=email).exists():
            messages.error(request, 'Já existe um usuário com este email.')
            return redirect('perfil')

        # Atualiza dados do usuário
        usuario_logado.nome = request.POST.get('nome')
        usuario_logado.sobrenome = request.POST.get('sobrenome')
        usuario_logado.email = email
        usuario_logado.senha = request.POST.get('senha')
        usuario_logado.data_nasc = request.POST.get('data_nasc')
        usuario_logado.sexo = request.POST.get('sexo')
        usuario_logado.peso = request.POST.get('peso')
        usuario_logado.altura = request.POST.get('altura')
        usuario_logado.imagem_perfil = request.POST.get('imagem_perfil')

        usuario_logado.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')

    def delete(self, request, *args, **kwargs):
        usuario_logado = self.get_usuario_logado(request)
        
        if usuario_logado:
            usuario_logado.delete()
            logout(request)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=400)

    def get_usuario_logado(self, request):
        return Usuario.objects.filter(email=request.user.username).first()

    def get_context(self, usuario):
        return {
            'nome': usuario.nome,
            'sobrenome': usuario.sobrenome,
            'email': usuario.email,
            'senha': usuario.senha,
            'data_nasc': usuario.data_nasc,
            'sexo': usuario.sexo,
            'peso': usuario.peso,
            'altura': usuario.altura,
            'imagem_perfil': usuario.imagem_perfil,
        }

class DeletePerfilView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        usuario_logado = Usuario.objects.filter(email=request.user.username).first()
        
        if usuario_logado:
            usuario_logado.delete()
            logout(request)
            messages.success(request, 'Perfil excluído com sucesso!')
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=400)

class TreinosProntosView(View):
    def get(self, request, *args, **kwargs):
        fichas = FichaTreino.objects.prefetch_related('exercicio_set').all()
        return render(request, 'treinosprontos.html', {'fichas': fichas})
    def post(self, request):
        pass

class InteracaoView(View):
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
            return redirect('interacao') 
        interacoes = Interacao.objects.all().order_by('-data_comentario')
        lista = [1, 2, 3, 4, 5]
        return render(request, 'interacao.html', {'interacoes': interacoes, 'lista': lista, 'form': form})

class EditarInteracaoView(UpdateView):
    model = Interacao
    form_class = EditarInteracaoForm
    template_name = 'editar_interacao.html'

    def get_success_url(self):
        return reverse_lazy('interacao')
    
    def form_valid(self, form):
        form.instance.ficha_treino = self.get_object().ficha_treino
        return super().form_valid(form)

class ExcluirInteracaoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        interacao = Interacao.objects.get(pk=pk)
        interacao.delete()
        return redirect('interacao')
    
class TreinarView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        fichas = FichaTreino.objects.all()
        exercicios = Exercicio.objects.all()
        return render(request, 'treinar.html', {'fichas': fichas, 'exercicios': exercicios})

    def post(self, request, *args, **kwargs):
        ficha_id = request.POST.get('ficha_treino') 
        ficha_treino = get_object_or_404(FichaTreino, id=ficha_id)
        usuario = get_object_or_404(Usuario, email=request.user.email)

        duracao = request.POST.get('duracao')
        if not duracao:
            messages.error(request, "Por favor, insira a duração do treino.")
            return redirect('treinar')   

        try:    
            with transaction.atomic():
                 treino_clonado = Treino.objects.create(
                    nome_treino=ficha_treino,
                    data_treino=timezone.now(),
                    usuario=usuario,
                    duracao=int(duracao)
                )

            for exercicio in Exercicio.objects.filter(ficha=ficha_treino):
                    peso_exercicio = request.POST.get(f'peso_{exercicio.id}', exercicio.peso_exercicio)
                    repeticoes = request.POST.get(f'repeticoes_{exercicio.id}', exercicio.repeticoes)
                    series = request.POST.get(f'series_{exercicio.id}', exercicio.series)
                    descanso = request.POST.get(f'descanso_{exercicio.id}', exercicio.descanso)

                    UsuarioTreino.objects.create(
                        usuario=usuario,
                        treino=treino_clonado,
                        nome_treino=ficha_treino.nome_ficha_treino,
                        data_treino=timezone.now(),
                        nome_exercicio=exercicio.nome_exercicio,
                        peso_exercicio=float(peso_exercicio) if peso_exercicio else exercicio.peso_exercicio,
                        repeticoes=int(repeticoes) if repeticoes else exercicio.repeticoes,
                        series=int(series) if series else exercicio.series,
                        descanso=int(descanso) if descanso else exercicio.descanso,
                    )
            messages.success(request, "Treino salvo com sucesso!")
            return redirect('index')
        
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return redirect('treinar')

class GetExerciciosView(View):
    def get(self, request, ficha_id, *args, **kwargs):
        exercicios = Exercicio.objects.filter(ficha_id=ficha_id)
        data = {
            'exercicios': [
                {
                    'id': exercicio.id,
                    'nome_exercicio': exercicio.nome_exercicio,
                    'repeticoes': exercicio.repeticoes,
                    'peso_exercicio': exercicio.peso_exercicio,
                    'series': exercicio.series,
                    'descanso': exercicio.descanso,
                }
                for exercicio in exercicios
            ]
        }
        return JsonResponse(data)
    
class ExibirView(View):
    def get(self, request, *args, **kwargs):
        usuario_logado = None
        for usuario in Usuario.objects.all():
            if usuario.email == request.user.username:
                usuario_logado = usuario
                break  

        if usuario_logado:  
            usuario = Usuario.objects.get(email=request.user.email)
            treinos = Treino.objects.filter(usuario=usuario)
            return render(request, 'exibirtreino.html', {
                'nome': usuario_logado.nome,
                'treinos': treinos
            })
        else:
            return render(request, 'exibirtreino.html', {
                'error': 'Perfil não encontrado.'
            })
    def post(self, request):
        pass