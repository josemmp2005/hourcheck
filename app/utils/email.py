import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email(email: str, token: str):
    link = f"https://localhost:3000/invitation?token={token}"
    asunto = "Invitation - HourCheck"
    cuerpo = f"""Hola,

Has sido invitado a HourCheck. Para aceptar la invitación, haz clic en el siguiente link:

{link}

Este link expirará en 1 hora.

Si no solicitaste esto, ignora este correo.

Saludos,
El equipo de HourCheck
"""

    mensaje = MIMEText(cuerpo)
    mensaje["Subject"] = asunto
    mensaje["From"] = SMTP_USER
    mensaje["To"] = email

    # Para testing: solo mostrar el email en lugar de enviarlo
    print("=== EMAIL DE PRUEBA ===")
    print(f"Para: {email}")
    print(f"Asunto: {asunto}")
    print(f"Contenido:\n{cuerpo}")
    print("========================")
    
    # Comentar estas líneas para testing sin envío real:
    # try:
    #     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    #         server.starttls()
    #         server.login(SMTP_USER, SMTP_PASSWORD)
    #         server.send_message(mensaje)
    #         print("Correo enviado correctamente")
    # except Exception as e:
    #     print("Error al enviar correo:", e)
    #     raise
