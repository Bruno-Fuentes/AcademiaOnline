# Generated by Django 5.1.1 on 2024-10-21 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_usuariotreino'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuariotreino',
            options={'verbose_name': 'Treino do Usuário', 'verbose_name_plural': 'Treinos dos Usuários'},
        ),
        migrations.RemoveField(
            model_name='usuariotreino',
            name='treino_original',
        ),
        migrations.AddField(
            model_name='usuariotreino',
            name='treino',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exercicios_realizados', to='app.treino'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuariotreino',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuario'),
        ),
    ]
