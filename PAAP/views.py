from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import Http404
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
import os
import csv
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

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
            cursor.execute(
                """
                SELECT type_plan
                FROM gestion_usuarios_plan 
                WHERE email_id = %s
                """,
                [email]
            )
            plan = cursor.fetchone()
        if user:
            # Guardar los datos en la sesión
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

def emailRetrieve_view(request):
    return render(request, 'emailRetrieve.html')
def emailNotification_view(request):
    return render(request, 'emailNotification.html')
def passwordRetrive_view(request):
    return render(request, 'passwordRetrieve.html')
def resources_view(request):
    return render(request, 'resources.html')
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

            # Enviar correo de verificación con imagen incrustada
            send_verification_email(email, name, verification_url)

            messages.success(request, "Te hemos enviado un correo de verificación. Confirma para completar el registro.")
            return redirect('login')  # Redirige a una página de espera o login

        else:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

def send_verification_email(email, name, verification_url):
    subject = "Verificación de correo"
    from_email = "angelohaziel2002l@gmail.com"
    recipient_list = [email]

    # Cuerpo del mensaje con imagen incrustada
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .button {{
                display: inline-block;
                background-color: #3c43cb;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2 style="text-align: center; color: #3c43cb;">¡Bienvenido a PAAP!</h2>
            <p>Hola <strong>{name}</strong>,</p>
            <p>Gracias por registrarte en nuestra plataforma. Para completar tu registro, por favor verifica tu correo haciendo clic en el siguiente botón:</p>
            <div style="text-align: center;">
                <a href="{{ verification_url }}" style="display: inline-block; background-color: #3c43cb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px; margin: 20px 0;">Verificar Correo</a>
            </div>
            <p>Si no puedes hacer clic en el botón, copia y pega este enlace en tu navegador:</p>
            <p style="word-wrap: break-word;"><a href="{verification_url}">{verification_url}</a></p>
            <p class="footer">Si no solicitaste este registro, por favor ignora este mensaje.</p>
        </div>
    </body>
    </html>
    """

    # Crear el correo
    email_message = EmailMultiAlternatives(subject, "", from_email, recipient_list)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

def verify_email(request, token):
    # Validar el token y obtener el registro del usuario temporal
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, username, name, password, email_recover, firstlastname, secondlastname 
            FROM gestion_usuarios_user_temporal 
            WHERE token=%s
            """,
            [token]
        )
        user_data = cursor.fetchone()  # Obtener el usuario temporal

    if not user_data:
        raise Http404("El token no es válido o ya ha sido usado.")

    # Extraer los datos del usuario
    id, email, username, name, password, email_recover, firstlastname, secondlastname = user_data

    # Insertar el usuario en la tabla definitiva
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO gestion_usuarios_user 
            (email, id_user, username, name, password, email_recover, status, firstlastname, secondlastname) 
            VALUES (%s, %s, %s, %s, %s, %s, 1, %s, %s)
            """,
            [email, id, username, name, password, email_recover, firstlastname, secondlastname]
        )

        # Eliminar el registro temporal
        cursor.execute(
            """
            DELETE FROM gestion_usuarios_user_temporal 
            WHERE token=%s
            """,
            [token]
        )
        cursor.execute(
            """
            INSERT INTO gestion_usuarios_plan 
            (id,hours,type_plan, email_id) 
            VALUES (%s, 0 , 'Integrado', %s)
            """,
            [id,email]
        )

    # Redirigir al dashboard con un mensaje de éxito
    messages.success(request, "Correo verificado exitosamente. Ya puedes acceder al sistema.")
    return redirect('dashboard')


def save_parameters(request):
    if request.method == 'POST':
        # Obtener valores del formulario
        model_name = request.POST.get('modelName')
        algorithm = request.POST.get('selectAlgorithm')
        algorithm_type = request.POST.get('algoritmoType')  # 0 = "Regresión" o 1 ="Clasificación"
        criterion = request.POST.get('criterioRadio') # 0 = Entropia o 1 = Indice Gini (Default)
        max_depth = request.POST.get('nodosRange') # Profundida Máxima (Nodos)
        max_leaf_nodes = request.POST.get('max-hojasRange') # Máximo de nodos hoja
        min_samples_split = request.POST.get('divisorRange') # Mínimo de Muestras para dividir un Nodo
        min_samples_leaf = request.POST.get('hojasRange') # Mínimo de Muestras en un Nodo Hoja
        min_impurity_decrease = request.POST.get('reduccionRange') # Reducción mínima de impureza para dividir
        ccp_alpha = request.POST.get('ccpRange') # Parámetro de poda costo-complejidad
        random_seed = request.POST.get('semillaRadio')
        email = request.session['email']
        if algorithm == 'kNeighbors':
            criterion = request.POST.get('criterioRadio-KNN') # 0 = Entropia o 1 = Indice Gini (Default)
            max_depth = request.POST.get('nodosRange-KNN') # Profundida Máxima (Nodos)
            max_leaf_nodes = request.POST.get('max-hojasRange-KNN') # Máximo de nodos hoja
            min_samples_split = request.POST.get('divisorRange-KNN') # Mínimo de Muestras para dividir un Nodo
            min_samples_leaf = request.POST.get('hojasRange-KNN') # Mínimo de Muestras en un Nodo Hoja
            min_impurity_decrease = request.POST.get('reduccionRange-KNN') # Reducción mínima de impureza para dividir
            ccp_alpha = request.POST.get('ccpRange-KNN') # Parámetro de poda costo-complejidad
            random_seed = request.POST.get('semillaRadio-KNN')
        if algorithm == 'randomForest':
            criterion = request.POST.get('criterioRadio-RF') # 0 = Entropia o 1 = Indice Gini (Default)
            max_depth = request.POST.get('nodosRange-RF') # Profundida Máxima (Nodos)
            max_leaf_nodes = request.POST.get('max-hojasRange-RF') # Máximo de nodos hoja
            min_samples_split = request.POST.get('divisorRange-RF') # Mínimo de Muestras para dividir un Nodo
            min_samples_leaf = request.POST.get('hojasRange-RF') # Mínimo de Muestras en un Nodo Hoja
            min_impurity_decrease = request.POST.get('reduccionRange-RF') # Reducción mínima de impureza para dividir
            ccp_alpha = request.POST.get('ccpRange-RF') # Parámetro de poda costo-complejidad
            random_seed = request.POST.get('semillaRadio-RF') 
        # Agregar el nombre del modelo al framework de mensajes
        messages.success(request, f'Datos Guardados')

        # Manejar la subida del archivo
        if request.FILES.get('file'):
            dataset = request.FILES['file']
            dataset_name = dataset.name
            dataset_path = os.path.join(settings.MEDIA_ROOT, 'file', dataset_name)
            os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
            with open(dataset_path, 'wb+') as destination:
                for chunk in dataset.chunks():
                    destination.write(chunk)

            # Guardar la ruta del dataset en la base de datos si es necesario
            messages.success(request, f'Dataset "{dataset_name}" subido con éxito')

        with connection.cursor() as cursor:
            # Obtener id_user
            cursor.execute(
                """
                SELECT id_user FROM gestion_usuarios_user WHERE email = %s
                """,
                [email]
            )
            id_user = cursor.fetchone()
            if not id_user:
                raise ValueError("Usuario no encontrado")
            id_user = id_user[0]  # Extraer el valor de la tupla

            # Calcular N_dataset
            cursor.execute(
                """
                SELECT COUNT(*) FROM hiperparametros WHERE email = %s
                """,
                [email]
            )
            n_dataset = cursor.fetchone()[0] + 1  # Incrementar en 1 para el nuevo dataset

            # Generar id_dataset único
            id_dataset = f"{id_user}{n_dataset}"

            # Insertar en la tabla 'hiperparametros'
            cursor.execute(
                """
                INSERT INTO hiperparametros (id_dataset, email, algoritmo, tipo, criterio, 
                nodosValue, max_hojasValue, divisorValue, hojasValue, reduccionValue, semilla, poda) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [id_dataset, email, algorithm, algorithm_type, criterion, max_depth,
                 max_leaf_nodes, min_samples_split, min_samples_leaf, min_impurity_decrease,
                 random_seed, ccp_alpha]
            )
            cursor.execute(
                """
                INSERT INTO gestion_usuarios_model (id_model, id_dataset, start_date, finish_date, name, type) 
                VALUES (%s, %s, "-", "-", %s, %s)
                """,
                [id_dataset, id_dataset,model_name, algorithm]
            )
            
        return redirect('ia')

