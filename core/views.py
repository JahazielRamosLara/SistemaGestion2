from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic.edit import CreateView
from .models import Documento, Estatus, Remitente, TransicionEstatus, ResumenResponsableAdicional
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .forms import TurnarDocumentoForm, GenerarSalidaForm, CapturaDocumentoForm, RemitenteForm, TurnarDocumentoForm, IniciarTramiteForm, ResumenAdicionalForm
from django.views.generic import ListView, DetailView, View, UpdateView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django import forms
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import enviar_notificacion_documento, generar_pdf_salida
from django.core.files.base import ContentFile
from datetime import date

# Create your views here.

def is_secretaria(user):

    if user.is_authenticated:
        return user.groups.filter(name = "Secretaria").exists()
    return False

def is_responsable(user):
    
    return user.groups.filter(name = "Responsable").exists()

class CapturaDocumentoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    
    model = Documento
    #fields = ["folio", "remitente", "asunto", "resumen", "archivo_pdf", "responsable", "responsables_adicionales"]
    form_class = CapturaDocumentoForm
    template_name = "core/captura_documento.html"
    success_url = reverse_lazy('core:dashboard_secretaria')

    def test_func(self):
        
        return is_secretaria(self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        remitente_form = RemitenteForm()
        context["remitente_form"] = remitente_form

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.captura_por = self.request.user 
        
        try:
            estatus_notificado = Estatus.objects.get(nombre = "Notificado")
        except Estatus.DoesNotExist:
            messages.error(self.request, 'Error al guardar: El estatus "Notificado" no existe en la base de datos.')
            return self.form_invalid(form)

        self.object.estatus_actual = estatus_notificado
        self.object.save()
        
        form.save_m2m()

        TransicionEstatus.objects.create(
            documento = self.object,
            usuario_origen = self.request.user,
            responsable_destino = self.object.responsable,
            nuevo_estatus = self.object.estatus_actual,
            comentario = f"Documento capturado y asignado a {self.object.responsable.username} por {self.request.user.username}."
        )

        responsables_adicionales = self.object.responsables_adicionales.all()
    
        for responsable_adicional in responsables_adicionales:
            TransicionEstatus.objects.create(
                documento=self.object,
                usuario_origen=self.request.user,
                responsable_destino=responsable_adicional,
                nuevo_estatus=self.object.estatus_actual,
                comentario=f"Documento capturado y notificado a {responsable_adicional.username} como responsable adicional por {self.request.user.username}."
            )

        todos_responsables = [self.object.responsable] + list(responsables_adicionales)
        correo_enviado = enviar_notificacion_documento(self.object, todos_responsables)
        nombres_adicionales = ", ".join([user.username for user in responsables_adicionales])

        nombres_adicionales = ", ".join([user.username for user in responsables_adicionales])

        if responsables_adicionales:
            mensaje = f'Documento {self.object.folio} capturado. Notificado a {self.object.responsable.username} y a {nombres_adicionales}.'
        else:
            mensaje = f'Documento {self.object.folio} capturado y notificado a {self.object.responsable.username}.'
        
        if correo_enviado:
            mensaje += " Correos enviados."
        else:
            mensaje += " No se pudieron enviar los correos (verifica que los usuarios tengan email)."

        messages.success(self.request, mensaje)

        return super().form_valid(form)
    
class DashboardSecretariaView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Documento
    template_name = "core/dashboard_secretaria.html"
    context_object_name = "documentos"

    def test_func(self):
        
        return is_secretaria(self.request.user)
    
    def get_queryset(self):
        
        vista = self.request.GET.get("vista", "pendientes")

        if vista == "historial":
            estados_finalizados = ["Archivado"]
            return Documento.objects.filter(
                estatus_actual__nombre__in = estados_finalizados
                ).order_by("-id")
        else:
            estados_pendientes = ["Capturado", "Notificado", "En Trámite", "Turnado", "Contestar por memo", "En Firma"]
        return Documento.objects.filter(
            estatus_actual__nombre__in = estados_pendientes
        ).order_by("-id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vista_actual"] = self.request.GET.get("vista", "pendientes")
        return context
    
class DashboardResponsableView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Documento
    template_name = "core/dashboard_responsable.html"
    context_object_name = "documentos"

    def test_func(self):
        return is_responsable(self.request.user)
    
    def get_queryset(self):
        vista = self.request.GET.get("vista", "pendientes")
        
        base_query = Documento.objects.filter(
            Q(responsable=self.request.user) | Q(responsables_adicionales=self.request.user)
        ).distinct()
        
        if vista == "historial":
            estados_finalizados = ["Archivado"]
            return base_query.filter(
                estatus_actual__nombre__in = estados_finalizados
            ).order_by("-id")
        else:
            
            estados_pendientes = ["Capturado", "Notificado", "En Trámite", "Turnado", "Contestar por memo", "En Firma"]
            return base_query.filter(
                estatus_actual__nombre__in = estados_pendientes
            ).order_by("-id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vista_actual"] = self.request.GET.get("vista", "pendientes")
        return context
    
class DetalleDocumentoView(LoginRequiredMixin, DetailView):
    
    model = Documento
    template_name = "core/detalle_documento.html"
    context_object_name = "documento"

class RemitenteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Remitente
    template_name = "core/gestion_remitentes.html"
    context_object_name = "remitentes"

    def test_func(self):

        return is_secretaria(self.request.user)
    
    def get_queryset(self):
        
        return Remitente.objects.all().order_by("pk")
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["form"] = RemitenteForm()
        return super().get_context_data(**kwargs)
    
    def post(self, request, *args, **kwargs):
       
        form = RemitenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:gestion_remitentes")
        
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

@method_decorator(csrf_exempt, name = "dispatch") # Solo para simplificar, usa @csrf_protect en producción
class RemitenteToggleActivoView(LoginRequiredMixin, View):

    def post(self, request, pk):

        remitente = get_object_or_404(Remitente, pk = pk)
        remitente.activo = not remitente.activo
        remitente.save()
        return JsonResponse({
            "status": "success", 
            "habilitado": remitente.activo,
            "nombre": str(remitente)
        })
    
class RemitenteCreateView(LoginRequiredMixin, CreateView):

    model = Remitente
    form_class = RemitenteForm
    template_name = "core/remitente_modal.html"
    success_url = reverse_lazy("core:captura_documento")
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.activo = True
        instance.save()
        full_name = f"{instance.trato}. {instance.nombre}"
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "id": instance.id, 
                "nombre": full_name
            })
    
        return super().form_valid(form)
    
    def form_invalid(self, form):

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            
            error_message = form.errors.as_text()
            
            return JsonResponse(
                {'error': error_message}, 
                status=400 
            )
        
        return super().form_invalid(form)
    
