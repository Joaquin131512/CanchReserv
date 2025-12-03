from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Cancha, Reserva, Resena, Horario
from django.core.mail import send_mail
import json

@login_required(login_url='autenticacion')
def home(request):
    """Página principal con listado de canchas"""
    canchas = Cancha.objects.filter(disponible=True)
    
    # Filtros
    tipo = request.GET.get('tipo')
    ubicacion = request.GET.get('ubicacion')
    busqueda = request.GET.get('busqueda')
    
    if tipo:
        canchas = canchas.filter(tipo=tipo)
    
    if ubicacion:
        canchas = canchas.filter(ubicacion__icontains=ubicacion)
    
    if busqueda:
        canchas = canchas.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda)
        )
    
    tipos_disponibles = Cancha.TIPOS_CANCHA
    
    context = {
        'canchas': canchas,
        'tipos_disponibles': tipos_disponibles,
        'tipo_seleccionado': tipo,
        'ubicacion_seleccionada': ubicacion,
    }
    
    return render(request, 'booking/home.html', context)


@login_required(login_url='autenticacion')
def detalle_cancha(request, cancha_id):
    """Detalle de una cancha específica"""
    cancha = get_object_or_404(Cancha, id=cancha_id)
    resenas = cancha.resenas.all()
    horarios = cancha.horarios.all().order_by('dia_semana')
    
    # Verificar si el usuario ya hizo una reseña
    resena_usuario = resenas.filter(usuario=request.user).first()
    
    context = {
        'cancha': cancha,
        'resenas': resenas,
        'horarios': horarios,
        'resena_usuario': resena_usuario,
        'dias_semana': dict(Horario.DIAS_SEMANA),
    }
    
    return render(request, 'booking/detalle_cancha.html', context)


@login_required(login_url='autenticacion')
def crear_reserva(request, cancha_id):
    """Crear una nueva reserva"""
    cancha = get_object_or_404(Cancha, id=cancha_id)
    
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        
        try:
            # Convertir strings a tipos de datos
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
            hora_fin_obj = datetime.strptime(hora_fin, '%H:%M').time()
            
            # Validaciones
            if fecha_obj < datetime.now().date():
                messages.error(request, 'No puedes reservar en fechas pasadas')
                return redirect('detalle_cancha', cancha_id=cancha_id)
            
            if hora_inicio_obj >= hora_fin_obj:
                messages.error(request, 'La hora de inicio debe ser menor a la hora de fin')
                return redirect('detalle_cancha', cancha_id=cancha_id)
            
            # Verificar disponibilidad
            dia_semana = fecha_obj.weekday()
            horario = cancha.horarios.filter(dia_semana=dia_semana).first()
            
            if not horario:
                messages.error(request, 'No hay horarios disponibles para este día')
                return redirect('detalle_cancha', cancha_id=cancha_id)
            
            if hora_inicio_obj < horario.hora_apertura or hora_fin_obj > horario.hora_cierre:
                messages.error(request, f'El horario debe estar entre {horario.hora_apertura} y {horario.hora_cierre}')
                return redirect('detalle_cancha', cancha_id=cancha_id)
            
            # Verificar si hay conflicto con otras reservas
            conflicto = Reserva.objects.filter(
                cancha=cancha,
                fecha=fecha_obj,
                estado__in=['confirmada', 'pendiente']
            ).filter(
                Q(hora_inicio__lt=hora_fin_obj) & Q(hora_fin__gt=hora_inicio_obj)
            ).exists()
            
            if conflicto:
                messages.error(request, 'Este horario ya está reservado')
                return redirect('detalle_cancha', cancha_id=cancha_id)
            
            # Calcular precio total
            duracion_minutos = (datetime.combine(datetime.now().date(), hora_fin_obj) - 
                              datetime.combine(datetime.now().date(), hora_inicio_obj)).total_seconds() / 60
            duracion_horas = duracion_minutos / 60
            total = Decimal(str(duracion_horas)) * cancha.precio_por_hora
            
            # Crear reserva
            reserva = Reserva.objects.create(
                usuario=request.user,
                cancha=cancha,
                fecha=fecha_obj,
                hora_inicio=hora_inicio_obj,
                hora_fin=hora_fin_obj,
                total=total,
                estado='confirmada'
            )
            
            messages.success(request, f'Reserva confirmada por ${total}')
            return redirect('mis_reservas')
        
        except ValueError:
            messages.error(request, 'Datos inválidos')
            return redirect('detalle_cancha', cancha_id=cancha_id)
    
    context = {'cancha': cancha}
    return render(request, 'booking/crear_reserva.html', context)


