from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Cancha(models.Model):
    TIPOS_CANCHA = [
        ('futbol', 'Fútbol'),
        ('tenis', 'Tenis'),
        ('padel', 'Pádel'),
        ('basquetbol', 'Básquetbol'),
        ('voleibol', 'Voleibol'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS_CANCHA)
    ubicacion = models.CharField(max_length=300)
    precio_por_hora = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to='canchas/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    calificacion = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_resenas = models.IntegerField(default=0)
    capacidad = models.IntegerField(default=10)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-creado']
        verbose_name_plural = "Canchas"
    
    def __str__(self):
        return self.nombre


class Horario(models.Model):
    DIAS_SEMANA = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    
    class Meta:
        unique_together = ['cancha', 'dia_semana']
    
    def __str__(self):
        return f"{self.cancha.nombre} - {self.get_dia_semana_display()}"


class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=8, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha']
        unique_together = ['cancha', 'fecha', 'hora_inicio']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.cancha.nombre} ({self.fecha})"


class Resena(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cancha', 'usuario']
        ordering = ['-creado']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.cancha.nombre} ({self.calificacion}★)"
