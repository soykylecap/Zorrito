from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from AppZorro.models import CajaPesos
from django.urls import reverse_lazy
from django.conf import settings

# Create your views here.

class Inicio(TemplateView):
    template_name = 'AppZorro/index.html'


class About(TemplateView):
    template_name = 'AppZorro/about.html'


class MovimientosListView(LoginRequiredMixin, ListView):
    model = CajaPesos
    template_name = "AppZorro/movimientos_list.html"
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
    template_name = "AppZorro/movimientos_detail.html"


class MovimientosCreateView(LoginRequiredMixin, CreateView):
    model = CajaPesos
    fields = ['fecha', 'rubro', 'detalle', 'ingreso', 'egreso', 'comprobante']
    template_name = "AppZorro/movimientos_create.html"
    success_url = reverse_lazy("Movimientos")
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)