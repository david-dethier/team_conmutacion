from django.contrib import admin
from django import forms

from api.v1.red.models import Nodo


class NodoForm(forms.ModelForm):
    class Meta:
        model = Nodo
        fields = "__all__"


class NodoAdmin(admin.ModelAdmin):

    form = NodoForm
    list_display = (
        "denominacion",
        "ciudad",
        "chasis",
        "modems_online",
        "modems_offline",
        "modems_percent_online",
    )
    search_fields = ["denominacion", "ciudad_id__nombre", "chasis"]
    search_help_text = "Busca por denominacion, chasis o ciudad."


admin.site.register(Nodo, NodoAdmin)
