from django import forms
from .models import Aluno, Professor, Disciplina, Turma

# ------------------------------------------------------------
# Formulário Aluno
# ------------------------------------------------------------
class AlunoForm(forms.ModelForm):
    # Campo de data de nascimento com formato customizado
    data_nascimento = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/yyyy'}),
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],  # Permitir diferentes formatos de data
    )
    
    # Campos de e-mail e telefone do responsável (opcionais)
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
        fields = '__all__'  # Inclui todos os campos do modelo Aluno


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