from django.db import models
from traitlets import default


class CiudadModel(models.Model):

    nombre = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255, default="La Pampa")
    cp = models.PositiveSmallIntegerField()
    cpa = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["nombre"]
        db_table = "gis_ciudad"
        verbose_name = "ciudad"
        verbose_name_plural = "ciudades"

    def __str__(self) -> str:
        return f"{self.nombre}"


class DomicilioGeoLocalizadoModel(models.Model):

    calle = models.CharField(max_length=255)
    numero = models.PositiveSmallIntegerField()
    casa = models.CharField(max_length=50, blank=True)
    barrio = models.CharField(max_length=255, blank=True)
    ciudad = models.ForeignKey(CiudadModel, on_delete=models.CASCADE)
    latitud = models.FloatField(null=True)
    longitud = models.FloatField(null=True)
    googlemaps_link = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    calle_alias = models.CharField(max_length=255, blank=True, default="")
    has_alias = models.BooleanField(default=False)
    is_pending_alias = models.BooleanField(default=False)

    class Meta:
        ordering = ["calle"]
        db_table = "gis_domicilio_geolocalizado"
        verbose_name = "Domicilio Geolocalizado"
        verbose_name_plural = "Domicilios Geolocalizados"

    def __str__(self) -> str:
        return f"{self.calle} {self.numero}, {self.barrio}, {self.ciudad}"
