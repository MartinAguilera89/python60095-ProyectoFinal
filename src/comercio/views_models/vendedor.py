from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..forms import VendedorForm
from ..mixins import SuperuserRequiredMixin
from ..models import Vendedor


class VendedorListView(LoginRequiredMixin, ListView):
    model = Vendedor

    def get_queryset(self):
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            return Vendedor.objects.filter(usuario__username__icontains=busqueda)
        return Vendedor.objects.all()


class VendedorCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm
    success_url = reverse_lazy('comercio:vendedor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Vendedor creado exitosamente')
        return super().form_valid(form)


class VendedorUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    success_url = reverse_lazy('comercio:vendedor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Vendedor actualizado exitosamente')
        return super().form_valid(form)


class VendedorDetailView(LoginRequiredMixin, DetailView):
    model = Vendedor


class VendedorDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Vendedor
    success_url = reverse_lazy('comercio:vendedor_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Vendedor eliminado exitosamente')
        return super().delete(request, *args, **kwargs)
