from django import forms
from .models import Interacao

class InteracaoForm(forms.ModelForm):
    class Meta:
        model = Interacao
        fields = ['ficha_treino', 'texto', 'nota']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 5}),
        }

class EditarInteracaoForm(forms.ModelForm):
    class Meta:
        model = Interacao
        fields = ['texto', 'nota']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 5}),
        }