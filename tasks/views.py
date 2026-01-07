# tasks/views.py
from django.shortcuts import render
from .models import DatosPersonales

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
