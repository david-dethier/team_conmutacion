from django import forms
from django.contrib import admin
from api.v1.metrics.models.reclamos import ReclamosCompletedWorkModel
from api.v1.metrics.models.commons import EmpresaModel, CuadrillaTecnicaModel
from api.v1.metrics.models.conexiones import ConexionesCompletedWorkModel
from api.v1.metrics.models.llamadas_tecnicas import LlamadasTecnicasModel
from api.v1.metrics.services import parse_llamadas_tecnicas


class CallForm(forms.ModelForm):
    class Meta:

        model = LlamadasTecnicasModel
        fields = ("telefono", "fecha")


class CallAdmin(admin.ModelAdmin):

    form = CallForm
    list_display = (
        "telefono",
        "fecha_detalle",
        "origen_src",
        "destino_dst",
        "estado_disposition",
    )

    date_hierarchy = "fecha_detalle"
    search_fields = ("telefono", "origen_src", "destino_dst", "estado_disposition")
    search_help_text = "Busca por teléfono, origen, destino o disposición."

    def save_model(self, request, obj, form, change):
        parse_llamadas_tecnicas(form.cleaned_data)


class ReclamosCompletedWorkForm(forms.ModelForm):
    class Meta:

        model = ReclamosCompletedWorkModel
        fields = "__all__"


class ReclamosCompletedWorkAdmin(admin.ModelAdmin):
    form = ReclamosCompletedWorkForm
    list_display = (
        "technical_team",
        "quantity",
        "date",
    )

    date_hierarchy = "date"
    search_fields = ("technical_team__alias",)
    search_help_text = "Busca por cuadrilla tecnica."


class ConexionesCompletedWorkForm(forms.ModelForm):
    class Meta:

        model = ConexionesCompletedWorkModel
        fields = "__all__"


class ConexionesCompletedWorkAdmin(admin.ModelAdmin):
    form = ConexionesCompletedWorkForm
    list_display = (
        "technical_team",
        "quantity",
        "date",
    )

    date_hierarchy = "date"
    search_fields = ("technical_team__alias",)
    search_help_text = "Busca por cuadrilla tecnica."


admin.site.register(LlamadasTecnicasModel, CallAdmin)
admin.site.register(EmpresaModel)
admin.site.register(CuadrillaTecnicaModel)
admin.site.register(ReclamosCompletedWorkModel, ReclamosCompletedWorkAdmin)
admin.site.register(ConexionesCompletedWorkModel, ConexionesCompletedWorkAdmin)
