# ------------------------------------------------------------
# Importações
# ------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, Turma, Professor, Disciplina
from .forms import AlunoForm, TurmaForm, ProfessorForm, DisciplinaForm


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

# Cadastrar aluno
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'core/cadastrar_aluno.html', {'form': form})


# ------------------------------------------------------------
# Gestão de Professores
# ------------------------------------------------------------

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
        if form.is_valid():
            professor = form.save()  # Salva o professor
            disciplinas = form.cleaned_data.get('disciplinas')
            if disciplinas:
                professor.disciplinas.set(disciplinas)
            return redirect('gerenciar_professores')
        else:
            print(form.errors)  # Imprime os erros para depuração
    else:
        form = ProfessorForm()
    return render(request, 'core/cadastrar_professor.html', {'form': form})


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