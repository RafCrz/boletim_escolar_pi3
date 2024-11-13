# boletim_escolar_v2/core/urls.py

from django.urls import path
from . import views
from .views import ProfessorLoginView, professor_logout, ProfessorHomeView, ProfessorPasswordChangeView, login_aluno, cadastrar_aluno
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # ------------------------------------------------------------
    # Páginas principais
    # ------------------------------------------------------------
    path('', views.index, name='index'),  # Página inicial
    path('professor/', ProfessorHomeView.as_view(), name='professor_home'),
    path('aluno/', views.aluno, name='aluno'),  # Página do aluno
    path('secretaria/', views.secretaria, name='secretaria'),  # Página da secretaria

    # ------------------------------------------------------------
    # Gestão de Alunos
    # ------------------------------------------------------------
    path('alunos/', views.gerenciar_alunos, name='gerenciar_alunos'),  # Gerenciar alunos
    path('secretaria/editar_aluno/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    path('secretaria/excluir_aluno/<int:aluno_id>/', views.excluir_aluno, name='excluir_aluno'),
    path('secretaria/consultar_aluno/<int:aluno_id>/', views.consultar_aluno, name='consultar_aluno'),
    path('login_aluno/', login_aluno, name='login_aluno'),
    path('aluno_home/', views.aluno_home, name='aluno_home'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Adiciona a URL para logout
    path('logout_aluno/', views.aluno_logout, name='logout_aluno'),  # Adiciona a URL para logout do aluno

    # ------------------------------------------------------------
    # Cadastro na Secretaria (Alunos, Professores, Disciplinas)
    # ------------------------------------------------------------
    #path('secretaria/cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('secretaria/cadastrar_aluno/', cadastrar_aluno, name='cadastrar_aluno'),
    path('secretaria/cadastrar_professor/', views.cadastrar_professor, name='cadastrar_professor'),
    path('secretaria/cadastrar_disciplina/', views.cadastrar_disciplina, name='cadastrar_disciplina'),

    # ------------------------------------------------------------
    # Gestão de Turmas
    # ------------------------------------------------------------
    path('gerenciar_turmas/', views.gerenciar_turmas, name='gerenciar_turmas'),
    path('secretaria/criar_turma/', views.criar_turma, name='criar_turma'),
    path('secretaria/editar_turma/<int:pk>/', views.editar_turma, name='editar_turma'),
    path('consultar_turma/<int:turma_id>/', views.consultar_turma, name='consultar_turma'),
    path('secretaria/excluir_turma/<int:pk>/', views.excluir_turma, name='excluir_turma'),
    path('turma/<int:turma_id>/', views.detalhes_turma, name='detalhes_turma'),

    # ------------------------------------------------------------
    # Gestão de Professores
    # ------------------------------------------------------------
    path('secretaria/gerenciar_professores/', views.gerenciar_professores, name='gerenciar_professores'),
    path('login_professor/', ProfessorLoginView.as_view(), name='login_professor'),
    path('logout_professor/', views.professor_logout, name='logout_professor'),
    path('professor/mudar-senha/', ProfessorPasswordChangeView.as_view(), name='mudar_senha_professor'),

    # Editar, Excluir e Consultar Professor
    path('secretaria/editar_professor/<int:professor_id>/', views.editar_professor, name='editar_professor'),
    path('secretaria/excluir_professor/<int:professor_id>/', views.excluir_professor, name='excluir_professor'),
    path('secretaria/consultar_professor/<int:professor_id>/', views.consultar_professor, name='consultar_professor'),

    # ------------------------------------------------------------
    # Gestão de Disciplinas
    # ------------------------------------------------------------
    path('disciplinas/', views.gerenciar_disciplinas, name='gerenciar_disciplinas'),
    path('disciplinas/editar/<int:disciplina_id>/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplinas/excluir/<int:disciplina_id>/', views.excluir_disciplina, name='excluir_disciplina'),
    path('disciplinas/consultar/<int:disciplina_id>/', views.consultar_disciplina, name='consultar_disciplina'),
    path('disciplinas/cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
]