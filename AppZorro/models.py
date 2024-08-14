from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings

# Create your models here.

class Rubros(models.Model):
    titulo = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.titulo}"

class CajaPesos(models.Model):
    fecha = models.DateField(default=date.today)
    rubro = models.ForeignKey(Rubros, null=True, on_delete=models.SET_NULL)
    detalle = models.CharField(max_length=60)
    ingreso = models.FloatField(default=0)
    egreso = models.FloatField(default=0)
    comprobante = models.ImageField(upload_to='comprobantes', null=True, blank = True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True, blank = True)
    action_time = models.DateTimeField(auto_now=True)



