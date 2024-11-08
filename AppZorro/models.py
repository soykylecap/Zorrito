from typing import Any
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
from dolar import DolarBlue


# Create your models here.


class Rubros(models.Model):
    titulo = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.titulo}"
    
class Obra(models.Model):
    fecha_inicio = models.DateField(default=date.today)
    nombre = models.CharField(max_length=30)
    m2_cubiertos = models.FloatField(default=0.00)
    m2_semicubiertos = models.FloatField(default=0.00)
    m2_total = models.FloatField(default=0.00, editable=False)
    dias_estimados = models.IntegerField(default=30)
    presupuesto_inicial = models.FloatField()


    def __str__(self) -> str:
        return self.nombre


class CajaPesos(models.Model):
    fecha = models.DateField(default=date.today)
    rubro = models.ForeignKey(Rubros, null=True, on_delete=models.RESTRICT)
    detalle = models.CharField(max_length=60)
    ingreso = models.FloatField(default=0)
    egreso = models.FloatField(default=0)
    comprobante = models.ImageField(upload_to='comprobantes', null=True, blank = True)
    obra = models.ForeignKey(Obra, null=True, on_delete=models.RESTRICT)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True, blank=True, editable=False)
    action_time = models.DateTimeField(auto_now=True, editable=False)
    cotiza = models.FloatField(default=DolarBlue.compra()) 
    conecta = models.OneToOneField('CajaDolares', null=True, blank=True, on_delete=models.CASCADE)
    

class CajaDolares(models.Model):
    fecha = models.DateField(default=date.today)
    detalle = models.CharField(max_length=60)
    es_cambio = models.BooleanField(default=True)
    ingreso = models.FloatField(default=0)
    egreso = models.FloatField(default=0)
    cotiza = models.FloatField(default=DolarBlue.compra()) 
    obra = models.ForeignKey(Obra, null=True, on_delete=models.RESTRICT)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True, blank=True, editable=False)
    action_time = models.DateTimeField(auto_now=True, editable=False)
    conecta = models.OneToOneField(CajaPesos, null=True, blank=True, on_delete=models.CASCADE)



class Tarea(models.Model):
    fecha = models.DateField(default=date.today)
    tarea = models.CharField(max_length=40)
    rubro = models.ForeignKey(Rubros, null=True, on_delete=models.RESTRICT)
    opciones_porcentaje = [(25, '25%'), (50, '50%'), (75, '75%'), (100, '100%')]
    porcentaje = models.IntegerField(choices=(opciones_porcentaje), default=100)
    cant_operarios = models.IntegerField(default=2)
    indice_jornada = models.FloatField(default=1)
    obra = models.ForeignKey(Obra, null=True, on_delete=models.RESTRICT)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True, blank=True, editable=False)

    def __str__(self):
        return self.tarea
