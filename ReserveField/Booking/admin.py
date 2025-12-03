from django.contrib import admin
from .models import Cancha, Horario, Reserva, Resena

@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'ubicacion', 'precio_por_hora', 'calificacion', 'disponible')
    list_filter = ('tipo', 'disponible', 'creado')
    search_fields = ('nombre', 'ubicacion', 'descripcion')
    readonly_fields = ('creado', 'actualizado', 'calificacion', 'total_resenas')
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'tipo', 'imagen')
        }),
        ('Ubicación y Tarifa', {
            'fields': ('ubicacion', 'precio_por_hora', 'capacidad')
        }),
        ('Estado', {
            'fields': ('disponible', 'calificacion', 'total_resenas')
        }),
        ('Fechas', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('cancha', 'get_dia_semana_display', 'hora_apertura', 'hora_cierre')
    list_filter = ('cancha', 'dia_semana')
    search_fields = ('cancha__nombre',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cancha', 'fecha', 'hora_inicio', 'hora_fin', 'estado', 'total')
    list_filter = ('estado', 'fecha', 'cancha')
    search_fields = ('usuario__username', 'cancha__nombre')
    readonly_fields = ('creado', 'actualizado', 'total')
    fieldsets = (
        ('Detalles', {
            'fields': ('usuario', 'cancha', 'fecha', 'hora_inicio', 'hora_fin')
        }),
        ('Información de Pago', {
            'fields': ('total', 'estado')
        }),
        ('Fechas', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cancha', 'calificacion', 'creado')
    list_filter = ('calificacion', 'creado', 'cancha')
    search_fields = ('usuario__username', 'cancha__nombre', 'comentario')
    readonly_fields = ('creado',)
