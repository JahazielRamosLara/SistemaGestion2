from django.core.mail import send_mail
from django.conf import settings

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