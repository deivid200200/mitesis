from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Avg, Count
from django.http import HttpResponseForbidden, HttpResponse
from django.template.loader import render_to_string
from .models import (
    Maestria, ModuloMaestria, Asignatura, ProfesorAsignatura,
    Estudiante, Calificacion, InscripcionModulo, Expediente, ActaCulminacion
)
from .forms import (
    MaestriaForm, ModuloMaestriaForm, AsignaturaForm, ProfesorAsignaturaForm,
    EstudianteForm, CalificacionForm, CalificacionEditForm, InscripcionModuloForm
)


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def calcular_promedio_ponderado(calificaciones):
    """
    Calcula el promedio ponderado a partir de una lista de calificaciones.
    Promedio = (suma de nota_final × créditos) / suma de créditos
    
    Args:
        calificaciones: QuerySet o lista de objetos Calificacion
    
    Returns:
        Decimal: Promedio ponderado (0 si no hay calificaciones válidas)
    """
    from decimal import Decimal
    
    suma_ponderada = Decimal('0')
    suma_creditos = Decimal('0')
    
    for cal in calificaciones:
        try:
            if cal.nota_final and cal.asignatura and cal.asignatura.creditos:
                nota = Decimal(str(cal.nota_final))
                creditos = Decimal(str(cal.asignatura.creditos))
                suma_ponderada += nota * creditos
                suma_creditos += creditos
        except (ValueError, TypeError, AttributeError):
            # Ignorar calificaciones con datos inválidos
            continue
    
    if suma_creditos > 0:
        resultado = suma_ponderada / suma_creditos
        return resultado.quantize(Decimal('0.01'))
    return Decimal('0.00')


# ============================================================================
# MIXINS PARA CONTROL DE ACCESO
# ============================================================================

class RolRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario tenga un rol específico"""
    required_role = None
    
    def test_func(self):
        if not hasattr(self.request.user, 'perfil'):
            return False
        return self.request.user.perfil.rol == self.required_role


class CoordinadorRequiredMixin(RolRequiredMixin):
    """Mixin para requerir que sea coordinador"""
    required_role = 'coordinador'


class ProfesorRequiredMixin(RolRequiredMixin):
    """Mixin para requerir que sea profesor"""
    required_role = 'profesor'


class SecretariaRequiredMixin(RolRequiredMixin):
    """Mixin para requerir que sea secretaria docente"""
    required_role = 'secretaria'


class AdminRequiredMixin(RolRequiredMixin):
    """Mixin para requerir que sea administrador"""
    required_role = 'administrador'


# ============================================================================
# VISTAS PARA COORDINADOR
# ============================================================================

class MaestriaListView(LoginRequiredMixin, CoordinadorRequiredMixin, ListView):
    """Lista de maestrías del coordinador"""
    model = Maestria
    template_name = 'academico/coordinador/maestria_list.html'
    context_object_name = 'maestrias'
    paginate_by = 10
    
    def get_queryset(self):
        return Maestria.objects.filter(coordinador=self.request.user)


class MaestriaCreateView(LoginRequiredMixin, CoordinadorRequiredMixin, CreateView):
    """Crear nueva maestría"""
    model = Maestria
    form_class = MaestriaForm
    template_name = 'academico/coordinador/maestria_form.html'
    success_url = reverse_lazy('maestria_list')
    
    def form_valid(self, form):
        form.instance.coordinador = self.request.user
        messages.success(self.request, f"Maestría '{form.instance.nombre}' creada exitosamente.")
        return super().form_valid(form)


class MaestriaUpdateView(LoginRequiredMixin, CoordinadorRequiredMixin, UpdateView):
    """Actualizar maestría"""
    model = Maestria
    form_class = MaestriaForm
    template_name = 'academico/coordinador/maestria_form.html'
    success_url = reverse_lazy('maestria_list')
    
    def get_queryset(self):
        return Maestria.objects.filter(coordinador=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f"Maestría '{form.instance.nombre}' actualizada exitosamente.")
        return super().form_valid(form)


class MaestriaDetailView(LoginRequiredMixin, CoordinadorRequiredMixin, DetailView):
    """Detalles de maestría con sus módulos y asignaturas"""
    model = Maestria
    template_name = 'academico/coordinador/maestria_detail.html'
    
    def get_queryset(self):
        return Maestria.objects.filter(coordinador=self.request.user)


# ============================================================================
# VISTAS PARA MÓDULOS
# ============================================================================

class ModuloListView(LoginRequiredMixin, CoordinadorRequiredMixin, ListView):
    """Lista de módulos de una maestría"""
    model = ModuloMaestria
    template_name = 'academico/coordinador/modulo_list.html'
    context_object_name = 'modulos'
    paginate_by = 10
    
    def get_queryset(self):
        maestria_id = self.kwargs.get('maestria_id')
        return ModuloMaestria.objects.filter(maestria_id=maestria_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maestria_id = self.kwargs.get('maestria_id')
        context['maestria'] = Maestria.objects.get(id=maestria_id)
        return context


class ModuloCreateView(LoginRequiredMixin, CoordinadorRequiredMixin, CreateView):
    """Crear nuevo módulo"""
    model = ModuloMaestria
    form_class = ModuloMaestriaForm
    template_name = 'academico/coordinador/modulo_form.html'
    
    def get_success_url(self):
        return reverse('academico:modulo_list', kwargs={'maestria_id': self.object.maestria_id})
    
    def form_valid(self, form):
        maestria_id = self.kwargs.get('maestria_id')
        form.instance.maestria_id = maestria_id
        messages.success(self.request, "Módulo creado exitosamente.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maestria_id = self.kwargs.get('maestria_id')
        context['maestria'] = Maestria.objects.get(id=maestria_id)
        return context


class ModuloUpdateView(LoginRequiredMixin, CoordinadorRequiredMixin, UpdateView):
    """Actualizar módulo"""
    model = ModuloMaestria
    form_class = ModuloMaestriaForm
    template_name = 'academico/coordinador/modulo_form.html'
    
    def get_success_url(self):
        return reverse('academico:modulo_list', kwargs={'maestria_id': self.object.maestria_id})
    
    def form_valid(self, form):
        messages.success(self.request, "Módulo actualizado exitosamente.")
        return super().form_valid(form)


# ============================================================================
# VISTAS PARA ASIGNATURAS
# ============================================================================

class AsignaturaListView(LoginRequiredMixin, CoordinadorRequiredMixin, ListView):
    """Lista de asignaturas de un módulo"""
    model = Asignatura
    template_name = 'academico/coordinador/asignatura_list.html'
    context_object_name = 'asignaturas'
    paginate_by = 10
    
    def get_queryset(self):
        modulo_id = self.kwargs.get('modulo_id')
        return Asignatura.objects.filter(modulo_id=modulo_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modulo_id = self.kwargs.get('modulo_id')
        context['modulo'] = ModuloMaestria.objects.get(id=modulo_id)
        return context


class AsignaturaCreateView(LoginRequiredMixin, CoordinadorRequiredMixin, CreateView):
    """Crear nueva asignatura"""
    model = Asignatura
    form_class = AsignaturaForm
    template_name = 'academico/coordinador/asignatura_form.html'
    
    def get_success_url(self):
        return reverse('academico:asignatura_list', kwargs={'modulo_id': self.object.modulo_id})
    
    def form_valid(self, form):
        modulo_id = self.kwargs.get('modulo_id')
        form.instance.modulo_id = modulo_id
        messages.success(self.request, "Asignatura creada exitosamente.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modulo_id = self.kwargs.get('modulo_id')
        context['modulo'] = ModuloMaestria.objects.get(id=modulo_id)
        return context


class AsignaturaUpdateView(LoginRequiredMixin, CoordinadorRequiredMixin, UpdateView):
    """Actualizar asignatura"""
    model = Asignatura
    form_class = AsignaturaForm
    template_name = 'academico/coordinador/asignatura_form.html'
    
    def get_success_url(self):
        return reverse('academico:asignatura_list', kwargs={'modulo_id': self.object.modulo_id})
    
    def form_valid(self, form):
        messages.success(self.request, "Asignatura actualizada exitosamente.")
        return super().form_valid(form)


# ============================================================================
# VISTAS PARA PROFESOR-ASIGNATURA
# ============================================================================

class ProfesorAsignaturaListView(LoginRequiredMixin, CoordinadorRequiredMixin, ListView):
    """Lista de profesores asignados a asignatura"""
    model = ProfesorAsignatura
    template_name = 'academico/coordinador/profesor_asignatura_list.html'
    context_object_name = 'asignaciones'
    
    def get_queryset(self):
        asignatura_id = self.kwargs.get('asignatura_id')
        return ProfesorAsignatura.objects.filter(asignatura_id=asignatura_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asignatura_id = self.kwargs.get('asignatura_id')
        context['asignatura'] = Asignatura.objects.get(id=asignatura_id)
        return context


class ProfesorAsignaturaCreateView(LoginRequiredMixin, CoordinadorRequiredMixin, CreateView):
    """Asignar profesor a asignatura"""
    model = ProfesorAsignatura
    form_class = ProfesorAsignaturaForm
    template_name = 'academico/coordinador/profesor_asignatura_form.html'
    
    def get_success_url(self):
        return reverse('academico:profesor_asignatura_list', kwargs={'asignatura_id': self.object.asignatura_id})
    
    def form_valid(self, form):
        asignatura_id = self.kwargs.get('asignatura_id')
        asignatura = get_object_or_404(Asignatura, id=asignatura_id)
        form.instance.asignatura = asignatura
        messages.success(self.request, f"Profesor '{form.instance.profesor.get_full_name()}' asignado a '{asignatura.nombre}' exitosamente.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asignatura_id = self.kwargs.get('asignatura_id')
        context['asignatura'] = Asignatura.objects.get(id=asignatura_id)
        return context


# ============================================================================
# VISTAS PARA PROFESOR - REGISTRAR CALIFICACIONES
# ============================================================================

class ProfesorAsignaturasView(LoginRequiredMixin, ProfesorRequiredMixin, ListView):
    """Lista de asignaturas asignadas al profesor"""
    model = ProfesorAsignatura
    template_name = 'academico/profesor/mis_asignaturas.html'
    context_object_name = 'asignaciones'
    
    def get_queryset(self):
        return ProfesorAsignatura.objects.filter(profesor=self.request.user, activo=True)


class RegistrarCalificacionesView(LoginRequiredMixin, ProfesorRequiredMixin, ListView):
    """Registrar calificaciones de estudiantes en una asignatura"""
    model = Calificacion
    template_name = 'academico/profesor/registrar_calificaciones.html'
    context_object_name = 'calificaciones'
    paginate_by = 30
    
    def get_queryset(self):
        asignatura_id = self.kwargs.get('asignatura_id')
        asignatura = get_object_or_404(Asignatura, id=asignatura_id)
        
        # Verificar que el profesor está asignado a esta asignatura
        try:
            profesor_asignatura = ProfesorAsignatura.objects.get(
                profesor=self.request.user,
                asignatura=asignatura
            )
        except ProfesorAsignatura.DoesNotExist:
            return Calificacion.objects.none()
        
        return Calificacion.objects.filter(
            asignatura_id=asignatura_id, 
            profesor=profesor_asignatura
        ).select_related('estudiante', 'asignatura').order_by('estudiante__usuario__first_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asignatura_id = self.kwargs.get('asignatura_id')
        context['asignatura'] = Asignatura.objects.get(id=asignatura_id)
        
        # Obtener todos los estudiantes inscritos en esta asignatura
        # (independientemente de si tienen calificación)
        inscripciones = InscripcionModulo.objects.filter(
            modulo=context['asignatura'].modulo
        ).select_related('estudiante')
        context['estudiantes_inscritos'] = [insc.estudiante for insc in inscripciones]
        
        return context


@login_required
def crear_calificacion_estudiante(request, asignatura_id, estudiante_id):
    """Crear/actualizar calificación de un estudiante"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'profesor':
        return HttpResponseForbidden()
    
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    
    try:
        profesor_asignatura = ProfesorAsignatura.objects.get(
            profesor=request.user,
            asignatura=asignatura
        )
    except ProfesorAsignatura.DoesNotExist:
        return HttpResponseForbidden()
    
    calificacion, created = Calificacion.objects.get_or_create(
        estudiante=estudiante,
        asignatura=asignatura,
        profesor=profesor_asignatura
    )
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Calificación registrada exitosamente.")
            return redirect('registrar_calificaciones', asignatura_id=asignatura_id)
    else:
        form = CalificacionForm(instance=calificacion)
    
    return render(request, 'academico/profesor/calificacion_form.html', {
        'form': form,
        'estudiante': estudiante,
        'asignatura': asignatura,
        'calificacion': calificacion
    })


