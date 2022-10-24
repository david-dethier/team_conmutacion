from django.db import models
from api.v1.gis.models import CiudadModel


class Nodo(models.Model):

    chasis = models.CharField(max_length=50)
    denominacion = models.CharField(max_length=50)
    modems_online = models.PositiveSmallIntegerField()
    modems_offline = models.PositiveSmallIntegerField()
    modems_percent_online = models.DecimalField(max_digits=5, decimal_places=2)
    ciudad = models.ForeignKey(CiudadModel, unique=False, on_delete=models.CASCADE, to_field="id")
    
    class Meta:

        ordering = ["denominacion"]
        db_table = "red_nodo"
        verbose_name = "Nodo"
        verbose_name_plural = "Nodos"
    
    def __str__(self) -> str:
        return f'Nodo: {self.denominacion} - {self.ciudad.nombre} - {self.chasis}'
    