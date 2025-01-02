from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Producto(models.Model):
    nombre = models.CharField(
        max_length=100,
        help_text='Ingrese el nombre del producto'
    )
    descripcion = models.TextField(
        help_text='Ingrese una descripción del producto'
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Ingrese el precio del producto'
    )
    stock = models.PositiveIntegerField(
        help_text='Ingrese la cantidad disponible del producto'
    )
    temporada = models.ForeignKey(
        'Temporada',
        on_delete=models.CASCADE,
        help_text='Seleccione la temporada del producto'
    )
    imagen = models.ImageField(
        upload_to='productos',
        blank=True,
        null=True,
        help_text='Seleccione una imagen para el producto'
    )

    def __str__(self):
        return self.nombre


class Temporada(models.Model):
    nombre = models.CharField(
        max_length=100,
        help_text='Ingrese el nombre de la temporada'
    )
    descripcion = models.TextField(
        help_text='Ingrese una descripción de la temporada'
    )

    def __str__(self):
        return self.nombre


class Vendedor(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='vendedor',
        help_text='Usuario asociado al vendedor'
    )
    celular = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Ingrese el número de celular del vendedor'
    )
    avatar = models.ImageField(
        upload_to='imagenes_perfil',
        blank=True,
        null=True,
        help_text='Seleccione una imagen de perfil para el vendedor'
    )

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'


class Venta(models.Model):
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Vendedor que realizó la venta'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='ventas',
        null=True,
        help_text='Producto vendido'
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        help_text='Cantidad de producto vendido'
    )
    fecha = models.DateTimeField(
        default=timezone.now,
        help_text='Fecha y hora de la venta'
    )
    precio_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        help_text='Precio total de la venta'
    )

    class Meta:
        ordering = ('-fecha',)

    def __str__(self):
        vendedor_nombre = self.vendedor.usuario.username if self.vendedor and self.vendedor.usuario else "Sin vendedor"
        return f'{vendedor_nombre} > {self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
