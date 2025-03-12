from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.conf import settings
import os
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from gestion_usuarios import CRUD

def send_verification_email(email, name, verification_url):
    subject = "Verificación de correo"
    from_email = "angelohaziel2002l@gmail.com"
    recipient_list = [email]
    image_path = os.path.join(settings.BASE_DIR, "static/resources/img/logotipoColor.png")
    pdf_url = "http://127.0.0.1:8000/static/resources/Aviso_de_Privacidad_2025.pdf"
    # Cuerpo del mensaje con imagen incrustada
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .button {{
                display: inline-block;
                background-color: #3c43cb;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2 style="text-align: center; color: #3c43cb;">¡Bienvenido a PAAP!</h2>
            <div style="text-align: center;">
            <img src="cid:logo_cid" alt="Logo de PAAP" style="width: 200px;"/>
            </div>
            <p>Hola <strong>{name}</strong>.</p>
            <p>Gracias por registrarte en nuestra plataforma. Para completar tu registro, por favor verifica tu correo, por favor, lee el siguiente aviso de privacidad y confirma dando clic en el enlace de abajo:</p>
            <div>
            <h3 style="text-align: center; color: #3c43cb;">Aviso de Privacidad</h2>
            </div>
            <div style="text-align: left;">
            <p>Fundamentados en las bases presentadas por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares, la empresa<strong> PAAP </strong>se hace responsable de recabar sus datos personales, del uso de los mismos y de su protección.</p>
            <p>Su información personal será usada para las siguientes funciones: Proveer los servicios solicitados, Notificarle información relacionada con el servicio solicitado, así como Notificarle cambios en los mismos, Realizar evaluaciones sobre los servicios y plataforma prestados a efecto de mejorar la calidad de estos.</p>
            <p>Para conseguir lo antes mencionado, necesitamos solicitarle los siguientes datos personales:</p>
            <ul>
                <li><strong>Nombre completo</strong></li>
                <li><strong>Dirección de correo electrónico</strong></li>
                <li><strong>Dirección de correo electrónico de respaldo</strong></li>
                <li><strong>Datos Bancarios*</strong></li>
            </ul>
            <p>Es importante recordarle sus derechos ARCO (Acceso, Rectificación y Cancelación) que puede ejercer en todo momento, así como Oponerse al tratamiento de estos. Si desea revocar nuestros permisos puede hacerlo desde la propia plataforma en la sección de Cuenta o enviar una solicitud al correo electrónico <a href="mailto:paap_oficial@paap-ja.com.mx">paap_oficial@paap-ja.com.mx</a> con el asunto “Remoción de permisos sobre datos personales” incluyendo la dirección de correo electrónico relacionada a la cuenta donde le enviaremos más instrucciones tan pronto nos sea posible.</p>
            <p>*La plataforma y la entrega de los servicios solicitados se aprueban una vez se resuelva el pago correspondiente. Nos basamos en los servicios de PayPal para el cobro de cualquier transacción, pero se aclara que <strong>PAAP NO GUARDA O MANEJA ESTOS DATOS, SE SOLICITAN POR MEDIO DE LA INTEGRACIÓN DE PAGOS CON PAYPAL.</strong></p>
            </div>
            <div style="text-align: center;">
                <a href="{ verification_url }" style="display: inline-block; background-color: #3c43cb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px; margin: 20px 0;">Verificar Correo</a>
            </div>
            <p>Si no puedes hacer clic en el botón, copia y pega este enlace en tu navegador:</p>
            <p style="word-wrap: break-word;"><a href="{verification_url}">{verification_url}</a></p>
            <div style="text-align: center;">
            <p>Puedes descargar el Aviso de Privacidad en el siguiente enlace:</p>
            <p><a href="{pdf_url}">Aviso de Pivacidad</a></p>
            </div>
            <p class="footer">Si no solicitaste este registro, por favor ignora este mensaje.</p>
        </div>
    </body>
    </html>
    """

    email_message = EmailMultiAlternatives(subject, "", from_email, recipient_list)
    email_message.attach_alternative(html_content, "text/html")

    # Adjuntar la imagen embebida
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            img = MIMEImage(img_file.read())
            img.add_header("Content-ID", "<logo_cid>")  # El CID que usaremos en el HTML
            img.add_header("Content-Disposition", "inline", filename="logotipoColor.png")
            email_message.attach(img)
    email_message.send()

def search_token_temporal(token):
    with connection.cursor() as cursor:
        cursor.execute(
        """
        SELECT * FROM gestion_usuarios_user_temporal
        WHERE token = %s
        """,
        [token]
        )
        token_data = cursor.fetchone()
    if token_data:
        return True
    else:
        return False


def verify_token(token, decision, password_recover):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, username, name, password, email_recover, firstlastname, secondlastname, created_at 
            FROM gestion_usuarios_user_temporal 
            WHERE token=%s
            """,
            [token]
        )
        user_data = cursor.fetchone()  # Obtener el usuario temporal

    if not user_data:
        return False
    else:
        # Extraer los datos del usuario
        id, email, username, name, password, email_recover, firstlastname, secondlastname, created_at = user_data
        if decision == 1:
            resultado  =  CRUD.add_new_user(id, email, username, name, password, email_recover, firstlastname, secondlastname, created_at, token)
        else: 
            if decision == 2:
                resultado = CRUD.update_user_password(password_recover,email,token,created_at)
        return resultado

def delete_temporal(token):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            delete FROM gestion_usuarios_user_temporal 
            WHERE token=%s
            """,
            [token]
        )

def send_email_recover(request, mail, retrieveEmail):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select * FROM gestion_usuarios_user 
            WHERE email=%s AND email_recover=%s
            """,
            [mail,retrieveEmail]
        )
        email_data = cursor.fetchone()
        
    if email_data:
        email, id_user, username, name, password, email_recover, status, firstlasname, secondlastname = email_data  
        token_recover = CRUD.add_user(username,name,firstlasname,secondlastname,email,email_recover,password,password)
        recovery_url = request.build_absolute_uri(f"/passwordRetrive/{token_recover}")
        subject = "Verificación de correo"
        from_email = "angelohaziel2002l@gmail.com"
        recipient_list = [retrieveEmail]
        html_content = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="UTF-8">
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    background-color: #f4f4f4;
                                    padding: 20px;
                                }}
                                .container {{
                                    max-width: 600px;
                                    margin: auto;
                                    background: white;
                                    border-radius: 10px;
                                    padding: 20px;
                                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                                }}
                                .button {{
                                    display: inline-block;
                                    background-color: #3c43cb;
                                    color: white;
                                    padding: 10px 20px;
                                    text-decoration: none;
                                    border-radius: 5px;
                                    font-size: 16px;
                                    margin: 20px 0;
                                }}
                                .footer {{
                                    text-align: center;
                                    font-size: 12px;
                                    color: #888;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <h2 style="text-align: center; color: #3c43cb;">Recuperación de Contraseña</h2>
                                <div style="text-align: center;">
                                    <img src="cid:logo_cid" alt="Logo de PAAP" style="width: 200px;"/>
                                </div>
                                <p>Hola <strong>{name}</strong>,</p>
                                <p>Hemos recibido una solicitud para recuperar la contraseña de tu cuenta. Si no fuiste tú, ignora este mensaje.</p>
                                <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p>
                                <div style="text-align: center;">
                                    <a href="{ recovery_url }" style="display: inline-block; background-color: #3c43cb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px; margin: 20px 0;">Recuperar Contraseña</a>
                                <p class="footer">Si no solicitaste este registro, por favor ignora este mensaje.</p>
                            </div>
                        </body>
                        </html>
        """
        email_message = EmailMultiAlternatives(subject, "", from_email, recipient_list)
        email_message.attach_alternative(html_content, "text/html")
        comprovasion = email_message.send()
        if comprovasion:
            return True
        else:
            return False
    else:
        return False    
