from django.contrib import admin
from AppZorro.models import Rubros, CajaPesos, Obra, Tarea, CajaDolares
from users.models import Imagen

# Register your models here.

#admin.site.register(Rubros)
#admin.site.register(CajaPesos)
#admin.site.register(Imagen)
admin.site.register(Obra)
admin.site.register(Tarea)
admin.site.register(CajaDolares)


@admin.register(Rubros)
class AdminRubros(admin.ModelAdmin):
    list_display = ("titulo",)
    ordering = ("titulo", )
    search_fields = ("titulo", )
    list_display_links = ("titulo", )
    search_help_text = "Busqueda por titulo de Rubro"
#    list_filter = ()
#    list_per_page = 3
#    list_editable = ("titulo", )

@admin.register(CajaPesos)
class AdminCajaPesos(admin.ModelAdmin):
    list_display = ("id", "fecha", "detalle", "rubro", "ingreso", "egreso", "obra" )
    ordering = ("fecha", "action_time")
    search_fields = ("detalle", )
    list_display_links = ("detalle", )
    search_help_text = "Busqueda por Detalle"
#    list_filter = ()
#    list_per_page = 3
#    list_editable = ("titulo", )



@admin.register(Imagen)
class AdminImagen(admin.ModelAdmin):
    list_display = ("user", "imagen" )
    ordering = ("user", )
    search_fields = ("user", )
    list_display_links = ("user", )
    search_help_text = "Busqueda por usuario"
#    list_filter = ()
#    list_per_page = 3
#    list_editable = ("titulo", )