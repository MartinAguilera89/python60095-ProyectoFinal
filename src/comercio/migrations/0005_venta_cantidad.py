# Generated by Django 5.1.4 on 2024-12-31 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercio', '0004_venta_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='cantidad',
            field=models.PositiveIntegerField(default=1, help_text='Cantidad de producto vendido'),
        ),
    ]
