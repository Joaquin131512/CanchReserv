from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def Autentificacion(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            return handle_login(request)
        elif action == 'register':
            return handle_register(request)
    
    return render(request, 'Auth/registro.html')

def handle_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    # Buscar todos los usuarios con ese email (el campo email no es único por defecto)
    users = User.objects.filter(email__iexact=email)

    if not users.exists():
        messages.error(request, 'El usuario no existe')
        return render(request, 'Auth/registro.html')

    # Intentar autenticar probando cada username asociado al email
    for user in users:
        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth is not None:
            login(request, user_auth)
            return redirect('booking_home')

    # Si llega aquí, no se pudo autenticar con ninguna cuenta asociada al email
    if users.count() > 1:
        messages.error(request, 'No fue posible iniciar sesión: existen varias cuentas con ese correo. Intenta iniciar sesión con tu nombre de usuario.')
    else:
        messages.error(request, 'Contraseña incorrecta')
    
    return render(request, 'Auth/registro.html')

def handle_register(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    
    # Validaciones
    if password != password_confirm:
        messages.error(request, 'Las contraseñas no coinciden')
        return render(request, 'Auth/registro.html')
    
    if User.objects.filter(email=email).exists():
        messages.error(request, 'El correo ya está registrado')
        return render(request, 'Auth/registro.html')
    
    if len(password) < 8:
        messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
        return render(request, 'Auth/registro.html')
    
    # Crear usuario
    username = email.split('@')[0]
    if User.objects.filter(username=username).exists():
        username = email.replace('@', '_').replace('.', '_')
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    
    messages.success(request, 'Registro exitoso. Por favor inicia sesión')
    return redirect('autenticacion')

def logout_view(request):
    logout(request)
    return redirect('autenticacion')