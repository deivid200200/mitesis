from django.contrib import admin
from django.contrib.auth.models import User
from .models import PerfilUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    fields = ('rol', 'numero_identidad', 'telefono', 'direccion', 'foto', 'activo')


class CustomUserAdmin(admin.ModelAdmin):
    inlines = [PerfilUsuarioInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_rol']
    list_filter = ['perfil__rol', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_rol(self, obj):
        if hasattr(obj, 'perfil'):
            return obj.perfil.get_rol_display()
        return '-'
    get_rol.short_description = 'Rol'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(PerfilUsuario)
