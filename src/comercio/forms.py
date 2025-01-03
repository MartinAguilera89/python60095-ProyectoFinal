from django import forms
from django.contrib.auth.models import User
from django.forms import formset_factory

from .models import Producto, Temporada, Vendedor, Venta
from datetime import datetime, date


def validar_nombre(nombre: str):
    if len(nombre) < 3:
        raise forms.ValidationError('La longitud debe ser mayor a 3 caracteres')
    if not any(c.isalpha() for c in nombre):
        raise forms.ValidationError('Debe contener al menos una letra')
    return nombre


class TemporadaForm(forms.ModelForm):
    class Meta:
        model = Temporada
        fields = ['nombre', 'descripcion']

    def clean_nombre(self):
        nombre: str = self.cleaned_data.get('nombre', '')
        return validar_nombre(nombre)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['temporada', 'nombre', 'descripcion', 'precio', 'stock']

    def clean_nombre(self):
        nombre: str = self.cleaned_data.get('nombre', '')
        return validar_nombre(nombre)


class VendedorForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text='Nombre de usuario para el nuevo vendedor'
    )
    email = forms.EmailField(
        required=False,
        help_text='Correo electrónico del vendedor (opcional)'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text='Contraseña para el nuevo vendedor'
    )

    class Meta:
        model = Vendedor
        fields = ('username', 'email', 'password', 'celular', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['celular'].required = False

    def save(self, commit=True):
        # Crear nuevo usuario
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data.get('email', ''),  # Email opcional
            password=self.cleaned_data['password']
        )
        
        # Crear vendedor
        vendedor = super().save(commit=False)
        vendedor.usuario = user
        if commit:
            vendedor.save()
        return vendedor


class VentaForm(forms.ModelForm):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto')
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')

    class Meta:
        model = Venta
        fields = ['vendedor', 'producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(VentaForm, self).__init__(*args, **kwargs)

        if self.user and self.user.is_superuser:
            self.fields['vendedor'] = forms.ModelChoiceField(
                queryset=Vendedor.objects.all(),
                label='Vendedor',
                help_text='Seleccione el vendedor para esta venta',
                required=True
            )
        elif self.user:
            try:
                vendedor = Vendedor.objects.get(usuario=self.user)
                self.fields['vendedor'].widget = forms.HiddenInput()
                self.fields['vendedor'].initial = vendedor
            except Vendedor.DoesNotExist:
                pass

    def save(self, commit=True):
        venta = super().save(commit=False)
        if not self.user.is_superuser:
            vendedor = Vendedor.objects.get(usuario=self.user)
            venta.vendedor = vendedor
        if commit:
            venta.save()
        return venta


class ProductoVentaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto')
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')

ProductoVentaFormSet = formset_factory(ProductoVentaForm, extra=1)