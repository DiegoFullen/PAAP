from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

def list_users(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT email, username, name, status FROM gestion_usuarios_user where status = 1")
        users = cursor.fetchall()
    return render(request, 'gestion_usuarios/user_list.html', {'users': users})

# Crear Usuario
def create_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        email_recover = request.POST.get('email_recover')
        status = request.POST.get('status') == "on"  # Checkbox handling

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO gestion_usuarios_user (email, username, name, password, email_recover, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [email, username, name, password, email_recover, status]
            )
        messages.success(request, "Usuario creado exitosamente")
        return redirect('user-list')

    # Pasar un usuario vacío para que el formulario esté limpio
    return render(request, 'gestion_usuarios/user_form.html', {'user': None})


# Editar Usuario
def edit_user(request, email):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        email_recover = request.POST.get('email_recover')
        status = request.POST.get('status') == "on"  # Checkbox handling

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE gestion_usuarios_user
                SET username=%s, name=%s, password=%s, email_recover=%s, status=%s
                WHERE email=%s
                """,
                [username, name, password, email_recover, status, email]
            )
        messages.success(request, "Usuario actualizado exitosamente")
        return redirect('user-list')

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT email, username, name, password, email_recover, status FROM gestion_usuarios_user WHERE email=%s",
            [email]
        )
        user = cursor.fetchone()

    # Convertir la tupla en un diccionario para facilitar el manejo en el template
    user_data = {
        'email': user[0],
        'username': user[1],
        'name': user[2],
        'password': user[3],
        'email_recover': user[4],
        'status': user[5]
    }
    return render(request, 'gestion_usuarios/user_form.html', {'user': user_data})

# Eliminar Usuario (actualizar status a 0)
def delete_user(request, email):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE gestion_usuarios_user SET status = 0 WHERE email = %s", [email])
    messages.success(request, "Usuario desactivado exitosamente")
    return redirect('user-list')


# Eliminar Usuario
def delete_user2(request, email):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM gestion_usuarios_user WHERE email=%s", [email])
    messages.success(request, "Usuario eliminado exitosamente")
    return redirect('user-list')


