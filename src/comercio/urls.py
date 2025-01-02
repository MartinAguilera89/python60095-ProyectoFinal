from django.urls import path

from .views import index
from .views_models import producto, temporada, vendedor
from .views_models.venta import VentaCreateView, VentaListView, VentaUpdateView, VentaDetailView, VentaDeleteView

app_name = 'comercio'

urlpatterns = [path('', index, name='index')]

urlpatterns += [
    path('producto/list/', producto.ProductoListView.as_view(), name='producto_list'),
    path('producto/create/', producto.ProductoCreateView.as_view(), name='producto_create'),
    path('producto/update/<int:pk>', producto.ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/detail/<int:pk>', producto.ProductoDetailView.as_view(), name='producto_detail'),
    path('producto/delete/<int:pk>', producto.ProductoDeleteView.as_view(), name='producto_delete'),
]

urlpatterns += [
    path('temporada/list/', temporada.temporada_list, name='temporada_list'),
    path('temporada/create/', temporada.temporada_create, name='temporada_create'),
    path('temporada/update/<int:pk>', temporada.temporada_update, name='temporada_update'),
    path('temporada/detail/<int:pk>', temporada.temporada_detail, name='temporada_detail'),
    path('temporada/delete/<int:pk>', temporada.temporada_delete, name='temporada_delete'),
]

urlpatterns += [
    path('vendedor/list/', vendedor.VendedorListView.as_view(), name='vendedor_list'),
    path('vendedor/create/', vendedor.VendedorCreateView.as_view(), name='vendedor_create'),
    path('vendedor/update/<int:pk>', vendedor.VendedorUpdateView.as_view(), name='vendedor_update'),
    path('vendedor/detail/<int:pk>', vendedor.VendedorDetailView.as_view(), name='vendedor_detail'),
    path('vendedor/delete/<int:pk>', vendedor.VendedorDeleteView.as_view(), name='vendedor_delete'),
]

urlpatterns += [
    path('venta/list/', VentaListView.as_view(), name='venta_list'),
    path('venta/create/', VentaCreateView.as_view(), name='venta_create'),
    path('venta/update/<int:pk>', VentaUpdateView.as_view(), name='venta_update'),
    path('venta/detail/<int:pk>', VentaDetailView.as_view(), name='venta_detail'),
    path('venta/delete/<int:pk>', VentaDeleteView.as_view(), name='venta_delete'),
]
