from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def enviar_notificacion_documento(documento, responsables):
    """
    Envía correo de notificación a los responsables de un documento.
    
    Args:
        documento: Instancia del modelo Documento
        responsables: Lista de usuarios (responsables)
    """
    
    # Asunto del correo
    asunto = f'Nuevo documento asignado - Folio: {documento.folio}'
    
    # Obtener emails de los responsables
    destinatarios = [user.email for user in responsables if user.email]
    
    # Si no hay emails, no enviar nada
    if not destinatarios:
        print("No hay destinatarios con email válido")
        return False
    
    # Crear el mensaje
    mensaje = f"""
Se le ha asignado un nuevo documento para su atención:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Folio: {documento.folio}
Remitente: {documento.remitente}
Asunto: {documento.asunto}
Resumen: {documento.resumen}
Estatus: {documento.estatus_actual.nombre}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para más detalles, acceda al sistema en:
https://jahaziel.pythonanywhere.com/documento/{documento.pk}/

---
Este es un correo automático, por favor no responda.
Sistema de Gestión de Documentos
Congreso del Estado de Jalisco
    """
    
    try:
        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            destinatarios,
            fail_silently=False,
        )
        print(f"Correo enviado exitosamente a: {', '.join(destinatarios)}")
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

def generar_pdf_salida(documento, asunto_salida, contenido_respuesta):
    """
    Genera un PDF de documento de salida oficial estilo memorándum
    Formato: Media carta (letter height / 2)
    """
    buffer = BytesIO()
    
    # Tamaño media carta: 21.59 cm x 27.94 cm
    media_carta = (21.59*cm, 27.94*cm)
    
    # Registrar fuente Arial Narrow obligatoriamente
    import os
    
    # Intentar diferentes rutas para encontrar Arial Narrow
    posibles_rutas = [
        'C:/Windows/Fonts/ARIALN.TTF',  # Windows
        'C:/WINDOWS/Fonts/ARIALN.TTF',
        '/usr/share/fonts/truetype/msttcorefonts/ARIALN.TTF',  # Linux
        '/System/Library/Fonts/ARIALN.TTF',  # Mac
        os.path.join(os.path.dirname(__file__), 'fonts', 'ARIALN.TTF'),  # Carpeta local
    ]
    
    posibles_rutas_bold = [
        'C:/Windows/Fonts/ARIALNB.TTF',
        'C:/WINDOWS/Fonts/ARIALNB.TTF',
        '/usr/share/fonts/truetype/msttcorefonts/ARIALNB.TTF',
        '/System/Library/Fonts/ARIALNB.TTF',
        os.path.join(os.path.dirname(__file__), 'fonts', 'ARIALNB.TTF'),
    ]
    
    # Buscar y registrar Arial Narrow
    font_registered = False
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            try:
                pdfmetrics.registerFont(TTFont('ArialNarrow', ruta))
                font_registered = True
                break
            except:
                continue
    
    # Buscar y registrar Arial Narrow Bold
    bold_registered = False
    for ruta in posibles_rutas_bold:
        if os.path.exists(ruta):
            try:
                pdfmetrics.registerFont(TTFont('ArialNarrow-Bold', ruta))
                bold_registered = True
                break
            except:
                continue
    
    if not font_registered or not bold_registered:
        font_name_bold = 'Helvetica-Bold'       
    font_name = 'ArialNarrow'
    font_name_bold = 'ArialNarrow-Bold'
    
    # Márgenes exactos: superior 1.25cm, inferior 1.5cm, izquierdo 6.5cm, derecho 1.6cm
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=media_carta,
        leftMargin=6.5*cm,
        rightMargin=1.6*cm,
        topMargin=1.25*cm,
        bottomMargin=1.5*cm
    )
    
    # Márgenes exactos: superior 1.25cm, inferior 1.5cm, izquierdo 6.5cm, derecho 1.6cm
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=media_carta,
        leftMargin=6.5*cm,
        rightMargin=1.6*cm,
        topMargin=1.25*cm,
        bottomMargin=1.5*cm
    )
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos base
    styles = getSampleStyleSheet()
    
    # Estilo para folio (esquina superior derecha, negrita)
    folio_style = ParagraphStyle(
        'FolioStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_RIGHT,
        fontName=font_name_bold,
        leading=12
    )
    
    # Estilo para fecha (debajo del folio, normal)
    fecha_style = ParagraphStyle(
        'FechaStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_RIGHT,
        fontName=font_name,
        leading=12
    )
    
    # Estilo para destinatario (negrita)
    destinatario_style = ParagraphStyle(
        'DestinatarioStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=12
    )
    
    # Estilo para cargo (negrita)
    cargo_style = ParagraphStyle(
        'CargoStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=12
    )
    
    # Estilo para asunto (todo en negrita)
    asunto_style = ParagraphStyle(
        'AsuntoStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=12
    )
    
    # Estilo para el contenido justificado
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        leading=12,
        fontName=font_name
    )
    
    # Estilo para "Atentamente" (negrita)
    atentamente_style = ParagraphStyle(
        'Atentamente',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=12
    )
    
    # Estilo para la frase del año (negrita)
    frase_style = ParagraphStyle(
        'FraseAnio',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=12
    )
    
    # Estilo para firma (negrita)
    firma_style = ParagraphStyle(
        'Firma',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=12
    )
    
    # === PREPARAR DATOS ===
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    if documento.fecha_salida:
        año = documento.fecha_salida.year
        dia = documento.fecha_salida.day
        mes = meses[documento.fecha_salida.month]
        fecha_texto = f"Guadalajara, Jalisco a {dia} de {mes} de {año}"
    else:
        año = "2025"
        fecha_texto = "Guadalajara, Jalisco"
    
    # Formatear el folio
    folio_formateado = f"INF-M/{documento.folio_salida}/{año}"
    
    # === CONSTRUIR DOCUMENTO ===
    
    # Folio (negrita, alineado a la derecha)
    elements.append(Paragraph(folio_formateado, folio_style))
    
    # Fecha (negrita, alineada a la derecha)
    elements.append(Paragraph(fecha_texto, folio_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Destinatario (negrita)
    nombre_completo = f"{documento.remitente.trato} {documento.remitente.nombre}" if documento.remitente else "N/A"
    elements.append(Paragraph(nombre_completo, destinatario_style))
    
    # Cargo/Área (negrita)
    cargo_destinatario = documento.remitente.area if documento.remitente and documento.remitente.area else "N/A"
    elements.append(Paragraph(cargo_destinatario, cargo_style))
    elements.append(Spacer(1, 0.4*cm))
    
    # Asunto (todo en negrita)
    elements.append(Paragraph(f"Asunto: {asunto_salida}", asunto_style))
    elements.append(Spacer(1, 0.4*cm))
    
    # === CONTENIDO DE LA RESPUESTA ===
    paragraphs = contenido_respuesta.split('\n')
    for para in paragraphs:
        if para.strip():
            elements.append(Paragraph(para.strip(), content_style))
            elements.append(Spacer(1, 0.2*cm))
    
    elements.append(Spacer(1, 0.4*cm))
    
    # === PIE DEL DOCUMENTO ===
    elements.append(Paragraph("Atentamente,", atentamente_style))
    elements.append(Spacer(1, 0.05*cm))
    
    # Frase del año con salto de línea
    frase_texto = '"2025, año de la eliminación de la transmisión<br/>materno infantil de enfermedades infecciosas"'
    elements.append(Paragraph(frase_texto, frase_style))
    elements.append(Spacer(1, 1*cm))
    
    # Firma (negrita)
    elements.append(Paragraph("Lic. Verónica Salazar Serrano", firma_style))
    elements.append(Paragraph("Coordinadora de Servicios Generales", firma_style))
    
    # Construir el PDF
    doc.build(elements)
    
    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf


def generar_pdf_salida_carta(documento, asunto_salida, contenido_respuesta):
    """
    Genera un PDF de documento de salida en formato CARTA
    Formato: Carta completa (letter)
    Márgenes: superior 1.75cm, inferior 1.5cm, izquierdo 5.5cm, derecho 1.5cm
    Fuente: Arial 11pt
    """
    buffer = BytesIO()
    
    # Tamaño carta completo
    from reportlab.lib.pagesizes import letter
    
    # Registrar fuente Arial
    import os
    
    # Intentar diferentes rutas para encontrar Arial
    posibles_rutas = [
        'C:/Windows/Fonts/ARIAL.TTF',
        'C:/WINDOWS/Fonts/ARIAL.TTF',
        '/usr/share/fonts/truetype/msttcorefonts/arial.ttf',
        '/System/Library/Fonts/Arial.ttf',
        os.path.join(os.path.dirname(__file__), 'fonts', 'ARIAL.TTF'),
    ]
    
    posibles_rutas_bold = [
        'C:/Windows/Fonts/ARIALBD.TTF',
        'C:/WINDOWS/Fonts/ARIALBD.TTF',
        '/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf',
        '/System/Library/Fonts/Arial Bold.ttf',
        os.path.join(os.path.dirname(__file__), 'fonts', 'ARIALBD.TTF'),
    ]
    
    # Buscar y registrar Arial
    font_registered = False
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            try:
                pdfmetrics.registerFont(TTFont('Arial', ruta))
                font_registered = True
                break
            except:
                continue
    
    # Buscar y registrar Arial Bold
    bold_registered = False
    for ruta in posibles_rutas_bold:
        if os.path.exists(ruta):
            try:
                pdfmetrics.registerFont(TTFont('Arial-Bold', ruta))
                bold_registered = True
                break
            except:
                continue
    
    if not font_registered or not bold_registered:
        font_name_bold = 'Helvetica-Bold'       
    font_name = 'Arial'
    font_name_bold = 'Arial-Bold'
    
    # Márgenes: superior 1.75cm, inferior 1.5cm, izquierdo 5.5cm, derecho 1.5cm
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        leftMargin=5.5*cm,
        rightMargin=1.5*cm,
        topMargin=1.75*cm,
        bottomMargin=1.5*cm
    )
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos base
    styles = getSampleStyleSheet()
    
    # Estilo para folio (esquina superior derecha, negrita)
    folio_style = ParagraphStyle(
        'FolioStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_RIGHT,
        fontName=font_name_bold,
        leading=13
    )
    
    # Estilo para destinatario (negrita)
    destinatario_style = ParagraphStyle(
        'DestinatarioStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=13
    )
    
    # Estilo para cargo (negrita)
    cargo_style = ParagraphStyle(
        'CargoStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=13
    )
    
    # Estilo para asunto (todo en negrita)
    asunto_style = ParagraphStyle(
        'AsuntoStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=13
    )
    
    # Estilo para el contenido justificado
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        leading=13,
        fontName=font_name
    )
    
    # Estilo para "Atentamente" (negrita)
    atentamente_style = ParagraphStyle(
        'Atentamente',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=13
    )
    
    # Estilo para la frase del año (negrita)
    frase_style = ParagraphStyle(
        'FraseAnio',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=13
    )
    
    # Estilo para firma (negrita)
    firma_style = ParagraphStyle(
        'Firma',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName=font_name_bold,
        leading=13
    )
    
    # === PREPARAR DATOS ===
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    if documento.fecha_salida:
        año = documento.fecha_salida.year
        dia = documento.fecha_salida.day
        mes = meses[documento.fecha_salida.month]
        fecha_texto = f"Guadalajara, Jalisco a {dia} de {mes} de {año}"
    else:
        año = "2025"
        fecha_texto = "Guadalajara, Jalisco"
    
    # Formatear el folio
    folio_formateado = f"INF-M/{documento.folio_salida}/{año}"
    
    # === CONSTRUIR DOCUMENTO ===
    
    # Folio (negrita, alineado a la derecha)
    elements.append(Paragraph(folio_formateado, folio_style))
    
    # Fecha (negrita, alineada a la derecha)
    elements.append(Paragraph(fecha_texto, folio_style))
    elements.append(Spacer(1, 0.6*cm))
    
    # Destinatario (negrita)
    nombre_completo = f"{documento.remitente.trato} {documento.remitente.nombre}" if documento.remitente else "N/A"
    elements.append(Paragraph(nombre_completo, destinatario_style))
    
    # Cargo/Área (negrita)
    cargo_destinatario = documento.remitente.area if documento.remitente and documento.remitente.area else "N/A"
    elements.append(Paragraph(cargo_destinatario, cargo_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Asunto (todo en negrita)
    elements.append(Paragraph(f"Asunto: {asunto_salida}", asunto_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # === CONTENIDO DE LA RESPUESTA ===
    paragraphs = contenido_respuesta.split('\n')
    for para in paragraphs:
        if para.strip():
            elements.append(Paragraph(para.strip(), content_style))
            elements.append(Spacer(1, 0.25*cm))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # === PIE DEL DOCUMENTO ===
    elements.append(Paragraph("Atentamente,", atentamente_style))
    elements.append(Spacer(1, 0.05*cm))
    
    # Frase del año con salto de línea
    frase_texto = '"2025, año de la eliminación de la transmisión<br/>materno infantil de enfermedades infecciosas"'
    elements.append(Paragraph(frase_texto, frase_style))
    elements.append(Spacer(1, 1.2*cm))
    
    # Firma (negrita)
    elements.append(Paragraph("Lic. Verónica Salazar Serrano", firma_style))
    elements.append(Paragraph("Coordinadora de Servicios Generales", firma_style))
    
    # Construir el PDF
    doc.build(elements)
    
    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf