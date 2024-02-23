from rest_framework.exceptions import NotFound
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import qrcode
import random
from django.core.mail import send_mail



def get_object_or_raise(object, pk, data_name):
    try:
        elt = object.objects.get(pk=pk)
    except Exception as e:
        raise NotFound({"details": f"Aucne donnée trouvée sur le model {data_name} contenant l'identifiant {pk}"})
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

    # Ajouter du texte au-dessus du QR code
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font)
    text_position = ((img.width - text_width) // 2, 10)
    draw.text(text_position, text, fill="black", font=font)

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


def sendemail(subject, message, email_list):
    return send_mail(subject, message, "mafoundou.bonheur@zandosoft.com", email_list)


def set_each_first_letter_in_upper(content):
    words = content.split(' ')
    # Mettre en majuscule la première lettre de chaque mot
    capitalized_words = [word.strip().capitalize() for word in words]
    return ' '.join(capitalized_words)