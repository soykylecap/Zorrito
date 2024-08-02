from django.urls import path
from AppZorro import views

urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('about/', views.about, name="About")
]
