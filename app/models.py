from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=45, verbose_name="Nome do Usuario")
    sobrenome = models.CharField(max_length=45, verbose_name="Sobrenome do Usuario")
    data_nasc = models.DateField(verbose_name="Data de Nascimento")
    sexo = models.CharField(max_length=20, verbose_name="Sexo")
    peso = models.FloatField(verbose_name="Peso")
    altura = models.FloatField(verbose_name="Altura")
    email = models.CharField(max_length=100, verbose_name="Email")
    senha = models.CharField(max_length=45, verbose_name="Senha")
    imagem_perfil = models.CharField(max_length=1000, verbose_name="Link da Imagem")


    def __str__(self):
        return f"{self.nome}, {self.sobrenome}, {self.data_nasc}, {self.sexo}, {self.peso}, {self.altura}, {self.email}, {self.senha}, {self.imagem_perfil}"
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Equipamento(models.Model):
    nome_equipamento = models.CharField(max_length=45, verbose_name="Nome do Equipamento")
    peso_equipamento = models.FloatField(verbose_name="Peso do Equipamento")

    def __str__(self):
        return f"{self.nome_equipamento}, {self.peso_equipamento}"
    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

class FichaTreino(models.Model):
    nome_ficha_treino = models.CharField(max_length=100, verbose_name="Nome da Ficha de Treino")
 

    def __str__(self):
        return f"{self.nome_ficha_treino}"
    class Meta:
        verbose_name = "Ficha de Treino"
        verbose_name_plural = "Fichas de Treino"

class Exercicio(models.Model):
    nome_exercicio = models.CharField(max_length=45, verbose_name="Nome do exercicio")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, verbose_name="Equipamento")
    repeticoes = models.IntegerField(verbose_name="Repeticoes")
    peso_exercicio = models.FloatField(verbose_name="Peso do Exercicio")
    series = models.IntegerField(verbose_name="Series")
    descanso = models.IntegerField(verbose_name="Descanso")
    ficha = models.ForeignKey(FichaTreino, on_delete=models.CASCADE, verbose_name="Ficha Treino")

    def __str__(self):
        return f"{self.nome_exercicio}, {self.equipamento}, {self.repeticoes}, {self.peso_exercicio}, {self.series}, {self.descanso}"
    class Meta:
        verbose_name = "Exercicio"
        verbose_name_plural = "Exercicios"

class Interacao(models.Model):  
    nome_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Nome do Usuario")
    texto = models.CharField(max_length=500, verbose_name="Texto")
    data_comentario = models.DateField(auto_now_add=True, verbose_name="Data do Comentario")
    ficha_treino = models.ForeignKey(FichaTreino, on_delete=models.CASCADE, verbose_name="Ficha de Treino")
    nota = models.IntegerField(verbose_name="Nota", default=0)

    def __str__(self):
        return f"{self.nome_usuario}, {self.texto}, {self.data_comentario}, {self.ficha_treino}, {self.nota}"
    
    class Meta:
        verbose_name = "Interacao"
        verbose_name_plural = "Interacoes"

class Treino(models.Model):
    nome_treino = models.ForeignKey(FichaTreino, on_delete=models.CASCADE, verbose_name="Nome do Treino")
    data_treino = models.DateField(verbose_name="Data do Treino")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    duracao = models.IntegerField(verbose_name="Duracao")

    def __str__(self):
        return f"{self.nome_treino}, {self.data_treino}, {self.usuario}, {self.duracao}"
    class Meta:
        verbose_name = "Treino"
        verbose_name_plural = "Treinos"

class UsuarioTreino(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios_realizados')  
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  
    nome_treino = models.CharField(max_length=255)
    data_treino = models.DateTimeField(default=timezone.now)
    nome_exercicio = models.CharField(max_length=255)
    peso_exercicio = models.FloatField(null=True, blank=True)
    repeticoes = models.IntegerField(null=True, blank=True)
    series = models.IntegerField(null=True, blank=True)
    descanso = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.nome_treino} - {self.nome_exercicio} - {self.data_treino}"

    class Meta:
        verbose_name = "Treino do Usuário"
        verbose_name_plural = "Treinos dos Usuários"

