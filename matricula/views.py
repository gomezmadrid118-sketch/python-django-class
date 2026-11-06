from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Curso, Estudiante

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CursoSerializer, EstudianteSerializer

from rest_framework import viewsets

def inicio(request):
    cursos = Curso.objects.all()
    estudiantes = Estudiante.objects.all()

    respuesta = f"""
    <h1>Información del colegio</h1>

    <h2>Cursos registrados: {cursos.count()}</h2>
    <ul>
    """

    for curso in cursos:
        respuesta += f"<li>{curso.nombre_curso} - {curso.annio}</li>"

    respuesta += """
    </ul>

    <h2>Estudiantes registrados:</h2>
    <ul>
    """

    for estudiante in estudiantes:
        respuesta += f"""
        <li>
            {estudiante.nombre} -
            Curso: {estudiante.curso.nombre_curso}
        </li>
        """

    respuesta += "</ul>"

    return HttpResponse(respuesta)

@api_view(["GET"])
def listado_cursos(request):
    cursos = Curso.objects.all()
    serializer = CursoSerializer(cursos, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def listado_estudiantes(request):
    estudiantes = Estudiante.objects.select_related("curso").all()
    serializer = EstudianteSerializer(estudiantes, many=True)
    return Response(serializer.data)



# @api_view(["GET"])
# def listado_cursos(request):
#     curso = Curso.objects.all()
#     serializer = CursoSerializer(curso, many=True)
#     return Response(serializer.data)

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all().order_by('nombre')
    serializer_class = EstudianteSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CursosDe2026APIView(APIView):
    """Muestra los cursos hechos en 2026."""

    def get(self, request):
        cursos = Curso.objects.filter(annio=2026)
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CursoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


from rest_framework import generics

class CursoListCreateView(generics.ListCreateAPIView):
    serializer_class = CursoSerializer

    def get_queryset(self):
        # Personalización: solo libros disponibles, ordenados por título
        return Curso.objects.filter(annio=2026).order_by('nombre')

class CursoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer