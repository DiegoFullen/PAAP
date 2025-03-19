from django.shortcuts import render, redirect
from gestion_usuarios import Email,CRUD, crud_plan, crud_user, crud_temporal
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.db import connection
from django.contrib import messages


#FUNCIONES PARA LA CARGA DEL INICIO DE LA PAGINA (ANTES DE REGISTRARSE)

#Función para cargar el Index
def index(request):
    return render(request, 'index.html')
#Función para iniciar sesión
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = crud_user.get_user(email)
        plan = crud_plan.get_plan(email)
        horas = int(plan.hours)  # Parte entera: horas
        minutos_decimal = plan.hours - horas  # Parte decimal: fracción de una hora
        minutos = int(round(minutos_decimal * 60))  # Convertir fracción a minutos
        tiempo = f"{horas}:{minutos:02d}"
        if user:
            if check_password(password, user.password):    
                if user.status:
                    # Cargar los Datos en la Sesión
                    request.session['email'] = user.email
                    request.session['username'] = user.username
                    request.session['name'] = user.name
                    request.session['password'] = user.password
                    request.session['email_recover'] = user.email_recover
                    request.session['firstlastname'] = user.firstlastname
                    request.session['secondlastname'] = user.secondlastname
                    request.session['hours'] = tiempo
                    request.session['plan'] = plan.type_plan
                    return redirect('dashboard')
                else:
                    messages.error(request, "Usuario desactivado")
                    return redirect('login')  
            else:
                messages.error(request, "La contraseña o el correo estan equivocados")
                return redirect('login') 
        else:
            messages.error(request, "El usuario no existe")
            return redirect('login')
    return render(request, 'login.html')
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
    else:
        models = CRUD.search_models(email)
        context = {'modelos': models, 'email':email}
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

