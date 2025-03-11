from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from gestion_usuarios import CRUD,Email
from django.utils.crypto import get_random_string
import os
import csv
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

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

        token = CRUD.add_user(username,name,lastname,lastname2,email,email_recover,password,password2)
        # Construir la URL de verificación
        if token:
            verification_url = request.build_absolute_uri(f"/gestion_usuarios/verify-email/{token}")
            # Enviar correo de verificación con imagen incrustada
            Email.send_verification_email(email, name, verification_url)
            messages.success(request, "Te hemos enviado un correo de verificación. Confirma para completar el registro.")
            return redirect('login')  # Redirige a una página de espera o login

        else:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')
def verify_email(request, token):
    if Email.verify_token(token,1,""):
        messages.success(request, "Correo verificado exitosamente. Ya puedes acceder al sistema.")
    else:
        messages.success(request, "El correo no pudo verificarse o el tiempo de espera expiro")
        Email.delete_temporal(token)
    return redirect('login')

def recover_password_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        retrieveEmail = request.POST.get('retrieveEmail')
        respuesta = Email.send_email_recover(request, email, retrieveEmail)
        if respuesta:
            return redirect('emailNotification')    
        else:
            return redirect('emailRetrieve')    
    else:
        return redirect('emailRetrieve')

def recover_password(request, token):
    if request.method == 'POST':
        password = request.POST.get('newPassword')
        newPasswordCon = request.POST.get('newPasswordCon')
        if password == newPasswordCon:
            respuesta = Email.verify_token(token,2,password)
            if respuesta:
                return redirect('login')
            else:
                return redirect('passwordRetrive', token = token)
        else:
            return redirect('passwordRetrive', token = token)


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