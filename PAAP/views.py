from django.shortcuts import render, redirect
from gestion_usuarios import Login
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
        user = Login.login_user(email,password)
        plan = Login.login_plan(email)
        if user:
            # Cargar los Datos en la Sesión
            request.session['email'] = user[0]
            request.session['username'] = user[2]
            request.session['name'] = user[3]
            request.session['password'] = user[4]
            request.session['email_recover'] = user[5]
            request.session['firstlastname'] = user[7]
            request.session['secondlastname'] = user[8]
            request.session['plan'] = plan
            return redirect('dashboard')
        else:
            messages.error(request, "Correo o contraseña incorrectos")
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
    return render(request, 'emailNotification.html')
#Función para la carga de la recuperación de la contraseñas
def passwordRetrive_view(request, token):
    context = {'token':token}
    return render(request, 'passwordRetrieve.html',context)

#FUNCIONES PARA LA CARGA DE LAS VISTAS DEL DASHBOARD
#Función para la vista del dashboard
def dashboard_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    return render(request, 'dashboard.html', {'email': email})
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
        'secondlastname': secondlastname
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
        'email_recover': email_recover
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
        'plan' : plan
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
           

def update_profile(request):
    if request.method == "POST":
        username = request.POST.get('userName')
        name = request.POST.get('accountName')
        lastname = request.POST.get('accountFLast')
        lastname2 = request.POST.get('accountSLast')
        email = request.POST.get('accountEmail')
        email_recover = request.POST.get('accountEmailBack')
        password = request.POST.get('accountPassword')
        password2 = request.POST.get('accountPassword2')

        if password == password2:
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT * FROM gestion_usuarios_user WHERE email=%s AND status=1", 
                [email]
                )
                user = cursor.fetchone()
                if user:
                    cursor.execute(
                    """
                    UPDATE gestion_usuarios_user 
                    SET username=%s, name=%s, password=%s, email_recover=%s, firstlastname=%s, secondlastname=%s
                    WHERE email=%s
                    """,
                    [username, name, password, email_recover, lastname, lastname2, email]
                    )
                cursor.execute(
                """
                SELECT *
                FROM gestion_usuarios_user 
                WHERE email=%s AND password=%s AND status=1
                """,
                [email, password]
                )
                user = cursor.fetchone()

        if user:
            request.session['email'] = user[0]
            request.session['username'] = user[2]
            request.session['name'] = user[3]
            request.session['password'] = user[4]
            request.session['email_recover'] = user[5]
            request.session['firstlastname'] = user[7]
            request.session['secondlastname'] = user[8]

            return redirect('account')
        else:
            messages.error(request, "No se pudo actualizar el perfil")
            return redirect('dashboard')
    else:
        messages.error(request, "Las contraseñas no coinciden")
        return redirect('account')


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

