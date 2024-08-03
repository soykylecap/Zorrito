from django.contrib import admin
from users.models import Imagen
# Register your models here.

admin.site.register(Imagen)

class AdminUsers(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    ordering = ("username", )
    search_fields = ("username", )
    list_editable = ("email", )
    list_display_links = ("username", )
#    list_filter = ("camada", )
#    list_per_page = 3
