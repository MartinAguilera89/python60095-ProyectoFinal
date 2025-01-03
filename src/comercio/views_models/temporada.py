from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import TemporadaForm
from ..models import Producto, Temporada


def is_superuser(user):
    return user.is_superuser


@login_required
def temporada_list(request: HttpRequest) -> HttpResponse:
    busqueda = request.GET.get('busqueda')
    if busqueda:
        queryset = Temporada.objects.filter(nombre__icontains=busqueda)
    else:
        queryset = Temporada.objects.all()
    return render(request, 'comercio/temporada_list.html', {'object_list': queryset})


@login_required
@user_passes_test(is_superuser)
def temporada_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TemporadaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Temporada creada exitosamente')
            return redirect('comercio:temporada_list')
    else:
        form = TemporadaForm()
    return render(request, 'comercio/temporada_form.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def temporada_update(request: HttpRequest, pk: int) -> HttpResponse:
    query = get_object_or_404(Temporada, pk=pk)
    if request.method == 'POST':
        form = TemporadaForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request, 'Temporada actualizada exitosamente')
            return redirect('comercio:temporada_list')
    else:
        form = TemporadaForm(instance=query)
    return render(request, 'comercio/temporada_form.html', {'form': form})


@login_required
def temporada_detail(request: HttpRequest, pk: int) -> HttpResponse:
    temporada = get_object_or_404(Temporada, pk=pk)
    productos = Producto.objects.filter(temporada=temporada)
    return render(
        request,
        'comercio/temporada_detail.html',
        {'object': temporada, 'productos': productos}
    )


@login_required
@user_passes_test(is_superuser)
def temporada_delete(request: HttpRequest, pk: int) -> HttpResponse:
    query = get_object_or_404(Temporada, pk=pk)
    if request.method == 'POST':
        query.delete()
        messages.success(request, 'Temporada eliminada exitosamente')
        return redirect('comercio:temporada_list')
    return render(request, 'comercio/temporada_confirm_delete.html', {'object': query})