"""@user_passes_test(is_secretaria)
@transaction.atomic
def notificar_documento(request, pk):

    documento = get_object_or_404(Documento, pk = pk)

    if documento.estatus_actual.nombre != "Capturado":
        messages.error(request, "Error: El documento ya fue notificado o tiene otro estado")
        return redirect("core:detalle_documento", pk = pk)
    
    estatus_notificado = Estatus.objects.get(nombre = "Notificado")
    documento.estatus_actual = estatus_notificado
    documento.save()

    if documento.responsable and documento.responsable.email:
        send_mail(
            subject = f"Oficio asignado - Folio {documento.folio}",
            message = f"Se le ha asignado el oficio: {documento.asunto}.",
            from_email = "jachachel@gmail.com",
            recipient_list = [documento.responsable.email],
            fail_silently = False
        )
    
    messages.success(request, f"Folio {documento.folio} notificado con éxito.")
    return redirect("core:dashboard_secretaria")
"""
@user_passes_test(is_responsable)
@transaction.atomic
def iniciar_tramite(request, pk):
    documento = get_object_or_404(Documento, pk=pk)

    # Verificar si es responsable principal o adicional
    es_principal = documento.responsable == request.user
    es_adicional = documento.responsables_adicionales.filter(id=request.user.id).exists()
    
    if not es_principal and not es_adicional:
        messages.error(request, "Error: No tiene permisos para este documento.")
        return redirect("core:dashboard_responsable")

    # Validación de estado
    if es_principal:
        if documento.estatus_actual.nombre != "Notificado":
            messages.error(request, "Error: Solo documentos en estado 'Notificado' pueden iniciar trámite.")
            return redirect("core:detalle_documento", pk=pk)
    else:
        if documento.estatus_actual.nombre not in ["Notificado", "En Trámite", "Turnado"]:
            messages.error(request, "Error: No puede enviar resumen en el estado actual del documento.")
            return redirect("core:detalle_documento", pk=pk)
    
    if request.method == "POST":
        if es_principal:
            # Formulario para responsable principal
            form = IniciarTramiteForm(request.POST, instance=documento)
            if form.is_valid():
                form.save()
                documento.responsables_que_enviaron_resumen.add(request.user)
                
                try:
                    nuevo_estatus = Estatus.objects.get(nombre="En Trámite")
                    documento.estatus_actual = nuevo_estatus
                    documento.save()
                    messages.success(request, f"Folio {documento.folio} marcado como 'En Trámite'.")
                except Estatus.DoesNotExist:
                    messages.error(request, "Error interno: El estatus 'En Trámite' no existe.")
                    return redirect("core:detalle_documento", pk=pk)
                
                return redirect("core:dashboard_responsable")
        else:
            # Formulario para responsable adicional
            form = ResumenAdicionalForm(request.POST)
            if form.is_valid():
                # Guardar resumen adicional
                ResumenResponsableAdicional.objects.create(
                    documento=documento,
                    responsable=request.user,
                    resumen=form.cleaned_data['resumen']
                )
                documento.responsables_que_enviaron_resumen.add(request.user)
                messages.success(request, "Resumen enviado exitosamente.")
                return redirect("core:dashboard_responsable")
    else:
        # Verificar si ya envió su resumen
        if documento.responsables_que_enviaron_resumen.filter(id=request.user.id).exists():
            messages.warning(request, "Ya ha enviado su resumen para este documento.")
            return redirect("core:dashboard_responsable")
        
        if es_principal:
            form = IniciarTramiteForm(instance=documento)
        else:
            form = ResumenAdicionalForm()
    
    context = {
        "form": form, 
        "documento": documento,
        "es_adicional": es_adicional
    }
    return render(request, "core/iniciar_tramite.html", context)

