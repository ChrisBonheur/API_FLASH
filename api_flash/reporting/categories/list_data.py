import base64
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader


def generate_list_pdf(data_param):
    # Créer un objet de type BytesIO pour stocker le PDF en mémoire
    buffer = BytesIO()

    # Créer un document PDF avec la taille de page "letter"
    pdf = SimpleDocTemplate(buffer, pagesize=A4)

    # Définir les données du tableau
    data = [
        [k for k in data_param['content'][0].keys()]
    ]

    for obj in data_param['content']:
        row = []
        for k, v in obj.items():
            row.append(v)
        data.append(row)
    # Créer le tableau
    table = Table(data)

    # Appliquer un style au tableau
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Créer un style pour l'en-tête
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(name='Header', alignment=TA_CENTER)

    # Ajouter une image à l'en-tête (à gauche)
    image_data = "image_base64_string_here"  # Remplacez ceci par votre chaîne base64 d'image
    #image = Image(BytesIO(base64.b64decode(image_data)))
    #image.width = 50
    #image.height = 50

    # Ajouter un titre à l'en-tête (à droite)
    title = data_param['title']
    title = Paragraph(f'<b>{title}</b>', header_style)

    # Assembler les éléments de l'en-tête
    header_content = [[title]]
    header_table = Table(header_content, colWidths=[200, 350])

    # Construire le document PDF
    pdf_elements = [header_table, table]

    # Générer le PDF
    pdf.build(pdf_elements)

    # Convertir le contenu du PDF en base64
    pdf_base64 = "data:application/pdf;base64," + base64.b64encode(buffer.getvalue()).decode()

    return pdf_base64
