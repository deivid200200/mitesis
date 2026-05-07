from django.contrib import admin
from .models import (
    Maestria, ModuloMaestria, Asignatura, ProfesorAsignatura, 
    Estudiante, InscripcionModulo, Calificacion, Expediente, ActaCulminacion
)


@admin.register(Maestria)
class MaestriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'coordinador', 'duracion_semestres', 'activa']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre', 'codigo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(ModuloMaestria)
class ModuloMaestriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'maestria', 'semestre', 'activo']
    list_filter = ['maestria', 'activo']
    search_fields = ['nombre', 'maestria__nombre']
    readonly_fields = ['fecha_inicio', 'fecha_fin']


class AsignaturaInline(admin.TabularInline):
    model = Asignatura
    extra = 1


@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'modulo', 'creditos', 'es_obligatoria', 'activa']
    list_filter = ['modulo', 'es_obligatoria', 'activa']
    search_fields = ['nombre', 'codigo']


@admin.register(ProfesorAsignatura)
class ProfesorAsignaturaAdmin(admin.ModelAdmin):
    list_display = ['profesor', 'asignatura', 'fecha_asignacion', 'activo']
    list_filter = ['asignatura__modulo', 'activo']
    search_fields = ['profesor__first_name', 'profesor__last_name', 'asignatura__nombre']


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'matricula', 'fecha_ingreso', 'estado']
    list_filter = ['estado', 'fecha_ingreso']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'matricula']
    readonly_fields = ['fecha_ingreso']


@admin.register(InscripcionModulo)
class InscripcionModuloAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'maestria', 'modulo', 'estado_inscripcion']
    list_filter = ['maestria', 'estado_inscripcion']
    search_fields = ['estudiante__usuario__first_name', 'estudiante__usuario__last_name']
    readonly_fields = ['fecha_inscripcion']


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'asignatura', 'nota_final', 'estado']
    list_filter = ['asignatura__modulo', 'estado', 'fecha_registro']
    search_fields = ['estudiante__usuario__first_name', 'asignatura__nombre']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']


@admin.register(Expediente)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'maestria', 'promedio_general', 'estado_general']
    list_filter = ['maestria', 'estado_general']
    search_fields = ['estudiante__usuario__first_name', 'estudiante__usuario__last_name']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(ActaCulminacion)
class ActaCulminacionAdmin(admin.ModelAdmin):
    list_display = ['numero_acta', 'expediente', 'promedio_final', 'estado', 'fecha_emision']
    list_filter = ['estado', 'fecha_emision']
    search_fields = ['numero_acta', 'expediente__estudiante__usuario__first_name']
    readonly_fields = ['fecha_emision']
