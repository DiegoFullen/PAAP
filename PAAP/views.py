from django.http import HttpResponse
from django.template import Template,Context
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

#def index(request):
#    doc = open("C:/Users/angel/OneDrive/Documentos/UNI/Proyectos/PAAP/htdocs/index.html")
#    plt=Template(doc.read())
#    doc.close()
#    ctx =Context()
#    documento = plt.render(ctx)
#    return HttpResponse(documento)

def index(request):
    return render(request, 'index.html')
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM gestion_usuarios_user WHERE email=%s AND password=%s",
                [email, password]
            )
            user = cursor.fetchone()
        if user:
            return redirect('dashboard')
        else:
            messages.error(request, "Correo o contraseña incorrectos")
            return redirect('login')

    return render(request, 'login.html')
def dashboard_view(reques):
    return render(reques, 'dashboard.html')
def ia_view(request):
    return render(request, 'ia.html')