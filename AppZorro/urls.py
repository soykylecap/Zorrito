from django.urls import path
from AppZorro import views


urlpatterns = [
    
    #path('', views.Inicio.as_view(), name="Inicio"),
    path('about/', views.About.as_view(), name="About"),
    path('', views.InicioTemplateView.as_view(), name="Inicio"),
    path('copia', views.InicioListView.as_view(), name="InicioCopia"),
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

urlpatterns += [
    path('dolares_list/', views.DolaresListView.as_view(), name="Dolares"),
    path('dolares_create/', views.DolaresCreateView.as_view(), name="CrearDolares"),
    path('dolares_venta/', views.DolaresVentaView.as_view(), name="VentaDolares"),
    path("dolares_update/<int:pk>/", views.DolaresUpdateView.as_view(), name="EditarDolares"),
    path("dolares_detail/<int:pk>/", views.DolaresDetailView.as_view(), name="DetalleDolar"),
    path('dolares_delete/<int:pk>/', views.DolaresDeleteView.as_view(), name="DolaresDelete"),
]

urlpatterns += [
    path('obra_list/', views.ObraListView.as_view(), name="Obras"),
    path("obra_detail/<int:pk>/", views.ObraDetailView.as_view(), name="DetalleObra"),
    path('obra_create/', views.ObraCreateView.as_view(), name="CrearObra"),
    path('obra_update/<int:pk>/', views.ObraUpdateView.as_view(), name="EditarObra"),
    path('obra_delete/<int:pk>/', views.ObraDeleteView.as_view(), name="BorrarObra"),
]

urlpatterns += [
    path('tarea_list/', views.TareaListView.as_view(), name="Tareas"),
    path("tarea_detail/<int:pk>/", views.TareaDetailView.as_view(), name="DetalleTarea"),
    path('tarea_create/', views.TareaCreateView.as_view(), name="CrearTarea"),
    # path('rubros_update/<int:pk>/', views.RubrosUpdateView.as_view(), name="EditarRubro"),
    # path('rubros_delete/<int:pk>/', views.RubrosDeleteView.as_view(), name="BorrarRubro"),
]