from django.contrib import admin

from .models import Aluno, Professor, Turma, Disciplina, Nota, Secretaria

# Registrar os modelos no admin
admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(Disciplina)
admin.site.register(Nota)
admin.site.register(Secretaria)