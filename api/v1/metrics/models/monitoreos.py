from django.db import models


class CablemodemCountMonitoredModel(models.Model):
    active_monitoring = models.PositiveSmallIntegerField(blank=False)

    class Meta:
        db_table = "metrics_monitoreo_cablemodem"
        verbose_name = "Cablemodem Monitoreado"
        verbose_name_plural = "Cablemodems Monitoreados"

    def validate_active_monitoring(self, data):
        return data

    def __str__(self) -> str:
        return f"Monitoreos activos: {self.active_monitoring}"


class NodoEventoModel(models.Model):
    eventid = models.PositiveBigIntegerField(primary_key=True)
    nodo = models.CharField(max_length=50)
    inicio = models.DateTimeField(blank=True, null=True)
    antiguedad = models.CharField(max_length=50, null=True, blank=True)
    fin = models.DateTimeField(blank=True, null=True)
    duracion = models.CharField(max_length=50, null=True, blank=True)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    equipos_afectados = models.PositiveSmallIntegerField()
    equipos_caidos = models.PositiveSmallIntegerField()
    porcentaje_online = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "metrics_nodo_evento"
        verbose_name = "Evento de Nodo"
        verbose_name_plural = "Eventos de Nodos"


class NodoEventoEquipoAfectadoModel(models.Model):
    evento = models.ForeignKey(NodoEventoModel, on_delete=models.CASCADE, related_name='afectados')
    macaddress = models.CharField(max_length=12)
    model = models.CharField(max_length=50)
    cuenta = models.PositiveBigIntegerField()
    domicilio = models.CharField(max_length=50)
    estado_provisioning = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    online_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "metrics_nodo_detalle_evento"
        verbose_name = "Detalle Evento de Nodo"
        verbose_name_plural = "Detalle Evento de Nodo"

    def __str__(self) -> str:
        return self.macaddress