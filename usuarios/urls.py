from django.urls import path
from . import views

# Autenticación
urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Usuarios - Gestión por administrador
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuario/crear/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuario/<int:pk>/editar/', views.UsuarioEditarView.as_view(), name='usuario_editar'),
    path('usuario/<int:pk>/eliminar/', views.UsuarioEliminarView.as_view(), name='usuario_eliminar'),
    path('usuario/<int:pk>/cambiar-contrasena/', views.CambiarContraseniaView.as_view(), name='cambiar_contrasena'),
    path('usuario/<int:usuario_id>/perfil/editar/', views.PerfilUsuarioEditarView.as_view(), name='perfil_editar_admin'),
    
    # Perfil personal
    path('perfil/actualizar/', views.PerfilActualizarView.as_view(), name='perfil_actualizar'),
    path('perfil/cambiar-contrasena/', views.CambiarContraseniaPropia.as_view(), name='cambiar_contrasena_propia'),
]