@login_required(login_url='autenticacion')
def mis_reservas(request):
    """Listado de reservas del usuario"""
    tab = request.GET.get('tab', 'proximas')
    busqueda = request.GET.get('busqueda', '')

    reservas_proximas = request.user.reservas.filter(
        fecha__gte=datetime.now().date(),
        estado__in=['confirmada', 'pendiente']
    ).order_by('fecha', 'hora_inicio')
    reservas_historial = request.user.reservas.filter(
        Q(fecha__lt=datetime.now().date()) |
        Q(estado__in=['completada', 'cancelada'])
    ).order_by('-fecha')

    if busqueda:
        reservas_proximas = reservas_proximas.filter(
            Q(cancha__nombre__icontains=busqueda) |
            Q(fecha__icontains=busqueda)
        )
        reservas_historial = reservas_historial.filter(
            Q(cancha__nombre__icontains=busqueda) |
            Q(fecha__icontains=busqueda)
        )

    context = {
        'tab': tab,
        'reservas_proximas': reservas_proximas,
        'reservas_historial': reservas_historial,
    }
    return render(request, 'booking/mis_reservas.html', context)


@login_required(login_url='autenticacion')
def cancelar_reserva(request, reserva_id):
    """Cancelar una reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    
    if request.method == 'POST':
        if reserva.fecha <= datetime.now().date():
            messages.error(request, 'No puedes cancelar reservas pasadas')
        else:
            reserva.estado = 'cancelada'
            reserva.save()
            messages.success(request, 'Reserva cancelada correctamente')
        
        return redirect('mis_reservas')
    
    return render(request, 'booking/cancelar_reserva.html', {'reserva': reserva})


@login_required(login_url='autenticacion')
def crear_resena(request, cancha_id):
    """Crear o editar una reseña"""
    cancha = get_object_or_404(Cancha, id=cancha_id)
    resena = cancha.resenas.filter(usuario=request.user).first()
    
    if request.method == 'POST':
        calificacion = request.POST.get('calificacion')
        comentario = request.POST.get('comentario', '')
        
        try:
            calificacion = int(calificacion)
            if not 1 <= calificacion <= 5:
                raise ValueError("Calificación inválida")
            
            # Crear o actualizar reseña
            if resena:
                resena.calificacion = calificacion
                resena.comentario = comentario
                resena.save()
                messages.success(request, 'Reseña actualizada')
            else:
                resena = Resena.objects.create(
                    cancha=cancha,
                    usuario=request.user,
                    calificacion=calificacion,
                    comentario=comentario
                )
                messages.success(request, 'Reseña creada')
            
            # Actualizar calificación promedio de la cancha
            actualizar_calificacion_cancha(cancha)
            
            return redirect('detalle_cancha', cancha_id=cancha_id)
        
        except (ValueError, TypeError):
            messages.error(request, 'Datos inválidos')
            return redirect('detalle_cancha', cancha_id=cancha_id)
    
    context = {
        'cancha': cancha,
        'resena': resena,
    }
    
    return render(request, 'booking/crear_resena.html', context)


def actualizar_calificacion_cancha(cancha):
    """Actualizar la calificación promedio de una cancha"""
    resenas = cancha.resenas.all()
    if resenas.exists():
        promedio = sum(r.calificacion for r in resenas) / resenas.count()
        cancha.calificacion = round(promedio, 1)
        cancha.total_resenas = resenas.count()
        cancha.save()


@login_required(login_url='autenticacion')
def obtener_horarios_disponibles(request, cancha_id):
    """API para obtener horarios disponibles (JSON)"""
    cancha = get_object_or_404(Cancha, id=cancha_id)
    fecha = request.GET.get('fecha')
    
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        dia_semana = fecha_obj.weekday()
        
        # Obtener horario del día
        horario = cancha.horarios.filter(dia_semana=dia_semana).first()
        
        if not horario:
            return JsonResponse({
                'success': False,
                'message': 'No hay horarios disponibles para este día'
            })
        
        # Obtener reservas existentes
        reservas_dia = cancha.reservas.filter(
            fecha=fecha_obj,
            estado__in=['confirmada', 'pendiente']
        ).values_list('hora_inicio', 'hora_fin')
        
        return JsonResponse({
            'success': True,
            'hora_apertura': str(horario.hora_apertura),
            'hora_cierre': str(horario.hora_cierre),
            'reservas_existentes': [(str(r[0]), str(r[1])) for r in reservas_dia]
        })
    
    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Fecha inválida'
        })


@login_required(login_url='autenticacion')
def contacto(request):
    mensaje_enviado = False
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        # Aquí podrías enviar el mensaje por email o guardarlo en la base de datos
        send_mail(
            subject=f"Contacto de {nombre}",
            message=mensaje,
            from_email=email,
            recipient_list=['soporte@reservacanchas.com'],
            fail_silently=True,
        )
        mensaje_enviado = True
    context = {
        'mensaje_enviado': mensaje_enviado
    }
    return render(request, 'booking/contacto.html', context)