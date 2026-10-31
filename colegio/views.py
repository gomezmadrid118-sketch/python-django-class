from django.shortcuts import render
from django.http import HttpResponse
from .models import Curso, Estudiante

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CursoSerializer, EstudianteSerializer

def inicio(request):
    cursos = Curso.objects.all()
    estudiantes = Estudiante.objects.all()

    respuesta = f"""
    <h1>Información del colegio</h1>

    <h2>Cursos registrados: {cursos.count()}</h2>
    <ul>
    """

    for curso in cursos:
        respuesta += f"<li>{curso.nombre_curso}</li>"

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