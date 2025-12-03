from django.core.management.base import BaseCommand
from Booking.models import Cancha, Horario
from django.utils import timezone

class Command(BaseCommand):
    help = 'Carga datos de ejemplo en la base de datos'

    def handle(self, *args, **options):
        # Crear canchas de ejemplo
        canchas_data = [
            {
                'nombre': 'Cancha Futbol',
                'descripcion': 'Hermosa cancha ubicada en puerto mont xxxxxxxx xxxxxxxx',
                'tipo': 'futbol',
                'ubicacion': 'La Vara 136, Puerto Montt',
                'precio_por_hora': 10.00,
                'capacidad': 22,
            },
            {
                'nombre': 'Tenis Club Palermo',
                'descripcion': 'Club de tenis con canchas profesionales de última generación',
                'tipo': 'tenis',
                'ubicacion': 'Palermo, CABA',
                'precio_por_hora': 25.00,
                'capacidad': 4,
            },
            {
                'nombre': 'Pádel Center Belgrano',
                'descripcion': 'Centro especializado en pádel con 8 canchas profesionales',
                'tipo': 'padel',
                'ubicacion': 'Belgrano, CABA',
                'precio_por_hora': 20.00,
                'capacidad': 4,
            },
            {
                'nombre': 'Parque Rivadavia Hoops',
                'descripcion': 'Canchas de básquetbol en el parque Rivadavia',
                'tipo': 'basquetbol',
                'ubicacion': 'Caballito, CABA',
                'precio_por_hora': 15.00,
                'capacidad': 10,
            },
            {
                'nombre': 'Complejo Deportivo Oeste',
                'descripcion': 'Complejo completo con múltiples canchas deportivas',
                'tipo': 'futbol',
                'ubicacion': 'Flores, CABA',
                'precio_por_hora': 12.00,
                'capacidad': 20,
            },
            {
                'nombre': 'Beach Volley Núñez',
                'descripcion': 'Canchas de voleibol de playa en zona norte',
                'tipo': 'voleibol',
                'ubicacion': 'Núñez, CABA',
                'precio_por_hora': 18.00,
                'capacidad': 12,
            },
        ]

        for data in canchas_data:
            cancha, created = Cancha.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    'descripcion': data['descripcion'],
                    'tipo': data['tipo'],
                    'ubicacion': data['ubicacion'],
                    'precio_por_hora': data['precio_por_hora'],
                    'capacidad': data['capacidad'],
                    'disponible': True,
                }
            )
            
            if created:
                # Crear horarios para la cancha (Lunes a Domingo)
                horarios = [
                    {'dia_semana': 0, 'hora_apertura': '09:00', 'hora_cierre': '22:00'},
                    {'dia_semana': 1, 'hora_apertura': '09:00', 'hora_cierre': '22:00'},
                    {'dia_semana': 2, 'hora_apertura': '09:00', 'hora_cierre': '22:00'},
                    {'dia_semana': 3, 'hora_apertura': '09:00', 'hora_cierre': '22:00'},
                    {'dia_semana': 4, 'hora_apertura': '09:00', 'hora_cierre': '22:00'},
                    {'dia_semana': 5, 'hora_apertura': '08:00', 'hora_cierre': '23:00'},
                    {'dia_semana': 6, 'hora_apertura': '08:00', 'hora_cierre': '23:00'},
                ]
                
                for horario_data in horarios:
                    Horario.objects.get_or_create(
                        cancha=cancha,
                        dia_semana=horario_data['dia_semana'],
                        defaults={
                            'hora_apertura': horario_data['hora_apertura'],
                            'hora_cierre': horario_data['hora_cierre'],
                        }
                    )
                
                self.stdout.write(self.style.SUCCESS(f'✓ Creada cancha: {cancha.nombre}'))
            else:
                self.stdout.write(f'- Cancha ya existe: {cancha.nombre}')

        self.stdout.write(self.style.SUCCESS('\n¡Datos de ejemplo cargados correctamente!'))
