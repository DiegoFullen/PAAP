from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.crypto import get_random_string


def index(request):
    return render(request, 'index.html')
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            # Seleccionar todas las columnas necesarias, incluida la contraseña
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
            # Guardar los datos en la sesión
            request.session['email'] = user[0]
            request.session['username'] = user[1]
            request.session['name'] = user[2]
            request.session['password'] = user[3]  # Guardar la contraseña
            request.session['email_recover'] = user[4]
            request.session['firstlastname'] = user[6]
            request.session['secondlastname'] = user[7]

            return redirect('dashboard')
        else:
            messages.error(request, "Correo o contraseña incorrectos")
            return redirect('login')
    return render(request, 'login.html')


def dashboard_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    return render(request, 'dashboard.html', {'email': email})
def ia_view(request):
    # Recuperar los datos de la sesión
    email = request.session.get('email')
    # Verificar si el usuario está autenticado
    if not email:
        return redirect('login')

    return render(request, 'ia.html')

def error404_view(request):
    return render(request, '404.html')
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
        'email_recover': email_recover
    })
def paymentUpgrade_view(request):
    return render(request, 'paymentUpgrade.html')
def pricing_view(request):
    return render(request, 'pricing.html')
def register_view(request):
    return render(request, 'register.html')
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
            request.session['username'] = user[1]
            request.session['name'] = user[2]
            request.session['password'] = user[3]  # Guardar la contraseña
            request.session['email_recover'] = user[4]
            request.session['firstlastname'] = user[6]
            request.session['secondlastname'] = user[7]

            return redirect('account')
        else:
            messages.error(request, "No se pudo actualizar el perfil")
            return redirect('dashboard')
    else:
        messages.error(request, "Las contraseñas no coinciden")
        return redirect('account')

def add_user(request):
     if request.method == "POST":
        username = request.POST.get('accountUsername')
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
                    """
                    INSERT INTO gestion_usuarios_user 
                    (email , username, name, password,email_recover, status,firstlastname,secondlastname) values 
                    (%s, %s, %s, %s, %s, 1, %s, %s)
                    """,
                    [email,username , name, password, email_recover, lastname, lastname2]
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
            request.session['username'] = user[1]
            request.session['name'] = user[2]
            request.session['password'] = user[3]  # Guardar la contraseña
            request.session['email_recover'] = user[4]
            request.session['firstlastname'] = user[6]
            request.session['secondlastname'] = user[7]

            return redirect('dashboard')
        else:
            messages.error(request, "No se pudo agregar el perfil")
            return redirect('dashboard')


def add_user(request):
    if request.method == "POST":
        username = request.POST.get('accountUsername')
        name = request.POST.get('accountName')
        lastname = request.POST.get('accountFLast')
        lastname2 = request.POST.get('accountSLast')
        email = request.POST.get('accountEmail')
        email_recover = request.POST.get('accountEmailBack')
        password = request.POST.get('accountPassword')
        password2 = request.POST.get('accountPassword2')

        if password == password2:
            token = get_random_string(length=32)  # Genera un token único

            with connection.cursor() as cursor:
                # Insertar datos del usuario junto con el token en la tabla temporal
                cursor.execute(
                    """
                    INSERT INTO gestion_usuarios_user_temporal 
                    (email, username, name, password, email_recover, status, firstlastname, secondlastname, token) 
                    VALUES (%s, %s, %s, %s, %s, 1, %s, %s, %s)
                    """,
                    [email, username, name, password, email_recover, lastname, lastname2, token]
                )

            # Construir la URL de verificación
            verification_url = request.build_absolute_uri(f"/verify-email/{token}")
            
            # Enviar correo de verificación
            send_mail(
                "Verificación de correo",
                f"Por favor verifica tu correo haciendo clic en el siguiente enlace: {verification_url}",
                "PAAP@paap.com",
                [email],
            )

            messages.success(request, "Te hemos enviado un correo de verificación. Confirma para completar el registro.")
            return redirect('login')  # Redirige a una página de espera o login

        else:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')


def verify_email(request, token):
    # Validar el token y obtener el registro del usuario temporal
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT email, username, name, password, email_recover, firstlastname, secondlastname 
            FROM gestion_usuarios_user_temporal 
            WHERE token=%s
            """,
            [token]
        )
        user_data = cursor.fetchone()  # Obtener el usuario temporal

    if not user_data:
        raise Http404("El token no es válido o ya ha sido usado.")

    # Extraer los datos del usuario
    email, username, name, password, email_recover, firstlastname, secondlastname = user_data

    # Insertar el usuario en la tabla definitiva
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO gestion_usuarios_user 
            (email, username, name, password, email_recover, status, firstlastname, secondlastname) 
            VALUES (%s, %s, %s, %s, %s, 1, %s, %s)
            """,
            [email, username, name, password, email_recover, firstlastname, secondlastname]
        )

        # Eliminar el registro temporal
        cursor.execute(
            """
            DELETE FROM gestion_usuarios_user_temporal 
            WHERE token=%s
            """,
            [token]
        )

    # Redirigir al dashboard con un mensaje de éxito
    messages.success(request, "Correo verificado exitosamente. Ya puedes acceder al sistema.")
    return redirect('dashboard')

def exit(request):
    request.session['email'] = ""
    request.session['username'] = ""
    request.session['name'] = ""
    request.session['password'] = ""  
    request.session['email_recover'] = ""
    request.session['firstlastname'] = ""
    request.session['secondlastname'] = ""

    return redirect('index')
        