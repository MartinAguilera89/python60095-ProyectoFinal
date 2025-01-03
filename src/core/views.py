from django.contrib import messages
from django.contrib.auth.decorators import login_not_required  # type: ignore
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from comercio.models import Vendedor
from .forms import CustomAuthenticationForm, CustomUserCreationForm, UserProfileForm


@login_not_required
def index(request):
    return render(request, 'core/index.html')


@login_not_required
def about(request):
    return render(request, 'core/about.html')


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'core/login.html'
    next_page = reverse_lazy('core:index')

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        usuario = form.get_user()
        messages.success(
            self.request, f'¡Bienvenido {usuario.username}!'
        )
        return super().form_valid(form)

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        messages.error(
            self.request, 'Error en el inicio de sesión. Por favor, verifica tu nombre de usuario y contraseña.',
            extra_tags='danger'
        )
        return super().form_invalid(form)


@method_decorator(login_not_required, name='dispatch')
class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('core:login')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        # Crear un vendedor asociado al usuario
        Vendedor.objects.create(usuario=self.object)
        messages.success(self.request, 'Registro de vendedor exitoso. Ahora puedes iniciar sesión.')
        return response


class UpdateProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'core/profile.html'

    def form_valid(self, form):
        messages.success(self.request, 'Cambios guardados correctamente')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.render_to_response({'form': form})

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('core:profile')
