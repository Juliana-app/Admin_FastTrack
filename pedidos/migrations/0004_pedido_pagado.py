# Generated by Django 5.2 on 2025-04-25 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_pedidoproducto_precio_unitario_alter_pedido_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
    ]
