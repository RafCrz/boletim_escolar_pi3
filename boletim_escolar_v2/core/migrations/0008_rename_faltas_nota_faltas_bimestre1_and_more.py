# Generated by Django 5.1.2 on 2024-10-26 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_nota'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nota',
            old_name='faltas',
            new_name='faltas_bimestre1',
        ),
        migrations.AddField(
            model_name='nota',
            name='faltas_bimestre2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nota',
            name='faltas_bimestre3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nota',
            name='faltas_bimestre4',
            field=models.IntegerField(default=0),
        ),
    ]
