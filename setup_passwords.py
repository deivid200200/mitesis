#!/usr/bin/env python
"""
Script para establecer contraseñas para los usuarios de prueba.
Uso: python manage.py shell < setup_passwords.py
"""

from django.contrib.auth.models import User

# Crear mapeo de usuarios y contraseñas
usuarios = {
    'admin': 'admin',
    'coordinador': 'coordinador',
    'profesor': 'profesor',
    'secretaria': 'secretaria',
    'estudiante': 'estudiante',
}

for username, password in usuarios.items():
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✓ Contraseña establecida para {username}")
    except User.DoesNotExist:
        print(f"✗ Usuario {username} no encontrado")

print("\n✓ Contraseñas establecidas exitosamente")
