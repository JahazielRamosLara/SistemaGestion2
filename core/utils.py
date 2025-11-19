from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

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
    
def generar_pdf_salida(documento, contenido_respuesta):
    """
    Genera un PDF de documento de salida oficial
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo para el encabezado
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # Estilo para el contenido
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16
    )
    
    # Estilo para datos en negritas
    bold_style = ParagraphStyle(
        'Bold',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    # === ENCABEZADO ===
    elements.append(Paragraph("GOBIERNO DEL ESTADO DE JALISCO", header_style))
    elements.append(Paragraph("PODER LEGISLATIVO", subtitle_style))
    elements.append(Paragraph("SECRETARÍA DEL CONGRESO", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # === INFORMACIÓN DEL DOCUMENTO ===
    info_data = [
        ["Folio de Salida:", documento.folio_salida or "N/A"],
        ["Fecha:", documento.fecha_salida.strftime("%d de %B de %Y") if documento.fecha_salida else "N/A"],
        ["Turno del folio:", documento.folio],
        ["Asunto:", documento.asunto],
        ["Destinatario:", str(documento.remitente)],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # === CONTENIDO DE LA RESPUESTA ===
    elements.append(Paragraph("<b>Contenido de la Respuesta:</b>", bold_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Dividir el contenido en párrafos
    paragraphs = contenido_respuesta.split('\n')
    for para in paragraphs:
        if para.strip():
            elements.append(Paragraph(para, content_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # === RESÚMENES DE RESPONSABLES ===
    if documento.resumen_responsable:
        elements.append(Paragraph("<b>Resumen del Responsable Principal:</b>", bold_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"<b>{documento.responsable.username}:</b> {documento.resumen_responsable}", content_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Resúmenes adicionales
    resumenes_adicionales = documento.resumenes_adicionales.all()
    if resumenes_adicionales:
        elements.append(Paragraph("<b>Resúmenes de Responsables Adicionales:</b>", bold_style))
        elements.append(Spacer(1, 0.1*inch))
        for resumen in resumenes_adicionales:
            elements.append(Paragraph(f"<b>{resumen.responsable.username}:</b> {resumen.resumen}", content_style))
            elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # === PIE DE PÁGINA ===
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("___________________________________", footer_style))
    elements.append(Paragraph("Coordinador de Servicios Generales", footer_style))
    
    # Construir el PDF
    doc.build(elements)
    
    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf