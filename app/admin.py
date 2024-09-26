from django.contrib import admin
from .models import *
from django.contrib import admin

class ExercicioInline(admin.TabularInline):
    model = Exercicio
    extra = 12

class FichaTreinoAdmin(admin.ModelAdmin):
    inlines = [ExercicioInline]

admin.site.register(Usuario)
admin.site.register(Interacao)
admin.site.register(Equipamento)
admin.site.register(Exercicio)
admin.site.register(FichaTreino, FichaTreinoAdmin)
admin.site.register(Treino)

