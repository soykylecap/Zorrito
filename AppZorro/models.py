from django.db import models
from django.conf import settings


# Create your models here.

class Conceptos(models.Model):
    titulo = models.CharField(max_length=30)
    tipo = models.CharField(max_length=7, choices=[('ING','Ingreso'), ('EGR','Egreso')])
    moneda = models.CharField(max_length=7, choices=[('PE','Pesos'),('US','Dolares')])
    def __str__(self):
        return f"{self.titulo} | {self.tipo} | {self.moneda}"

class SubCajas(models.Model):
    nombre = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=20)

class CajaDolares(models.Model):
    fecha = models.DateField(auto_now=True)
    concepto = models.ForeignKey(Conceptos, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=30)
    cotizacion = models.IntegerField()
    ingreso = models.FloatField()
    egreso = models.FloatField()
    subcaja = models.CharField(max_length=7, choices=[('CD','Cuenta Diego'),('CK','Cuenta Kyle')])
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_time = models.DateTimeField(auto_now=True)

class CajaPesos(models.Model):
    fecha = models.DateField(auto_now=True)
    concepto = models.ForeignKey(Conceptos, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=30)
    caja_dolar = models.ForeignKey(CajaDolares, on_delete=models.CASCADE)
    ingreso = models.FloatField()
    egreso = models.FloatField()
    subcaja = models.ForeignKey(SubCajas, on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_time = models.DateTimeField(auto_now=True)
    
    



class Autor(models.Model):
    nombre = models.CharField(max_length=100)

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
