from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from datetime import date

from ..forms import VentaForm, ProductoVentaFormSet, ProductoVentaForm
from ..models import Vendedor, Venta

class VentaListView(LoginRequiredMixin, ListView):
    model = Venta

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            vendedor = Vendedor.objects.get(usuario=self.request.user)
            return Venta.objects.filter(vendedor=vendedor)
        except Vendedor.DoesNotExist:
            return Venta.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for venta in context['object_list']:
            venta.producto = venta.producto
        return context


class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    success_url = reverse_lazy('comercio:venta_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        try:
            Vendedor.objects.get(usuario=request.user)
            return super().dispatch(request, *args, **kwargs)
        except Vendedor.DoesNotExist:
            messages.error(
                request,
                'Debe ser vendedor para crear ventas. Por favor, contacte al administrador.'
            )
            return redirect('comercio:venta_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            with transaction.atomic():
                if self.request.user.is_superuser:
                    form.instance.vendedor = form.cleaned_data['vendedor']
                else:
                    vendedor = Vendedor.objects.get(usuario=self.request.user)
                    form.instance.vendedor = vendedor
                
                producto = form.cleaned_data['producto']
                cantidad = form.cleaned_data['cantidad']
                form.instance.producto = producto
                
                producto.stock -= cantidad
                producto.save()
                
                form.instance.fecha_compra = date.today()
                form.instance.precio_total = form.cleaned_data['cantidad'] * form.instance.producto.precio
                
                form.save()
                messages.success(self.request, 'Venta creada exitosamente')
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al crear la venta: {str(e)}')
            return self.form_invalid(form)


class VentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    success_url = reverse_lazy('comercio:venta_list')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            vendedor = Vendedor.objects.get(usuario=self.request.user)
            return Venta.objects.filter(vendedor=vendedor)
        except Vendedor.DoesNotExist:
            return Venta.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            with transaction.atomic():
                venta = form.save(commit=False)
                venta.producto.stock += self.get_object().cantidad
                venta.producto.stock -= venta.cantidad
                venta.precio_total = venta.producto.precio * venta.cantidad
                venta.producto.save()
                venta.save()
                messages.success(self.request, 'Venta actualizada exitosamente')
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar la venta: {str(e)}')
            return self.form_invalid(form)


class VentaDetailView(LoginRequiredMixin, DetailView):
    model = Venta

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            vendedor = Vendedor.objects.get(usuario=self.request.user)
            return Venta.objects.filter(vendedor=vendedor)
        except Vendedor.DoesNotExist:
            return Venta.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class VentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Venta
    success_url = reverse_lazy('comercio:venta_list')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        try:
            vendedor = Vendedor.objects.get(usuario=self.request.user)
            return Venta.objects.filter(vendedor=vendedor)
        except Vendedor.DoesNotExist:
            return Venta.objects.none()

    def delete(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                venta = self.get_object()
                venta.producto.stock += venta.cantidad
                venta.producto.save()
                messages.success(request, 'Venta eliminada exitosamente')
                return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Error al eliminar la venta: {str(e)}')
            return redirect('comercio:venta_list')