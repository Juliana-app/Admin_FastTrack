# Generated by Django 5.2 on 2025-04-23 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sede', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='sede',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sede.sede'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('mesero', 'Mesero'), ('cajero', 'Cajero'), ('administrador', 'Administrador')], max_length=20),
        ),
    ]
