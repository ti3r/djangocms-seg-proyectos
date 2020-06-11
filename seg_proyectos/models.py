from cms.models import pluginmodel
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000)
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField(default= timezone.now )
    fecha_fin = models.DateField(default= timezone.now )
    class Meta:
        verbose_name = _('Proyectos')
        verbose_name_plural = _('Proyectos')


    def __str__(self):
        return f"{self.nombre}"


class EntradaHoras(models.Model):
    valor = models.DecimalField(default=1.0, max_digits=3, decimal_places=1)
    fecha = models.DateField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user"), blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name = _('Entrada de Horas')
        verbose_name_plural = _('Entrada de Horas')


    def __str__(self):
        return f"""{self.usuario} - {self.fecha}[{self.valor} hrs]"""

    def agregar_detalle(self, detalle):
        delta = detalle.salida - detalle.entrada - detalle.descanso
        self.valor += (delta.seconds // 3600)
        self.save()

class EntradaHorasDetalle(models.Model):
    horas = models.ForeignKey(EntradaHoras, on_delete=models.SET_NULL, null=True)
    entrada = models.DateTimeField(null=False)
    salida = models.DateTimeField(null=False)
    descanso = models.DurationField(null=True)
    class Meta:
        verbose_name = _('Entradas / Salidas')
        verbose_name_plural = _('Entradas / Salidas')

    def admin_usuario_str(self):
        return f"""{self.horas.usuario}"""
    admin_usuario_str.short_description = 'Usuario'

    def admin_proy_str(self):
        return f"""{self.horas.proyecto}"""

    admin_proy_str.short_description = 'Proyecto'


#Plugin models
class ListaProyectosPlugin(pluginmodel.CMSPlugin):
    tam_pagina = models.IntegerField(default=10)


class ResumenProyectosPlugin(pluginmodel.CMSPlugin):
    all_active = models.BooleanField(name="Todos Activos", null=True)


class ResumenProyectoPlugin(pluginmodel.CMSPlugin):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)

class EntradaDeHorasPlugin(pluginmodel.CMSPlugin):
    mostrar_inactivos = models.BooleanField(default=False)

class EntradaDeHorasDetallePlugin(pluginmodel.CMSPlugin):
    mostrar_inactivos = models.BooleanField(default=False)