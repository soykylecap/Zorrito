#from django.db.models.query import QuerySet
#from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from AppZorro.models import CajaPesos, Rubros
from django.urls import reverse_lazy
#from django.conf import settings

# Create your views here.



#class Inicio(TemplateView):
#    template_name = 'AppZorro/index.html'

class About(TemplateView):
    template_name = 'AppZorro/about.html'

class InicioListView(ListView):
    model = CajaPesos
    template_name = 'AppZorro/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contar todos los registros del modelo
        total_registros = CajaPesos.objects.count()
        # Agregar el conteo a la variable de contexto
        context['total_registros'] = total_registros
        return context


#Vistas para CajaPesos

class MovimientosListView(LoginRequiredMixin, ListView):
    model = CajaPesos
    ordering = ["fecha"]

    def get_queryset(self):
        queryset = super().get_queryset()
        saldo_parcial = 0
        for cuenta in queryset:
            saldo_parcial += cuenta.ingreso - cuenta.egreso
            cuenta.saldo_parcial = saldo_parcial
        return queryset


class MovimientosDetailView(LoginRequiredMixin, DetailView):
    model = CajaPesos

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        id_actual = self.object.id

        # No me funcionó usar ----> previo = CajaPesos.objects.filter(id__gt=id_actual).order_by('-id').first()
        objetos_ordenados = list(CajaPesos.objects.order_by('id'))

        min = objetos_ordenados[0]
        max = objetos_ordenados[-1]

        min = min.id
        max = max.id


        if self.object.id == min:
            previo = min
        else:
            previo = objetos_ordenados[objetos_ordenados.index(self.object)-1]
            previo = previo.id

        if self.object.id == max:
            siguiente = max
        else:
            siguiente = CajaPesos.objects.filter(id__gt=id_actual).order_by('id').first()
            siguiente = siguiente.id

        context['siguiente'] = siguiente
        context['previo'] = previo

        return self.render_to_response(context)


class MovimientosCreateView(LoginRequiredMixin, CreateView):
    model = CajaPesos
    fields = ['fecha', 'detalle', 'rubro', 'ingreso', 'egreso', 'comprobante']
    success_url = reverse_lazy("Movimientos")
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class MovimientosDeleteView(LoginRequiredMixin, DeleteView):
    model = CajaPesos
    success_url = reverse_lazy("Movimientos")


class MovimientosUpdateView(LoginRequiredMixin, UpdateView):
    model = CajaPesos
    success_url = reverse_lazy("Movimientos")
    fields = ['fecha', 'detalle', 'rubro', 'ingreso', 'egreso', 'comprobante']
    template_name = "AppZorro/CajaPesos_update.html"



#Vistas para Rubros

class RubrosListView(LoginRequiredMixin, ListView):
    model = Rubros

class RubrosCreateView(LoginRequiredMixin, CreateView):
    model = Rubros
    fields = ['titulo',]
    success_url = reverse_lazy("Rubros")

class RubrosDeleteView(LoginRequiredMixin, DeleteView):
    model = Rubros
    success_url = reverse_lazy("Rubros")

class RubrosUpdateView(LoginRequiredMixin, UpdateView):
    model = Rubros
    success_url = reverse_lazy("Rubros")
    fields = ['titulo',]
    template_name = "AppZorro/Rubros_update.html"