from django.db.models import Sum, RestrictedError
from AppZorro.models import Obra

class EnObra:
    @classmethod
    def set(cls, obra):
        with open("./obra_actual.txt", "w", encoding="utf-8") as f:
            f.write(obra)
    
    @classmethod
    def get(cls):
        with open("./obra_actual.txt", "r", encoding="utf-8") as f:
            obra_actual = int(f.read())
        return obra_actual
    


    
class TotalesCaja:
    def __init__(self, modelo):
        self.modelo = modelo

    def get(self):
        egresos = self.modelo.objects.all().aggregate(Sum('egreso'))
        ingresos = self.modelo.objects.all().aggregate(Sum('ingreso'))
        totales = dict()
        totales['egresos'] = egresos['egreso__sum']
        totales['ingresos'] = ingresos['ingreso__sum']
        totales['saldo'] = ingresos['ingreso__sum'] - egresos['egreso__sum']
        return totales
    
class DatosYTotalesCaja(TotalesCaja):
    
    def __init__(self, modelo, **kwargs):
        super().__init__(modelo)
        self.cantidad = kwargs.get('cantidad')
        self.orden = kwargs.get('orden')
        if not self.orden: self.orden = '-fecha'
        self.campos = kwargs.get('campos')
        if not self.campos: self.campos = ''
    
    def get(self):
        totales = super().get()
        totales['datos'] = self.modelo.objects.order_by(self.orden).values(*self.campos).filter(obra=EnObra.get())[:self.cantidad]
        return totales