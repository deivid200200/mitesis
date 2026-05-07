# Sistema de Gestión Académica de Maestrías

## Descripción
Sistema web completo para la gestión de información académica de programas de maestría con soporte para múltiples roles de usuario.

## Características principales

### Roles de usuario:
1. **Administrador**: Gestión de usuarios y cuentas del sistema
2. **Coordinador de Maestría**: Registro de módulos, asignaturas y asignación de profesores
3. **Profesor**: Registro de calificaciones de estudiantes
4. **Secretaria Docente**: Inscripción de estudiantes, edición de notas y generación de documentos
5. **Estudiante**: Visualización de notas, expediente y recorrido académico

### Funcionalidades

#### Coordinador
- Crear y gestionar maestrías
- Crear módulos de maestría
- Crear asignaturas y asignarlas a módulos
- Asignar profesores a asignaturas

#### Profesor
- Ver asignaturas asignadas
- Registrar calificaciones de estudiantes
  - Nota Parcial 1
  - Nota Parcial 2
  - Nota de Trabajo
  - Nota Final

#### Secretaria Docente
- Listar estudiantes del sistema
- Inscribir estudiantes en módulos
- Editar calificaciones (corrección de errores)
- Ver expediente completo del estudiante
- Exportar acta de notas en Excel
- Generar acta de culminación cuando se completan todas las asignaturas

#### Estudiante
- Ver expediente académico completo
- Ver todas las notas por asignatura
- Ver módulos inscritos
- Ver promedio general
- Calcular créditos aprobados

#### Administrador
- Gestionar usuarios
- Ver estadísticas del sistema
- Crear nuevos usuarios

## Instalación

### Requisitos previos
- Python 3.8+
- Django 6.0+
- virtualenv o conda

### Pasos de instalación

1. Crear y activar el entorno virtual:
```bash
python -m venv enviroment
.\enviroment\Scripts\Activate  # Windows
source enviroment/bin/activate  # Linux/Mac
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Realizar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Crear datos de prueba:
```bash
python manage.py generar_datos
```

5. Crear superusuario (opcional, ya que el comando anterior crea usuarios de prueba):
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor de desarrollo:
```bash
python manage.py runserver
```

7. Acceder a la aplicación:
```
http://localhost:8000/login/
```

## Credenciales de prueba

Después de ejecutar `python manage.py generar_datos`, puedes usar:

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin | Administrador |
| coordinador | coordinador | Coordinador de Maestría |
| profesor | profesor | Profesor |
| secretaria | secretaria | Secretaria Docente |
| estudiante | estudiante | Estudiante |

## Estructura del proyecto

```
newproject/
├── academico/              # App para gestión académica
│   ├── models.py          # Modelos: Maestría, Módulo, Asignatura, etc.
│   ├── views.py           # Vistas para cada rol
│   ├── forms.py           # Formularios
│   ├── urls.py            # Rutas URL
│   └── admin.py           # Configuración admin
├── usuarios/              # App para autenticación
│   ├── models.py          # Modelo PerfilUsuario
│   ├── views.py           # Vistas de login/registro
│   └── forms.py           # Formularios de usuario
├── reportes/              # App para generación de reportes
│   ├── views.py           # Generación de PDF y Excel
│   └── urls.py
├── templates/             # Plantillas HTML
│   ├── base.html          # Template base
│   ├── dashboard.html     # Dashboard
│   ├── academico/         # Templates por rol
│   ├── usuarios/
│   └── reportes/
└── manage.py
```

## Modelos de datos

### Principales
- **Maestria**: Programa de posgrado
- **ModuloMaestria**: Semestre/módulo dentro de una maestría
- **Asignatura**: Curso dentro de un módulo
- **ProfesorAsignatura**: Relación profesor-asignatura
- **Estudiante**: Datos adicionales del estudiante
- **InscripcionModulo**: Inscripción de estudiante en módulo
- **Calificacion**: Notas de estudiante en asignatura
- **Expediente**: Histórico académico del estudiante
- **ActaCulminacion**: Acta de graduación

## Exportación de documentos

### Expediente en PDF
Descarga el expediente completo del estudiante en formato PDF.

### Acta de Notas en Excel
Exporta todas las notas de un estudiante en formato XLSX con formato profesional.

### Acta de Culminación
Genera automáticamente cuando el estudiante aprueba todas las asignaturas.

## Notas importantes

1. El sistema calcula automáticamente el estado de aprobado/reprobado basado en la nota final y la calificación mínima.
2. Los promedio se calculan automáticamente en el expediente.
3. Solo la secretaria puede editar calificaciones después de que fueron registradas.
4. El acta de culminación se genera automáticamente cuando todas las asignaturas están aprobadas.

## Funcionalidades futuras

- Envío de notificaciones por email
- Generación de reportes analíticos
- Gráficos de progreso académico
- Sistema de chat para comunicación
- Integración con otros sistemas académicos
- Cálculo de promedio ponderado
- Sistema de apelaciones

## Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contacte al equipo de desarrollo.

## Licencia

Este proyecto está bajo licencia MIT.
