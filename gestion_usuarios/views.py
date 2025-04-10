import os
import csv
import json
import logging

from django.shortcuts import redirect
from django.db import connection
from django.contrib import messages
from gestion_usuarios import CRUD,Email,crud_user, crud_model,crud_dataset,crud_plan
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from gestion_usuarios.models import User, Model,Dataset,Hiperparameters_KNN,Hiperparameters_RandomForest,Hiperparameters_Tree
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Clases IA
from algoritmos.modelos_ml import ModelosML 

logger = logging.getLogger(__name__)

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

        # Crear contexto con los valores actuales
        context = {
            'username': username,
            'name': name,
            'lastname': lastname,
            'lastname2': lastname2,
            'email': email,
            'email_recover': email_recover,
        }

        # Verificar si las contraseñas coinciden
        if password != password2:
            messages.error(request, "Las contraseñas no coinciden.", extra_tags='password')
            return render(request, 'register.html', context)

        # Verificar que el correo y la recuperación sean diferentes
        if email == email_recover:
            messages.error(request, "Los correos son iguales", extra_tags='recover')
            context['email_recover'] = ''
            return render(request, 'register.html', context)

        # Verificar si el correo electrónico ya está registrado
        if crud_user.get_user(email):
            messages.error(request, "Ya hay un usuario enlazado a este correo.", extra_tags='email')
            context['email'] = ''
            return render(request, 'register.html', context)

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.", extra_tags='username')
            context['username'] = ''
            return render(request, 'register.html', context)

        # Crear el usuario y enviar el correo de verificación
        token = CRUD.add_user(username, name, lastname, lastname2, email, email_recover, password, password2)
        if token:
            verification_url = request.build_absolute_uri(f"/gestion_usuarios/verify-email/{token}")
            Email.send_verification_email(email, name, verification_url)
            messages.success(request, "Te hemos enviado un correo de verificación. Confirma para completar el registro.")
            return redirect('login')
        else:
            messages.error(request, "Hubo un error al crear el usuario.")
            return render(request, 'register.html', context)

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
        email = request.session.get('email')
        if not email:
            return redirect('login')  # Redirigir si no hay email en sesión
        
        update_data = {
            'username': request.POST.get('userName', '').strip(),
            'name': request.POST.get('accountName', '').strip(),
            'firstlastname': request.POST.get('accountFLast', '').strip(),
            'secondlastname': request.POST.get('accountSLast', '').strip(),
            'email_recover': request.POST.get('accountEmailBack', '').strip(),
        }
        
        # Filtrar campos vacíos
        update_data = {k: v for k, v in update_data.items() if v}
        
        # Manejo especial para contraseña
        password = request.POST.get('accountPassword', '').strip()
        password2 = request.POST.get('accountPassword2', '').strip()
        
        if password and password2 and password == password2:
            update_data['password'] = make_password(password)  
        
        try:
            if update_data:  # Solo actualizar si hay datos
                if crud_user.update_user(email, **update_data):
                    user = crud_user.get_user(email)
                    if not user:
                        messages.error(request, "El usuario no existe")
                        return redirect('login')
                    plan = crud_plan.get_plan(email)
                    horas = int(plan.hours)
                    minutos = int(round((plan.hours - horas) * 60))
                    tiempo = f"{horas}:{minutos:02d}"
                    request.session.update({
                        'email': user.email,
                        'username': user.username,
                        'name': user.name,
                        'email_recover': user.email_recover,
                        'firstlastname': user.firstlastname,
                        'secondlastname': user.secondlastname,
                        'hours': tiempo,
                        'plan': plan.type_plan
                    })
                    return redirect('account')
                
            return redirect('accountEdit')
        except Exception as e:
            return redirect('accountEdit')
            
    return redirect('dashboard')

