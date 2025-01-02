# Generated by Django 5.1.4 on 2024-12-30 03:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercio', '0003_remove_venta_cantidad_remove_venta_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='cantidad',
            field=models.PositiveIntegerField(default=0, help_text='Cantidad del producto vendido'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='producto',
            field=models.ForeignKey(default=1, help_text='Producto vendido', on_delete=django.db.models.deletion.CASCADE, to='comercio.producto'),
            preserve_default=False,
        ),
    ]