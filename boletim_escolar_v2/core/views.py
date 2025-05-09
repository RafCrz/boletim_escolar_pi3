#boletim_escolar_v2/core/views.py

# ------------------------------------------------------------
# Importações
# ------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, Turma, Professor, Disciplina, Nota, Secretaria
from .forms import AlunoForm, TurmaForm, ProfessorForm, DisciplinaForm, SecretariaForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from boletim_escolar_v2.settings import YOUR_GOOGLE_CLIENT_ID

from django.http import HttpResponse

import matplotlib
matplotlib.use('Agg')  # Define o backend para evitar interface gráfica

import matplotlib.pyplot as plt
import pandas as pd
from django.db.models import Avg
from io import BytesIO

import json, time
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import redirect

# ------------------------------------------------------------
# Páginas Gerais (Index, Professor, Aluno, Secretaria)
# ------------------------------------------------------------

def index(request):
    return render(request, 'core/index.html')

def professor(request):
    return render(request, 'core/professor.html')

def aluno(request):
    return render(request, 'core/aluno.html')

def secretaria(request):
    return render(request, 'core/secretaria.html')

def faq(request):
    return render(request, 'core/faq.html')






def dashboard(request):
    aluno = request.user.aluno_profile
    notas = Nota.objects.filter(aluno=aluno)
    disciplinas = notas.values_list('disciplina__nome', flat=True).distinct()
    data = {'Bimestre': ['1º Bimestre', '2º Bimestre', '3º Bimestre', '4º Bimestre']}

    for disciplina in disciplinas:
        notas_disciplina = notas.filter(disciplina__nome=disciplina)
        data[disciplina] = [
            notas_disciplina.aggregate(Avg('nota_bimestre1'))['nota_bimestre1__avg'],
            notas_disciplina.aggregate(Avg('nota_bimestre2'))['nota_bimestre2__avg'],
            notas_disciplina.aggregate(Avg('nota_bimestre3'))['nota_bimestre3__avg'],
            notas_disciplina.aggregate(Avg('nota_bimestre4'))['nota_bimestre4__avg']
        ]

    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 5))

    for disciplina in disciplinas:
        plt.plot(df['Bimestre'], df[disciplina], marker='o', label=disciplina)

    plt.title('Desempenho por Bimestres')
    plt.xlabel('Bimestres')
    plt.ylabel('Notas')
    plt.legend()
    plt.grid(True)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')









# ------------------------------------------------------------
# Gestão de Secretaria
# ------------------------------------------------------------

class SecretariaLoginView(LoginView):
    template_name = 'core/login_secretaria.html'
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if hasattr(user, 'secretaria_profile'):
            login(self.request, user)
            return redirect('secretaria_home')
        else:
            messages.error(self.request, "Você não tem permissão para acessar esta página como secretaria.")
            return redirect('login_secretaria')

@login_required
def secretaria_home(request):
    secretaria = request.user.secretaria_profile
    return render(request, 'core/secretaria_home.html', {'secretaria': secretaria})


def secretaria_logout(request):
    logout(request)
    return redirect('login_secretaria')  # Redireciona para a página de login da secretaria

# ------------------------------------------------------------
# Gestão de Turmas
# ------------------------------------------------------------

# Gerenciar turmas (listar turmas)
def gerenciar_turmas(request):
    turmas = Turma.objects.all()
    return render(request, 'core/gerenciar_turmas.html', {'turmas': turmas})

# Consultar uma turma específica
def consultar_turma(request, turma_id):
    turma = Turma.objects.get(id=turma_id)
    return render(request, 'core/consultar_turma.html', {'turma': turma})

# Excluir uma turma
def excluir_turma(request, pk):
    turma = Turma.objects.get(pk=pk)
    turma.delete()
    return redirect('gerenciar_turmas')

