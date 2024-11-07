# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('professor/', views.professor, name='professor'),  # Página do professor
    path('aluno/', views.aluno, name='aluno'),  # Página do aluno
    path('secretaria/', views.secretaria, name='secretaria'),  # Página da secretaria
    path('alunos/', views.gerenciar_alunos, name='gerenciar_alunos'),


    # URLs para cadastro na Secretaria
    path('secretaria/cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('secretaria/cadastrar_professor/', views.cadastrar_professor, name='cadastrar_professor'),
    path('secretaria/cadastrar_disciplina/', views.cadastrar_disciplina, name='cadastrar_disciplina'),

    # URL para editar aluno
    path('secretaria/editar_aluno/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    # URL para excluir aluno
    path('secretaria/excluir_aluno/<int:aluno_id>/', views.excluir_aluno, name='excluir_aluno'),
    # URL para consultar aluno
    path('secretaria/consultar_aluno/<int:aluno_id>/', views.consultar_aluno, name='consultar_aluno'),



]
