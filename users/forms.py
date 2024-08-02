from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Username")
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        # Si queremos EDIAR los mensajes de ayuda editamos este dict,
            # de lo contrario lo limpiamos de ésta forma.
        #help_text = {k: "" for k in fields}



class UserEditForm(UserCreationForm):
    password1 = None
    password2 = None
    email = forms.EmailField(label="Ingrese su email:")
    imagen = forms.ImageField(label="Imagen", required=False)

    class Meta:
        model = User
        fields = ['email', 'imagen']
        help_texts = {k:"" for k in fields}