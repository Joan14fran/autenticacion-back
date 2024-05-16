import random
from django.core.mail import EmailMessage, EmailMultiAlternatives
from .models import User, OneTimePasssword
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import secrets

def generateOtp():
    otp = ''.join(secrets.choice('0123456789') for _ in range(6))
    return otp


def send_code_to_user(email):
    subject = "Código de acceso de un solo uso para verificación de correo electrónico"
    otp_code = generateOtp()
    user = User.objects.get(email=email)
    current_site = "Sistema de Autenticacion"

    # Renderizar la plantilla HTML para el correo electrónico
    email_html = render_to_string('accounts/email_verification.html', {
        'user': user,
        'current_site': current_site,
        'otp_code': otp_code
    })

    # Crear el correo electrónico
    email = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(email_html),  # Cuerpo en texto plano para clientes de correo que no admiten HTML
        from_email=settings.EMAIL_HOST,
        to=[email]
    )
    email.attach_alternative(email_html, "text/html")  # Adjuntar la versión HTML del correo electrónico

    # Guardar el código OTP en la base de datos
    OneTimePasssword.objects.create(user=user, code=otp_code)
    
    # Enviar el correo electrónico
    email.send(fail_silently=True)
    
def send_normal_email(data):
    email = EmailMultiAlternatives(
        subject=data['email_subject'],
        body=strip_tags(data['email_body']),  # Cuerpo en texto plano para clientes de correo que no admiten HTML
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.attach_alternative(data['email_body'], "text/html")  # Adjuntar la versión HTML del correo electrónico

    email.send(fail_silently=True)
    