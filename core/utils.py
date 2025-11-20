from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas

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
    """
    buffer = BytesIO()
    
    # Configurar el documento con márgenes más amplios
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=1.2*inch, 
        leftMargin=1.2*inch,
        topMargin=1*inch, 
        bottomMargin=1*inch
    )
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo para el encabezado superior (GOBIERNO, PODER, SECRETARÍA)
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=3,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=13
    )
    
    # Estilo para el área e info superior derecha
    area_style = ParagraphStyle(
        'AreaStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        alignment=TA_RIGHT,
        fontName='Helvetica',
        leading=11
    )
    
    # Estilo para datos dentro del cuadro
    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        fontName='Helvetica',
        leading=13,
        leftIndent=15,
        rightIndent=15
    )
    
    # Estilo para el contenido justificado
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        leading=14,
        leftIndent=15,
        rightIndent=15,
        spaceBefore=4,
        spaceAfter=4
    )
    
    # Estilo para "Atentamente" (alineado a la izquierda)
    atentamente_style = ParagraphStyle(
        'Atentamente',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        spaceAfter=40,
        spaceBefore=25,
        leftIndent=15
    )
    
    # Estilo para firma y cargo (alineado a la izquierda)
    firma_style = ParagraphStyle(
        'Firma',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=11,
        leftIndent=15
    )
    
    # === ENCABEZADO SUPERIOR ===
    elements.append(Paragraph("GOBIERNO DEL ESTADO DE JALISCO", header_style))
    elements.append(Paragraph("PODER LEGISLATIVO", header_style))
    elements.append(Paragraph("SECRETARÍA DEL CONGRESO", header_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # === INICIO DEL CUADRO ===
    cuadro_content = []
    
    # Obtener la fecha en formato español
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
    
    # Formatear el folio como INF-M/foliosalida/año
    folio_formateado = f"INF-M/{documento.folio_salida}/{año}"
    
    # Info superior derecha dentro del cuadro
    info_superior_derecha = f"""
    <b>{folio_formateado}</b><br/>
    {fecha_texto}
    """
    
    cuadro_content.append([Paragraph(info_superior_derecha, area_style)])
    
    # Espaciado inicial dentro del cuadro
    cuadro_content.append([Spacer(1, 0.15*inch)])
    
    # Información del destinatario (remitente original)
    nombre_completo = f"{documento.remitente.trato}. {documento.remitente.nombre}" if documento.remitente else "N/A"
    cargo_destinatario = documento.remitente.area if documento.remitente and documento.remitente.area else "N/A"
    
    info_destinatario = f"""
    <b>{nombre_completo}</b><br/>
    {cargo_destinatario}
    """
    cuadro_content.append([Paragraph(info_destinatario, value_style)])
    
    cuadro_content.append([Spacer(1, 0.15*inch)])
    
    # Turno del folio
    turno_text = f"<b>Turno del folio: {documento.folio}</b>"
    cuadro_content.append([Paragraph(turno_text, value_style)])
    
    cuadro_content.append([Spacer(1, 0.15*inch)])
    
    # Asunto
    asunto_text = f"<b>Asunto:</b><br/>{asunto_salida}"
    cuadro_content.append([Paragraph(asunto_text, value_style)])
    
    # Espacio reducido entre asunto y contenido
    cuadro_content.append([Spacer(1, 0.15*inch)])
    
    # === CONTENIDO DE LA RESPUESTA ===
    # Agregar cada párrafo del contenido
    paragraphs = contenido_respuesta.split('\n')
    for para in paragraphs:
        if para.strip():
            cuadro_content.append([Paragraph(para.strip(), content_style)])
    
    # Espacio antes de la firma
    cuadro_content.append([Spacer(1, 0.3*inch)])
    
    # === PIE DEL DOCUMENTO (alineado a la izquierda) ===
    cuadro_content.append([Paragraph("Atentamente", atentamente_style)])
    
    # Espacio para firma (línea alineada a la izquierda)
    cuadro_content.append([Paragraph("_________________________________", firma_style)])
    
    # Nombre y cargo del firmante (alineado a la izquierda)
    firma_texto = """
    <b>Lic. Verónica Salazar Serrano</b><br/>
    <b>Coordinadora de Servicios Generales</b>
    """
    cuadro_content.append([Paragraph(firma_texto, firma_style)])
    
    # Espaciado antes de la frase
    cuadro_content.append([Spacer(1, 0.15*inch)])
    
    # Frase del año (cursiva, centrada, pequeña)
    frase_style = ParagraphStyle(
        'FraseAnio',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    frase_texto = "2025, año de la eliminación de la transmisión materno infantil de enfermedades infecciosas"
    cuadro_content.append([Paragraph(frase_texto, frase_style)])
    
    # Espaciado final
    cuadro_content.append([Spacer(1, 0.15*inch)])
    
    # Crear la tabla con todo el contenido del cuadro
    main_table = Table(cuadro_content, colWidths=[6*inch])
    main_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1.5, colors.black),  # Borde exterior del cuadro
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(main_table)
    
    # Construir el PDF
    doc.build(elements)
    
    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf