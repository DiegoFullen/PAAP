from django.db import connection

def login_user (email, password):
    #Buscar el usuario en la base de datos dentro y evaluar si este esta activo o no
    with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM gestion_usuarios_user 
                WHERE email=%s AND password=%s AND status=1
                """,
                [email, password]
            )
            user = cursor.fetchone()    
    return user
def login_plan (email):
    with connection.cursor() as cursor: 
        cursor.execute(
                """
                SELECT type_plan
                FROM gestion_usuarios_plan 
                WHERE email_id = %s
                """,
                [email]
            )
        plan = cursor.fetchone()
    return plan