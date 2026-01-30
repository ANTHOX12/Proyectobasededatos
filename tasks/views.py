# tasks/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import (
    DatosPersonales,
    CursoRealizado,
    ExperienciaLaboral,
    ProductoAcademico,
    Reconocimiento,
    VentaGarage,
    Formacion,
)

# =======================
# HOME (tu pantalla normal)
# =======================
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
            "formacion": [],
        })

    # ✅ CAMBIO: ya NO lo limito a 3, ahora trae TODOS los cursos activos
    cursos = CursoRealizado.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by("-fecha_inicio")  # <-- sin [:3]

    # ✅ (Opcional) también quité el límite en experiencia para que sea consistente
    experiencias = ExperienciaLaboral.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by("-fecha_de_inicio_de_gestion")  # <-- sin [:3]

    productos = ProductoAcademico.objects.filter(
    perfil=perfil,
    activarparaqueseveaenfront=True
).order_by("-fecha_inicio", "-id")


    reconocimientos = Reconocimiento.objects.filter(
    perfil=perfil,
    activarparaqueseveaenfront=True
).order_by("-fecha_reconocimiento", "-id")



    garage = VentaGarage.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    )

    formacion = Formacion.objects.filter(
        perfil=perfil,
        activarparaqueseveaenfront=True
    ).order_by("-id")

    return render(request, "home.html", {
        "perfil": perfil,
        "cursos": cursos,
        "experiencias": experiencias,
        "productos": productos,
        "reconocimientos": reconocimientos,
        "garage": garage,
        "formacion": formacion,
    })


# =======================
# ✅ PDF (SIN WeasyPrint)
# genera HTML imprimible y el navegador lo guarda como PDF
# =======================
@xframe_options_exempt
def generar_pdf(request):
    perfil = DatosPersonales.objects.filter(perfil_activo=1).first()
    if not perfil:
        return HttpResponse("No hay perfil activo.", status=404)

    include_raw = (request.GET.get("include") or "").strip()

    if include_raw:
        include = {x.strip() for x in include_raw.split(",") if x.strip()}
    else:
        keys = ["datos", "perfil", "formacion", "experiencia", "cursos", "reconocimientos", "producto", "garage"]
        include = {k for k in keys if request.GET.get(k) == "1"}

    if not include:
        include = {"datos", "perfil", "formacion", "experiencia", "cursos", "reconocimientos", "producto", "garage"}

    ctx = {
        "perfil": perfil,
        "include": include,

        "inc_datos": "datos" in include,
        "inc_perfil": "perfil" in include,
        "inc_formacion": "formacion" in include,
        "inc_experiencia": "experiencia" in include,
        "inc_cursos": "cursos" in include,
        "inc_reconocimientos": "reconocimientos" in include,
        "inc_producto": "producto" in include,
        "inc_garage": "garage" in include,
    }

    ctx["experiencias"] = (
        ExperienciaLaboral.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
        .order_by("-fecha_de_inicio_de_gestion")
        if ctx["inc_experiencia"] else []
    )

    ctx["reconocimientos"] = (
        Reconocimiento.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
        if ctx["inc_reconocimientos"] else []
    )

    # ✅ acá ya estaba bien (sin límite), lo dejo igual
    ctx["cursos"] = (
        CursoRealizado.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
        .order_by("-fecha_inicio")
        if ctx["inc_cursos"] else []
    )

    ctx["formacion"] = (
        Formacion.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
        .order_by("-id")
        if ctx["inc_formacion"] else []
    )

    ctx["productos"] = (
        ProductoAcademico.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
        if ctx["inc_producto"] else []
    )

    ctx["garage"] = (
        VentaGarage.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
        if ctx["inc_garage"] else []
    )

    response = render(request, "cv_pdf.html", ctx)
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response
