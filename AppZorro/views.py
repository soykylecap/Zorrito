#from django.db.models.query import QuerySet

from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from AppZorro.models import CajaPesos, Rubros, CajaDolares, Obra, Tarea
from django.urls import reverse_lazy
from django.db.models import Sum, RestrictedError
from dolar import DolarBlue
from main import EnObra, TotalesCaja, DatosYTotalesCaja
from AppZorro.graficos import grafico_torta, survey




class About(TemplateView):
    template_name = 'AppZorro/about.html'

class InicioListView(ListView):
    model = CajaPesos
    template_name = 'AppZorro/index_copia.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        total_registros = CajaPesos.objects.count()
        context.clear()

        



        context['dolar_compra'] = DolarBlue.compra()
        context['dolar_venta'] = DolarBlue.venta()
        context['total_registros'] = total_registros

        return context



class InicioTemplateView(TemplateView):
    template_name = 'AppZorro/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pesos = DatosYTotalesCaja(CajaPesos, orden='-fecha', campos=('fecha', 'detalle', 'ingreso', 'egreso'), cantidad=5)
        dolares = DatosYTotalesCaja(CajaDolares, orden='-fecha', campos=('fecha', 'detalle', 'ingreso', 'egreso'), cantidad=5)
        
        context['pesos'] = pesos.get()
        context['dolares'] = dolares.get()


        context['obra'] =  Obra.objects.get(id=EnObra.get())
        context['tareas'] = Tarea.objects.order_by('-fecha').filter(obra=EnObra.get())[:5]
        #context['rubros'] = Rubros.objects.order_by('-fecha').filter(obra=EnObra.get())[:5]

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        totales = TotalesCaja(CajaPesos)
        context['totales'] = totales.get()
        context['dolar_compra'] = DolarBlue.compra()
        context['dolar_venta'] = DolarBlue.venta()
        return context



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

    def get_queryset(self):
        queryset = super().get_queryset()
        for rubro in queryset:
            suma_egreso= CajaPesos.objects.filter(rubro_id=rubro).aggregate(Sum('egreso'))
            suma_ingreso= CajaPesos.objects.filter(rubro_id=rubro).aggregate(Sum('ingreso'))
            rubro.suma_egreso = suma_egreso['egreso__sum']
            rubro.suma_ingreso = suma_ingreso['ingreso__sum']
            #labels += rubro.titulo
            #sizes += rubro.suma_egreso
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pesos = TotalesCaja(CajaPesos)
        context['pesos'] = pesos.get()
        

        queryset = context['object_list']

        labels = list()
        sizes = []
        for rubro in queryset:
            suma_egreso = CajaPesos.objects.filter(rubro_id=rubro).aggregate(Sum('egreso'))
            suma_egreso_valor = suma_egreso.get('egreso__sum', 0)
            rubro.suma_egreso = float(suma_egreso_valor) if suma_egreso_valor else 0
            if rubro.suma_egreso and rubro.id != 23:
                labels.append(rubro.titulo)
                sizes.append(float(rubro.suma_egreso))
        uri = grafico_torta(labels, sizes)
        context['grafico'] = uri

        return context


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        totales = TotalesCaja(CajaDolares)
        context['totales'] = totales.get()
        context['dolar_compra'] = DolarBlue.compra()
        context['dolar_venta'] = DolarBlue.venta()
        return context


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


#Vistas para Obras

class ObraCreateView(LoginRequiredMixin, CreateView):
    model = Obra
    fields = ['fecha_inicio', 'nombre', 'm2_cubiertos', 'm2_semicubiertos', 'dias_estimados', 'presupuesto_inicial']
    success_url = reverse_lazy("Obras")
    
    def form_valid(self, form):
        form.instance.m2_total = form.instance.m2_cubiertos + form.instance.m2_semicubiertos
        return super().form_valid(form)

class ObraUpdateView(LoginRequiredMixin, UpdateView):
    model = Obra
    success_url = reverse_lazy("Obras")
    fields = ['fecha_inicio', 'nombre', 'm2_cubiertos', 'm2_semicubiertos', 'dias_estimados', 'presupuesto_inicial']
    template_name = "AppZorro/Obra_update.html"

    def form_valid(self, form):
        form.instance.m2_total = form.instance.m2_cubiertos + form.instance.m2_semicubiertos
        return super().form_valid(form)

class ObraDeleteView(LoginRequiredMixin, DeleteView):
    model = Obra
    success_url = reverse_lazy("Obras")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        try:
            return super().post(request, *args, **kwargs)
        except RestrictedError:
            form = self.get_form()
            #print (f'ESTO ES {form}')
            messages.error(self.request, "No se puede eliminar esta obra porque tiene movimientos asociados.")

            
        
            return self.form_invalid(form)





class ObraListView(LoginRequiredMixin, ListView):
    model = Obra

class ObraDetailView(LoginRequiredMixin, DetailView):
    model = Obra

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dias = Tarea.objects.count()
        costo = CajaPesos.objects.aggregate(total_sum=Sum('egreso'))
        costo = costo['total_sum']
        presupuesto = context['object'].presupuesto_inicial
        ganancia = presupuesto - (costo / DolarBlue.venta())
        context['m2_totales'] = context['object'].m2_cubiertos + context['object'].m2_semicubiertos
        context['dias_obra'] = dias
        context['costo_final'] = costo
        context['ganancia'] = ganancia
        return context


#Vistas para Tareas

class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class TareaDetailView(LoginRequiredMixin, DetailView):
    model = Tarea

class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['fecha', 'tarea', 'rubro', 'porcentaje', 'cant_operarios']
    success_url = reverse_lazy("Tareas")

    def form_valid(self, form):
        print (form.instance.porcentaje)
        form.instance.indice_jornada = 1 * form.instance.cant_operarios * (form.instance.porcentaje / 100)
        form.instance.autor = self.request.user
        form.instance.obra = Obra.objects.get(id=EnObra.get())
        return super().form_valid(form)