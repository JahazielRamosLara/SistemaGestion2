from django.db import models
from django. contrib.auth.models import User

# Create your models here.

class Estatus(models.Model):

    nombre = models.CharField(max_length = 50, unique = True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
class Remitente(models.Model):

    TRATOS_CHOICES = (
        ("Dip", "Diputado/a"),
        ("C", "Ciudadano/a"),
        ("Mtro", "Maestro/a"),
        ("Dr", "Doctor/a"),
        ("Ing", "Ingeniero/a"),
        ("Pdte", "Presidente"),
        ("Pdta", "Presidenta"),
    )

    nombre = models.CharField(max_length = 255, unique = True, verbose_name = "Nombre del Remitente")
    trato = models.CharField(
        max_length = 10,
        choices=TRATOS_CHOICES,
        default = "C."
    )
    area = models.CharField(max_length = 100, blank = True, null = True)
    activo = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.trato} {self.nombre}"
    
    class Meta:
        verbose_name_plural = "Remitentes"
        ordering = ["nombre"]

class Documento(models.Model):

    #Entrada
    folio = models.CharField(max_length = 20, unique = True, help_text = "Número de folio de entrada.")
    remitente = models.ForeignKey(
        "Remitente",
        on_delete = models.SET_NULL,
        null = True,
        verbose_name = "Remitente"
    )
    asunto = models.CharField(max_length = 255)
    resumen = models.TextField()
    fecha_captura = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Captura")

    #Digitalización del archivo
    archivo_pdf = models.FileField(upload_to = "documentos/entradas/")

    #Gestión y flujo
    responsable = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='documento', 
        verbose_name="Responsable"
    )
    responsables_adicionales = models.ManyToManyField(
        User,
        related_name="documentos_adicionales", 
        verbose_name="Otros",
        blank=True 
    )
    estatus_actual = models.ForeignKey(Estatus, on_delete = models.PROTECT, related_name = "documentos_en_estado")

    resumen_responsable = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Resumen del Responsable"
    )

    responsables_que_enviaron_resumen = models.ManyToManyField(
        User,
        related_name="documentos_con_resumen_enviado",
        blank=True,
        verbose_name="Responsables que enviaron resumen"
    )

    #Salida
    #Documento de respuesta generado
    documento_salida = models.FileField(
        upload_to = "documentos/salidas/", 
        null=True, blank=True, 
        verbose_name="Archivo de Salida (Respuesta)")
    fecha_archivo = models.DateField(
        null=True, blank=True, 
        verbose_name = "Fecha de Archivado")
    fecha_salida = models.DateField(
        null=True, blank=True, 
        verbose_name = "Fecha de Salida")
    folio_salida = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True,
        help_text="Número de folio de salida.",
        verbose_name = "Folio de Salida"
    )
    
    asunto_salida = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Asunto de Salida"
    )
    
    contenido_respuesta = models.TextField(
        null=True,
        blank=True,
        verbose_name="Contenido de la Respuesta"
    )
    
    def todos_enviaron_resumen(self):
        """Verifica si todos los responsables (principal + adicionales) enviaron su resumen"""
    # Total de responsables = principal (1) + adicionales
        total_responsables = 1 + self.responsables_adicionales.count()
    
    # Cuántos ya enviaron resumen
        enviados = self.responsables_que_enviaron_resumen.count()
    
        return enviados >= total_responsables

    def __str__(self):
        return f"Folio {self.folio} - {self.estatus_actual.nombre}"

class TransicionEstatus(models.Model):
    
    documento = models.ForeignKey(
        Documento, 
        on_delete=models.CASCADE, 
        verbose_name="Documento Auditado"
    )
    
    usuario_origen = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='transiciones_realizadas',
        verbose_name="Usuario Origen"
    )
    
    responsable_destino = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='documentos_asignados_historial',
        verbose_name="Responsable Destino"
    )
    
    nuevo_estatus = models.ForeignKey(
        'Estatus', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Nuevo Estatus"
    )
    fecha_transicion = models.DateTimeField(
        auto_now_add=True
    )
    comentario = models.TextField(
        blank=True, 
        null=True,
    )

    class Meta:
        ordering = ['fecha_transicion']

    def __str__(self):
        return f"Documento {self.documento.folio} - Turnado por {self.usuario_origen} a {self.responsable_destino}"
    
class ResumenResponsableAdicional(models.Model):
    
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='resumenes_adicionales')
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    resumen = models.TextField(verbose_name="Resumen")
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['documento', 'responsable']
    
    def __str__(self):
        return f"{self.responsable.username} - {self.documento.folio}"