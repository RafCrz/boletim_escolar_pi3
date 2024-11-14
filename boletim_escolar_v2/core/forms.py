#boletim_escolar_v2/core/forms.py

from django import forms
from .models import Aluno, Professor, Disciplina, Turma, Secretaria


# ------------------------------------------------------------
# Formulário Secretaria
# ------------------------------------------------------------
class SecretariaForm(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = ['nome', 'email', 'telefone']


# ------------------------------------------------------------
# Formulário Aluno
# ------------------------------------------------------------
class AlunoForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/yyyy'}),
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
    )
    email_responsavel = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'exemplo@dominio.com'})
    )
    telefone_responsavel = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(xx) xxxx-xxxx'})
    )

    class Meta:
        model = Aluno
        exclude = ['user']  # Exclui o campo user do formulário


# ------------------------------------------------------------
# Formulário Turma
# ------------------------------------------------------------
class TurmaForm(forms.ModelForm):
    # Campo para selecionar múltiplos alunos (opcional)
    alunos = forms.ModelMultipleChoiceField(
        queryset=Aluno.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Não é mais obrigatório
    )
    
    # Campo para selecionar múltiplos professores (opcional)
    professores = forms.ModelMultipleChoiceField(
        queryset=Professor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Não é mais obrigatório
    )

    class Meta:
        model = Turma
        fields = ['ano', 'classe', 'alunos', 'professores']  # Campos para criação/edição da turma


# ------------------------------------------------------------
# Formulário Professor
# ------------------------------------------------------------
class ProfessorForm(forms.ModelForm):
    
    # Campo para selecionar múltiplas disciplinas (opcional)
    disciplinas = forms.ModelMultipleChoiceField(
        queryset=Disciplina.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # O campo é opcional
    )

    class Meta:
        model = Professor
        fields = ['nome', 'email', 'telefone', 'disciplinas']  # Inclui os novos campos e disciplinas


# ------------------------------------------------------------
# Formulário Disciplina
# ------------------------------------------------------------
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome']  # Apenas o nome da disciplina