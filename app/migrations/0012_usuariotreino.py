# Generated by Django 5.1.1 on 2024-10-21 13:25

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_delete_usuariotreino'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioTreino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_treino', models.CharField(max_length=255)),
                ('data_treino', models.DateTimeField(default=django.utils.timezone.now)),
                ('nome_exercicio', models.CharField(max_length=255)),
                ('peso_exercicio', models.FloatField(blank=True, null=True)),
                ('repeticoes', models.IntegerField(blank=True, null=True)),
                ('series', models.IntegerField(blank=True, null=True)),
                ('descanso', models.IntegerField(blank=True, null=True)),
                ('treino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercicios_realizados', to='app.treino')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuario')),
            ],
            options={
                'verbose_name': 'Treino do Usuário',
                'verbose_name_plural': 'Treinos dos Usuários',
            },
        ),
    ]