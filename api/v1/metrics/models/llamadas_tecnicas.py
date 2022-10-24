from django.db import models


class LlamadasTecnicasModel(models.Model):
    telefono = models.PositiveSmallIntegerField(null=False)
    fecha = models.DateField(null=False)
    fecha_detalle = models.DateTimeField(max_length=100, blank=True)
    origen_src = models.CharField(max_length=100, blank=True)
    destino_dst = models.CharField(max_length=100, blank=True)
    canal_channel = models.CharField(max_length=100, blank=True)
    canal_destino_dstchannel = models.CharField(max_length=100, blank=True)
    estado_disposition = models.CharField(max_length=100, blank=True)
    id_unico = models.CharField(max_length=100, blank=True)
    grabacion = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-fecha"]
        db_table = 'metrics_llamada_tecnica'
        verbose_name_plural = "Llamadas Tecnicas"

    def __str__(self) -> str:
        return f"{self.telefono} ( {self.fecha} )  - Origen: {self.origen_src}, Destino: {self.destino_dst} - {self.estado_disposition}"
