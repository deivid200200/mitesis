# Sistema de Gestión de Maestrías

Un sistema web completo para gestionar programas de posgrado. Desde la inscripción de estudiantes hasta la generación de documentos de graduación, todo en un solo lugar.

## ¿Qué puedes hacer aquí?

### Para Administradores
- Gestionar todos los usuarios del sistema
- Asignar roles (coordinador, profesor, secretaria, estudiante)
- Ver estadísticas generales: total de usuarios, activos, inactivos
- Monitorear la distribución de roles con gráficos
- Cambiar contraseñas de usuarios
- Activar/desactivar perfiles

### Para Coordinadores de Maestría
- Crear y gestionar maestrías con código, descripción y duración
- Organizar módulos (semestres) dentro de cada maestría
- Crear asignaturas para cada módulo con créditos y horas
- Asignar profesores a asignaturas
- Ver un panel con todas tus maestrías
- Editar datos en cualquier momento

### Para Profesores
- Ver las asignaturas que tienes a cargo
- Registrar notas a estudiantes:
  - Nota parcial 1 y 2
  - Nota de trabajo/proyecto
  - Nota final
- Ver el listado de estudiantes inscritos
- Dashboard con resumen de asignaturas y estudiantes

### Para Secretaria Docente
- Inscribir estudiantes en módulos
- Ver el listado completo de estudiantes
- Editar calificaciones si hay errores
- Ver el expediente completo de cada estudiante
- Generar reportes en PDF del expediente
- Exportar actas de calificaciones en Excel
- Crear actas de culminación para graduados

### Para Estudiantes
- Ver tu expediente académico completo
- Consultar todas tus notas por asignatura
- Ver en qué módulos estás inscrito
- Calcular tu promedio general
- Seguimiento del progreso con gráfico visual
- Acceder a tus documentos académicos

## Empezar

### Lo que necesitas
- Python 3.8 o superior
- Django 6.0
- Un navegador web cualquiera

### Instalación rápida

1. **Clonar o descargar el proyecto**
```bash
git clone https://github.com/deivid200200/mitesis.git
cd mitesis
```

2. **Configurar el entorno virtual**

En Windows:
```bash
python -m venv enviroment
.\enviroment\Scripts\Activate
```

En Linux/Mac:
```bash
python -m venv enviroment
source enviroment/bin/activate
```

3. **Instalar las dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar migraciones**
```bash
python manage.py migrate
```

5. **Cargar datos de ejemplo**
```bash
python manage.py generar_datos
```

6. **Iniciar el servidor**
```bash
python manage.py runserver
```

7. **Abrir en el navegador**
```
http://localhost:8000/login/
```

## Cuentas de prueba

Después de correr el comando `generar_datos`, tienes estas cuentas disponibles:

```
Admin:       usuario: admin            | contraseña: admin
Coordinador: usuario: coordinador      | contraseña: coordinador
Profesor:    usuario: profesor         | contraseña: profesor
Secretaria:  usuario: secretaria       | contraseña: secretaria
Estudiante:  usuario: estudiante       | contraseña: estudiante
```

## Cómo funciona

### Flujo típico

1. **El Coordinador** crea una maestría con sus módulos y asignaturas
2. **El Coordinador** asigna profesores a esas asignaturas
3. **La Secretaria** inscribe estudiantes en los módulos
4. **El Profesor** registra las calificaciones de sus estudiantes
5. **El Estudiante** consulta sus notas y expediente
6. **La Secretaria** genera reportes y actas cuando sea necesario

### Datos que se guardan

- **Maestrías**: Nombre, código, descripción, duración, coordinador
- **Módulos**: Número, nombre, semestre, fechas de inicio/fin
- **Asignaturas**: Código, créditos, horas teóricas y prácticas, calificación mínima
- **Estudiantes**: Nombre, matrícula, email, teléfono, foto de perfil
- **Calificaciones**: Notas parciales, de trabajo y final con fecha de registro
- **Inscripciones**: Registro de qué estudiante está en qué módulo

## Archivos del proyecto

```
.
├── academico/              # Gestión académica
│   ├── models.py          # Modelos (Maestría, Asignatura, Calificación, etc)
│   ├── views.py           # Vistas para cada rol
│   ├── forms.py           # Formularios de creación/edición
│   ├── urls.py            # Rutas de la app
│   └── management/        # Comando para generar datos de prueba
├── usuarios/              # Autenticación y perfiles
│   ├── models.py          # Modelo PerfilUsuario
│   ├── views.py           # Login, logout, edición de perfil
│   ├── forms.py           # Formularios de usuario
│   └── urls.py
├── reportes/              # Generación de documentos
│   ├── views.py           # PDF y Excel
│   └── urls.py
├── templates/             # HTML de todas las páginas
│   ├── base.html          # Plantilla base con navegación
│   ├── dashboard.html     # Panel principal
│   ├── academico/         # Vistas académicas por rol
│   ├── usuarios/          # Gestión de usuarios
│   └── reportes/          # Reportes
├── static/                # CSS, JS, imágenes
│   ├── css/              # Estilos personalizados
│   ├── img/              # Imágenes
│   └── js/               # Scripts
└── manage.py             # Comando principal de Django
```

## Características técnicas

**Backend**: Django 6.0 con Python
**Frontend**: Bootstrap 5 + Tailwind CSS + Lucide Icons
**Base de datos**: SQLite (desarrollo) - fácil de cambiar a PostgreSQL
**Reportes**: PDF con ReportLab y Excel con openpyxl
**Gráficos**: Chart.js para visualizaciones
**Validación**: Django forms con validaciones personalizadas

## Funciones principales por vista

### Dashboard
- Panel personalizado por rol
- Gráficos de distribución
- Estadísticas en tiempo real
- Accesos rápidos a funciones frecuentes

### Gestión de Maestrías
- CRUD completo (crear, leer, actualizar, eliminar)
- Validación de datos
- Sincronización de módulos y asignaturas

### Registro de Calificaciones
- Interfaz intuitiva para notas
- Validación de rangos (0-5)
- Historial de cambios

### Reportes
- Expediente académico en PDF
- Actas de calificaciones en Excel
- Documentos de graduación

## Personalización

Puedes cambiar:
- Colores en `static/css/styles.css`
- Campos de los modelos en `models.py`
- Validaciones en `forms.py`
- La estructura de reportes en `reportes/views.py`

## Próximas mejoras

- [ ] Sistema de notificaciones por email
- [ ] Más opciones de reportes
- [ ] Importación de estudiantes desde CSV
- [ ] Sistema de calificaciones automático
- [ ] API REST para móviles

## ¿Problemas?

Revisa:
1. Que Python esté instalado: `python --version`
2. Que Django esté instalado: `pip list | grep Django`
3. Que las migraciones se ejecutaran bien: `python manage.py showmigrations`
4. Los logs en `debug_logs/` si hay errores

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


