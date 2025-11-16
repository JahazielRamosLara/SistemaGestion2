from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("captura/", views.CapturaDocumentoView.as_view(), name = "captura_documento"),
    #path("notificar/<int:pk>/", views.notificar_documento, name = "notificar_documento"),
    path("tramite/<int:pk>/", views.iniciar_tramite, name = "iniciar_tramite"),
    path("contestar_memo/<int:pk>/", views.devolver_para_contestar, name = "devolver_para_contestar"),
    path("responsable/turnar/<int:pk>/", views.turnar_documento, name = "turnar_documento"),
    path("dashboard/secretaria/", views.DashboardSecretariaView.as_view(), name = "dashboard_secretaria"),
    path("dashboard/responsable/", views.DashboardResponsableView.as_view(), name = "dashboard_responsable"),
    path("salida/generar/<int:pk>/", views.generar_salida, name = "generar_salida"),
    path("archivo/<int:pk>/", views.archivar_documento, name = "archivar_documento"),
    path("documento/<int:pk>/", views.DetalleDocumentoView.as_view(), name = "detalle_documento"),
    path("remitentes/gestion/", views.RemitenteListView.as_view(), name = "gestion_remitentes"),
    path("remitentes/desactivar/<int:pk>/", views.desactivar_remitente, name = "desactivar_remitente"),
    path("remitente/crear/", views.RemitenteCreateView.as_view(), name = "crear_remitente"),
    path("remitente/gestion/", views.RemitenteListView.as_view(), name = "gestion_remitente"),
    path("remitente/toggle/<int:pk>/", views.RemitenteToggleActivoView.as_view(), name = "remitente_toggle_activo"),
    ]