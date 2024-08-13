from django.urls import path
from AppZorro import views


urlpatterns = [
    
    #path('', views.Inicio.as_view(), name="Inicio"),
    path('about/', views.About.as_view(), name="About"),
    path('', views.InicioListView.as_view(), name="Inicio"),
]

urlpatterns += [
    path('movimientos_list/', views.MovimientosListView.as_view(), name="Movimientos"),
    path('movimientos_create/', views.MovimientosCreateView.as_view(), name="CrearMovimiento"),
    path('movimientos_update/<int:pk>/', views.MovimientosUpdateView.as_view(), name="EditarMovimiento"),
    path('movimientos_detail/<int:pk>/', views.MovimientosDetailView.as_view(), name="Detalles"),
    path('movimientos_delete/<int:pk>/', views.MovimientosDeleteView.as_view(), name="MovimientosDelete"),
]

urlpatterns += [
    path('rubros_list/', views.RubrosListView.as_view(), name="Rubros"),
    path('rubros_create/', views.RubrosCreateView.as_view(), name="CrearRubro"),
    path('rubros_update/<int:pk>/', views.RubrosUpdateView.as_view(), name="EditarRubro"),
    path('rubros_delete/<int:pk>/', views.RubrosDeleteView.as_view(), name="BorrarRubro"),
]