from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path("api/cursos/", views.listado_cursos, name="api_cursos"),
    path("api/estudiantes/", views.listado_estudiantes, name="api_estudiantes"),
]