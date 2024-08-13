from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from AppZorro.models import CajaPesos, Rubros
from django.urls import reverse_lazy
from django.conf import settings

# Create your views here.



class Inicio(TemplateView):
    template_name = 'AppZorro/index.html'

class About(TemplateView):
    template_name = 'AppZorro/about.html'



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