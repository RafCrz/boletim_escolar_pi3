# core/forms.py

from django import forms
from .models import Aluno, Professor, Disciplina

class AlunoForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/yyyy'}),
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],  # Permitir diferentes formatos
    )
    email_responsavel = forms.EmailField(
        required=False,  # O campo é opcional
        widget=forms.EmailInput(attrs={'placeholder': 'exemplo@dominio.com'})
    )
    telefone_responsavel = forms.CharField(
        required=False,  # O campo é opcional
        widget=forms.TextInput(attrs={'placeholder': '(xx) xxxx-xxxx'})
    )

    class Meta:
        model = Aluno
        fields = '__all__'  # Inclui todos os campos, incluindo os novos

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'  # Inclui todos os campos do modelo Professor

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'  # Inclui todos os campos do modelo Disciplina
