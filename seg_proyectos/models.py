from cms.models import pluginmodel
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre}"


class EntradaHoras(models.Model):
    valor = models.FloatField(default=1.0)
    fecha = models.DateField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user"), blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"""{self.usuario} - {self.fecha}[{self.valor} hrs]"""


#Plugin models
class ListaProyectosPlugin(pluginmodel.CMSPlugin):
    tam_pagina = models.IntegerField(default=10)


class ResumenProyectosPlugin(pluginmodel.CMSPlugin):
    all_active = models.BooleanField(name="Todos Activos", null=True)


class ResumenProyectoPlugin(pluginmodel.CMSPlugin):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)