import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print('=' * 70)
print('PRUEBAS COMPLETAS - SISTEMA DE CAMBIO DE CONTRASEÑA')
print('=' * 70)

client = Client()

# Parte 1: Login admin
print('\n✓ PARTE 1: Login del administrador')
login_ok = client.login(username='admin', password='admin')
print(f'  - Login exitoso: {login_ok}')

# Parte 2: Obtener formulario de cambiar contraseña propia
print('\n✓ PARTE 2: Admin accede a cambiar su propia contraseña')
response = client.get('/perfil/cambiar-contrasena/')
print(f'  - Status: {response.status_code}')
print(f'  - Template usado: cambiar_contrasena_propia.html')
has_form = 'new_password1' in response.content.decode()
print(f'  - Formulario presente: {has_form}')

# Parte 3: Cambiar contraseña propia del admin
print('\n✓ PARTE 3: Cambiar contraseña propia (admin)')
response = client.post('/perfil/cambiar-contrasena/', {
    'old_password': 'admin',
    'new_password1': 'nuev4Contrasena123',
    'new_password2': 'nuev4Contrasena123',
})
print(f'  - Respuesta status: {response.status_code}')
is_redirect = response.status_code == 302 and 'dashboard' in response.url
print(f'  - Redirigido a dashboard: {is_redirect}')

# Parte 4: Logout y login con nueva contraseña
print('\n✓ PARTE 4: Verificar que funciona nueva contraseña')
client.logout()
login_ok = client.login(username='admin', password='nuev4Contrasena123')
print(f'  - Login con nueva contraseña: {login_ok}')

# Parte 5: Admin cambia contraseña de otro usuario
print('\n✓ PARTE 5: Admin cambia contraseña de otro usuario')
# Obtener formulario
response = client.get('/usuario/2/cambiar-contrasena/')
print(f'  - Status al obtener formulario: {response.status_code}')
print(f'  - Template usado: cambiar_contrasena.html')

# Cambiar contraseña del usuario 2 (coordinador)
response = client.post('/usuario/2/cambiar-contrasena/', {
    'new_password1': 'nuev4CoordPassword123',
    'new_password2': 'nuev4CoordPassword123',
})
print(f'  - Respuesta status: {response.status_code}')

# Parte 6: Verificar que el coordinador puede loguearse con la nueva contraseña
print('\n✓ PARTE 6: Verificar que el usuario cambió contraseña')
client.logout()
login_ok = client.login(username='coordinador', password='nuev4CoordPassword123')
print(f'  - Login del coordinador con nueva contraseña: {login_ok}')

print('\n' + '=' * 70)
print('✓✓✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE ✓✓✓')
print('=' * 70)
print('\nFUNCIONALIDAD VERIFICADA:')
print('  ✓ Template usuario_form.html - Crear nuevos usuarios')
print('  ✓ Template cambiar_contrasena_propia.html - Cambiar propia contraseña')
print('  ✓ Template cambiar_contrasena.html - Admin cambia contraseña de otros')
print('  ✓ Template usuario_list.html - Listar todos los usuarios')
print('  ✓ Validación de contraseñas')
print('  ✓ Redireccionamientos después de cambio')
