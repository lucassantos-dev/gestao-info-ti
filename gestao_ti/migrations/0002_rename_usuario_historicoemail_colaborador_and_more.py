# Generated by Django 5.1.5 on 2025-02-04 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_ti', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicoemail',
            old_name='usuario',
            new_name='colaborador',
        ),
        migrations.AddField(
            model_name='email',
            name='colaborador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='gestao_ti.colaborador'),
        ),
        migrations.DeleteModel(
            name='HistoricoColaborado',
        ),
    ]
