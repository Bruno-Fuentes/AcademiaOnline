from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    def post(self, request):
        pass
    
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    def post(self, request):
        pass

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

class interacaoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'interacao.html')
    def post(self, request):
        pass
