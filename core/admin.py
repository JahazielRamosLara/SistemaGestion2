from django.contrib import admin
from .models import Estatus, Documento, Remitente

# Register your models here.

admin.site.register(Estatus)
admin.site.register(Documento)
admin.site.register(Remitente)