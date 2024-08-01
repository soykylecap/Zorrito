"""
URL configuration for Clases_Coder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from AppZorro import views

urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('about/', views.about, name="About")
]


"""
# Cursos
urlpatterns += [
    path('curso-list/', views.CursoListView.as_view(), name="CursoList"),
    path('curso-detail/<int:pk>/', views.CursoDetailView.as_view(), name="CursoDetail"),
    path('curso-create/', views.CursoCreateView.as_view(), name="CursoCreate"),
    path('curso-update/<int:pk>/', views.CursoUpdateView.as_view(), name="CursoUpdate"),
    path('curso-delete/<int:pk>/', views.CursoDeleteView.as_view(), name="CursoDelete"),
]
"""