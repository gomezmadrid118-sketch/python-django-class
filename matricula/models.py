from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Curso(models.Model):
    nombre_curso = models.CharField(max_length=50)
    annio = models.IntegerField(
    validators=[MinValueValidator(1900), MaxValueValidator(2100)],
    help_text='Ingresa un año de 4 dígitos, ej. 2026',
)
    def __str__(self):
        return self.nombre_curso

class Estudiante(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    curso = models.ForeignKey(
Curso,
on_delete=models.CASCADE,
related_name='estudiantes'
)
    def __str__(self):
        return self.nombre

