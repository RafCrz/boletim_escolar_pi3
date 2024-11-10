from faker import Faker
from core.models import Aluno
from django.contrib.auth.models import User

# Inicializando o Faker
fake = Faker('pt_BR')

# Função para criar alunos aleatórios
def criar_alunos_aleatorios(n=80):
    for _ in range(n):
        # Gerar dados aleatórios
        nome = fake.name()  # Nome completo
        rm = fake.unique.random_number(digits=6)  # Número único de matrícula
        ra_rg = fake.random_number(digits=9)
        data_nascimento = fake.date_of_birth(minimum_age=6, maximum_age=10)  # Idade entre 6 e 10 anos
        status = 'ativo'  # Status fixo como 'ativo'
        email_responsavel = fake.email()
        telefone_responsavel = fake.phone_number()

        # Criar usuário associado ao aluno
        username = str(rm)
        password = 'senha@123'
        user = User.objects.create_user(username=username, password=password)

        # Criar e salvar o aluno no banco de dados
        Aluno.objects.create(
            user=user,
            nome=nome,
            rm=str(rm),  # Garantir que seja tratado como string
            ra_rg=str(ra_rg),  # Garantir que seja tratado como string
            data_nascimento=data_nascimento,
            status=status,
            email_responsavel=email_responsavel,
            telefone_responsavel=telefone_responsavel,
        )

# Chamar a função para criar 80 alunos
criar_alunos_aleatorios(80)
