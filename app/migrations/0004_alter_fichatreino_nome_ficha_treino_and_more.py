# Generated by Django 5.1.1 on 2024-10-01 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_fichatreino_exercicio_exercicio_ficha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichatreino',
            name='nome_ficha_treino',
            field=models.CharField(max_length=100, verbose_name='Nome da Ficha de Treino'),
        ),
        migrations.AlterField(
            model_name='interacao',
            name='data_comentario',
            field=models.DateField(auto_now_add=True, verbose_name='Data do Comentario'),
        ),
    ]
