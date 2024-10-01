from django import forms
from .models import Interacao

class InteracaoForm(forms.ModelForm):
    class Meta:
        model = Interacao
        fields = ['ficha_treino', 'texto', 'nota']
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 5}),
        }
