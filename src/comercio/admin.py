from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Producto, Temporada, Vendedor, Venta


class VendedorAdminForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text='Nombre de usuario para el nuevo vendedor'
    )
    email = forms.EmailField(
        help_text='Correo electrónico del vendedor'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text='Contraseña para el nuevo vendedor'
    )

    class Meta:
        model = Vendedor
        fields = ('username', 'email', 'password', 'celular', 'avatar')

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        
        vendedor = super().save(commit=False)
        vendedor.usuario = user
        if commit:
            vendedor.save()
        return vendedor


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'temporada', 'stock')
    list_filter = ('temporada',)
    search_fields = ('nombre', 'descripcion')


@admin.register(Temporada)
class TemporadaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    form = VendedorAdminForm
    list_display = ('usuario', 'celular', 'mostrar_avatar')
    search_fields = ('usuario__username', 'celular')
    exclude = ('usuario',)

    def mostrar_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.avatar.url
            )
        return '(Sin avatar)'
    mostrar_avatar.short_description = 'Avatar'


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('mostrar_vendedor', 'precio_total', 'fecha')  
    list_filter = ('vendedor',)  
    search_fields = ('vendedor__usuario__username',)  

    def mostrar_vendedor(self, obj):
        if obj.vendedor:
            return obj.vendedor.usuario.username
        return '(Sin vendedor)'
    mostrar_vendedor.short_description = 'Vendedor'
