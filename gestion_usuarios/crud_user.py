from gestion_usuarios.models import User, Temporal

#CREAR USUARIOS
def create_user(email, username, password, name, firstlastname, secondlastname, email_recover, status):
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
        name=name,
        firstlastname=firstlastname,
        secondlastname=secondlastname,
        email_recover=email_recover,
        status=status
    )
    return user

#TRANSFERIR UN USUARIO DE TEMPORAL
def transfer_temporal_to_user(token):
    try:
        # Obtener el registro temporal
        temporal = Temporal.objects.get(token=token)

        # Crear el usuario con los datos del registro temporal
        user = User.objects.create_user(
            email=temporal.email,
            username=temporal.username,
            password=temporal.password,  # Usar la contraseña ya cifrada
            name=temporal.name,
            firstlastname=temporal.firstlastname,
            secondlastname=temporal.secondlastname,
            email_recover=temporal.email_recover,
            status=True  # O cualquier otro valor por defecto
        )

        # Eliminar el registro temporal (opcional)
        temporal.delete()

        return user
    except Temporal.DoesNotExist:
        return None

#LEER UDUARIOS
# Obtener un usuario por email
def get_user(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None

#Obtener un usuario por email y username
def get_user_email(email, email_recover):
    try:
        user = User.objects.get(email=email,email_recover=email_recover)
        return user
    except User.DoesNotExist:
        return None
# Obtener todos los usuarios
def get_all_users():
    return User.objects.all()

# ACTUALIZAR UN USUARIO
def update_user(email, **kwargs):
    try:
        user = User.objects.get(email=email)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user
    except User.DoesNotExist:
        return None

    
#ELIMINAR UN USUARIO
def delete_user(email):
    try:
        user = User.objects.get(email=email)
        user.delete()
        return True
    except User.DoesNotExist:
        return False