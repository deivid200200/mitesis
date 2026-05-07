from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import (
    Maestria, ModuloMaestria, Asignatura, ProfesorAsignatura,
    Estudiante, Calificacion, InscripcionModulo
)


class MaestriaForm(forms.ModelForm):
    """Formulario para crear/editar maestrías"""
    class Meta:
        model = Maestria
        fields = ['nombre', 'codigo', 'descripcion', 'coordinador', 'creditos_totales', 'duracion_semestres', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Maestría'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: MAE-001'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'coordinador': forms.Select(attrs={'class': 'form-control'}),
            'creditos_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracion_semestres': forms.NumberInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['nombre'].initial = self.instance.nombre
            self.fields['codigo'].initial = self.instance.codigo
            self.fields['descripcion'].initial = self.instance.descripcion
            self.fields['coordinador'].initial = self.instance.coordinador
            self.fields['creditos_totales'].initial = self.instance.creditos_totales
            self.fields['duracion_semestres'].initial = self.instance.duracion_semestres
            self.fields['activa'].initial = self.instance.activa


class ModuloMaestriaForm(forms.ModelForm):
    """Formulario para crear/editar módulos de maestría"""
    class Meta:
        model = ModuloMaestria
        fields = ['numero_modulo', 'nombre', 'descripcion', 'semestre', 'fecha_inicio', 'fecha_fin', 'activo']
        widgets = {
            'numero_modulo': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del módulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['numero_modulo'].initial = self.instance.numero_modulo
            self.fields['nombre'].initial = self.instance.nombre
            self.fields['descripcion'].initial = self.instance.descripcion
            self.fields['semestre'].initial = self.instance.semestre
            self.fields['fecha_inicio'].initial = self.instance.fecha_inicio
            self.fields['fecha_fin'].initial = self.instance.fecha_fin
            self.fields['activo'].initial = self.instance.activo


class AsignaturaForm(forms.ModelForm):
    """Formulario para crear/editar asignaturas"""
    class Meta:
        model = Asignatura
        fields = ['nombre', 'codigo', 'descripcion', 'creditos', 
                 'horas_teoricas', 'horas_practicas', 'es_obligatoria', 'calificacion_minima', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'creditos': forms.NumberInput(attrs={'class': 'form-control'}),
            'horas_teoricas': forms.NumberInput(attrs={'class': 'form-control'}),
            'horas_practicas': forms.NumberInput(attrs={'class': 'form-control'}),
            'es_obligatoria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'calificacion_minima': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['nombre'].initial = self.instance.nombre
            self.fields['codigo'].initial = self.instance.codigo
            self.fields['descripcion'].initial = self.instance.descripcion
            self.fields['creditos'].initial = self.instance.creditos
            self.fields['horas_teoricas'].initial = self.instance.horas_teoricas
            self.fields['horas_practicas'].initial = self.instance.horas_practicas
            self.fields['es_obligatoria'].initial = self.instance.es_obligatoria
            self.fields['calificacion_minima'].initial = self.instance.calificacion_minima
            self.fields['activa'].initial = self.instance.activa


class ProfesorAsignaturaForm(forms.ModelForm):
    """Formulario para asignar profesores a asignaturas"""
    profesor = forms.ModelChoiceField(
        queryset=User.objects.filter(perfil__rol='profesor'),
        label='Profesor',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = ProfesorAsignatura
        fields = ['profesor', 'activo']
        widgets = {
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        profesor = cleaned_data.get('profesor')
        
        if profesor:
            # Verificar que el usuario seleccionado tenga rol de profesor
            if not hasattr(profesor, 'perfil') or profesor.perfil.rol != 'profesor':
                raise ValidationError("El usuario seleccionado no tiene el rol de profesor.")
        
        return cleaned_data


class EstudianteForm(forms.ModelForm):
    """Formulario para crear/editar información adicional de estudiantes"""
    class Meta:
        model = Estudiante
        fields = ['matricula', 'estado']
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: EST-2026-001'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class CalificacionForm(forms.ModelForm):
    """Formulario para registrar calificaciones"""
    class Meta:
        model = Calificacion
        fields = ['nota_parcial1', 'nota_parcial2', 'nota_trabajo', 'nota_final', 'observaciones']
        widgets = {
            'nota_parcial1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'nota_parcial2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'nota_trabajo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'nota_final': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['nota_parcial1'].initial = self.instance.nota_parcial1
            self.fields['nota_parcial2'].initial = self.instance.nota_parcial2
            self.fields['nota_trabajo'].initial = self.instance.nota_trabajo
            self.fields['nota_final'].initial = self.instance.nota_final
            self.fields['observaciones'].initial = self.instance.observaciones
    
    def clean(self):
        cleaned_data = super().clean()
        nota_final = cleaned_data.get('nota_final')
        
        if nota_final is not None:
            if not (0 <= nota_final <= 5):
                raise ValidationError("La nota final debe estar entre 0 y 5.")
        
        return cleaned_data


class CalificacionEditForm(forms.ModelForm):
    """Formulario para que la secretaria edite calificaciones"""
    class Meta:
        model = Calificacion
        fields = ['nota_final', 'observaciones']
        widgets = {
            'nota_final': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['nota_final'].initial = self.instance.nota_final
            self.fields['observaciones'].initial = self.instance.observaciones


class InscripcionModuloForm(forms.ModelForm):
    """Formulario para inscribir estudiantes en módulos"""
    class Meta:
        model = InscripcionModulo
        fields = ['estudiante', 'maestria', 'modulo']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control', 'id': 'id_estudiante'}),
            'maestria': forms.Select(attrs={'class': 'form-control', 'id': 'id_maestria', 'onchange': 'filtrarModulos()'}),
            'modulo': forms.Select(attrs={'class': 'form-control', 'id': 'id_modulo'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Siempre mostrar todos los módulos disponibles
        self.fields['modulo'].queryset = ModuloMaestria.objects.all()
        
        # Cargar iniciales si es edición
        if self.instance and self.instance.pk:
            self.fields['estudiante'].initial = self.instance.estudiante
            self.fields['maestria'].initial = self.instance.maestria
            self.fields['modulo'].initial = self.instance.modulo
    
    def clean(self):
        cleaned_data = super().clean()
        maestria = cleaned_data.get('maestria')
        modulo = cleaned_data.get('modulo')
        estudiante = cleaned_data.get('estudiante')
        
        # Validar que el módulo pertenece a la maestría seleccionada
        if maestria and modulo:
            if modulo.maestria != maestria:
                raise ValidationError("El módulo seleccionado no pertenece a la maestría especificada.")
        
        # Validar que no haya duplicados
        if estudiante and modulo:
            existe = InscripcionModulo.objects.filter(
                estudiante=estudiante,
                modulo=modulo
            ).exists()
            if existe:
                raise ValidationError("Este estudiante ya está inscrito en este módulo.")
        
        return cleaned_data
