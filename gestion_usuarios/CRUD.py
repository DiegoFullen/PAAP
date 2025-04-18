from django.db import connection
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta 
from gestion_usuarios import crud_temporal,crud_user,crud_plan,crud_dataset,crud_model, crud_hiperparameters_tree, crud_hiperparameters_KNN, crud_hiperparameters_RF
from django.contrib.auth.hashers import make_password
from gestion_usuarios.models import User

#Funciones de CRUD


def add_user(username, name, lastname,lastname2,email,email_recover,password,password2):
    if password == password2:
            token = get_random_string(length=32)
            temporal = crud_temporal.create_temporal(email,username,password,name,lastname,lastname2,email_recover,token)
            if temporal:
                return token
            else: return None
    else: return None

def add_recover_password_request(username, name, lastname,lastname2,email,email_recover,password):
    token = get_random_string(length=32)
    temporal = crud_temporal.create_request_temporal(email,username,password,name,lastname,lastname2,email_recover,token)
    if temporal:
        return token
    else: return None

def add_new_user(created_at, token):
    if timezone.now() <= created_at + timedelta(minutes=15):
            user = crud_user.transfer_temporal_to_user(token)
            if user:
                if user.email.endswith("@ceti.mx"):
                    crud_plan.create_plan(0,"Escolar", user.email)
                    return True
                else:
                    crud_plan.create_plan(0,"Integrado", user.email)
                    return True
            else:
                 crud_user.delete_user(user.email)
                 return False
    else:
         crud_temporal.delete_temporal(token)
         return False

def update_user_password(password, email ,token,created_at):
    if timezone.now() <= created_at + timedelta(minutes=15): 
        cifred_password = make_password(password)
        crud_user.update_user(email, password=cifred_password)
        crud_temporal.delete_temporal(token)
        return True
    else:
        return False    

def update_user(email, **kwargs):
    """
    Actualiza los campos del usuario que no estén vacíos.
    
    Args:
        email (str): Email del usuario a actualizar (identificador)
        **kwargs: Campos a actualizar (username, password, name, lastname, etc.)
        
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    from .models import User  # Asegúrate de importar tu modelo User
    
    try:
        user = User.objects.get(email=email)
        update_fields = []
        
        for field, value in kwargs.items():
            if value is not None and value != '':  # Solo actualizar si el valor no es None ni vacío
                if field == 'password':
                    # Si es password, lo ciframos antes de guardar
                    user.set_password(value)
                else:
                    setattr(user, field, value)
                update_fields.append(field)
        
        if update_fields:  # Solo guardar si hay campos para actualizar
            user.save(update_fields=update_fields)
        
        return True
    except User.DoesNotExist:
        return False

def search_models(email):
    modelos = crud_model.get_user_models(email)
    return modelos

def save_hiperparameters_tree(email,model_id,type,prime_stack,criterion,
                                               splitter,max_depth,min_samples_split,
                                               min_leaf_split,max_leaf_nodes,min_impurity_decrease,
                                               max_features,random_state,ccp_alpha,class_weight):
    if type == 0:
        if crud_hiperparameters_tree.create_hiperparameters_tree_regression(email,model_id,type,prime_stack,criterion,
                                                splitter,max_depth,min_samples_split,
                                                min_leaf_split,max_leaf_nodes,min_impurity_decrease,
                                                max_features,random_state,ccp_alpha,class_weight):
            return True
        else: return False
    elif type == 1: 
        if crud_hiperparameters_tree.create_hiperparameters_tree_classify(email,model_id,type,prime_stack,criterion,
                                               splitter,max_depth,min_samples_split,
                                               min_leaf_split,max_leaf_nodes,min_impurity_decrease,
                                               max_features,random_state,ccp_alpha,class_weight):
            return True
        else: return False
    else: return False

def save_hiperparameters_knn(email,model_id,type,prime_stack,n_neighbors,weights,algorithm,leaf_size,p,metric):
    if  crud_hiperparameters_KNN.create_hiperparameters_KNN(email,model_id,type,prime_stack,n_neighbors,weights,algorithm,leaf_size,p,metric):
        return True
    else: return False

def save_hiperparameters_RF(email,model_id,type,prime_stack,n_estimators,criterion,max_depth,min_samples_split,
                              min_samples_leaft, max_features,bootstrap,oob_score,max_samples,random_state,class_weight):
    if  crud_hiperparameters_RF.create_hiperparameters_RF(email,model_id,type,prime_stack,n_estimators,criterion,max_depth,min_samples_split,
                              min_samples_leaft, max_features,bootstrap,oob_score,max_samples,random_state,class_weight):
        return True
    else: return False

def reduce_hours(minutes, email):
    try:
        plan = crud_plan.get_plan(email)
        if plan is None:  # Verificación más explícita
            print(f"No se encontró plan para el email: {email}")
            return False
            
        hours = plan.hours - minutes
        
        # FORMA CORRECTA de llamar a update_plan:
        updated_plan = crud_plan.update_plan(
            email_id=email,  # Primer parámetro NOMBRADO
            hours=hours      # Segundo parámetro como parte de kwargs
        )
        
        return updated_plan is not None
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return False
