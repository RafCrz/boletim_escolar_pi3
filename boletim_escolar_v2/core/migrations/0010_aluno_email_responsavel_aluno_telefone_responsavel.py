# Generated by Django 5.1.2 on 2024-11-07 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_aluno_numero_chamada_alter_aluno_ra_rg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='email_responsavel',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='aluno',
            name='telefone_responsavel',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
