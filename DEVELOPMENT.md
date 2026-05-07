# Guía de Desarrollo

## Workflow de Git

### Para agregar cambios:

```bash
# Ver archivos modificados
git status

# Agregar cambios específicos
git add archivo.py

# O agregar todos los cambios
git add .

# Hacer commit con mensaje descriptivo
git commit -m "Descripción clara del cambio"

# Subir a GitHub
git push origin main
```

### Ejemplos de mensajes de commit:

```
git commit -m "feat: agregar validación en formulario de usuario"
git commit -m "fix: corregir error en cálculo de promedio"
git commit -m "docs: actualizar documentación de instalación"
git commit -m "refactor: mejorar estructura de views.py"
git commit -m "style: aplicar formato con black"
```

## Crear ramas para features

```bash
# Crear rama nueva
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y commits
git add .
git commit -m "agregar nueva funcionalidad"

# Subir rama
git push origin feature/nueva-funcionalidad

# En GitHub, crear Pull Request desde la rama
# Una vez aprobado, mergear a main
```

## Comandos útiles

```bash
# Ver historial de commits
git log --oneline

# Ver cambios sin staged
git diff

# Ver cambios staged
git diff --staged

# Deshacer cambios en archivo
git checkout -- archivo.py

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1
```

## Pull Request (PR) Checklist

Antes de hacer push a una rama nueva:
- [ ] Tests pasando
- [ ] Código formateado
- [ ] Sin archivos de debugging
- [ ] Commit messages claros
- [ ] Documentación actualizada

## Configuración local

```bash
# Verificar configuración actual
git config --global --list

# Cambiar nombre
git config --global user.name "Tu Nombre"

# Cambiar email
git config --global user.email "tu@email.com"
```
