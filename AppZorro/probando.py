from django.apps import AppConfig


class AppzorroConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "AppZorro"


from models import CajaPesos, Rubros, CajaDolares, Obra

objetos_pesos = CajaPesos.get_object()
print (objetos_pesos)
