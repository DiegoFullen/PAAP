from gestion_usuarios.models import Temporal
from django.utils import timezone

def create_temporal(email, username, password, name, firstlastname, secondlastname, email_recover, token):
    temporal = Temporal(
        email=email,
        username=username,
        name=name,
        firstlastname=firstlastname,
        secondlastname=secondlastname,
        email_recover=email_recover,
        token=token,
        created_at=timezone.now()
    )
    temporal.set_password(password)  # Cifra la contraseña
    temporal.save()
    return temporal

def create_request_temporal(email, username, password, name, firstlastname, secondlastname, email_recover, token):
    temporal = Temporal(
        email=email,
        username=username,
        name=name,
        firstlastname=firstlastname,
        secondlastname=secondlastname,
        email_recover=email_recover,
        password=password,
        token=token,
        created_at=timezone.now()
    )
    temporal.save()
    return temporal

# Obtener un registro temporal por email
def get_temporal(email):
    try:
        temporal = Temporal.objects.get(email=email)
        return temporal
    except Temporal.DoesNotExist:
        return None
# Obtener un registro temporal por el token
def get_temporal_token(token):
    try:
        temporal = Temporal.objects.get(token=token)
        return temporal
    except Temporal.DoesNotExist:
        return None

# Obtener todos los registros temporales
def get_all_temporals():
    return Temporal.objects.all()

# Actualizar un registro temporal
def update_temporal(email, **kwargs):
    try:
        temporal = Temporal.objects.get(email=email)
        for key, value in kwargs.items():
            setattr(temporal, key, value)
        temporal.save()
        return temporal
    except Temporal.DoesNotExist:
        return None
    
# Eliminar un registro temporal
def delete_temporal(token):
    try:
        temporal = Temporal.objects.get(token=token)
        temporal.delete()
        return True
    except Temporal.DoesNotExist:
        return False
    
