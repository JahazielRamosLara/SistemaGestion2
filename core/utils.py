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

    print("=" * 60)
    print("DEBUG - ENVÍO DE CORREO")
    print(f"Responsables recibidos: {responsables}")
    print(f"Emails encontrados: {destinatarios}")
    print(f"Cantidad de destinatarios: {len(destinatarios)}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 60)
    
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
        print(f"🔄 Intentando enviar correo a: {destinatarios}")
        resultado = send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            destinatarios,
            fail_silently=False,
        )
        print(f"✅ send_mail retornó: {resultado}")
        print(f"Correo enviado exitosamente a: {', '.join(destinatarios)}")
        return True
    except Exception as e:
        print(f"Error al enviar correo: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False