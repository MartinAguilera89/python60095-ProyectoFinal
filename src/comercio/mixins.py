from django.contrib import messages
from django.shortcuts import redirect


class SuperuserRequiredMixin:
    """
    Mixin que restringe el acceso a superusuarios.
    Si el usuario no es superusuario, será redirigido a la página de inicio
    con un mensaje de error.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(
                request,
                'No tiene permisos para acceder a esta página. Se requieren permisos de administrador.'
            )
            return redirect('comercio:venta_list')
        return super().dispatch(request, *args, **kwargs)
