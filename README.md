# Práctica Django: crear una app nueva

Este proyecto sirve para practicar Django. Ya tiene algunos ejemplos como `colegio`,
`biblioteca` e `inventario`.

En esta guía vamos a crear una app nueva, parecida a `colegio`, pero con otro tema:
una **tienda**.

La tienda tendrá:

- Categorías.
- Productos.
- Una página para ver los productos.
- Una API sencilla.

La idea es repetir los mismos pasos aprendidos en `colegio`:

```text
crear app → crear modelos → hacer migraciones → registrar en admin
→ crear vistas → crear URLs → probar
```

---

## 1. Preparar el proyecto

Abrir PowerShell dentro de la carpeta del proyecto:

```powershell
cd "C:\Users\USER\OneDrive\Desktop\SENA\Python\python-django-class"
```

Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Comprobar que Django funciona:

```powershell
python manage.py check
```

Si aparece `System check identified no issues`, todo está bien.

---

## 2. Crear la aplicación

Crear una app llamada `tienda`:

```powershell
python manage.py startapp tienda
```

Ahora abrir `config/settings.py` y agregar `"tienda"` dentro de `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "inventario",
    "saludos",
    "biblioteca",
    "colegio",
    "tienda",
]
```

Guardar el archivo.

---

## 3. Crear los modelos

Abrir `tienda/models.py` y escribir:

```python
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="productos",
    )

    def __str__(self):
        return self.nombre
```

### ¿Qué significa este código?

- `Categoria` guarda grupos como **ropa**, **tecnología** o **alimentos**.
- `Producto` guarda el nombre, precio y cantidad disponible.
- `ForeignKey` conecta cada producto con una categoría.
- `__str__` muestra un nombre entendible en el administrador.

---

## 4. Crear las tablas

Cada vez que se crea o modifica un modelo, ejecutar:

```powershell
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` prepara los cambios.

`migrate` crea o actualiza las tablas de la base de datos.

---

## 5. Mostrar los modelos en el administrador

Abrir `tienda/admin.py` y escribir:

```python
from django.contrib import admin
from .models import Categoria, Producto


admin.site.register(Categoria)
admin.site.register(Producto)
```

Crear un usuario administrador:

```powershell
python manage.py createsuperuser
```

Escribir el nombre de usuario, correo y contraseña.

Luego iniciar Django:

```powershell
python manage.py runserver
```

Abrir en el navegador:

<http://127.0.0.1:8000/admin/>

Desde allí se pueden crear categorías y productos.

---

## 6. Crear una página para la tienda

Abrir `tienda/views.py` y escribir:

```python
from django.http import HttpResponse
from .models import Categoria, Producto


def inicio(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()

    respuesta = "<h1>Mi tienda</h1>"
    respuesta += f"<h2>Productos registrados: {productos.count()}</h2>"
    respuesta += "<h3>Categorías</h3><ul>"

    for categoria in categorias:
        respuesta += f"<li>{categoria.nombre}</li>"

    respuesta += "</ul><h3>Productos</h3><ul>"

    for producto in productos:
        respuesta += f"""
        <li>
            {producto.nombre} -
            Precio: ${producto.precio} -
            Stock: {producto.stock} -
            Categoría: {producto.categoria.nombre}
        </li>
        """

    respuesta += "</ul>"
    return HttpResponse(respuesta)
```

### ¿Qué hace esta vista?

1. Busca las categorías.
2. Busca los productos.
3. Cuenta cuántos productos existen.
4. Recorre los datos con un `for`.
5. Muestra todo en una respuesta HTML.

Es la misma idea de la vista `inicio` de la app `colegio`.

---

## 7. Crear las URLs de la app

Crear el archivo `tienda/urls.py`:

```python
from django.urls import path
from . import views


urlpatterns = [
    path("", views.inicio, name="inicio_tienda"),
]
```

Ahora abrir `config/urls.py` y agregar:

```python
path("tienda/", include("tienda.urls")),
```

El archivo debe tener importado `include`:

```python
from django.urls import include, path
```

La sección de URLs puede quedar así:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("inventario/", include("inventario.urls")),
    path("saludos/", include("saludos.urls")),
    path("biblioteca/", include("biblioteca.urls")),
    path("colegio/", include("colegio.urls")),
    path("tienda/", include("tienda.urls")),
]
```

Probar la página en:

<http://127.0.0.1:8000/tienda/>

---

## 8. Crear una API sencilla

La API permite ver los productos en formato JSON.

### Serializador

Crear `tienda/serializers.py`:

```python
from rest_framework import serializers
from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(
        source="categoria.nombre",
        read_only=True,
    )

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "precio",
            "stock",
            "categoria",
            "categoria_nombre",
        ]
```

### Vista de la API

Agregar en `tienda/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductoSerializer


@api_view(["GET"])
def listado_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)
```

### URL de la API

Modificar `tienda/urls.py`:

```python
from django.urls import path
from . import views


urlpatterns = [
    path("", views.inicio, name="inicio_tienda"),
    path(
        "api/productos/",
        views.listado_productos,
        name="api_productos",
    ),
]
```

Probar en el navegador:

<http://127.0.0.1:8000/tienda/api/productos/>

También se puede probar desde PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/tienda/api/productos/
```

---

## 9. Crear datos desde la consola

Abrir la consola de Django:

```powershell
python manage.py shell
```

Escribir:

```python
from tienda.models import Categoria, Producto

categoria = Categoria.objects.create(nombre="Tecnología")

producto = Producto.objects.create(
    nombre="Teclado",
    precio=85000,
    stock=10,
    categoria=categoria,
)

producto
```

Consultar los datos:

```python
Categoria.objects.all()
Producto.objects.all()
Producto.objects.filter(stock__gt=0)
producto.categoria.nombre
```

Salir:

```python
exit()
```

---

## 10. Cómo repetirlo con otro tema

La misma estructura se puede usar para cualquier tema:

| Tema | Modelo principal | Otro modelo |
|---|---|---|
| Biblioteca | Libro | Autor |
| Restaurante | Plato | Categoría |
| Gimnasio | Cliente | Plan |
| Veterinaria | Mascota | Dueño |
| Cine | Película | Género |
| Tienda | Producto | Categoría |

Por ejemplo, para una app de restaurante:

```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)


class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
```

Después se repiten los mismos pasos:

```text
1. Crear la app.
2. Agregarla a settings.py.
3. Crear los modelos.
4. Ejecutar makemigrations y migrate.
5. Registrar los modelos en admin.py.
6. Crear una vista.
7. Crear urls.py.
8. Conectar las URLs principales.
9. Crear serializers si se necesita una API.
10. Probar en el navegador.
```

---

## 11. Comandos más usados

```powershell
# Crear una aplicación
python manage.py startapp nombre_app

# Revisar errores de Django
python manage.py check

# Crear cambios de modelos
python manage.py makemigrations

# Aplicar cambios a la base de datos
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser

# Iniciar el servidor
python manage.py runserver

# Abrir la consola de Django
python manage.py shell

# Ejecutar pruebas
python manage.py test
```

## 12. Actividad recomendada

Después de terminar la tienda, crear otra app sin copiar todo de forma automática.

Opciones:

1. `restaurante`: categorías y platos.
2. `veterinaria`: dueños y mascotas.
3. `gimnasio`: clientes y planes.

Debe tener como mínimo:

- Dos modelos relacionados.
- Datos creados desde el administrador.
- Una página que liste los datos.
- Una API que muestre el modelo principal.
- Una consulta hecha desde `python manage.py shell`.
