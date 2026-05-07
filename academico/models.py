from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class Maestria(models.Model):
    """Modelo para las maestrías"""
    nombre = models.CharField(max_length=200, unique=True, verbose_name='Nombre de la Maestría')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código')
    coordinador = models.ForeignKey(User, on_delete=models.PROTECT, 
                                   limit_choices_to={'perfil__rol': 'coordinador'},
                                   related_name='maestrias_coordinadas',
                                   verbose_name='Coordinador')
    creditos_totales = models.IntegerField(default=0, verbose_name='Créditos Totales')
    duracion_semestres = models.IntegerField(default=4, verbose_name='Duración en Semestres')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Maestría"
        verbose_name_plural = "Maestrías"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class ModuloMaestria(models.Model):
    """Modelo para los módulos/semestres de una maestría"""
    maestria = models.ForeignKey(Maestria, on_delete=models.CASCADE, 
                                related_name='modulos', verbose_name='Maestría')
    numero_modulo = models.IntegerField(verbose_name='Número de Módulo')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Módulo')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    semestre = models.IntegerField(verbose_name='Semestre', validators=[MinValueValidator(1)])
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fecha de Finalización')
    
    class Meta:
        verbose_name = "Módulo de Maestría"
        verbose_name_plural = "Módulos de Maestría"
        ordering = ['maestria', 'semestre']
        unique_together = ['maestria', 'numero_modulo']
    
    def __str__(self):
        return f"{self.maestria.nombre} - Módulo {self.numero_modulo}"


class Asignatura(models.Model):
    """Modelo para las asignaturas de un módulo"""
    modulo = models.ForeignKey(ModuloMaestria, on_delete=models.CASCADE, 
                              related_name='asignaturas', verbose_name='Módulo')
    nombre = models.CharField(max_length=150, verbose_name='Nombre de la Asignatura')
    codigo = models.CharField(max_length=50, verbose_name='Código de Asignatura')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    creditos = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Créditos')
    horas_teoricas = models.IntegerField(default=0, verbose_name='Horas Teóricas')
    horas_practicas = models.IntegerField(default=0, verbose_name='Horas Prácticas')
    es_obligatoria = models.BooleanField(default=True, verbose_name='Es Obligatoria')
    calificacion_minima = models.DecimalField(max_digits=3, decimal_places=1, default=3.0,
                                             verbose_name='Calificación Mínima')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    
    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        ordering = ['modulo', 'nombre']
        unique_together = ['modulo', 'codigo']
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class ProfesorAsignatura(models.Model):
    """Relación entre Profesor y Asignatura"""
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, 
                                limit_choices_to={'perfil__rol': 'profesor'},
                                related_name='asignaturas_profesor',
                                verbose_name='Profesor')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE,
                                  related_name='profesores',
                                  verbose_name='Asignatura')
    fecha_asignacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Asignación')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = "Profesor-Asignatura"
        verbose_name_plural = "Profesor-Asignatura"
        unique_together = ['profesor', 'asignatura']
        ordering = ['asignatura', 'profesor']
    
    def __str__(self):
        return f"{self.profesor.get_full_name()} - {self.asignatura.nombre}"