# ============================================================================
# VISTAS PARA SECRETARIA - GESTIÓN DE ESTUDIANTES
# ============================================================================

class EstudianteListView(LoginRequiredMixin, SecretariaRequiredMixin, ListView):
    """Lista de estudiantes"""
    model = Estudiante
    template_name = 'academico/secretaria/estudiante_list.html'
    context_object_name = 'estudiantes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Estudiante.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(usuario__first_name__icontains=search) |
                Q(usuario__last_name__icontains=search) |
                Q(matricula__icontains=search)
            )
        return queryset


class InscribirEstudianteEnModuloView(LoginRequiredMixin, SecretariaRequiredMixin, CreateView):
    """Inscribir estudiante en un módulo"""
    model = InscripcionModulo
    form_class = InscripcionModuloForm
    template_name = 'academico/secretaria/inscripcion_modulo_form.html'
    success_url = reverse_lazy('estudiante_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Estudiante inscrito exitosamente en el módulo.")
        return super().form_valid(form)


class EditarCalificacionView(LoginRequiredMixin, SecretariaRequiredMixin, UpdateView):
    """Secretaria puede editar calificaciones"""
    model = Calificacion
    form_class = CalificacionEditForm
    template_name = 'academico/secretaria/editar_calificacion.html'
    
    def get_success_url(self):
        return reverse_lazy('ver_expediente_estudiante', kwargs={'estudiante_id': self.object.estudiante_id})
    
    def form_valid(self, form):
        messages.success(self.request, "Calificación actualizada exitosamente.")
        return super().form_valid(form)


@login_required
def ver_expediente_estudiante(request, estudiante_id):
    """Ver expediente completo del estudiante"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'secretaria':
        return HttpResponseForbidden()
    
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    expediente = Expediente.objects.filter(estudiante=estudiante).first()
    calificaciones = Calificacion.objects.filter(estudiante=estudiante)
    inscripciones = InscripcionModulo.objects.filter(estudiante=estudiante)
    
    context = {
        'estudiante': estudiante,
        'expediente': expediente,
        'calificaciones': calificaciones,
        'inscripciones': inscripciones
    }
    return render(request, 'academico/secretaria/expediente_estudiante.html', context)


class CalificacionesListView(LoginRequiredMixin, SecretariaRequiredMixin, ListView):
    """Listar todas las calificaciones para editar"""
    model = Calificacion
    template_name = 'academico/secretaria/calificaciones_list.html'
    context_object_name = 'calificaciones'
    paginate_by = 30
    
    def get_queryset(self):
        queryset = Calificacion.objects.select_related('estudiante', 'asignatura')
        search = self.request.GET.get('search')
        estado = self.request.GET.get('estado')
        
        if search:
            queryset = queryset.filter(
                Q(estudiante__usuario__first_name__icontains=search) |
                Q(estudiante__usuario__last_name__icontains=search) |
                Q(asignatura__nombre__icontains=search)
            )
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset.order_by('-fecha_actualizacion')


@login_required
def exportar_acta_calificaciones(request, estudiante_id):
    """Exportar acta de calificaciones como PDF"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'secretaria':
        return HttpResponseForbidden()
    
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    expediente = Expediente.objects.filter(estudiante=estudiante).first()
    calificaciones = Calificacion.objects.filter(estudiante=estudiante).select_related('asignatura')
    
    # Obtener el coordinador de la maestría del estudiante
    coordinador = None
    if expediente and expediente.maestria:
        coordinador = expediente.maestria.coordinador
    
    # Obtener la secretaria logueada
    secretaria = request.user
    
    # Calcular el promedio ponderado
    promedio_ponderado = calcular_promedio_ponderado(calificaciones)
    
    context = {
        'estudiante': estudiante,
        'expediente': expediente,
        'calificaciones': calificaciones,
        'coordinador': coordinador,
        'secretaria': secretaria,
        'promedio_ponderado': promedio_ponderado,
    }
    
    # Renderizar como HTML que puede ser impreso como PDF
    html_string = render_to_string('academico/secretaria/acta_calificaciones_pdf.html', context)
    
    response = HttpResponse(content_type='text/html; charset=utf-8')
    response.write(html_string)
    return response


@login_required
def generar_acta_culminacion(request, estudiante_id):
    """Generar acta de culminación si todas las notas están aprobadas"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'secretaria':
        return HttpResponseForbidden()
    
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    expediente = get_object_or_404(Expediente, estudiante=estudiante)
    
    # Verificar si ya existe el acta (usando filter para evitar RelatedObjectDoesNotExist)
    acta_existente = ActaCulminacion.objects.filter(expediente=expediente).first()
    if acta_existente:
        messages.warning(request, "El acta de culminación ya existe para este estudiante.")
        return redirect('ver_expediente_estudiante', estudiante_id=estudiante_id)
    
    # Verificar que hay maestría asignada
    if not expediente.maestria:
        messages.error(request, "El estudiante no tiene maestría asignada.")
        return redirect('ver_expediente_estudiante', estudiante_id=estudiante_id)
    
    # Obtener todas las calificaciones del estudiante en esa maestría
    calificaciones = Calificacion.objects.filter(
        estudiante=estudiante,
        asignatura__modulo__maestria=expediente.maestria
    ).select_related('asignatura')
    
    if not calificaciones.exists():
        messages.error(request, "El estudiante no tiene calificaciones registradas.")
        return redirect('ver_expediente_estudiante', estudiante_id=estudiante_id)
    
    # Verificar que todas estén aprobadas
    todas_aprobadas = all(cal.estado == 'aprobada' for cal in calificaciones)
    
    if not todas_aprobadas:
        calificaciones_pendientes = calificaciones.exclude(estado='aprobada')
        count = calificaciones_pendientes.count()
        messages.error(request, f"Hay {count} asignatura(s) que no están aprobadas. No se puede generar el acta.")
        return redirect('ver_expediente_estudiante', estudiante_id=estudiante_id)
    
    # Calcular promedio ponderado usando la función auxiliar
    promedio_final = calcular_promedio_ponderado(calificaciones)
    
    # Crear el acta
    from reportes.views import generar_numero_acta
    acta = ActaCulminacion.objects.create(
        expediente=expediente,
        numero_acta=generar_numero_acta(),
        promedio_final=promedio_final,
        titulo_otorgado=f"Magister en {expediente.maestria.nombre}",
    )
    
    messages.success(request, f"Acta de culminación generada exitosamente: {acta.numero_acta}")
    return redirect('ver_expediente_estudiante', estudiante_id=estudiante_id)


@login_required
def exportar_acta_culminacion(request, estudiante_id):
    """Exportar acta de culminación como PDF"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'secretaria':
        return HttpResponseForbidden()
    
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    expediente = get_object_or_404(Expediente, estudiante=estudiante)
    acta = ActaCulminacion.objects.filter(expediente=expediente).first()
    
    if not acta:
        messages.error(request, "No hay acta de culminación registrada para este estudiante.")
        return redirect('ver_expediente_estudiante', estudiante_id=estudiante_id)
    
    # Obtener el coordinador de la maestría
    coordinador = None
    if expediente and expediente.maestria:
        coordinador = expediente.maestria.coordinador
    
    # Obtener la secretaria logueada
    secretaria = request.user
    
    context = {
        'estudiante': estudiante,
        'expediente': expediente,
        'acta': acta,
        'coordinador': coordinador,
        'secretaria': secretaria,
    }
    
    # Renderizar como HTML que puede ser impreso como PDF
    html_string = render_to_string('academico/secretaria/acta_culminacion_pdf.html', context)
    
    response = HttpResponse(content_type='text/html; charset=utf-8')
    response.write(html_string)
    return response


# ============================================================================
# VISTAS PARA ESTUDIANTE
# ============================================================================

@login_required
def mi_expediente(request):
    """Ver mi expediente como estudiante"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'estudiante':
        return HttpResponseForbidden()
    
    try:
        estudiante = request.user.estudiante
    except Estudiante.DoesNotExist:
        messages.error(request, "No se encontró tu registro como estudiante.")
        return redirect('dashboard')
    
    expediente = Expediente.objects.filter(estudiante=estudiante).first()
    calificaciones = Calificacion.objects.filter(estudiante=estudiante)
    inscripciones = InscripcionModulo.objects.filter(estudiante=estudiante)
    
    context = {
        'estudiante': estudiante,
        'expediente': expediente,
        'calificaciones': calificaciones,
        'inscripciones': inscripciones
    }
    return render(request, 'academico/estudiante/mi_expediente.html', context)


@login_required
def mis_notas(request):
    """Ver mis notas como estudiante"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'estudiante':
        return HttpResponseForbidden()
    
    try:
        estudiante = request.user.estudiante
    except Estudiante.DoesNotExist:
        messages.error(request, "No se encontró tu registro como estudiante.")
        return redirect('dashboard')
    
    calificaciones = Calificacion.objects.filter(estudiante=estudiante).select_related('asignatura')
    
    context = {
        'calificaciones': calificaciones,
        'promedio': calificaciones.aggregate(Avg('nota_final'))['nota_final__avg'] or 0
    }
    return render(request, 'academico/estudiante/mis_notas.html', context)

