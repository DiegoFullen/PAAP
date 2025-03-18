from django.db import connection
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta 
from gestion_usuarios import crud_temporal,crud_user,crud_plan,crud_dataset,crud_model
from django.contrib.auth.hashers import make_password

#Funciones de CRUD
def add_user(username, name, lastname,lastname2,email,email_recover,password,password2):
    if password == password2:
            token = get_random_string(length=32)  # Genera un token único
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
    
def search_models(email):
    modelos = crud_model.get_user_models(email)
    #with connection.cursor() as cursor:
        # Consulta SQL con JOIN
    #    cursor.execute(
    #        """
    #        SELECT gm.id_model, gm.name, gm.type, gd.name
    #        FROM gestion_usuarios_model gm
    #        INNER JOIN gestion_usuarios_dataset gd ON gm.id_dataset = gd.id_dataset
    #        WHERE gm.email_id = %s
    #        """,
    #        [email]  # Filtra por el email del usuario
    #    )
        # Obtener todos los resultados
    #    modelos = cursor.fetchall()
    return modelos


def select_hiperparametros(id_dataset):
     with connection.cursor() as cursor:
        # Consulta SQL con JOIN
        cursor.execute(
            """
            SELECT * FROM hiperparametros WHERE id_dataset = %s
            """,
            [id_dataset]  # Filtra por el email del usuario
        )
        # Obtener todos los resultados
        hiperparametros = cursor.fetchall()
        return hiperparametros

def select_dataset(id_dataset):
     with connection.cursor() as cursor:
        # Consulta SQL con JOIN
        cursor.execute(
            """
            SELECT * FROM gestion_usuarios_dataset WHERE id_dataset = %s
            """,
            [id_dataset]  # Filtra por el email del usuario
        )
        # Obtener todos los resultados
        data_dataset = cursor.fetchall()
        return data_dataset
     