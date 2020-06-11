from django.contrib import admin
from seg_proyectos.models import Proyecto, EntradaHoras, EntradaHorasDetalle
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'activo')


@admin.register(EntradaHoras)
class EntradaHorasAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'valor', 'proyecto')
    list_filter = ('usuario', 'proyecto')
    ordering = ('-fecha',)
    site_title = _('Entrada de Horas')

class EntradaHorasDetalleUsuarioFilter(admin.SimpleListFilter):
    title = _('Usuario')
    parameter_name = 'usuario'

    def lookups(self, request, model_admin):
        users = EntradaHoras.objects.order_by('usuario_id').distinct('usuario_id', 'usuario')
        res = [(u.usuario_id, f'''{u.usuario}''') for u in users]
        return res
        #return (
        #    ('alex', _('alex')),
        #)

    def queryset(self, request, queryset):
        val = self.value()
        return queryset.filter(horas__usuario__id=val) if val else queryset.all()

@admin.register(EntradaHorasDetalle)
class EntradaHorasDetalleAdmin(admin.ModelAdmin):
    list_display = ('admin_usuario_str', 'admin_proy_str' ,'entrada', 'salida', 'descanso')
    list_filter = (EntradaHorasDetalleUsuarioFilter,)
    ordering = ('-entrada', )