def update_hours(request):
    try:
        # Obtener el parámetro 'hours' desde la URL
        hours = request.GET.get('horas')
        if not hours:
            messages.error(request, "No se proporcionaron horas en la URL.")
            return redirect('payment')

        try:
            hours = int(hours)  # Validar que sea un entero
        except ValueError:
            messages.error(request, "El parámetro de horas no es válido.")
            return redirect('payment')

        # Obtener el email del usuario desde la sesión
        email = request.session.get('email')
        if not email:
            messages.error(request, "No se encontró un usuario en la sesión.")
            return redirect('login')

        # Conexión a la base de datos
        with connection.cursor() as cursor:
            # Consultar el registro del usuario
            cursor.execute(
                """
                SELECT hours FROM gestion_usuarios_plan WHERE email_id = %s
                """,
                [email]
            )
            result = cursor.fetchone()
            if not result:
                messages.error(request, "No se encontró un plan asociado al usuario.")
                return redirect('payment')

            # Sumar las horas actuales con las nuevas
            current_hours = result[0]  # Suponiendo que 'hours' es la primera columna
            updated_hours = current_hours + hours

            # Actualizar las horas en la base de datos
            cursor.execute(
                """
                UPDATE gestion_usuarios_plan
                SET hours = %s
                WHERE email_id = %s
                """,
                [updated_hours, email]
            )

        messages.success(request, f"Se han agregado {hours} horas a tu plan.")
        return redirect('payment')

    except Exception as e:
        print(f"Error: {e}")
        messages.error(request, "Ocurrió un error al actualizar las horas.")
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

def error404_view(request):
    return render(request, '404.html')

def error401_view(request):
    return render(request, '401.html')

def error500_view(request):
    return render(request, '500.html')

def upload_csv(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        # Validar la extensión del archivo
        if not file.name.endswith(".csv"):
            return JsonResponse({"message": "El archivo debe ser un .csv"}, status=400)

        # Guardar el archivo en una carpeta temporal
        fs = FileSystemStorage(location="Dataset/")  # Asegúrate de crear esta carpeta
        filename = fs.save(file.name, file)

        file_path = fs.path(filename)

        # Comprobar que el archivo es legible como CSV
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, None)  # Leer encabezados si existen
                rows = list(reader)  # Leer el resto del archivo

                # Comprobar que hay datos
                if not rows:
                    raise ValueError("El archivo CSV está vacío.")

        except Exception as e:
            os.remove(file_path)  # Eliminar el archivo si hay un error
            return JsonResponse({"message": f"Error al procesar el archivo: {str(e)}"}, status=400)

        # Si todo está bien, devolver una respuesta
        return JsonResponse({"message": f"Archivo {file.name} subido y procesado correctamente."})

    return JsonResponse({"message": "Método no permitido."}, status=405)  