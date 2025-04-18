from django.shortcuts import render, redirect
from gestion_usuarios import CRUD, crud_plan, crud_user, crud_temporal
from django.contrib.auth.hashers import check_password
from django.http import Http404
from django.db import connection
from django.contrib import messages
import requests
from django.conf import settings
import os
from PAAP.settings import BASE_DIR


#FUNCIONES PARA LA CARGA DEL INICIO DE LA PAGINA (ANTES DE REGISTRARSE)

#Función para cargar el Index
def index(request):
    return render(request, 'index.html')
#Función para iniciar sesión
def login_view(request):
    if request.method == "POST":
        # Validación del CAPTCHA primero
        captcha_response = request.POST.get('g-recaptcha-response')
        if not captcha_response:
            messages.error(request, "Por favor, completa el CAPTCHA.")
            return redirect('login')
        
        # Validación con Google (versión mejorada)
        try:
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': captcha_response
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data=data,
                headers=headers,
                timeout=5  # Timeout de 5 segundos
            )
            result = response.json()
            
            if not result.get('success'):
                error_codes = result.get('error-codes', ['unknown-error'])
                messages.error(request, f"Error en CAPTCHA: {', '.join(error_codes)}")
                return redirect('login')

        except requests.exceptions.RequestException as e:
            messages.error(request, "Error al validar el CAPTCHA. Inténtalo nuevamente.")
            return redirect('login')

        # Resto de tu lógica de autenticación...
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = crud_user.get_user(email)
        
        if not user:
            messages.error(request, "El usuario no existe")
            return redirect('login')
            
        if not check_password(password, user.password):
            messages.error(request, "La contraseña o el correo están equivocados")
            return redirect('login')
            
        if not user.status:
            messages.error(request, "Usuario desactivado")
            return redirect('login')
            
        # Resto de tu lógica de sesión...
        plan = crud_plan.get_plan(email)
        horas = int(round(plan.hours)/60)
        minutos = int(round((plan.hours % 60)))
        tiempo = f"{horas}:{minutos:02d}"
        
        request.session.update({
            'email': user.email,
            'username': user.username,
            'name': user.name,
            'password': user.password,
            'email_recover': user.email_recover,
            'firstlastname': user.firstlastname,
            'secondlastname': user.secondlastname,
            'hours': tiempo,
            'plan': plan.type_plan
        })
        
        return redirect('dashboard')
    context = { 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY}
    return render(request, 'login.html',context)
#Función del Pricing view
def pricing_view(request):
    return render(request, 'pricing.html')
#Función para registrarse
def register_view(request):
    return render(request, 'register.html')
#Función para cargar la recuperación de contraseña
def emailRetrieve_view(request):
    return render(request, 'emailRetrieve.html')
#Función para la notificación de la recuperación de la contraseña
def emailNotification_view(request):
    email = request.session.get('email', 'Correo no disponible')
    context = {'email': email}
    return render(request, 'emailNotification.html', context)
#Función para la carga de la recuperación de la contraseñas
def passwordRetrive_view(request, token):
    token2 = token.rstrip('/')
    context = {'token':token}
    if crud_temporal.get_temporal_token(token2):
        return render(request, 'passwordRetrieve.html',context)
    else:
        raise Http404("El token no existe o es inválido.")

#FUNCIONES PARA LA CARGA DE LAS VISTAS DEL DASHBOARD
#Función para la vista del dashboard
def dashboard_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    
    modelos = CRUD.search_models(email)
    
    # Procesar cada modelo
    for modelo in modelos:
        modelo['type_cr'] = "Regresión" if modelo['type_cr'] == 0 else "Clasificación"
        modelo['type'] = "Árboles de Decisión" if modelo['type'] == "arbolDesicion" else "K-Nearest Neighbors" if modelo['type'] == "kNeighbors" else "Random Forest"
        
        # Procesar solo las rutas de imágenes
    for modelo in modelos:
        model_dir = os.path.join('file', email, str(modelo['id_model']))
        model_dir = os.path.normpath(model_dir).replace('\\', '/')
        modelo['image_urls'] = []
        
        absolute_dir = os.path.join(settings.BASE_DIR, model_dir)
        if os.path.exists(absolute_dir):
            for img in os.listdir(absolute_dir):
                if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    modelo['image_urls'].append(
                        f"{settings.MODELS_MEDIA_URL}{email}/{modelo['id_model']}/{img}"
                    )
        print(modelo['image_urls'])
    context = {
        'modelos': modelos, 
        'email': email
    }
    return render(request, 'dashboard.html', context)

