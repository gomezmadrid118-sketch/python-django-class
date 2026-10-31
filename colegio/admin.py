from django.contrib import admin
from .models import Curso, Estudiante

# Register your models here.


@admin.register(Curso)
class CursosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_curso")
    search_fields = ("nombre_curso",)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "curso")
    search_fields = ("nombre",)
    list_filter = ("curso",)