def save_parameters(request):
    # Validar request
    if request.method == 'POST':
        email = request.session['email']
        
        # Obtener valores del formulario
        model = request.POST.get('modelName')               # Nombre del modelo
        algorithm = request.POST.get('selectAlgorithm')     # Tipo de algoritmo
        algorithm_type = request.POST.get('algoritmoType')  # Clasificación o Regresión
        primeStack = request.POST.get('primeStack')         # Columna objetivo
        number = crud_dataset.count_dataset(email) + 1      # Asignar ID del nuevo modelo
        model_name = f"{email}-{number}"                    # Nombre de almacenamiento servidor
        dataset_id = f"{model_name}_dataset"
        
        if algorithm_type == "regression":
            algorithm_type_b = 0
        else:
            algorithm_type_b = 1
        # Tipo 0 Regresion
        # Tipo 1 Clasificacion
        messages.success(request, f'{model_name} || {algorithm} || {algorithm_type} || {primeStack}')
        crud_model.create_model(model_name,dataset_id,None,None,model,algorithm,algorithm_type_b,primeStack)
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

        # Store model information in session for entrenar_modelo
        request.session['model_name'] = model_name
        request.session['dataset_name'] = dataset_name

        # --------- Arboles de Desicion -------------
        if algorithm == "arbolDesicion":
            # -------- Regresion --------------------
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
                print ("Hiperparametros: ", email,model_name,0,primeStack,criterion,splitter,max_depth,min_samples_split,min_leaf_split,max_leaf_nodes,min_impurity_decrease,max_features, random_state,ccp_alpha, 0)
                if envio:
                    messages.success(request, f'Hiperparametros Cargados con Exito') 
                    return entrenar_modelo(request)   
                else:
                    messages.success(request, f'Error al cargar los parametros')
                    return redirect('ia')
            # ---------- Clasificacion --------------
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
                    return entrenar_modelo(request)  
                else:
                    messages.success(request, f'Error al cargar los parametros')
                    return redirect('ia')
        
        # ------------ KNN -----------------
        elif algorithm == "kNeighbors":
            # ---------- Regresion ------------
            if algorithm_type == "regression":
                n_neighbors = request.POST.get('neighborsInput-KNN_reg')
                weights = request.POST.get('neighborsInput-KNN_reg')
                algorithm_knn = request.POST.get('algorithmRadio-KNN_reg')
                leaf_size = request.POST.get('lifeSizeInput-KNN_reg')
                p = request.POST.get('pInput-KNN_reg')
                metric = request.POST.get('metricaRadio-KNN_reg')
                algorithm_type_knn = 0
            # ------------ Clasificacion --------
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
                return entrenar_modelo(request)   
            else:
                messages.success(request, f'Error al cargar los parametros')
                return redirect('ia')
        
        # -------- Random Forest ------------------
        elif algorithm == "randomForest":
            # ---------- Regresion ---------
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
            # ------------ Clasificacion --------
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
                return entrenar_modelo(request)   
            else:
                messages.success(request, f'Error al cargar los parametros')
                return redirect('ia')
    else:
        messages.success(request, f'No existe un metodo Post')
        return redirect('ia')      

