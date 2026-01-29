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

    # 1) soporta 2 formatos:
    #   A) ?include=datos,perfil,formacion...
    #   B) ?datos=1&perfil=1&formacion=1... (por si luego lo quieres así)
    include_raw = (request.GET.get("include") or "").strip()

    if include_raw:
        include = {x.strip().lower() for x in include_raw.split(",") if x.strip()}
    else:
        keys = ["datos", "perfil", "formacion", "experiencia", "cursos", "reconocimientos", "producto", "garage"]
        include = {k for k in keys if request.GET.get(k) == "1"}

    # 2) si viene vacío => TODO por defecto
    if not include:
        include = {"datos", "perfil", "formacion", "experiencia", "cursos", "reconocimientos", "producto", "garage"}

    # 3) flags para el template (cv_pdf.html)
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

    # 4) data según checks
    ctx["experiencias"] = (
        ExperienciaLaboral.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
        .order_by("-fecha_de_inicio_de_gestion")
        if ctx["inc_experiencia"] else []
    )

    ctx["reconocimientos"] = (
        Reconocimiento.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
        if ctx["inc_reconocimientos"] else []
    )

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

    # ✅ 5) texto del perfil para el template (en tu HTML se llama perfil_texto)
    #     (usa primero perfil_profesional; si no existe, intenta con descripcion_de_perfil)
    ctx["perfil_texto"] = (
        (getattr(perfil, "perfil_profesional", None) or "").strip()
        or (getattr(perfil, "descripcion_de_perfil", None) or "").strip()
        or ""
    )

    # ✅ 6) has_certs: evita el TemplateSyntaxError (Django template NO soporta paréntesis)
    ctx["has_certs"] = (
        (ctx["inc_cursos"] and any(getattr(c, "rutacertificado", None) for c in ctx["cursos"])) or
        (ctx["inc_reconocimientos"] and any(getattr(r, "rutacertificado", None) for r in ctx["reconocimientos"])) or
        (ctx["inc_experiencia"] and any(getattr(e, "ruta_certificado", None) for e in ctx["experiencias"]))
    )

    # 7) template imprimible
    response = render(request, "cv_pdf.html", ctx)

    # evita cache (para que refleje cambios al toque)
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response
