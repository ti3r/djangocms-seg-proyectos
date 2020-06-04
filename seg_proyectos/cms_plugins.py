from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf.urls import url
from django.http import HttpResponseBadRequest, HttpResponse

from seg_proyectos.models import ListaProyectosPlugin, Proyecto, EntradaHoras, ResumenProyectoPlugin, ResumenProyectosPlugin
from django.utils.translation import ugettext_lazy as _


GRUPO_PLUGINS = _("Seguimiento Proyecto")


@plugin_pool.register_plugin
class ListaProyectosPlugin(CMSPluginBase):
    model = ListaProyectosPlugin
    render_template = "seg_proy/index.html"
    cache = False
    name = _("Lista de Proyectos")
    module = GRUPO_PLUGINS

    def render(self, context, instance, placeholder):
        context = super(ListaProyectosPlugin, self).render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class EntradaDeHorasPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "seg_proy/entrada_horas.html"
    cache = False
    name = _("Entrada de Horas")
    module = GRUPO_PLUGINS

    def render(self, context, instance, placeholder):
        context = super(EntradaDeHorasPlugin, self).render(context, instance, placeholder)
        proyectos = Proyecto.objects.all()
        context.update({'proyectos': proyectos})
        return context

    def get_plugin_urls(self):
        urlpatterns = [
            url(r'^crear_entradas/$', self.crear_entrada_horas, name='crear_entrada_horas'),
        ]

        return urlpatterns

    def crear_entrada_horas(self, request):
        if not 'plugin_id' in request.POST and not 'placeholder_id' in request.POST:
            return HttpResponseBadRequest('plugin_id or placeholder_id POST parameter(s) missing.')

        return HttpResponse('OK')


@plugin_pool.register_plugin
class ResumenProyectoPlugin(CMSPluginBase):
    model = ResumenProyectoPlugin
    render_template = "seg_proy/resumen_proyecto.html"
    cache = False
    name = _("Resumen de Proyecto")
    module = GRUPO_PLUGINS

    def render(self, context, instance, placeholder):
        context = super(ResumenProyectoPlugin, self).render(context, instance, placeholder)
        [listado_horas, total] = self.get_listado_horas(instance)
        context.update({'horas': listado_horas, 'total': total})
        return context

    def get_listado_horas(self, instance):
        horas = EntradaHoras.objects.filter(proyecto=instance.proyecto)
        res = []
        tot = 0.0
        for h in horas:
            r = {'usuario': h.usuario, 'fecha': h.fecha, 'horas': h.valor}
            tot += h.valor
            res.append(r)
        return [res, tot]


@plugin_pool.register_plugin
class ResumenProyectosPlugin(CMSPluginBase):
    model = ResumenProyectosPlugin
    render_template = "seg_proy/resumen_proyectos.html"
    cache = False
    name = _("Resumen de Proyectos")
    module = GRUPO_PLUGINS
    allow_children = True
    child_classes = ['ResumenProyectoPlugin']

    def render(self, context, instance, placeholder):
        context = super(ResumenProyectosPlugin, self).render(context, instance, placeholder)
        return context