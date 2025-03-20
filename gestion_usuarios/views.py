from django.shortcuts import redirect
from django.db import connection
from django.contrib import messages
from gestion_usuarios import CRUD,Email,crud_user, crud_model,crud_dataset
from django.utils import timezone
import os
import csv
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from gestion_usuarios.models import User
from django.contrib import messages

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

        # Verificar si las contraseñas coinciden
        if password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'register.html')

        # Verificar si el correo electrónico ya está registrado
        if crud_user.get_user(email):
            messages.error(request, "Ya hay un usuario enlazado a este correo.")
            return render(request, 'register.html')

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return render(request, 'register.html')

        # Crear el usuario y enviar el correo de verificación
        token = CRUD.add_user(username, name, lastname, lastname2, email, email_recover, password, password2)
        if token:
            verification_url = request.build_absolute_uri(f"/gestion_usuarios/verify-email/{token}")
            Email.send_verification_email(email, name, verification_url)
            messages.success(request, "Te hemos enviado un correo de verificación. Confirma para completar el registro.")
            return redirect('login')  # Redirigir al login después de enviar el correo
        else:
            messages.error(request, "Hubo un error al crear el usuario.")
            return render(request, 'register.html')

    return render(request, 'register.html')

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
            request.session['email'] = email
            return redirect('emailNotification')    
        else:
            messages.error(request, "El correo de recuperación no coincide con el correo ingresado, por favor rebice el correo que ingreso")
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

def update_profile(request):
    if request.method == "POST":
        username = request.POST.get('userName')
        name = request.POST.get('accountName')
        lastname = request.POST.get('accountFLast')
        lastname2 = request.POST.get('accountSLast')
        email = request.session.get('email')
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
                else:
                    return redirect('resources')
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
    else:
            return redirect('dashboard')

