from django.shortcuts import render
from .models import (
    DatosPersonales,
    CursoRealizado,
    ExperienciaLaboral,
    ProductoAcademico,
    Reconocimiento,
)

def home(request):
    datos = DatosPersonales.objects.first()
    cursos = CursoRealizado.objects.all()
    experiencia = ExperienciaLaboral.objects.all()
    productos = ProductoAcademico.objects.all()
    reconocimientos = Reconocimiento.objects.all()

    return render(request, "home.html", {
        "datos": datos,
        "cursos": cursos,
        "experiencia": experiencia,
        "productos": productos,
        "reconocimientos": reconocimientos,
    })
