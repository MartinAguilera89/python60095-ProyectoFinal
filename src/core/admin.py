from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def has_delete_permission(self, request, obj=None):
        # Si el usuario es superusuario
        if request.user.is_superuser:
            # Si no hay objeto seleccionado o el objeto no es staff
            if obj is None or not obj.is_staff:
                return True
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si el usuario no es superusuario, filtra los superusuarios
        if not request.user.is_superuser:
            qs = qs.filter(is_superuser=False)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('is_superuser', 'is_staff')
        return super().get_readonly_fields(request, obj)

# Desregistrar el UserAdmin por defecto
admin.site.unregister(User)
# Registrar nuestro UserAdmin personalizado
admin.site.register(User, CustomUserAdmin)
