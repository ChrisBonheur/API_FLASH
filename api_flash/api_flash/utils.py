from rest_framework.exceptions import NotFound
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import qrcode
import random
from django.core.mail import send_mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.cache import cache
import logging as lg



def get_object_or_raise(object, pk, data_name):
    try:
        elt = object.objects.get(pk=pk)
    except Exception as e:
        raise NotFound({"detail": f"Aucne donnée trouvée sur le model {data_name} contenant l'identifiant {pk}"})
    else:
        return elt



def generate_qr_code_with_text(data, text):
    # Générer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convertir l'image en base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    base64_encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return f'data:image/png;base64,{base64_encoded}'


def gen_matricule(id: int, prefix: str, length: int = 1_000_000):
    length_to_str = len(f"{length}")
    id_to_str = len(f"{id}")
    
    if id > length:
        return f"{prefix}{id}"
    
    zero_to_add = length_to_str - id_to_str
    zeros_str = "".join(["0" for item in range(zero_to_add)])
    return f"{prefix}{zeros_str}{id}"


def generate_number(num_digits):
    min_value = 10 ** (num_digits - 1)
    max_value = (10 ** num_digits) - 1  
    return random.randint(min_value, max_value)


async def sendemail(subject, message, email_list):
    # Paramètres du serveur SMTP
    smtp_server = 'mail.umng-flash.com'
    smtp_port = 587 # Port SMTP (généralement 587 pour TLS ou 465 pour SSL)
    smtp_username = 'flash@umng-flash.com'
    smtp_password = "e@f25Bc76"

    # Adresse e-mail de l'expéditeur
    from_email = smtp_username

    # Objet et contenu de l'e-mail
    body = message
    to_emails = ', '.join(email_list)
    # Création de l'e-mail
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_emails
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP et envoi de l'e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Démarre la connexion TLS (si nécessaire)
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_emails, msg.as_string())
        print('email enoye')
    except Exception as e:
        print(f'Erreur lors de l\'envoi de l\'e-mail : {str(e)}')
    finally:
        try:
            server.quit()  # Ferme la connexion SMTP
        except Exception:
            pass


def set_each_first_letter_in_upper(content):
    words = content.split(' ')
    # Mettre en majuscule la première lettre de chaque mot
    capitalized_words = [word.strip().capitalize() for word in words]
    return ' '.join(capitalized_words)



def get_or_create_cache_from_model(cache_name, model, Q_object=None):
    """get or create cache if not exist for model filter
    Args:
        cache_name (str): name of cache
        model (model class): model to filter
        Q_object: filter model with Q object from django.db.models 
    """
    if cache.get(cache_name, "not exist") == "not exist":
        try:
            if Q_object != None:
                cache.set(cache_name, model.objects.filter(Q_object))
            else:
                cache.set(cache_name, model.objects.all())
        except NameError as e:
            lg.critical(f"Model name not found : {e}")
        except Exception as e:
            lg.warning(e)
    
    return cache.get(cache_name, "not exist")