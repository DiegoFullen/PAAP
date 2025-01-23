#from allauth.socialaccount.signals import social_account_added
from django.db import connection
from django.dispatch import receiver

#@receiver(social_account_added)
def create_user_in_custom_table(request, sociallogin, **kwargs):
    user = sociallogin.user  # Usuario autenticado por Google
    email = user.email
    name = user.first_name + " " + user.last_name if user.last_name else user.first_name

    # Inserta el usuario en tu tabla personalizada si no existe
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT IGNORE INTO gestion_usuarios_users (email, username, name, password, email_recover, status) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            [email, email.split('@')[0], name, "", "", "activo"]
        )
