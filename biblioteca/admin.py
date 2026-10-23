from django.contrib import admin
from .models import Autor, Libro
# Register your models here.

# admin.site.register(Autor)
# admin.site.register(Libro)

from django.contrib import admin
from .models import Autor, Libro
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacionalidad')
    search_fields = ('nombre',)
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'precio', 'disponible')
    list_filter = ('disponible', 'autor')
    search_fields = ('titulo',)