@user_passes_test(is_responsable)
@transaction.atomic
def devolver_para_contestar(request, pk):
    documento = get_object_or_404(Documento, pk=pk)

    # Solo el responsable principal puede devolver
    if documento.responsable != request.user:
        messages.error(request, "Error: Solo el responsable principal puede devolver el documento.")
        return redirect("core:detalle_documento", pk=pk)
    
    # Verificar que todos hayan enviado resumen
    if not documento.todos_enviaron_resumen():
        messages.error(request, "Error: Debe esperar a que todos los responsables adicionales envíen su resumen.")
        return redirect("core:dashboard_responsable")

    if documento.estatus_actual.nombre != "En Trámite":
        messages.error(request, "Error: Solo documentos en estado 'En Trámite' pueden devolverse.")
        return redirect("core:detalle_documento", pk=pk)
    
    try:
        nuevo_estatus = Estatus.objects.get(nombre="Contestar por memo")
        documento.estatus_actual = nuevo_estatus
        documento.save()
        messages.success(request, f"Folio {documento.folio} devuelto a Secretaría para 'Contestar por memo'.")
    except Estatus.DoesNotExist:
        messages.error(request, "Error: El estatus de destino no existe.")
    
    return redirect("core:dashboard_responsable")
    

@user_passes_test(is_responsable)
@transaction.atomic
def turnar_documento(request, pk):

    documento = get_object_or_404(Documento, pk = pk)

    estado_actual = documento.estatus_actual.nombre
    if estado_actual not in ["Notificado", "En Trámite", "Turnado"]:
        messages.error(request, "Error: El documento no puede ser turnado en este estado.")
        return redirect("core:detalle_documento", pk = pk)
    
    if request.method == "POST":
        form = TurnarDocumentoForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.cleaned_data["nuevo_responsable"]

            estatus_turnado = Estatus.objects.get(nombre = "Turnado")

            documento.estatus_actual = estatus_turnado
            documento.responsable = nuevo_usuario
            documento.save()

            messages.success(request, f"Folio {documento.folio} turnado con éxito a {nuevo_usuario.username}.")
            return redirect("core:dashboard_responsable")
    else:
        form = TurnarDocumentoForm()

    return render(request, "core/turnar_documento.html", {"form": form, "documento": documento})
    