def entrenar_modelo(request):
    try:
        if request.content_type == 'application/json':
            # Para llamadas API
            data = json.loads(request.body)
            print("DATA JSON:", data)

        else:
            # Para llamadas desde formulario
            email = request.session.get('email')
            model_name = request.session.get('model_name')
            
            # Obtener el dataset path 
            dataset_name = request.session.get('dataset_name')
            dataset_path = os.path.join(settings.MEDIA_ROOT, 'file', email, model_name, dataset_name)
            model_path = os.path.join(settings.MEDIA_ROOT, 'file', email, model_name)

            # Tipo de algoritmo y problema
            modelo_tipo = request.POST.get('selectAlgorithm')
            problema = request.POST.get('algoritmoType')
            
            # Diccionario de configuracion
            data = {
                "config": {
                    "modelo": modelo_tipo,
                    "tipo": problema,
                    "email": email,
                    "model_name": model_name,
                    "dataset": {
                        "path": dataset_path,
                        "name": dataset_name,
                        "target_column": request.POST.get('primeStack')  # Columna objetivo
                    }
                },
                "hiperparametros": {}  # Se llenan segun el algoritmo
            }
            
            # --------------- Arboles de decisión ---------------
            if modelo_tipo == "arbolDesicion":
                suffix = "_reg" if problema == "regression" else "_class"
                if suffix == "_reg":
                    criterion_map = {
                        "0": "squared_error",
                        "1": "absolute_error",
                        "2": "friedman_mse",
                        "3": "poisson"
                    }

                    splitter_map = {
                        "0": "best",
                        "1": "random"
                    }

                    data["hiperparametros"] = {
                        "criterion": criterion_map.get(request.POST.get('criterioRadio-Tree_reg'), "squared_error"),
                        "splitter": splitter_map.get(request.POST.get('semillaRadio-Tree_reg'), "best"),
                        "max_depth": int(request.POST.get(f'nodosRange-Tree{suffix}', 0)),
                        "min_samples_split": int(request.POST.get(f'divisorRange-Tree{suffix}', 2)),
                        "min_samples_leaf": int(request.POST.get(f'hojasRange-Tree{suffix}', 0)),
                        "max_leaf_nodes": int(request.POST.get(f'max-hojasRange-Tree{suffix}', 0)),
                    }
                elif suffix == "_class":    
                    criterion_map = {
                        "0": "squared_error",
                        "1": "absolute_error",
                        "2": "friedman_mse",
                        "3": "poisson"
                    }

                    splitter_map = {
                        "0": "best",
                        "1": "random"
                    }
                
                    data["hiperparametros"] = {
                        "criterion": criterion_map.get(request.POST.get('criterioRadio-Tree_reg'), "squared_error"),
                        "splitter": splitter_map.get(request.POST.get('semillaRadio-Tree_reg'), "best"),
                        "max_depth": int(request.POST.get(f'nodosRange-Tree{suffix}', 0)),
                        "min_samples_split": int(request.POST.get(f'divisorRange-Tree{suffix}', 2)),
                        "min_samples_leaf": int(request.POST.get(f'hojasRange-Tree{suffix}', 0)),
                        "max_leaf_nodes": int(request.POST.get(f'max-hojasRange-Tree{suffix}', 0)),
                    }
            # -----------------------------------------------------------

            # ------------------------ KNN ------------------------------
            elif modelo_tipo == "kNeighbors":
                # Para KNN
                suffix = "_reg" if problema == "regression" else "_class"

                algorithm_map = {
                    "automatic": "auto",
                    "1": "ball_tree",
                    "2": "kd_tree",
                    "3": "brute",
                }
                    
                data["hiperparametros"] = {
                    "n_neighbors": int(request.POST.get(f'neighborsInput-KNN{suffix}', 5)),
                    "weights": request.POST.get(f'weightsRadio-KNN{suffix}', "uniform"),
                    "algorithm": algorithm_map.get(request.POST.get(f'algorithmRadio-KNN{suffix}', "auto")),
                    "leaf_size": int(request.POST.get(f'lifeSizeInput-KNN{suffix}', 2)),
                    "p" : int(request.POST.get(f'pInput-KNN{suffix}', 0)),
                    "metric" : request.POST.get(f'metricaRadio-KNN{suffix}', "euclidean"),
                }
                
            # ---------------------Random Forest ------------------------------------------
            elif modelo_tipo == "randomForest":
                # Para Random Forest
                suffix = "_reg" if problema == "regression" else "_class"
                data["hiperparametros"] = {
                    "n_neighbors": int(request.POST.get(f'neighborsInput-KNN{suffix}', 5)),
                    "weights": request.POST.get(f'weightsRadio-KNN{suffix}', "uniform"),
                    "algorithm": request.POST.get(f'algorithmRadio-KNN{suffix}', "auto"),
                    # ...otros parámetros...
                }
                pass
            # ------------------------------------------------------------------------------

        # Extraer la información para procesar
        config = data.get("config", {})
        modelo_tipo = config.get("modelo") if "config" in data else data.get("modelo")
        problema = config.get("tipo") if "config" in data else data.get("tipo")
        hiperparametros = data.get("hiperparametros", {})
        
        # Si el dataset no está en los hiperparámetros, añadirlo
        if "dataset" not in hiperparametros and "config" in data and "dataset" in config:
            hiperparametros["dataset"] = config["dataset"]
        
        config = data["config"]
        #dataset_info = config["dataset"]  # Diccionario con path y target_column

        # ------------ Procesar modelo
        print("Procesando modelo")
        modelo = ModelosML(dataset_path, model_path)
        print("Columna objetivo:", request.POST.get('primeStack'))  # Verifica el valor recibido

        if modelo_tipo == "kNeighbors" and problema == "classify":
            resultado = modelo.knn_clasificacion(**hiperparametros)
        elif modelo_tipo == "kNeighbors" and problema == "regression":
            resultado = modelo.knn_regresion(**hiperparametros)
        elif modelo_tipo == "randomForest" and problema == "classify":
            resultado = modelo.random_forest_clasificacion(**hiperparametros)
        elif modelo_tipo == "randomForest" and problema == "regression":
            resultado = modelo.random_forest_regresion(**hiperparametros)
        elif modelo_tipo == "arbolDesicion" and problema == "classify":
            resultado = modelo.arbol_clasificacion(**hiperparametros)
        elif modelo_tipo == "arbolDesicion" and problema == "regression":
            resultado = modelo.arbol_regresion(**hiperparametros)
        else:
            return JsonResponse({"error": "Modelo o tipo inválido"}, status=400)
        
        # Devolver resultado apropiado
        if request.content_type == 'application/json':
            return JsonResponse({"mensaje": "Modelo entrenado con éxito", "resultado": resultado})
        else:
            messages.success(request, "Modelo entrenado con éxito")
            return redirect('dashboard')
            
    except Exception as e:
        # Manejar errores
        print(f"Error: {str(e)}")
        if request.content_type == 'application/json':
            return JsonResponse({"error": str(e)}, status=500)
        else:
            messages.error(request, f"Error al entrenar modelo: {str(e)}")
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
                SET hours = %s, type_plan='Premium'
                WHERE email_id = %s
                """,
                [updated_hours, email]
            )
        plan = crud_plan.get_plan(email)
        horas = int(round(plan.hours)/60)
        minutos = int(round((plan.hours % 60)))
        tiempo = f"{horas}:{minutos:02d}"
        
        request.session.update({
            'hours': tiempo,
            'plan': plan.type_plan
        })
        #messages.success(request, f"Se han agregado {hours} horas a tu plan.")
        return redirect('account')

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

def delete_model(request, model_id, dataset_id):
    try:
        modelo = Model.objects.get(id_model=model_id)
        modelo.delete()
        dataset = Dataset.objects.get(id_dataset=dataset_id)
        dataset.delete()
        if Hiperparameters_KNN.objects.filter(model_id=model_id).exists():
            hiper_knn = Hiperparameters_KNN.objects.get(model_id=model_id)
            hiper_knn.delete()
        elif Hiperparameters_RandomForest.objects.filter(model_id=model_id).exists():
            hiper_rf = Hiperparameters_RandomForest.objects.get(model_id=model_id)
            hiper_rf.delete()
        elif Hiperparameters_Tree.objects.filter(model_id=model_id).exists():
            hiper_tree = Hiperparameters_Tree.objects.get(model_id=model_id)
            hiper_tree.delete()

        return redirect('dashboard')
    except Exception as e:
        print(f"Error al eliminar: {e}")
        return redirect('dashboard')
