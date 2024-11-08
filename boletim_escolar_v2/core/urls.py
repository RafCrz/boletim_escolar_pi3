from django.urls import path
from . import views

urlpatterns = [
    # ------------------------------------------------------------
    # Páginas principais
    # ------------------------------------------------------------
    path('', views.index, name='index'),  # Página inicial
    path('professor/', views.professor, name='professor'),  # Página do professor
    path('aluno/', views.aluno, name='aluno'),  # Página do aluno
    path('secretaria/', views.secretaria, name='secretaria'),  # Página da secretaria

    # ------------------------------------------------------------
    # Gestão de Alunos
    # ------------------------------------------------------------
    path('alunos/', views.gerenciar_alunos, name='gerenciar_alunos'),  # Gerenciar alunos
    
    # Editar, Excluir e Consultar Aluno
    path('secretaria/editar_aluno/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    path('secretaria/excluir_aluno/<int:aluno_id>/', views.excluir_aluno, name='excluir_aluno'),
    path('secretaria/consultar_aluno/<int:aluno_id>/', views.consultar_aluno, name='consultar_aluno'),

    # ------------------------------------------------------------
    # Cadastro na Secretaria (Alunos, Professores, Disciplinas)
    # ------------------------------------------------------------
    path('secretaria/cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('secretaria/cadastrar_professor/', views.cadastrar_professor, name='cadastrar_professor'),
    path('secretaria/cadastrar_disciplina/', views.cadastrar_disciplina, name='cadastrar_disciplina'),

    # ------------------------------------------------------------
    # Gestão de Turmas
    # ------------------------------------------------------------
    path('gerenciar_turmas/', views.gerenciar_turmas, name='gerenciar_turmas'),  # Gerenciar turmas
    
    # Criar, Editar, Excluir e Consultar Turma
    path('secretaria/criar_turma/', views.criar_turma, name='criar_turma'),  # Criar turma
    path('secretaria/editar_turma/<int:pk>/', views.editar_turma, name='editar_turma'),  # Editar turma
    path('consultar_turma/<int:turma_id>/', views.consultar_turma, name='consultar_turma'),  # Consultar turma
    path('secretaria/excluir_turma/<int:pk>/', views.excluir_turma, name='excluir_turma'),

    # ------------------------------------------------------------
    # Gestão de Professores
    # ------------------------------------------------------------
    path('secretaria/gerenciar_professores/', views.gerenciar_professores, name='gerenciar_professores'),  # Gerenciar professores

    # Editar, Excluir e Consultar Professor
    path('secretaria/editar_professor/<int:professor_id>/', views.editar_professor, name='editar_professor'),
    path('secretaria/excluir_professor/<int:professor_id>/', views.excluir_professor, name='excluir_professor'),
    path('secretaria/consultar_professor/<int:professor_id>/', views.consultar_professor, name='consultar_professor'),

    # ------------------------------------------------------------
    # Gestão de Disciplinas
    # ------------------------------------------------------------
    path('disciplinas/', views.gerenciar_disciplinas, name='gerenciar_disciplinas'),  # Gerenciar disciplinas
    path('disciplinas/editar/<int:disciplina_id>/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplinas/excluir/<int:disciplina_id>/', views.excluir_disciplina, name='excluir_disciplina'),
    path('disciplinas/consultar/<int:disciplina_id>/', views.consultar_disciplina, name='consultar_disciplina'),
    path('disciplinas/cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
]