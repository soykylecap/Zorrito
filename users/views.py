from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from users.forms import UserEditForm, UserRegisterForm
from users.models import Imagen

# Create your views here.

def login_request(request):
    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username= usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                return render(request, "AppZorro/index.html")

        msg_login = "Usuario o contraseña incorrectos"

    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form, "msg_login": msg_login})



# Vista de registro
def register(request):
    msg_register = ""
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Si los datos ingresados en el form son válidos, con form.save()
            # creamos un nuevo user usando esos datos
            form.save()
            return render(request,"AppZorro/index.html")
        else:
            msg_register = "Error en los datos ingresados"
            msg_register += f" | {form.errors}"

    form = UserRegisterForm()     
    return render(request,"users/register.html" ,  {"form":form, "msg_register": msg_register})




# Vista de editar el perfil
# Obligamos a loguearse para editar los datos del usuario
@login_required
def edit(request):

    # El usuario para poder editar su perfil primero debe estar logueado.
    # Al estar logueado, podremos encontrar dentro del request la instancia
    # del usuario -> request.user
    usuario = request.user

    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST, request.FILES)

        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            datos = {
                    'email': usuario.email,
                    'imagen': usuario.imagen
                }
            miFormulario = UserEditForm(initial=datos)

            usuario.email = informacion['email']
            usuario.save()


            # Creamos nueva imagen en la tabla
            try:
                avatar = Imagen.objects.get(user=usuario)
            except Imagen.DoesNotExist:
                avatar = Imagen(user=usuario, imagen=informacion["imagen"])
                avatar.save()
            else:
                avatar.imagen = informacion["imagen"]
                avatar.save()

            return render(request, "AppZorro/index.html")

    else:
        datos = {
            'first_name': usuario.first_name,
            'email': usuario.email
        }
        miFormulario = UserEditForm(initial=datos)

    return render(request, "users/edit.html", {"mi_form": miFormulario, "usuario": usuario})


