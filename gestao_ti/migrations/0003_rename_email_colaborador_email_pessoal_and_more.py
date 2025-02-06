# Generated by Django 5.1.5 on 2025-02-04 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_ti', '0002_rename_usuario_historicoemail_colaborador_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colaborador',
            old_name='email',
            new_name='email_pessoal',
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='filial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colaboradores', to='gestao_ti.filial'),
        ),
        migrations.AlterField(
            model_name='email',
            name='colaborador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emails', to='gestao_ti.colaborador'),
        ),
    ]
