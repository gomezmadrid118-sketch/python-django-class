from django.urls import path
from . import views

urlpatterns = [
# path('', views.inicio, name='biblioteca'),
path('', views.resumen, name='resumen_biblioteca'),
]