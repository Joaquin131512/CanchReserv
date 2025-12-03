# ReservaCancha - Sistema de Reserva de Canchas Deportivas

## Descripción
Aplicación Django para la reserva de canchas deportivas. Incluye autenticación de usuarios, catálogo de canchas, sistema de reservas, horarios y reseñas.

## Requisitos Previos
- Python 3.9+
- pip
- Git

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repo>
cd ReserveField
```

### 2. Crear ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install django pillow
```

### 4. Realizar migraciones
```bash
python manage.py migrate
```

### 5. Cargar datos de ejemplo (Opcional)
```bash
python manage.py cargar_datos
```

### 6. Crear superusuario para admin
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`

## Estructura del Proyecto

### Aplicaciones
- **Autenticacion**: Manejo de registro e inicio de sesión de usuarios
- **Booking**: Sistema principal de reservas de canchas

### Modelos Principales

#### Cancha
- Información de la cancha deportiva
- Tipo (Fútbol, Tenis, Pádel, Básquetbol, Voleibol)
- Precio por hora
- Ubicación
- Calificación y reseñas

#### Horario
- Horarios de apertura y cierre por día de la semana
- Relación con Cancha

#### Reserva
- Reservas de usuarios
- Fecha y hora
- Estado (Pendiente, Confirmada, Completada, Cancelada)
- Total a pagar

#### Reseña
- Calificación y comentarios de usuarios
- Relación con Cancha y Usuario

## URLs Principales

### Autenticación
- `/` - Página de login/registro
- `/logout/` - Cerrar sesión

### Booking
- `/home/` - Página principal con listado de canchas
- `/home/cancha/<id>/` - Detalle de cancha
- `/home/cancha/<id>/reservar/` - Crear reserva
- `/home/mis-reservas/` - Mis reservas
- `/home/cancha/<id>/resena/` - Crear/editar reseña

## Funcionalidades

### Usuarios
- ✅ Registro con validación de email
- ✅ Inicio de sesión
- ✅ Recuperación de contraseña (placeholder)
- ✅ Gestión de perfil

### Canchas
- ✅ Listado de canchas disponibles
- ✅ Filtrado por tipo y ubicación
- ✅ Búsqueda por nombre
- ✅ Detalle completo de cancha
- ✅ Horarios disponibles

### Reservas
- ✅ Crear reserva con selección de fecha/hora
- ✅ Validación de disponibilidad
- ✅ Cálculo automático de precio
- ✅ Cancelación de reservas
- ✅ Historial de reservas

### Reseñas
- ✅ Crear y editar reseñas
- ✅ Sistema de calificación (1-5 estrellas)
- ✅ Cálculo automático de promedio

## Configuración

### Settings Importantes

```python
# Media files (Subidas de usuarios)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Redirección post-login
LOGIN_REDIRECT_URL = 'booking_home'
LOGIN_URL = 'autenticacion'
```

## Administración

Accede al panel administrativo en `/admin/` con tu superusuario.

En el admin puedes:
- Crear y editar canchas
- Gestionar horarios
- Ver y gestionar reservas
- Moderar reseñas

## Tecnologías

- **Backend**: Django 5.2
- **Frontend**: Tailwind CSS
- **Base de datos**: SQLite (desarrollo)
- **Autenticación**: Django Auth

## Próximas Mejoras

- [ ] Sistema de pagos integrado
- [ ] Notificaciones por email
- [ ] App móvil
- [ ] Integración con Google Calendar
- [ ] Sistema de puntos/recompensas
- [ ] Filtros avanzados

## Licencia

MIT License

## Soporte

Para reportar bugs o sugerencias, contacta a: soporte@reservacanchas.com