#Función para la vista del entrenamiento de IA
def ia_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    return render(request, 'ia.html')
#Función para la vista de los recursos
def resources_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    return render(request, 'resources.html')
#Función para la vista de la Cuenta
def account_view(request):
   # Recuperar los datos de la sesión
    email = request.session.get('email')
    email_recover = request.session.get('email_recover')
    username = request.session.get('username')
    name = request.session.get('name')
    password = request.session.get('password') # Recuperar la contraseña
    firstlastname = request.session.get('firstlastname')
    secondlastname = request.session.get('secondlastname')
    plan =request.session.get('plan')
    hours = request.session.get('hours')
    
    # Verificar si el usuario está autenticado
    if not email:
        return redirect('login')
    # Pasar las variables al contexto de la plantilla
    return render(request, 'account.html', {
        'email': email,
        'email_recover':email_recover,
        'username': username,
        'name': name,
        'password': password,  # Enviar la contraseña
        'firstlastname': firstlastname,
        'secondlastname': secondlastname,
        'plan': plan,
        'hours': hours
    })
def accountEdit_view(request):
    # Recuperar los datos de la sesión
    email = request.session.get('email')
    username = request.session.get('username')
    name = request.session.get('name')
    password = request.session.get('password')  # Recuperar la contraseña
    email_recover = request.session.get('email_recover')
    firstlastname = request.session.get('firstlastname')
    secondlastname = request.session.get('secondlastname')
    plan = request.session.get('plan')

    # Verificar si el usuario está autenticado
    if not email:
        return redirect('login')

    # Pasar las variables al contexto de la plantilla
    return render(request, 'accountEdit.html', {
        'email': email,
        'username': username,
        'name': name,
        'password': password,  # Enviar la contraseña
        'firstlastname': firstlastname,
        'secondlastname': secondlastname,
        'email_recover': email_recover,
        'plan':plan
    })
def payment_view(request):
    # Recuperar los datos de la sesión
    email = request.session.get('email')
    username = request.session.get('username')
    name = request.session.get('name')
    password = request.session.get('password')  # Recuperar la contraseña
    email_recover = request.session.get('email_recover')
    firstlastname = request.session.get('firstlastname')
    secondlastname = request.session.get('secondlastname')
    plan = request.session.get('plan')
    hours = request.session.get('hours')

    # Verificar si el usuario está autenticado
    if not email:
        return redirect('login')

    # Pasar las variables al contexto de la plantilla
    return render(request, 'payment.html', {
        'email': email,
        'username': username,
        'name': name,
        'password': password,  # Enviar la contraseña
        'firstlastname': firstlastname,
        'secondlastname': secondlastname,
        'email_recover': email_recover,
        'plan' : plan,
        'hours': hours
    })
def paymentUpgrade_view(request):
    username = request.session.get('username')
    plan = request.session.get('plan')
    return render(request, 'paymentUpgrade.html',{
       'username': username,
       'plan': plan 
    })

def upgrade_plan(request):
    if request.method == "POST":
        plan = request.POST.get('selectLevel')
        request.session['plan'] = plan
        email = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE gestion_usuarios_plan 
                SET type_plan = %s
                WHERE email_id = %s 
                """,
                [plan, email]
            )
        return redirect('payment')
           

def exit(request):
    request.session['email'] = ""
    request.session['username'] = ""
    request.session['name'] = ""
    request.session['password'] = ""  
    request.session['email_recover'] = ""
    request.session['firstlastname'] = ""
    request.session['secondlastname'] = ""

    return redirect('index')

def error404_view(request,exception):
    return render(request, '404.html',status=404)

def error401_view(request):
    return render(request, '401.html',status=401)

def error500_view(request):
    return render(request, '500.html',status=500)


