from django.shortcuts import render
#from .models import 
#from AppZorro.forms import 

# Create your views here.

def inicio(request):
    return render(request, "AppZorro/index.html")

def about(request):
    return render(request, "AppZorro/index.html")