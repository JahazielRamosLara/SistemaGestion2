from django import forms
from django.contrib.auth.models import User
from .models import Documento, Remitente
from django.forms.widgets import SelectMultiple
from django.contrib.auth import get_user_model

User = get_user_model()

class TurnarDocumentoForm(forms.Form):

    nuevo_responsable = forms.ModelChoiceField(
        queryset = User.objects.all(),
        label = "Turnar a"
    )

class GenerarSalidaForm(forms.ModelForm):
    
    class Meta:
        model = Documento
        fields = ["fecha_salida", "documento_salida"]

class CapturaDocumentoForm(forms.ModelForm):

    remitente = forms.ModelChoiceField(
        queryset=Remitente.objects.filter(activo=True),
        label = "Remitente",
        empty_label = "---------",
        widget=forms.Select(attrs = {"class": "form-control"})
    )

    responsable = forms.ModelChoiceField(
        queryset = User.objects.filter(groups__name = "Responsable"),
        label = "Responsable",
        empty_label = "---------",
        required = True,
        widget = forms.Select(attrs = {
            "class": "form-control",
            "id": "id_responsable"
            })
    )

    responsables_adicionales = forms.ModelMultipleChoiceField(
        queryset = User.objects.filter(groups__name = "Responsable"),
        widget = SelectMultiple(attrs = {"class": "form-control"}),
        required = False,
        label = "Otros"
    )

    class Meta:

        model = Documento
        fields = ("folio", "remitente", "asunto", "resumen", "archivo_pdf", "responsable", "responsables_adicionales")
        widgets = {
            "folio": forms.TextInput(attrs={"class": "form-control"}),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "resumen": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        base_queryset = User.objects.filter(groups__name = "Responsable")
        
        if self.instance and self.instance.pk:
            responsible_principal_id = self.instance.responsable.pk
            self.fields["responsables_adicionales"].queryset = base_queryset.exclude(pk = responsible_principal_id)
        else:
            self.fields["responsables_adicionales"].queryset = base_queryset
            
        self.fields["remitente"].queryset = Remitente.objects.filter(activo=True)

class RemitenteForm(forms.ModelForm):

    class Meta:

        model = Remitente
        fields = ["trato", "nombre", "area"]
        widgets = {
            "nombre": forms.TextInput(attrs = {"class": "form-control"}),
            
            "area": forms.TextInput(attrs = {"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['trato'].choices
        
class IniciarTramiteForm(forms.ModelForm):

    class Meta:

        model = Documento
        fields = ["resumen_responsable"]
        widgets = {
            "resumen_responsable": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Escriba un resumen breve del trámite que va a realizar..."
            })
        }
        labels = {
            "resumen_responsable": "Resumen del Trámite"
        }

class ResumenAdicionalForm(forms.Form):
    resumen = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Escriba su resumen como responsable adicional...',
            'required': True
        }),
        label='Su Resumen'
    )