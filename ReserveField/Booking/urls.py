from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='booking_home'),
    path('cancha/<int:cancha_id>/', views.detalle_cancha, name='detalle_cancha'),
    path('cancha/<int:cancha_id>/reservar/', views.crear_reserva, name='crear_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('reserva/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('cancha/<int:cancha_id>/resena/', views.crear_resena, name='crear_resena'),
    path('api/horarios-disponibles/<int:cancha_id>/', views.obtener_horarios_disponibles, name='api_horarios'),
    path('contacto/', views.contacto, name='contacto'),
]
