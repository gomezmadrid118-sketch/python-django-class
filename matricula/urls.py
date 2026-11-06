from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cursos', views.CursoViewSet, basename='curso')
router.register('estudiantes', views.EstudianteViewSet, basename='estudiante')

urlpatterns = [
    path("", views.inicio, name="inicio_matricula"),
    path("api/estudiantes/", views.listado_estudiantes, name="api_estudiantes"),
    path("api/cursos/", views.listado_cursos, name="api_cursos"),
    path('cursos/2026/', views.CursosDe2026APIView.as_view(), name='cursos_de_2026'),
    path('', include(router.urls)),
]
