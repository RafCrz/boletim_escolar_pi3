from django.db import models

# Modelo Aluno
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    rm = models.CharField(max_length=20, unique=True)
    ra_rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField()
    status = models.CharField(max_length=11, choices=[('ativo', 'Ativo'), ('transferido', 'Transferido'), ('suplente', 'Suplente')], default='ativo')
    email_responsavel = models.EmailField(max_length=100, blank=True, null=True)  # Novo campo (não obrigatório)
    telefone_responsavel = models.CharField(max_length=15, blank=True, null=True)  # Novo campo (não obrigatório)

    def __str__(self):
        return self.nome
    




# Modelo Professor
class Professor(models.Model):
    # Nome do professor
    nome = models.CharField(max_length=100)
    
    # Quantidade de aulas previstas e aulas dadas por bimestre
    aulas_previstas_bimestre1 = models.IntegerField(default=0)
    aulas_dadas_bimestre1 = models.IntegerField(default=0)
    aulas_previstas_bimestre2 = models.IntegerField(default=0)
    aulas_dadas_bimestre2 = models.IntegerField(default=0)
    aulas_previstas_bimestre3 = models.IntegerField(default=0)
    aulas_dadas_bimestre3 = models.IntegerField(default=0)
    aulas_previstas_bimestre4 = models.IntegerField(default=0)
    aulas_dadas_bimestre4 = models.IntegerField(default=0)  

    def __str__(self):
        # Representação do professor pelo nome ao ser exibido
        return self.nome
    

# Modelo Disciplina
class Disciplina(models.Model):
    # Nome da disciplina
    nome = models.CharField(max_length=100)

    # Professor responsável pela disciplina
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE, related_name='disciplinas')

    def __str__(self):
        # Representação da disciplina pelo nome
        return self.nome
    

# Modelo Turma
class Turma(models.Model):
    # Nome da turma, por exemplo: "1A", "2B"
    nome = models.CharField(max_length=10)
    
    # Ano escolar da turma
    ano = models.IntegerField()

    # Lista de alunos associados a esta turma
    alunos = models.ManyToManyField('Aluno')

    # Lista de professores e disciplinas associados à turma
    professores = models.ManyToManyField('Professor')

    def __str__(self):
        # Representação da turma pelo nome e ano
        return f"{self.nome} - Ano {self.ano}"
    

# Modelo Nota
class Nota(models.Model):
    # Nota do aluno em uma disciplina específica
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)

    # Notas de cada bimestre
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
        # Representação da nota pelo aluno e disciplina
        return f"{self.aluno.nome} - {self.disciplina.nome}"
