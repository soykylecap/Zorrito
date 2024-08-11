from django.urls import path
from AppZorro import views
from AppZorro.views import Inicio, About, MovimientosListView, MovimientosDetailView, MovimientosCreateView, MovimientosDeleteView, MovimientosUpdateView

urlpatterns = [
    
    path('', Inicio.as_view(), name="Inicio"),
    path('about/', About.as_view(), name="About")
]

urlpatterns += [
    path('movimientos_list/', MovimientosListView.as_view(), name="Movimientos"),
    path('movimientos_create/', MovimientosCreateView.as_view(), name="CrearMovimiento"),
    path('movimientos_update/<int:pk>/', MovimientosUpdateView.as_view(), name="EditarMovimiento"),
    path('movimientos_detail/<int:pk>/', MovimientosDetailView.as_view(), name="Detalles"),
    path('movimientos_delete/<int:pk>/', MovimientosDeleteView.as_view(), name="MovimientosDelete"),
]