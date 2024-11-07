# core/views.py

from django.shortcuts import render, redirect
from .models import Aluno, Professor, Disciplina
from .forms import AlunoForm, ProfessorForm, DisciplinaForm


def index(request):
    return render(request, 'core/index.html')

def professor(request):
    # Página para o professor inserir notas
    return render(request, 'core/professor.html')

def aluno(request):
    # Página para o aluno consultar suas notas
    return render(request, 'core/aluno.html')

def secretaria(request):
    # Página para o administrador da secretaria gerenciar cadastros
    return render(request, 'core/secretaria.html')



def gerenciar_alunos(request):
    query = request.GET.get('q', '')  # Pega o parâmetro 'q' da URL (campo de busca)
    alunos = Aluno.objects.all()  # Obter todos os alunos

    if query:
        # Se houver uma busca, filtra pelo nome do aluno
        alunos = alunos.filter(nome__icontains=query)
    
    # Ordena os alunos por nome em ordem alfabética
    alunos = alunos.order_by('nome')

    return render(request, 'core/gerenciar_alunos.html', {'alunos': alunos, 'query': query})




# Editar Aluno
def editar_aluno(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)  # Buscar o aluno com o ID específico
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)  # Passar a instância para editar
        if form.is_valid():
            form.save()  # Salvar as alterações
            return redirect('gerenciar_alunos')  # Redirecionar para a página de gerenciamento
    else:
        form = AlunoForm(instance=aluno)  # Preencher o formulário com os dados do aluno
    
    return render(request, 'core/editar_aluno.html', {'form': form, 'aluno': aluno})


# Excluir Aluno
def excluir_aluno(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)  # Buscar o aluno
    aluno.delete()  # Excluir o aluno
    return redirect('gerenciar_alunos')  # Redirecionar para a lista de alunos


# Consultar Aluno
def consultar_aluno(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)  # Buscar o aluno com o ID específico
    return render(request, 'core/consultar_aluno.html', {'aluno': aluno})



# Cadastro de Aluno
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'core/cadastrar_aluno.html', {'form': form})

# Cadastro de Professor
def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('secretaria')
    else:
        form = ProfessorForm()
    return render(request, 'core/cadastrar_professor.html', {'form': form})

# Cadastro de Disciplina
def cadastrar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('secretaria')
    else:
        form = DisciplinaForm()
    return render(request, 'core/cadastrar_disciplina.html', {'form': form})