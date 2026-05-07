from django.urls import path
from . import views

app_name = 'academico'

# URLs para COORDINADOR
coordinador_patterns = [
    # Maestrías
    path('maestrias/', views.MaestriaListView.as_view(), name='maestria_list'),
    path('maestria/crear/', views.MaestriaCreateView.as_view(), name='maestria_create'),
    path('maestria/<int:pk>/editar/', views.MaestriaUpdateView.as_view(), name='maestria_update'),
    path('maestria/<int:pk>/', views.MaestriaDetailView.as_view(), name='maestria_detail'),
    
    # Módulos
    path('maestria/<int:maestria_id>/modulos/', views.ModuloListView.as_view(), name='modulo_list'),
    path('maestria/<int:maestria_id>/modulo/crear/', views.ModuloCreateView.as_view(), name='modulo_create'),
    path('modulo/<int:pk>/editar/', views.ModuloUpdateView.as_view(), name='modulo_update'),
    
    # Asignaturas
    path('modulo/<int:modulo_id>/asignaturas/', views.AsignaturaListView.as_view(), name='asignatura_list'),
    path('modulo/<int:modulo_id>/asignatura/crear/', views.AsignaturaCreateView.as_view(), name='asignatura_create'),
    path('asignatura/<int:pk>/editar/', views.AsignaturaUpdateView.as_view(), name='asignatura_update'),
    
    # Profesor-Asignatura
    path('asignatura/<int:asignatura_id>/profesores/', views.ProfesorAsignaturaListView.as_view(), name='profesor_asignatura_list'),
    path('asignatura/<int:asignatura_id>/profesor/asignar/', views.ProfesorAsignaturaCreateView.as_view(), name='profesor_asignatura_create'),
]

# URLs para PROFESOR
profesor_patterns = [
    path('profesor/asignaturas/', views.ProfesorAsignaturasView.as_view(), name='profesor_asignaturas'),
    path('profesor/asignatura/<int:asignatura_id>/calificaciones/', views.RegistrarCalificacionesView.as_view(), name='registrar_calificaciones'),
    path('profesor/asignatura/<int:asignatura_id>/estudiante/<int:estudiante_id>/calificar/', views.crear_calificacion_estudiante, name='crear_calificacion'),
]

# URLs para SECRETARIA
secretaria_patterns = [
    path('secretaria/estudiantes/', views.EstudianteListView.as_view(), name='estudiante_list'),
    path('secretaria/inscripcion/crear/', views.InscribirEstudianteEnModuloView.as_view(), name='inscripcion_modulo_create'),
    path('secretaria/calificacion/<int:pk>/editar/', views.EditarCalificacionView.as_view(), name='editar_calificacion'),
    path('secretaria/estudiante/<int:estudiante_id>/expediente/', views.ver_expediente_estudiante, name='ver_expediente_estudiante'),
    path('secretaria/calificaciones/', views.CalificacionesListView.as_view(), name='calificaciones_list'),
    path('secretaria/estudiante/<int:estudiante_id>/acta-calificaciones/', views.exportar_acta_calificaciones, name='exportar_acta_calificaciones'),
    path('secretaria/estudiante/<int:estudiante_id>/acta-culminacion/generar/', views.generar_acta_culminacion, name='generar_acta_culminacion'),
    path('secretaria/estudiante/<int:estudiante_id>/acta-culminacion/', views.exportar_acta_culminacion, name='exportar_acta_culminacion'),
]

# URLs para ESTUDIANTE
estudiante_patterns = [
    path('estudiante/mi-expediente/', views.mi_expediente, name='mi_expediente'),
    path('estudiante/mis-notas/', views.mis_notas, name='mis_notas'),
]

# Combinar todas las URLs
urlpatterns = coordinador_patterns + profesor_patterns + secretaria_patterns + estudiante_patterns
