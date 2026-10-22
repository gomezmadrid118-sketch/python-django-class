from django.db import models

# Create your models here.
from django.db import models
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    def __str__(self):
        return self.nombre
