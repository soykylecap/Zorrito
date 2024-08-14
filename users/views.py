from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView
from users.forms import UserEditForm, UserRegisterForm
from users.models import Imagen
from AppZorro.models import CajaPesos 





# Create your views here.

def login_request(request):
    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contrasenia)
            total_registros = CajaPesos.objects.count()
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '')
                if next_url == '':
                    return render(request, "AppZorro/index.html", {'total_registros':total_registros, })
                return redirect(next_url)
        msg_login = "Usuario o contraseña incorrectos"
    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form, "msg_login": msg_login})



def register(request):
    msg_register = ""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            usuario_del_form = form.cleaned_data
            usuario1 = User.objects.get(username=usuario_del_form['username'])
            avatar = Imagen(user=usuario1, imagen="/avatares/avatar_defecto.png")
            avatar.save()
            return render(request,"AppZorro/index.html")
        else:
            msg_register = form.errors
            print (msg_register)
    form = UserRegisterForm()     
    return render(request,"users/register.html" ,  {"form":form, "msg_register": msg_register})



@login_required
def edit(request):
    usuario = request.user
    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            datos = {
                    'username':usuario.username,
                    'email': usuario.email,
                }
            miFormulario = UserEditForm(initial=datos)
            usuario.email = informacion['email']
            usuario.save()
            try:
                avatar = Imagen.objects.get(user=usuario)
                print(Imagen)
            except Imagen.DoesNotExist:
                if informacion["imagen"] != "":
                    avatar = Imagen(user=usuario, imagen=informacion["imagen"])
                    avatar.save()
                else:
                    avatar = Imagen(user=usuario, imagen="/avatares/avatar_defecto.png")  
                    avatar.save()
            else:
                if informacion["imagen"]:
                    avatar.imagen = informacion["imagen"]
                    avatar.save()
            return render(request, "AppZorro/index.html")
    else:
        datos = {
            'username': usuario.username,
            'email': usuario.email
        }
        miFormulario = UserEditForm(initial=datos)
    return render(request, "users/edit.html", {"mi_form": miFormulario, "usuario": usuario})


class UsersLogoutView(LogoutView, ListView):
    model = CajaPesos
    template_name = 'AppZorro/index.html'
    object_list = 0
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_registros = CajaPesos.objects.count()
        context['total_registros'] = total_registros
        return context