# Criar nova turma
def criar_turma(request):
    alunos = Aluno.objects.all().order_by('nome')  # Busca todos os alunos
    professores = Professor.objects.all().order_by('nome')  # Busca todos os professores

    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            turma.alunos.set(request.POST.getlist('alunos'))
            turma.professores.set(request.POST.getlist('professores'))
            return redirect('gerenciar_turmas')
    else:
        form = TurmaForm()

    return render(request, 'core/criar_turma.html', {'form': form, 'alunos': alunos, 'professores': professores})


# Editar turma existente
def editar_turma(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    alunos = Aluno.objects.all()
    professores = Professor.objects.all()

    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_turmas')
    else:
        form = TurmaForm(instance=turma)

    return render(request, 'core/editar_turma.html', {
        'form': form,
        'alunos': alunos,
        'professores': professores,
        'turma': turma
    })


# ------------------------------------------------------------
# Gestão de Alunos
# ------------------------------------------------------------



def login_aluno(request):
    if request.method == 'POST':
        rm = request.POST['rm']
        password = request.POST['password']
        user = authenticate(request, username=rm, password=password)
        if user is not None:
            if hasattr(user, 'aluno_profile'):
                login(request, user)
                return redirect('aluno_home')
            else:
                messages.error(request, "Você não tem permissão para acessar esta página como aluno.")
        else:
            messages.error(request, "RM ou senha incorretos.")
    return render(request, 'core/login_aluno.html')










@login_required
def aluno_home(request):
    aluno = request.user.aluno_profile  # Acessa o perfil do aluno logado, assumindo que você tenha um perfil de aluno
    notas = Nota.objects.filter(aluno=aluno)  # Filtra as notas do aluno logado

    return render(request, 'core/aluno_home.html', {
        'notas': notas  # Passa as notas para o template
    })




















@login_required
def adicionar_notas(request, turma_id, disciplina_id):
    turma = get_object_or_404(Turma, id=turma_id)
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    # Ordena os alunos pelo nome em ordem alfabética
    alunos = turma.alunos.all().order_by('nome')
    
    if request.method == 'POST':
        for aluno in alunos:
            nota, created = Nota.objects.get_or_create(aluno=aluno, disciplina=disciplina)
            # Salva as notas e faltas de cada bimestre
            nota.nota_bimestre1 = float(request.POST.get(f'nota_bimestre1_{aluno.id}', 0))
            nota.faltas_bimestre1 = int(request.POST.get(f'faltas_bimestre1_{aluno.id}', 0))
            nota.nota_bimestre2 = float(request.POST.get(f'nota_bimestre2_{aluno.id}', 0))
            nota.faltas_bimestre2 = int(request.POST.get(f'faltas_bimestre2_{aluno.id}', 0))
            nota.nota_bimestre3 = float(request.POST.get(f'nota_bimestre3_{aluno.id}', 0))
            nota.faltas_bimestre3 = int(request.POST.get(f'faltas_bimestre3_{aluno.id}', 0))
            nota.nota_bimestre4 = float(request.POST.get(f'nota_bimestre4_{aluno.id}', 0))
            nota.faltas_bimestre4 = int(request.POST.get(f'faltas_bimestre4_{aluno.id}', 0))
            
            # Calcula a média final e atualiza o status
            nota.media_final = (nota.nota_bimestre1 + nota.nota_bimestre2 + nota.nota_bimestre3 + nota.nota_bimestre4) / 4
            nota.status_final = request.POST.get(f'status_final_{aluno.id}', 'P')
            
            nota.save()
        return redirect('adicionar_notas', turma_id=turma.id, disciplina_id=disciplina.id)
    
    # Carrega as notas existentes e informações dos alunos
    alunos_notas = [(aluno, Nota.objects.filter(aluno=aluno, disciplina=disciplina).first()) for aluno in alunos]
    
    return render(request, 'core/adicionar_notas.html', {
        'turma': turma,
        'disciplina': disciplina,
        'alunos_notas': alunos_notas,
        'status_choices': Nota.STATUS_CHOICES  # Passa as opções de status para o template
    })


# Gerenciar alunos (listar alunos)
def gerenciar_alunos(request):
    query = request.GET.get('q', '')
    alunos = Aluno.objects.all()

    if query:
        alunos = alunos.filter(nome__icontains=query)

    alunos = alunos.order_by('nome')
    return render(request, 'core/gerenciar_alunos.html', {'alunos': alunos, 'query': query})

# Editar aluno específico
def editar_aluno(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_alunos')
    else:
        form = AlunoForm(instance=aluno)

    return render(request, 'core/editar_aluno.html', {'form': form, 'aluno': aluno})

# Excluir aluno
def excluir_aluno(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)
    aluno.delete()
    return redirect('gerenciar_alunos')

# Consultar dados de um aluno
def consultar_aluno(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)
    return render(request, 'core/consultar_aluno.html', {'aluno': aluno})


# Função de logout do aluno
def aluno_logout(request):
    logout(request)
    return redirect('login_aluno')


# Cadastrar aluno

def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        user_form = UserCreationForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            aluno = form.save(commit=False)
            rm = form.cleaned_data['rm']
            username = rm
            print(f"RM: {rm}")
            print(f"Username: {username}")
            # Verificar se o username já existe
            if User.objects.filter(username=username).exists():
                messages.error(request, "O RM já está em uso. Por favor, escolha outro.")
                return render(request, 'core/cadastrar_aluno.html', {'form': form, 'user_form': user_form})
            user = user_form.save(commit=False)
            user.username = username
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            aluno.user = user
            aluno.save()
            print("Aluno cadastrado com sucesso!")
            return redirect('gerenciar_alunos')
        else:
            print(form.errors)
            print(user_form.errors)
    else:
        form = AlunoForm()
        user_form = UserCreationForm()
    return render(request, 'core/cadastrar_aluno.html', {'form': form, 'user_form': user_form})

# View para mudar a senha do aluno
class AlunoPasswordChangeView(PasswordChangeView):
    template_name = 'core/password_change.html'  # O template para a alteração de senha
    success_url = reverse_lazy('aluno_home')  # Redireciona para a página inicial do aluno após mudança de senha
    
# ------------------------------------------------------------
# Gestão de Professores
# ------------------------------------------------------------

# View para mudar a senha do professor
class ProfessorPasswordChangeView(PasswordChangeView):
    template_name = 'core/password_change.html'
    success_url = reverse_lazy('professor_home')  # Redireciona para a página inicial do professor após mudança de senha

    
class ProfessorLoginView(LoginView):
    template_name = 'core/login_professor.html'
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        # Verifica se o usuário tem o perfil de professor
        if hasattr(user, 'professor_profile'):
            login(self.request, user)
            return redirect('professor_home')
        else:
            messages.error(self.request, "Você não tem permissão para acessar esta página como professor.")
            return redirect('login_professor')

# Página inicial do professor após login
class ProfessorHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'core/professor_home.html'

    def test_func(self):
        return hasattr(self.request.user, 'professor_profile')

    def handle_no_permission(self):
        messages.error(self.request, "Acesso restrito a professores.")
        return redirect('login_professor')
    

    def get_context_data(self, **kwargs):
        professor = self.request.user.professor_profile
        turmas = professor.turmas.all()
        disciplinas = professor.disciplinas.all()
        context = super().get_context_data(**kwargs)
        context['turmas'] = turmas
        context['disciplinas'] = disciplinas
        return context


# Função de logout do professor
def professor_logout(request):
    logout(request)
    return redirect('login_professor')


# Gerenciar professores (listar professores)
def gerenciar_professores(request):
    query = request.GET.get('q', '')  # Busca por nome
    professores = Professor.objects.all()

    if query:
        professores = professores.filter(nome__icontains=query)  # Filtro por nome

    professores = professores.order_by('nome')  # Ordena por nome
    return render(request, 'core/gerenciar_professores.html', {'professores': professores, 'query': query})

# Editar dados de um professor
def editar_professor(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            professor = form.save()
            # Caso existam disciplinas selecionadas no formulário
            disciplinas = form.cleaned_data.get('disciplinas')
            if disciplinas:
                professor.disciplinas.set(disciplinas)
            return redirect('gerenciar_professores')
    else:
        form = ProfessorForm(instance=professor)
    
    return render(request, 'core/editar_professor.html', {'form': form, 'professor': professor})

# Excluir um professor
def excluir_professor(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    professor.delete()
    return redirect('gerenciar_professores')

# Consultar dados de um professor
def consultar_professor(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    return render(request, 'core/consultar_professor.html', {'professor': professor})


# Cadastrar professor
def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        user_form = UserCreationForm(request.POST)

        if form.is_valid():
            # Preencher o username automaticamente com base no nome do professor
            nome = form.cleaned_data['nome']
            username = nome.split()[0].lower() + nome.split()[-1].lower()  # Exemplo: 'João Silva' -> 'joaosilva'

            # Verificar se o username já existe
            while User.objects.filter(username=username).exists():
                username = username + str(randint(1, 999))  # Adiciona um número aleatório ao username

            # Atribuir o username ao formulário de criação de usuário
            user_form.fields['username'].initial = username

            # Definir uma senha padrão (exemplo: 'senha@123')
            user_form.fields['password1'].initial = 'senha@123'
            user_form.fields['password2'].initial = 'senha@123'

            if user_form.is_valid():  # Validar o formulário de usuário depois de modificar os dados
                # Salvar o usuário
                user = user_form.save()

                # Salvar o professor, associando o usuário criado
                professor = form.save(commit=False)
                professor.user = user  # Associa o usuário ao professor
                professor.save()

                # Se houver disciplinas associadas, associar ao professor
                disciplinas = form.cleaned_data.get('disciplinas')
                if disciplinas:
                    professor.disciplinas.set(disciplinas)

                return redirect('gerenciar_professores')
            else:
                print(user_form.errors)  # Para depuração
        else:
            print(form.errors)  # Para depuração
    else:
        form = ProfessorForm()
        user_form = UserCreationForm()  # Cria o formulário de usuário vazio

    return render(request, 'core/cadastrar_professor.html', {
        'form': form,
        'user_form': user_form  # Passa o formulário de usuário para o template
    })


# ------------------------------------------------------------
# Gestão de Disciplinas
# ------------------------------------------------------------

# Gerenciar disciplinas (listar disciplinas)
def gerenciar_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'core/gerenciar_disciplinas.html', {'disciplinas': disciplinas})

# Editar dados de uma disciplina
def editar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_disciplinas')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'core/editar_disciplina.html', {'form': form, 'disciplina': disciplina})

# Consultar dados de uma disciplina
def consultar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    return render(request, 'core/consultar_disciplina.html', {'disciplina': disciplina})

# Excluir disciplina
def excluir_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    disciplina.delete()
    return redirect('gerenciar_disciplinas')

# Cadastrar disciplina
def cadastrar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()  # Salva a nova disciplina
            return redirect('gerenciar_disciplinas')  # Redireciona para o gerenciamento de disciplinas
    else:
        form = DisciplinaForm()  # Exibe o formulário vazio
    return render(request, 'core/cadastrar_disciplina.html', {'form': form})

# ------------------------------------------------------------
# Verificação de toked de ID do Google
# ------------------------------------------------------------
    
def get_context_data(self, **kwargs):
    context = super(IndexViews, self).get_context_data(**kwargs)
    context['YOUR_GOOGLE_CLIENT_ID'] = YOUR_GOOGLE_CLIENT_ID
        
    return context
    
@csrf_exempt
def google_login(request):
    time.sleep(3)
    token = request.body       
    token = token.decode("utf-8").encode("windows-1252").decode("utf-8")
    token = json.loads(token)
    token = token['id_token']

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), YOUR_GOOGLE_CLIENT_ID)
        userid = idinfo['sub']
        print(idinfo)
        
    except ValueError:
        pass

    return render(request, 'index.html')
    