@user_passes_test(is_secretaria)
@transaction.atomic
def archivar_documento(request, pk):

    documento = get_object_or_404(Documento, pk = pk)

    if documento.estatus_actual.nombre != "En Firma":
        messages.error(request, "Error: Solo documentos en estado 'En Firma' pueden ser archivados.")
        return redirect("core:dashboard_secretaria")
    
    try:
        estatus_archivado = Estatus.objects.get(nombre = "Archivado")
        documento.estatus_actual = estatus_archivado
        documento.save()

        messages.success(request, f"Folio {documento.folio} archivado con éxito.")

    except Estatus.DoesNotExist:
        messages.error(request, "Error interno: El estatus 'Archivado' no existe.")
        
        return redirect("core:dashboard_secretaria")
    
    return redirect("core:dashboard_secretaria")

@user_passes_test(is_secretaria)
@transaction.atomic
def generar_salida(request, pk):
    
    documento = get_object_or_404(Documento, pk=pk)

    if documento.estatus_actual.nombre != "Contestar por memo":
        messages.error(request, "Error: El documento no puede ser respondido en este estado.")
        return redirect("core:detalle_documento", pk=pk)
    
    if request.method == "POST":
        form = GenerarSalidaForm(request.POST)

        if form.is_valid():
            # Obtener datos del formulario
            folio_salida = form.cleaned_data['folio_salida']
            contenido_respuesta = form.cleaned_data['contenido_respuesta']
            
            # Asignar folio y fecha automática
            documento.folio_salida = folio_salida
            documento.fecha_salida = date.today()
            
            # Generar el PDF
            try:
                pdf_content = generar_pdf_salida(documento, contenido_respuesta)
                
                # Guardar el PDF en el campo documento_salida
                nombre_archivo = f"salida_{documento.folio_salida.replace('/', '_')}.pdf"
                documento.documento_salida.save(nombre_archivo, ContentFile(pdf_content), save=False)
                
                # Cambiar estado a "En Firma"
                estatus_firma = Estatus.objects.get(nombre="En Firma")
                documento.estatus_actual = estatus_firma
                documento.save()
                
                messages.success(request, f"Documento de salida generado exitosamente. Folio: {documento.folio_salida}")
                return redirect("core:dashboard_secretaria")
                
            except Exception as e:
                messages.error(request, f"Error al generar el PDF: {str(e)}")
                return redirect("core:generar_salida", pk=pk)
    else:
        form = GenerarSalidaForm()

    context = {
        "form": form,
        "documento": documento,
    }
    
    return render(request, "core/generar_salida.html", context)

@login_required
def home_redirect(request):

    if is_secretaria(request.user):
        return redirect("core:dashboard_secretaria")
    elif is_responsable(request.user):
        return redirect("core:dashboard_responsable")
    else:
        return redirect("/admin/")
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Secretaria').exists())
def desactivar_remitente(request, pk):
    
    if request.method == 'POST':
        remitente = get_object_or_404(Remitente, pk=pk)
        remitente.activo = False 
        remitente.save()
        return redirect('gestion_remitentes')
    return HttpResponseRedirect(reverse_lazy('gestion_remitentes'))