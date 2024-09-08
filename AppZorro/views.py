#from django.db.models.query import QuerySet
#from django.http import HttpRequest, HttpResponse
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from AppZorro.models import CajaPesos, Rubros, CajaDolares, Obra
from django.urls import reverse_lazy
from dolar import DolarBlue
from main import EnObra

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
        total_registros = CajaPesos.objects.count()
        context.clear()

        context['dolar_compra'] = DolarBlue.compra()
        context['dolar_venta'] = DolarBlue.venta()
        context['total_registros'] = total_registros

        return context


#Vistas para CajaPesos

class MovimientosListView(LoginRequiredMixin, ListView):
    model = CajaPesos
    ordering = ["fecha"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        saldo_parcial = 0
        for cuenta in queryset:
            if hasattr(cuenta.conecta, 'id'):
                cuenta.mandar = cuenta.conecta.id
            else:
                cuenta.mandar = 0
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
        #objetos_ordenados = list(CajaPesos.objects.order_by('id').exclude(rubro_id=23))

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
            #siguiente = CajaPesos.objects.filter(id__gt=id_actual).exclude(rubro_id=23).order_by('id').first()
            siguiente = CajaPesos.objects.filter(id__gt=id_actual).order_by('id').first()
            siguiente = siguiente.id

        context['siguiente'] = siguiente
        context['previo'] = previo

        return self.render_to_response(context)


class MovimientosCreateView(LoginRequiredMixin, CreateView):
    model = CajaPesos
    fields = ['fecha', 'detalle', 'rubro', 'ingreso', 'egreso', 'cotiza', 'comprobante']
    success_url = reverse_lazy("Movimientos")
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.obra = Obra.objects.get(id=EnObra.get())
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
    queryset = Rubros.objects.exclude(titulo="Cambio Moneda")

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





#Vistas para CajaDolares

class DolaresListView(LoginRequiredMixin, ListView):
    model = CajaDolares
    ordering = ["fecha"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        saldo_parcial = 0
        for cuenta in queryset:
            saldo_parcial += cuenta.ingreso - cuenta.egreso
            cuenta.saldo_parcial = saldo_parcial
        return queryset


class DolaresDetailView(LoginRequiredMixin, DetailView):
    model = CajaDolares

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        id_actual = self.object.id

        # No me funcionó usar ----> previo = CajaDolares.objects.filter(id__gt=id_actual).order_by('-id').first()
        objetos_ordenados = list(CajaDolares.objects.order_by('id'))

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
            siguiente = CajaDolares.objects.filter(id__gt=id_actual).order_by('id').first()
            siguiente = siguiente.id

        context['siguiente'] = siguiente
        context['previo'] = previo

        return self.render_to_response(context)


class DolaresCreateView(LoginRequiredMixin, CreateView):
    model = CajaDolares
    fields = ['fecha', 'detalle', 'cotiza', 'ingreso', 'egreso']
    success_url = reverse_lazy("Dolares")
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.es_cambio = False
        form.instance.obra = Obra.objects.get(id=EnObra.get())
        return super().form_valid(form)
    

class DolaresVentaView(LoginRequiredMixin, CreateView):
    model = CajaDolares 
    fields = ['fecha', 'detalle', 'ingreso', 'egreso', 'cotiza']
    template_name = "AppZorro/CajaDolares_form_venta.html"
    success_url = reverse_lazy("Dolares")
    
    def form_valid(self, form):

        form.instance.autor = self.request.user
        form.instance.es_cambio = True
        form.instance.obra = Obra.objects.get(id=EnObra.get())

        if form.instance.egreso > 0:
            nuevo_detalle = f"Vendimos u$s {int(form.instance.egreso)} a {form.instance.detalle}"
        elif form.instance.ingreso > 0:
            nuevo_detalle = f"Compramos u$s {int(form.instance.ingreso)} a {form.instance.detalle}"

        form.instance.detalle = nuevo_detalle
        form_limpio = form.cleaned_data
        egreso_pesos = form_limpio['ingreso'] * form_limpio['cotiza'] 
        ingreso_pesos = form_limpio['egreso'] * form_limpio['cotiza']

        instancia_pesos = CajaPesos(fecha=form_limpio['fecha'], rubro=Rubros.objects.get(id=23), detalle=nuevo_detalle, ingreso=ingreso_pesos, egreso=egreso_pesos, cotiza=form_limpio['cotiza'], obra=Obra.objects.get(id=EnObra.get()), autor=self.request.user)
        instancia_pesos.save() #graba en pesos
        form.instance.conecta = instancia_pesos
        self.object = form.save() #graba en dolares
        instancia_pesos.conecta = self.object
        instancia_pesos.save()
        return super().form_valid(form)


class DolaresDeleteView(LoginRequiredMixin, DeleteView):
    model = CajaDolares
    success_url = reverse_lazy("Dolares")


class DolaresUpdateView(LoginRequiredMixin, UpdateView):
    model = CajaDolares
    success_url = reverse_lazy("Dolares")
    fields = ['fecha', 'detalle', 'cotiza', 'ingreso', 'egreso']
    template_name = "AppZorro/CajaDolares_update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['en_pesos'] = (self.object.ingreso + self.object.egreso) * self.object.cotiza
        return self.render_to_response(context)

    def form_valid(self, form):

        instance = form.save(commit=False)  # No guardamos aún
        
        if instance.es_cambio:
            objeto_pesos = instance.conecta  # Asume que conecta es una relación inversa
            instance_pesos = CajaPesos(objeto_pesos.id)
            instance_pesos.fecha = instance.fecha
            instance_pesos.rubro = Rubros.objects.get(id=23)
            instance_pesos.detalle = instance.detalle
            instance_pesos.ingreso = instance.egreso * instance.cotiza
            instance_pesos.egreso = instance.ingreso * instance.cotiza
            instance_pesos.cotiza = instance.cotiza
            instance_pesos.obra = Obra.objects.get(id=EnObra.get())
            instance_pesos.autor = self.request.user
            instance_pesos.conecta = self.object
            instance_pesos.save()
        return super().form_valid(form)

