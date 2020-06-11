from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf.urls import url
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
from django.forms import DateInput, NumberInput

from seg_proyectos.models import *
from seg_proyectos.forms import EntradaHorasForm
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, timedelta

GRUPO_PLUGINS = _("Seguimiento Proyecto")

## Mixins
class ProyectosPluginMixin():

    def agregar_proyectos_a_context(self, context, mostrar_inactivos = False):
        proyectos = Proyecto.objects.all() if mostrar_inactivos else Proyecto.objects.filter(activo= True)
        context.update({'proyectos': proyectos})

    def obtener_proyecto(self, proyecto_id):
        return Proyecto.objects.get(id=proyecto_id)


@plugin_pool.register_plugin
class ListaProyectosPlugin(CMSPluginBase, ProyectosPluginMixin):
    model = ListaProyectosPlugin
    render_template = "seg_proy/lista_proyectos.html"
    cache = False
    name = _("Lista de Proyectos")
    module = GRUPO_PLUGINS

    def render(self, context, instance, placeholder):
        context = super(ListaProyectosPlugin, self).render(context, instance, placeholder)
        self.agregar_proyectos_a_context(context, True)
        return context


@plugin_pool.register_plugin
class EntradaDeHorasPlugin(CMSPluginBase, ProyectosPluginMixin):
    model = EntradaDeHorasPlugin
    render_template = "seg_proy/entrada_horas.html"
    cache = False
    name = _("Entrada de Horas")
    module = GRUPO_PLUGINS

    def render(self, context, instance, placeholder):
        context = super(EntradaDeHorasPlugin, self).render(context, instance, placeholder)

        request = context['request']
        if request.POST.get('form_plugin_id') == str(instance.id):
            ent_horas = self.crear_entrada_horas(request)
            if ent_horas is not None: context.update({'ent_horas': ent_horas, 'post_ok': True})
        else:
            context.update({'form': EntradaHorasForm()})
        self.agregar_proyectos_a_context(context, instance.mostrar_inactivos)
        return context

    def crear_entrada_horas(self, request):
        form = EntradaHorasForm(request.POST)
        if form.is_valid():
            horas = form.save(commit=False)
            horas.usuario = request.user
            horas.save()
            return horas
        else:
            return None


@plugin_pool.register_plugin
class EntradaDeHorasDetallePlugin(CMSPluginBase, ProyectosPluginMixin):
    model = EntradaDeHorasDetallePlugin
    render_template = "seg_proy/entrada_horas_detalle.html"
    cache = False
    name = _("Entrada y Salida")
    module = GRUPO_PLUGINS

    def render(self, context, instance, placeholder):
        context = super(EntradaDeHorasDetallePlugin, self).render(context, instance, placeholder)
        request = context['request']
        if request.POST.get('form_plugin_id') == str(instance.id):
            det = self.crear_detalle(request)
            if det is not None:
                context.update({'detalle': det, 'post_ok': 'ok'})
        self.agregar_proyectos_a_context(context, instance.mostrar_inactivos)
        return context

    def crear_detalle(self, request) -> EntradaHorasDetalle:
        form = EntradaDeHorasDetalleForm(request.POST)
        ent = datetime.fromisoformat(request.POST.get('entrada'))
        sal = datetime.fromisoformat(request.POST.get('salida'))
        desc = timedelta(hours=float(request.POST.get('descanso'))) if request.POST['descanso'] else timedelta(hours=0)
        proy = self.obtener_proyecto(request.POST.get('proyecto'))
        if ent and sal and proy:
            detalle = EntradaHorasDetalle(entrada=ent, salida=sal, descanso = desc)
            horas = self.obtener_horas_padre(request.user, proy, detalle)
            detalle.horas = horas
            detalle.save()
            horas.agregar_detalle(detalle)
            return detalle
        return None

    def obtener_horas_padre(self, usuario, proyecto, detalle):
        fecha = detalle.entrada.date()
        existente = EntradaHoras.objects.filter(usuario=usuario, proyecto=proyecto, fecha=fecha).last()
        return existente if existente else EntradaHoras(usuario=usuario, proyecto=proyecto, fecha=fecha)


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
            tot += float(h.valor)
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

