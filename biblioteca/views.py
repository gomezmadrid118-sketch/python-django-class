from django.shortcuts import render
from django.http import HttpResponse
from .models import Libro

# Create your views here.
# def inicio(request):
#     return HttpResponse("Chingue su madre el City")

def resumen(request):
    total = Libro.objects.count()
    return HttpResponse(f"Actualmente hay {total} libros registrados en la biblioteca.")