from django.db import models


class EmpresaModel(models.Model):
    company_name = models.CharField(max_length=25, unique=True, verbose_name="empresa")
    boss_name = models.CharField(max_length=50, unique=False, verbose_name="encargado")
    work_phone = models.CharField(max_length=13, verbose_name="telefono del encargado")
    is_in_service = models.BooleanField(default=True, verbose_name="en servicio")

    class Meta:
        db_table = "common_empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self) -> str:
        return f"[ {self.company_name} ] - Responsable: {self.boss_name} ( {self.work_phone} )"


class CuadrillaTecnicaModel(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name="nombre")
    alias = models.CharField(max_length=15, unique=True, verbose_name="abreviación")
    work_phone = models.CharField(
        max_length=13, verbose_name="numero telefónico", blank=True
    )
    company_model = models.ForeignKey(
        EmpresaModel, on_delete=models.PROTECT, verbose_name="empresa"
    )
    is_in_service = models.BooleanField(default=True, verbose_name="en servicio")

    class Meta:
        db_table = "common_cuadrilla_tecnica"
        verbose_name = "Cuadrilla Tecnica"
        verbose_name_plural = "Cuadrillas Tecnicas"

    def __str__(self) -> str:
        return f"{self.alias} - {self.company_model.company_name}"
