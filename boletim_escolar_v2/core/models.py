#boletim_escolar_v2/core/models.py


from django.db import models
from django.contrib.auth.models import User



# ------------------------------------------------------------
# Modelo Secretaria
# ------------------------------------------------------------

class Secretaria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='secretaria_profile')
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nome
    

# ------------------------------------------------------------
# Modelo Aluno
# ------------------------------------------------------------
class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno_profile')
    nome = models.CharField(max_length=100)
    rm = models.CharField(max_length=20, unique=True)  # Registro de matrícula único
    ra_rg = models.CharField(max_length=20, blank=True, null=True)  # RA ou RG (opcional)
    data_nascimento = models.DateField()  # Data de nascimento do aluno
    
    # Status do aluno (Ativo, Transferido ou Suplente)
    status = models.CharField(
        max_length=11,
        choices=[('ativo', 'Ativo'), ('transferido', 'Transferido'), ('suplente', 'Suplente')],
        default='ativo'
    )
    
    # Dados de contato do responsável (não obrigatórios)
    email_responsavel = models.EmailField(max_length=100, blank=True, null=True)
    telefone_responsavel = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nome


# ------------------------------------------------------------
# Modelo Disciplina
# ------------------------------------------------------------
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)  # Nome da disciplina

    def __str__(self):
        return self.nome


# ------------------------------------------------------------
# Modelo Professor
# ------------------------------------------------------------
class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')  # Conexão com o User do Django
    nome = models.CharField(max_length=255)  # Nome completo do professor
    
    # Informações de contato (opcionais)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    # Relacionamento muitos-para-muitos com Disciplina
    disciplinas = models.ManyToManyField(Disciplina, related_name='professores')

    def __str__(self):
        return self.nome
    

# ------------------------------------------------------------
# Modelo Turma
# ------------------------------------------------------------
class Turma(models.Model):
    ano = models.PositiveIntegerField()  # Ano da turma (Exemplo: 2024)
    classe = models.CharField(max_length=5, default='Indefinido')  # Classe (Exemplo: 1A, 2B, etc.)
    
    # Relacionamento muitos-para-muitos com Aluno e Professor
    alunos = models.ManyToManyField(Aluno, related_name='turmas')
    professores = models.ManyToManyField(Professor, related_name='turmas')

    def __str__(self):
        return f"{self.ano} - {self.classe}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"


# ------------------------------------------------------------
# Modelo Nota
# ------------------------------------------------------------
class Nota(models.Model):
    # Relacionamento com Aluno e Disciplina
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)

    # Notas e faltas de cada bimestre
    nota_bimestre1 = models.FloatField(default=0)
    faltas_bimestre1 = models.IntegerField(default=0)
    nota_bimestre2 = models.FloatField(default=0)
    faltas_bimestre2 = models.IntegerField(default=0)
    nota_bimestre3 = models.FloatField(default=0)
    faltas_bimestre3 = models.IntegerField(default=0)
    nota_bimestre4 = models.FloatField(default=0)
    faltas_bimestre4 = models.IntegerField(default=0)

    # Média final do aluno
    media_final = models.FloatField(default=0)

    # Status final do aluno
    STATUS_CHOICES = [
        ('P', 'Promovido'),
        ('PC', 'Promovido pelo conselho'),
        ('T', 'Transferido'),
        ('R', 'Retido'),
        ('NC', 'Não Comparecimento'),
        ('AB', 'Abandono'),
        ('RC', 'Reclassificado'),
        ('RM', 'Remanejado'),
    ]
    status_final = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina.nome}"