def save_parameters(request):
    if request.method == 'POST':
        email = request.session['email']
        # Obtener valores del formulario
        model = request.POST.get('modelName')
        algorithm = request.POST.get('selectAlgorithm')
        algorithm_type = request.POST.get('algoritmoType') #Clasificación o Regresión
        primeStack = request.POST.get('primeStack')
        number = crud_dataset.count_dataset(email) + 1
        model_name = f"{email}-{number}"
        dataset_id = f"{model_name}_dataset"
        messages.success(request, f'{model_name} || {algorithm} || {algorithm_type} || {primeStack}')
        crud_model.create_model(model_name,dataset_id,None,None,model,algorithm,primeStack)
        upload_date = timezone.now()
            # Manejar la subida del archivo
        if request.FILES.get('file'):
            dataset = request.FILES['file']
            dataset_name = dataset.name
            dataset_size = dataset.size
            dataset_path = os.path.join(settings.MEDIA_ROOT, 'file',email, model_name, dataset_name)
            os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
            with open(dataset_path, 'wb+') as destination:
                for chunk in dataset.chunks():
                    destination.write(chunk)
        crud_dataset.create_dataset(dataset_id,upload_date,dataset_name,dataset_size,email)


        if algorithm == "arbolDesicion":
            if algorithm_type == "regression":
                criterion = request.POST.get('criterioRadio-Tree_reg')
                # 0 = Squared Error || 1 = Absolute Error
                # 2 = Friedman MSE  || 3 = Poisson
                splitter = request.POST.get('semillaRadio-Tree_reg')
                # 0 = Mejor || 1 = Aleatorio
                max_depth = request.POST.get('nodosRange-Tree_reg')
                min_samples_split = request.POST.get('divisorRange-Tree_reg')
                min_leaf_split = request.POST.get('hojasRange-Tree_reg')
                max_leaf_nodes = request.POST.get('max-hojasRange-Tree_reg')
                min_impurity_decrease = request.POST.get('reduccionRange-Tree_reg')
                max_features = request.POST.get('max_charInput-Tree_reg')
                random_state = request.POST.get('controlInput-Tree_reg')
                ccp_alpha = request.POST.get('ccpRange-Tree_reg')
                envio = CRUD.save_hiperparameters_tree(email,model_name,0,primeStack,criterion,splitter,max_depth,min_samples_split,min_leaf_split,max_leaf_nodes,min_impurity_decrease,max_features, random_state,ccp_alpha, 0)
                if envio:
                    messages.success(request, f'Hiperparametros Cargados con Exito') 
                    return redirect('dashboard')   
                else:
                    messages.success(request, f'Error al cargar los parametros')
                    return redirect('ia')
            elif algorithm_type == "classify":
                criterion = request.POST.get('criterioRadio-Tree_class')
                # 0 = Entropi   || 1 = Indice Gini
                # 2 = Log Loss
                splitter = request.POST.get('semillaRadio-Tree_class')
                # 0 = Mejor || 1 = Aleatorio
                max_depth = request.POST.get('nodosRange-Tree_class')
                min_samples_split = request.POST.get('divisorRange-Tree_class')
                min_leaf_split = request.POST.get('hojasRange-Tree_class')
                max_leaf_nodes = request.POST.get('max-hojasRange-Tree_class')
                min_impurity_decrease = request.POST.get('reduccionRange-Tree_class')
                max_features = request.POST.get('max_charInput-Tree_class')
                random_state = request.POST.get('controlInput-Tree_class')
                ccp_alpha = request.POST.get('ccpRange-Tree_class')
                class_weight = request.POST.get('classWeight-Tree_class')
                envio = CRUD.save_hiperparameters_tree(email,model_name,1,primeStack,criterion,splitter,max_depth,min_samples_split,min_leaf_split,max_leaf_nodes,min_impurity_decrease,max_features, random_state,ccp_alpha,class_weight)
                if envio:
                    messages.success(request, f'Hiperparametros Cargados con Exito') 
                    return redirect('dashboard')   
                else:
                    messages.success(request, f'Error al cargar los parametros')
                    return redirect('ia')
        elif algorithm == "kNeighbors":
            if algorithm_type == "regression":
                n_neighbors = request.POST.get('neighborsInput-KNN_reg')
                weights = request.POST.get('neighborsInput-KNN_reg')
                algorithm_knn = request.POST.get('algorithmRadio-KNN_reg')
                leaf_size = request.POST.get('lifeSizeInput-KNN_reg')
                p = request.POST.get('pInput-KNN_reg')
                metric = request.POST.get('metricaRadio-KNN_reg')
                algorithm_type_knn = 0
            elif algorithm_type == "classify":
                n_neighbors = request.POST.get('neighborsInput-KNN_class')
                weights = request.POST.get('neighborsInput-KNN_class')
                algorithm_knn = request.POST.get('algorithmRadio-KNN_reg')
                leaf_size = request.POST.get('lifeSizeInput-KNN_class')
                p = request.POST.get('pInput-KNN_class')
                metric = request.POST.get('metricaRadio-KNN_class')
                algorithm_type_knn = 1
            envio = CRUD.save_hiperparameters_knn(email,model_name,algorithm_type_knn,primeStack,n_neighbors,weights,algorithm_knn,leaf_size,p,metric)
            if envio:
                messages.success(request, f'Hiperparametros Cargados con Exito') 
                return redirect('dashboard')   
            else:
                messages.success(request, f'Error al cargar los parametros')
                return redirect('ia')
        elif algorithm == "randomForest":
            if algorithm_type == "regression":
                n_estimators = request.POST.get('splitQuality-RNF_reg')
                criterion_RF = request.POST.get('criterioRadio-RNF_reg')
                max_depth_RF = request.POST.get('nodosRange-RNF_reg')
                min_samples_split_RF = request.POST.get('divisorRange-RNF_reg')
                min_samples_leaft = request.POST.get('hojasRange-RNF_reg')
                max_features_RF = request.POST.get('max_charInput-RNF_reg')
                bootstrap = request.POST.get('reemplazoRadio-RNF_reg')
                oob_score = request.POST.get('bagRadio-RNF_reg')
                max_samples = request.POST.get('max_sampleInput-RNF_reg')
                random_state_RF = request.POST.get('randomControlInput-RNF_reg')
                class_weight_RF = 0
                algorithm_type_RF = 0
            elif algorithm_type == "classify":
                n_estimators = request.POST.get('splitQuality-RNF_class')
                criterion_RF = request.POST.get('criterioRadio-RNF_class')
                max_depth_RF = request.POST.get('nodosRange-RNF_class')
                min_samples_split_RF = request.POST.get('divisorRange-RNF_class')
                min_samples_leaft = request.POST.get('hojasRange-RNF_class')
                max_features_RF = request.POST.get('max_charInput-RNF_class')
                bootstrap = request.POST.get('reemplazoRadio-RNF_class')
                oob_score = request.POST.get('bagRadio-RNF_class')
                max_samples = request.POST.get('max_sampleInput-RNF_class')
                random_state_RF = request.POST.get('randomControlInput-RNF_class')
                class_weight_RF = request.POST.get('criterioRadio-Tree_class')
                algorithm_type_RF = 1
            if bootstrap == "false":
                bootstrap_RF = False
            elif bootstrap == "true":
                bootstrap_RF = True
            envio = CRUD.save_hiperparameters_RF(email,model_name,algorithm_type_RF,primeStack,n_estimators,criterion_RF,max_depth_RF,min_samples_split_RF,
                              min_samples_leaft, max_features_RF,bootstrap_RF,oob_score,max_samples,random_state_RF,class_weight_RF)
            if envio:
                messages.success(request, f'Hiperparametros Cargados con Exito') 
                return redirect('dashboard')   
            else:
                messages.success(request, f'Error al cargar los parametros')
                return redirect('ia')
    else:
        messages.success(request, f'No existe un metodo Post')
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