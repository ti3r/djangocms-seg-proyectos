from django.contrib import admin
from seg_proyectos.models import Proyecto, EntradaHoras


# Register your models here.
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    pass


@admin.register(EntradaHoras)
class EntradaHorasAdmin(admin.ModelAdmin):
    pass