class Estudiante(models.Model):
    """Modelo para información adicional del estudiante"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,
                                  limit_choices_to={'perfil__rol': 'estudiante'},
                                  related_name='estudiante',
                                  verbose_name='Usuario')
    matricula = models.CharField(max_length=50, unique=True, verbose_name='Matrícula')
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de Ingreso')
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
            ('egresado', 'Egresado'),
            ('retirado', 'Retirado'),
        ],
        default='activo',
        verbose_name='Estado'
    )
    
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['usuario__first_name']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.matricula}"


class InscripcionModulo(models.Model):
    """Inscripción del estudiante en un módulo de maestría"""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE,
                                  related_name='inscripciones_modulo',
                                  verbose_name='Estudiante')
    modulo = models.ForeignKey(ModuloMaestria, on_delete=models.PROTECT,
                              related_name='inscripciones',
                              verbose_name='Módulo')
    maestria = models.ForeignKey(Maestria, on_delete=models.PROTECT,
                                related_name='inscripciones_estudiantes',
                                verbose_name='Maestría')
    fecha_inscripcion = models.DateField(auto_now_add=True, verbose_name='Fecha de Inscripción')
    estado_inscripcion = models.CharField(
        max_length=20,
        choices=[
            ('inscrito', 'Inscrito'),
            ('cursando', 'Cursando'),
            ('completado', 'Completado'),
            ('retirado', 'Retirado'),
        ],
        default='inscrito',
        verbose_name='Estado'
    )
    
    class Meta:
        verbose_name = "Inscripción en Módulo"
        verbose_name_plural = "Inscripciones en Módulo"
        unique_together = ['estudiante', 'modulo']
        ordering = ['maestria', 'estudiante']
    
    def __str__(self):
        return f"{self.estudiante} - {self.modulo}"


class Calificacion(models.Model):
    """Calificaciones de estudiantes por asignatura"""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE,
                                  related_name='calificaciones',
                                  verbose_name='Estudiante')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE,
                                  related_name='calificaciones',
                                  verbose_name='Asignatura')
    profesor = models.ForeignKey(ProfesorAsignatura, on_delete=models.PROTECT,
                                related_name='calificaciones',
                                verbose_name='Profesor')
    nota_final = models.DecimalField(max_digits=4, decimal_places=2,
                                    validators=[MinValueValidator(0), MaxValueValidator(5)],
                                    verbose_name='Nota Final')
    nota_parcial1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                       validators=[MinValueValidator(0), MaxValueValidator(5)],
                                       verbose_name='Nota Parcial 1')
    nota_parcial2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                       validators=[MinValueValidator(0), MaxValueValidator(5)],
                                       verbose_name='Nota Parcial 2')
    nota_trabajo = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                      validators=[MinValueValidator(0), MaxValueValidator(5)],
                                      verbose_name='Nota de Trabajo')
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('en_curso', 'En Curso'),
            ('aprobada', 'Aprobada'),
            ('reprobada', 'Reprobada'),
        ],
        default='pendiente',
        verbose_name='Estado'
    )
    fecha_registro = models.DateField(auto_now_add=True, verbose_name='Fecha de Registro')
    fecha_actualizacion = models.DateField(auto_now=True, verbose_name='Fecha de Actualización')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    
    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        unique_together = ['estudiante', 'asignatura']
        ordering = ['estudiante', 'asignatura']
    
    def __str__(self):
        return f"{self.estudiante} - {self.asignatura}: {self.nota_final}"
    
    def save(self, *args, **kwargs):
        """Actualizar estado automáticamente según la nota final"""
        if self.nota_final:
            if self.nota_final >= self.asignatura.calificacion_minima:
                self.estado = 'aprobada'
            else:
                self.estado = 'reprobada'
        super().save(*args, **kwargs)


class Expediente(models.Model):
    """Expediente académico del estudiante"""
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE,
                                     related_name='expediente',
                                     verbose_name='Estudiante')
    maestria = models.ForeignKey(Maestria, on_delete=models.PROTECT,
                                related_name='expedientes',
                                verbose_name='Maestría')
    promedio_general = models.DecimalField(max_digits=4, decimal_places=2, default=0,
                                          verbose_name='Promedio General')
    creditos_cursados = models.IntegerField(default=0, verbose_name='Créditos Cursados')
    creditos_aprobados = models.IntegerField(default=0, verbose_name='Créditos Aprobados')
    asignaturas_completadas = models.IntegerField(default=0, verbose_name='Asignaturas Completadas')
    asignaturas_aprobadas = models.IntegerField(default=0, verbose_name='Asignaturas Aprobadas')
    estado_general = models.CharField(
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('completado', 'Completado'),
            ('en_prueba', 'En Prueba Académica'),
            ('suspendido', 'Suspendido'),
        ],
        default='activo',
        verbose_name='Estado General'
    )
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        ordering = ['estudiante']
    
    def __str__(self):
        return f"Expediente de {self.estudiante}"


class ActaCulminacion(models.Model):
    """Acta de culminación de la maestría"""
    expediente = models.OneToOneField(Expediente, on_delete=models.CASCADE,
                                     related_name='acta_culminacion',
                                     verbose_name='Expediente')
    fecha_emision = models.DateField(auto_now_add=True, verbose_name='Fecha de Emisión')
    fecha_graduacion = models.DateField(null=True, blank=True, verbose_name='Fecha de Graduación')
    numero_acta = models.CharField(max_length=100, unique=True, verbose_name='Número de Acta')
    promedio_final = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Promedio Final')
    titulo_otorgado = models.CharField(max_length=200, verbose_name='Título Otorgado')
    estado = models.CharField(
        max_length=20,
        choices=[
            ('generada', 'Generada'),
            ('registrada', 'Registrada'),
            ('entregada', 'Entregada'),
        ],
        default='generada',
        verbose_name='Estado'
    )
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    
    class Meta:
        verbose_name = "Acta de Culminación"
        verbose_name_plural = "Actas de Culminación"
        ordering = ['fecha_emision']
    
    def __str__(self):
        return f"Acta {self.numero_acta} - {self.expediente.estudiante}"
