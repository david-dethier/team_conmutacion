from django import forms
from django.contrib import admin
from .models import CiudadModel
from .models import DomicilioGeoLocalizadoModel
from .selectors import fetch_geolocation, generate_googlemaps_link


class DomicilioGeoCodificadoForm(forms.ModelForm):
    class Meta:
        model = DomicilioGeoLocalizadoModel
        fields = ("calle", "numero", "casa", "ciudad", "calle_alias")


class DomicilioGeoCodificadoAdmin(admin.ModelAdmin):
    form = DomicilioGeoCodificadoForm
    list_display = (
        "calle",
        "numero",
        "casa",
        "barrio",
        "ciudad",
        "calle_alias",
        "googlemaps_link",
        "modified",
    )
    search_fields = ("calle", "numero", "barrio", "ciudad__nombre", "calle_alias")
    search_help_text = "Busca por calle, numero, barrio, ciudad o alias."

    def save_model(self, request, obj, form, change):
        location = fetch_geolocation(
            obj.calle, obj.numero, obj.ciudad.nombre, obj.ciudad.provincia
        )
        obj.calle = location["address"]["road"]
        obj.barrio = location["address"]["suburb"]
        obj.latitud = location["latitude"]
        obj.longitud = location["longitude"]
        obj.googlemaps_link = generate_googlemaps_link(location["latitude"], location["longitude"])
        return super().save_model(request, obj, form, change)


admin.site.register(CiudadModel)
admin.site.register(DomicilioGeoLocalizadoModel, DomicilioGeoCodificadoAdmin)
