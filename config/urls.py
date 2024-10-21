"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', IndexView.as_view(), name='index'),
    path('login.html', LoginView.as_view(), name='login'),
    path('perfil.html', PerfilView.as_view(), name='perfil'),
    path('treinosprontos.html', TreinosProntosView.as_view(), name='treinosprontos'),
    path('treinar.html', TreinarView.as_view(), name='treinar'),
    path('get_exercicios/<int:ficha_id>/', GetExerciciosView.as_view(), name='get_exercicios'),
    path('interacao.html', InteracaoView.as_view(), name='interacao'),
    path('editar_interacao/<int:pk>/', EditarInteracaoView.as_view(), name='editar_interacao'),
    path('interacao/excluir/<int:pk>/', ExcluirInteracaoView.as_view(), name='excluir_interacao'),
    path('exibirtreino.html', ExibirView.as_view(), name='exibirtreino'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('cadastro.html', CadastroView.as_view(), name='cadastro'),
]
