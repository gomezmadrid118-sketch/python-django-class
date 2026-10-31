from django.db import models


# Create your models here.
class Curso(models.Model):
    nombre_curso = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_curso

class Estudiante(models.Model):
    nombre = models.CharField(max_length=50)
    curso = models.ForeignKey(
Curso,
on_delete=models.CASCADE,
related_name='estudiantes'
)
    def __str__(self):
        return self.nombre

