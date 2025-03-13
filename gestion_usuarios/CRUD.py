from django.db import connection
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta

#Funciones de CRUD
def add_user(username, name, lastname,lastname2,email,email_recover,password,password2):
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
    return token

def add_new_user(id, email, username, name, password, email_recover, firstlastname, secondlastname, created_at, token):
    if datetime.now() <= created_at + timedelta(minutes=15):

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
            return True
    else:
         return False

def update_user_password(password, email ,token,created_at):
    if datetime.now() <= created_at + timedelta(minutes=15): 
        with connection.cursor() as cursor:
                    cursor.execute(
                    """
                    UPDATE gestion_usuarios_user SET password = %s
                    WHERE email = %s
                    """,
                    [password, email]
                    )

                    # Eliminar el registro temporal
                    cursor.execute(
                    """
                    DELETE FROM gestion_usuarios_user_temporal 
                    WHERE token=%s
                    """,
                    [token]
                    )
        return True
    else:
        return False    
    
def search_models(email):
    with connection.cursor() as cursor:
        # Consulta SQL con JOIN
        cursor.execute(
            """
            SELECT gm.id_model, gm.name, gm.type, gd.name_dataset
            FROM gestion_usuarios_model gm
            INNER JOIN gestion_usuarios_dataset gd ON gm.id_dataset = gd.id_dataset
            WHERE gm.email_id = %s
            """,
            [email]  # Filtra por el email del usuario
        )
        # Obtener todos los resultados
        modelos = cursor.fetchall()
        return modelos