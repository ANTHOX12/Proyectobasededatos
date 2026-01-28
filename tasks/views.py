# tasks/views.py
from django.shortcuts import render
from .models import (
    DatosPersonales,
    CursoRealizado,
    ExperienciaLaboral,
    ProductoAcademico,
    Reconocimiento,
    VentaGarage,
    Formacion,   # ✅ NUEVO
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
            "garage": [],
            "formacion": [],      # ✅ NUEVO
        })

    cursos = CursoRealizado.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by("-fecha_inicio")[:3]

    experiencias = ExperienciaLaboral.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by("-fecha_de_inicio_de_gestion")[:3]

    productos = ProductoAcademico.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    reconocimientos = Reconocimiento.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    garage = VentaGarage.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    formacion = Formacion.objects.filter(   # ✅ NUEVO
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by("-id")  # (si luego pones fecha, cambiamos esto a -fecha)

    return render(request, "home.html", {
        "perfil": perfil,
        "cursos": cursos,
        "experiencias": experiencias,
        "productos": productos,
        "reconocimientos": reconocimientos,
        "garage": garage,
        "formacion": formacion,   # ✅ NUEVO
    })
