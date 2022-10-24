from django.db import models
from api.v1.metrics.models.commons import CuadrillaTecnicaModel


class ReclamosCompletedWorkModel(models.Model):
    date = models.DateField(verbose_name="fecha")
    quantity = models.PositiveSmallIntegerField(
        verbose_name="terminados"
    )
    technical_team = models.ForeignKey(CuadrillaTecnicaModel, on_delete=models.PROTECT, verbose_name="cuadrilla")

    class Meta:
        ordering = ["-date"]
        db_table = 'metrics_reclamos_completedworks'
        verbose_name_plural = "Reclamos Realizado"
        verbose_name = "Reclamo Realizado"

    def __str__(self) -> str:
        return f"{self.technical_team.name} ( {self.date} ) - Cantidad: {self.quantity}"


