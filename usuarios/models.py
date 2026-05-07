from django.db import models
from django.contrib.auth.models import User, Group
    

# Create your models here.


class PerfilUsuario(models.Model):
    ROLES_CHOICES =(
        ('administrador', 'Administrador'),
        ('coordinador', 'Coordinador de Maestría'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
        ('secretaria', 'Secretaria Docente'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='coordinador', verbose_name='Rol del Usuario')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    numero_identidad = models.CharField(max_length=20, blank=True, unique=True, null=True, verbose_name='Número de Identidad')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True, verbose_name='Foto de Perfil')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        ordering = ['usuario__first_name']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.get_rol_display()})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        grupo, _ = Group.objects.get_or_create(name=self.rol)
        self.usuario.groups.clear()
        self.usuario.groups.add(grupo)
    
