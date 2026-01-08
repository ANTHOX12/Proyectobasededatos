# tasks/views.py
from django.shortcuts import render
from .models import (
    DatosPersonales,
    CursoRealizado,
    ExperienciaLaboral,
    ProductoAcademico,
    Reconocimiento,
)

def home(request):
    perfil = DatosPersonales.objects.filter(perfil_activo=1).first()

    if not perfil:
        return render(request, "home.html", {
            "perfil": None,
            "cursos": [],
            "experiencias": [],
            "productos": [],
            "reconocimientos": [],
        })

    cursos = CursoRealizado.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by("-fecha_inicio")[:3]

    experiencias = ExperienciaLaboral.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    productos = ProductoAcademico.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    reconocimientos = Reconocimiento.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    return render(request, "home.html", {
        "perfil": perfil,
        "cursos": cursos,
        "experiencias": experiencias,
        "productos": productos,
        "reconocimientos": reconocimientos,
    })


