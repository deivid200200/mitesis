from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario
from academico.models import (
    Maestria, ModuloMaestria, Asignatura, ProfesorAsignatura,
    Estudiante, InscripcionModulo, Calificacion, Expediente
)
from decimal import Decimal


class Command(BaseCommand):
    help = 'Genera datos de prueba para el sistema de maestrías'

    def handle(self, *args, **options):
        # Crear usuarios
        self.stdout.write(self.style.SUCCESS('Creando usuarios...'))
        
        usuarios_datos = [
            ('admin', 'admin@maestrias.com', 'Admin', 'Sistema', 'administrador', '0000000001'),
            ('coordinador', 'coordinador@maestrias.com', 'Juan', 'Coordinador', 'coordinador', '0000000002'),
            ('profesor', 'profesor@maestrias.com', 'Carlos', 'Profesor', 'profesor', '0000000003'),
            ('secretaria', 'secretaria@maestrias.com', 'María', 'Secretaria', 'secretaria', '0000000004'),
            ('estudiante', 'estudiante@maestrias.com', 'Pedro', 'Estudiante', 'estudiante', '0000000005'),
        ]
        
        usuarios = {}
        for username, email, first_name, last_name, rol, cedula in usuarios_datos:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            # Establecer contraseña
            user.set_password(username)
            user.save()
            
            # Nota: El administrador del negocio NO es superuser de Django
            # Es un usuario normal con rol 'administrador' que gestiona usuarios desde el dashboard
            
            # Crear o actualizar perfil
            if not hasattr(user, 'perfil'):
                PerfilUsuario.objects.create(
                    usuario=user,
                    rol=rol,
                    numero_identidad=cedula
                )
            else:
                user.perfil.rol = rol
                user.perfil.numero_identidad = cedula
                user.perfil.save()
            
            usuarios[rol] = user
            status = "Creado" if created else "Actualizado"
            self.stdout.write(f"  ✓ {username} ({status})")
        
        coordinador_user = usuarios['coordinador']
        profesor_user = usuarios['profesor']
        estudiante_user = usuarios['estudiante']
        
        # Crear Maestría
        self.stdout.write(self.style.SUCCESS('Creando maestría...'))
        maestria, created = Maestria.objects.get_or_create(
            codigo='MAE-2026-001',
            defaults={
                'nombre': 'Maestría en Ingeniería de Software',
                'descripcion': 'Programa de postgrado especializado en ingeniería de software avanzada y desarrollo de sistemas',
                'coordinador': coordinador_user,
                'creditos_totales': 60,
                'duracion_semestres': 4,
            }
        )
        self.stdout.write(f"  ✓ {maestria.nombre}")
        
        # Crear Módulos
        self.stdout.write(self.style.SUCCESS('Creando módulos...'))
        for i in range(1, 5):
            ModuloMaestria.objects.get_or_create(
                maestria=maestria,
                numero_modulo=i,
                defaults={
                    'nombre': f'Módulo {i}',
                    'semestre': i,
                }
            )
        self.stdout.write(f"  ✓ {ModuloMaestria.objects.filter(maestria=maestria).count()} módulos creados")
        
        # Crear Asignaturas
        self.stdout.write(self.style.SUCCESS('Creando asignaturas...'))
        modulos = ModuloMaestria.objects.filter(maestria=maestria)
        asignaturas_por_modulo = {
            1: ['Fundamentals de Ingeniería de Software', 'Gestión de Proyectos'],
            2: ['Análisis de Sistemas', 'Diseño de Software'],
            3: ['Testing y Calidad', 'Arquitectura de Software'],
            4: ['DevOps', 'Seguridad en Software'],
        }
        
        asignaturas_creadas = 0
        for modulo in modulos:
            for nombre in asignaturas_por_modulo.get(modulo.numero_modulo, []):
                Asignatura.objects.get_or_create(
                    modulo=modulo,
                    codigo=f'AS-{modulo.numero_modulo}-{nombre[:3].upper()}',
                    defaults={
                        'nombre': nombre,
                        'creditos': 3,
                        'horas_teoricas': 48,
                        'horas_practicas': 16,
                        'es_obligatoria': True,
                    }
                )
                asignaturas_creadas += 1
        self.stdout.write(f"  ✓ {asignaturas_creadas} asignaturas creadas")
        
        # Asignar Profesor a Asignaturas
        self.stdout.write(self.style.SUCCESS('Asignando profesores...'))
        asignaturas = Asignatura.objects.all()
        profesores_asignados = 0
        for asignatura in asignaturas[:4]:
            _, created = ProfesorAsignatura.objects.get_or_create(
                profesor=profesor_user,
                asignatura=asignatura,
            )
            if created:
                profesores_asignados += 1
        self.stdout.write(f"  ✓ Profesor asignado a {profesores_asignados} asignaturas")
        
        # Crear Estudiante
        self.stdout.write(self.style.SUCCESS('Creando estudiantes...'))
        estudiante, created = Estudiante.objects.get_or_create(
            usuario=estudiante_user,
            defaults={
                'matricula': 'EST-2026-001',
                'estado': 'activo',
            }
        )
        self.stdout.write(f"  ✓ Estudiante {estudiante.usuario.get_full_name()}")
        
        # Crear Expediente
        self.stdout.write(self.style.SUCCESS('Creando expedientes...'))
        Expediente.objects.get_or_create(
            estudiante=estudiante,
            maestria=maestria,
        )
        self.stdout.write(f"  ✓ Expediente creado")
        
        # Inscribir Estudiante en Módulos
        self.stdout.write(self.style.SUCCESS('Inscribiendo estudiante en módulos...'))
        modulos_inscritos = 0
        for modulo in modulos:
            _, created = InscripcionModulo.objects.get_or_create(
                estudiante=estudiante,
                modulo=modulo,
                maestria=maestria,
            )
            if created:
                modulos_inscritos += 1
        self.stdout.write(f"  ✓ Estudiante inscrito en {modulos_inscritos} módulos")
        
        # Crear Calificaciones
        self.stdout.write(self.style.SUCCESS('Creando calificaciones...'))
        profesor_asignaciones = ProfesorAsignatura.objects.all()
        calificaciones_creadas = 0
        for prof_asig in profesor_asignaciones:
            _, created = Calificacion.objects.get_or_create(
                estudiante=estudiante,
                asignatura=prof_asig.asignatura,
                profesor=prof_asig,
                defaults={
                    'nota_parcial1': Decimal('4.5'),
                    'nota_parcial2': Decimal('4.2'),
                    'nota_trabajo': Decimal('4.0'),
                    'nota_final': Decimal('4.2'),
                    'estado': 'aprobada',
                }
            )
            if created:
                calificaciones_creadas += 1
        self.stdout.write(f"  ✓ {calificaciones_creadas} calificaciones creadas")
        
        self.stdout.write(self.style.SUCCESS('\n✓ ✓ ✓ Datos de prueba creados exitosamente! ✓ ✓ ✓'))
        self.stdout.write(self.style.WARNING('\nCredenciales de prueba:'))
        self.stdout.write('┌─────────────┬──────────────┬────────────────────────────┐')
        self.stdout.write('│ Usuario     │ Contraseña   │ Rol                        │')
        self.stdout.write('├─────────────┼──────────────┼────────────────────────────┤')
        self.stdout.write('│ admin       │ admin        │ Administrador              │')
        self.stdout.write('│ coordinador │ coordinador  │ Coordinador de Maestría    │')
        self.stdout.write('│ profesor    │ profesor     │ Profesor                   │')
        self.stdout.write('│ secretaria  │ secretaria   │ Secretaria Docente         │')
        self.stdout.write('│ estudiante  │ estudiante   │ Estudiante                 │')
        self.stdout.write('└─────────────┴──────────────┴────────────────────────────┘')
        self.stdout.write('\n¡Puedes acceder a http://localhost:8000/login/ para probar!')

