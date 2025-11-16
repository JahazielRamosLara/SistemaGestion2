from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic.edit import CreateView
from .models import Documento, Estatus, Remitente, TransicionEstatus
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .forms import TurnarDocumentoForm, GenerarSalidaForm, CapturaDocumentoForm, RemitenteForm, TurnarDocumentoForm
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
    template_name = "core\captura_documento.html"
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
            estatus_capturado = Estatus.objects.get(nombre="Capturado")
        except Estatus.DoesNotExist:
            messages.error(self.request, 'Error al guardar: El estatus "Capturado" no existe en la base de datos.')
            return self.form_invalid(form)

        self.object.estatus_actual = estatus_capturado
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
        nombres_adicionales = ", ".join([user.username for user in responsables_adicionales])

        if responsables_adicionales:
            mensaje = f'Documento {self.object.folio} capturado. Notificado a {self.object.responsable.username} y a {nombres_adicionales}.'
        else:
            mensaje = f'Documento {self.object.folio} capturado y notificado a {self.object.responsable.username}.'
        
        messages.success(self.request, mensaje)

        return super().form_valid(form)
    
class DashboardSecretariaView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Documento
    template_name = "core/dashboard_secretaria.html"
    context_object_name = "documentos"

    def test_func(self):
        
        return is_secretaria(self.request.user)
    
    def get_queryset(self):
        
        estados_gestion_sec = ["Capturado", "Contestar por memo", "En Firma"]

        return Documento.objects.filter(
            estatus_actual__nombre__in = estados_gestion_sec
        ).order_by("-id")
    
class DashboardResponsableView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Documento
    template_name = "core/dashboard_responsable.html"
    context_object_name = "documentos"

    def test_func(self):
        return is_responsable(self.request.user)
    
    def get_queryset(self):
        
        estados_gestion_responsable = ["Notificado", "En Trámite", "Turnado", "Terminado"]

        return Documento.objects.filter(
            Q(responsable=self.request.user) | Q(responsables_adicionales=self.request.user),
            estatus_actual__nombre__in=estados_gestion_responsable
        ).distinct().order_by("-id")
    
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
    
@user_passes_test(is_secretaria)
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

@user_passes_test(is_responsable)
@transaction.atomic
def iniciar_tramite(request, pk):

    documento = get_object_or_404(Documento, pk = pk)

    if documento.estatus_actual.nombre != "Notificado":
        messages.error(request, "Error: Solo documentos en estado 'Notificado' pueden iniciar trámite.")
        return redirect("core:detalle_documento", pk = pk)
    
    try:
        nuevo_estatus = Estatus.objects.get(nombre = "En Trámite")
        documento.estatus_actual = nuevo_estatus
        documento.save()
        messages.success(request, f"Folio {documento.folio} marcado como 'En Trámite'.")
    except Estatus.DoesNotExist:
        messages.error(request, "Error interno: El estatus 'En Trámite' no existe.")

    return redirect("core:dashboard_responsable")

@user_passes_test(is_responsable)
@transaction.atomic
def devolver_para_contestar(request, pk):
    
    documento = get_object_or_404(Documento, pk = pk)

    estado_actual = documento.estatus_actual.nombre
    if estado_actual != "En Trámite":
        messages.error(request, "Error: Solo documentos en estado 'En Trámite' pueden devolverse para contestar.")
        return redirect("core:detalle_documento", pk=pk)
    
    try:
        nuevo_estatus = Estatus.objects.get(nombre = "Contestar por memo")
        documento.estatus_actual = nuevo_estatus
        documento.save()
        messages.success(request, f"Folio {documento.folio} devuelto a Secretaria para 'Contestar por memo'.")
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
    
    documento = get_object_or_404(Documento, pk = pk)

    if documento.estatus_actual.nombre != "Contestar por memo":
        messages.error(request, "Error: El documento no puede ser respondido en este estado.")
        return redirect("core:detalle_documento", pk = pk)
    
    if request.method == "POST":
        form = GenerarSalidaForm(request.POST, request.FILES, instance = documento)

        if form.is_valid():
            form.save()

            try:
                estatus_archivado = Estatus.objects.get(nombre = "En Firma")
                documento.estatus_actual = estatus_archivado
                documento.save()
                messages.success(request, f"Folio {documento.folio} marcado como 'En Firma'.")
                return redirect("core:dashboard_secretaria")
            except Estatus.DoesNotExist:
                messages.error(request, "Error interno: El estatus 'En Firma' no existe.")
                return redirect("detalle_documento", pk = pk)
    else:
        form = GenerarSalidaForm(instance = documento)

    return render(request, "core/generar_salida.html", {"form": form, "documento": documento})

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