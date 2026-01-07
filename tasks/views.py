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
    # Trae el primer perfil activo (si existe)
    perfil = DatosPersonales.objects.filter(perfil_activo=1).first()

    # Si no hay perfil todavía, manda listas vacías para que no explote el HTML
    if not perfil:
        return render(request, "home.html", {
            "perfil": None,
            "cursos": [],
            "experiencias": [],
            "productos": [],
            "reconocimientos": [],
        })

    # Trae todo lo relacionado con ese perfil (y solo lo marcado para front)
    cursos = perfil.cursos.filter(activarparaqueseveaenfront=True)
    experiencias = perfil.experiencias.filter(activarparaqueseveaenfront=True)
    productos = perfil.productos_academicos.filter(activarparaqueseveaenfront=True)
    reconocimientos = perfil.reconocimientos.filter(activarparaqueseveaenfront=True)

    return render(request, "home.html", {
        "perfil": perfil,
        "cursos": cursos,
        "experiencias": experiencias,
        "productos": productos,
        "reconocimientos": reconocimientos,
    })
