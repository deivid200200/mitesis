from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

from .models import PerfilUsuario
from .forms import CustomUserCreationForm, PerfilUsuarioForm, UsuarioEditarForm, PerfilUsuarioEditarForm

# Create your views here.

class AdministradorRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario tiene rol de administrador del negocio"""
    def test_func(self):
        return (
            hasattr(self.request.user, 'perfil') and 
            self.request.user.perfil.rol == 'administrador'
        )
    
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a esta sección. Solo administradores.")
        return redirect('dashboard')


def login_view(request):
    """Vista de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    
    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')


@login_required
def dashboard(request):
    """Dashboard principal - redirecciona según el rol"""
    if not hasattr(request.user, 'perfil'):
        return render(request, 'dashboard.html')
    
    rol = request.user.perfil.rol
    context = {'rol': rol}
    
    if rol == 'administrador':
        # Dashboard administrador del negocio
        from django.contrib.auth.models import User
        usuarios_total = User.objects.count()
        usuarios_activos = User.objects.filter(is_active=True).count()
        usuarios_inactivos = User.objects.filter(is_active=False).count()
        
        # Contar por rol
        from django.db.models import Count
        usuarios_por_rol = (
            PerfilUsuario.objects
            .values('rol')
            .annotate(count=Count('id'))
        )
        
        context.update({
            'usuarios_total': usuarios_total,
            'usuarios_activos': usuarios_activos,
            'usuarios_inactivos': usuarios_inactivos,
            'usuarios_por_rol': usuarios_por_rol,
        })
    
    elif rol == 'coordinador':
        # Dashboard coordinador
        from academico.models import Maestria
        maestrias = Maestria.objects.filter(coordinador=request.user)
        context['maestrias'] = maestrias
    
    elif rol == 'profesor':
        # Dashboard profesor
        from academico.models import ProfesorAsignatura, Calificacion
        asignaturas = ProfesorAsignatura.objects.filter(profesor=request.user, activo=True).select_related('asignatura')
        context['asignaturas'] = asignaturas
        context['total_asignaturas'] = asignaturas.count()
        
        # Contar estudiantes asignados
        from django.db.models import Count
        total_estudiantes = Calificacion.objects.filter(
            profesor__profesor=request.user
        ).values('estudiante').distinct().count()
        context['total_estudiantes'] = total_estudiantes
    
    elif rol == 'secretaria':
        # Dashboard secretaria
        from academico.models import Estudiante, InscripcionModulo
        estudiantes_total = Estudiante.objects.count()
        inscripciones = InscripcionModulo.objects.filter(estado_inscripcion='inscrito').count()
        context.update({
            'estudiantes_total': estudiantes_total,
            'inscripciones_pendientes': inscripciones,
        })
    
    elif rol == 'estudiante':
        # Dashboard estudiante
        try:
            from academico.models import Expediente, Calificacion
            estudiante = request.user.estudiante
            expediente = Expediente.objects.filter(estudiante=estudiante).first()
            calificaciones = Calificacion.objects.filter(estudiante=estudiante)
            context.update({
                'expediente': expediente,
                'promedio': calificaciones.aggregate(__import__('django.db.models', fromlist=['Avg']).Avg('nota_final'))['nota_final__avg'] or 0,
                'calificaciones_totales': calificaciones.count(),
            })
        except:
            pass
    
    return render(request, 'dashboard.html', context)


class UsuarioListView(AdministradorRequiredMixin, LoginRequiredMixin, ListView):
    """Lista de usuarios del sistema - Solo para administrador"""
    model = User
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search,
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset.order_by('-date_joined')


class UsuarioCreateView(AdministradorRequiredMixin, LoginRequiredMixin, CreateView):
    """Crear nuevo usuario - Solo para administrador"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')
    
    def form_valid(self, form):
        # Guardar el usuario primero
        response = super().form_valid(form)
        
        # Extraer el rol del formulario
        rol = form.cleaned_data.get('rol', 'coordinador')
        
        # Crear PerfilUsuario con el rol especificado
        PerfilUsuario.objects.create(
            usuario=self.object,
            rol=rol
        )
        
        messages.success(self.request, f"Usuario '{form.instance.username}' creado exitosamente con rol de {rol}.")
        return response


class UsuarioEditarView(AdministradorRequiredMixin, LoginRequiredMixin, UpdateView):
    """Editar usuario - Solo para administrador"""
    model = User
    form_class = UsuarioEditarForm
    template_name = 'usuarios/usuario_editar.html'
    success_url = reverse_lazy('usuario_list')
    
    def get_object(self, queryset=None):
        usuario_id = self.kwargs.get('pk')
        try:
            return User.objects.get(pk=usuario_id)
        except User.DoesNotExist:
            raise Http404("Usuario no encontrado")
    
    def form_valid(self, form):
        messages.success(self.request, f"Usuario '{form.instance.username}' actualizado exitosamente.")
        return super().form_valid(form)


class UsuarioEliminarView(AdministradorRequiredMixin, LoginRequiredMixin, DeleteView):
    """Eliminar usuario - Solo para administrador"""
    model = User
    template_name = 'usuarios/usuario_confirmar_eliminar.html'
    success_url = reverse_lazy('usuario_list')
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        username = user.username
        messages.success(request, f"Usuario '{username}' eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


class PerfilUsuarioEditarView(AdministradorRequiredMixin, LoginRequiredMixin, UpdateView):
    """Editar perfil de usuario (rol, datos) - Solo para administrador"""
    model = PerfilUsuario
    form_class = PerfilUsuarioEditarForm
    template_name = 'usuarios/perfil_editar_admin.html'
    success_url = reverse_lazy('usuario_list')
    
    def get_object(self, queryset=None):
        usuario_id = self.kwargs.get('usuario_id')
        try:
            return PerfilUsuario.objects.get(usuario_id=usuario_id)
        except PerfilUsuario.DoesNotExist:
            raise Http404("Perfil de usuario no encontrado")
    
    def form_valid(self, form):
        messages.success(self.request, f"Perfil de usuario actualizado exitosamente.")
        return super().form_valid(form)


class PerfilActualizarView(LoginRequiredMixin, UpdateView):
    """Actualizar perfil del usuario logueado"""
    model = PerfilUsuario
    form_class = PerfilUsuarioForm
    template_name = 'usuarios/perfil_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_object(self, queryset=None):
        return self.request.user.perfil
    
    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado exitosamente.")
        return super().form_valid(form)


class CambiarContraseniaView(AdministradorRequiredMixin, LoginRequiredMixin, FormView):
    """Admin puede cambiar contraseña de cualquier usuario"""
    form_class = SetPasswordForm
    template_name = 'usuarios/cambiar_contrasena.html'
    success_url = reverse_lazy('usuario_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        usuario_id = self.kwargs.get('pk')
        kwargs['user'] = User.objects.get(pk=usuario_id)
        return kwargs
    
    def form_valid(self, form):
        form.save()
        usuario = User.objects.get(pk=self.kwargs.get('pk'))
        messages.success(self.request, f"Contraseña de '{usuario.username}' cambiada exitosamente.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = User.objects.get(pk=self.kwargs.get('pk'))
        return context


class CambiarContraseniaPropia(LoginRequiredMixin, FormView):
    """Cualquier usuario logueado puede cambiar su propia contraseña"""
    form_class = SetPasswordForm
    template_name = 'usuarios/cambiar_contrasena_propia.html'
    success_url = reverse_lazy('dashboard')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Tu contraseña ha sido cambiada exitosamente.")
        return super().form_valid(form)
