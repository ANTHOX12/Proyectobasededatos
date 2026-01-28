from django.contrib import admin
from django import forms
from django.utils import timezone

from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimiento,
    CursoRealizado,
    ProductoAcademico,
    VentaGarage,
    Formacion,
)


def years_last(n: int):
    y = timezone.localdate().year
    return range(y, y - n, -1)


# ----------------- DatosPersonales -----------------
class DatosPersonalesAdminForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "fechana_de_nacimiento" in self.fields:
            self.fields["fechana_de_nacimiento"].widget = forms.SelectDateWidget(
                years=years_last(90)
            )


@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    form = DatosPersonalesAdminForm


# ----------------- ExperienciaLaboral -----------------
class ExperienciaLaboralAdminForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "fecha_de_inicio_de_gestion" in self.fields:
            self.fields["fecha_de_inicio_de_gestion"].widget = forms.SelectDateWidget(
                years=years_last(30)
            )
        if "fecha_fin_de_gestion" in self.fields:
            self.fields["fecha_fin_de_gestion"].widget = forms.SelectDateWidget(
                years=years_last(30)
            )


@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    form = ExperienciaLaboralAdminForm

    class Media:
        js = ("tasks/admin/js/experiencia_fechas.js",)


# ----------------- Reconocimiento -----------------
class ReconocimientoAdminForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "fecha_reconocimiento" in self.fields:
            self.fields["fecha_reconocimiento"].widget = forms.SelectDateWidget(
                years=years_last(30)
            )


@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    form = ReconocimientoAdminForm


# ----------------- CursoRealizado -----------------
class CursoRealizadoAdminForm(forms.ModelForm):
    class Meta:
        model = CursoRealizado
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "fecha_inicio" in self.fields:
            self.fields["fecha_inicio"].widget = forms.SelectDateWidget(
                years=years_last(30)
            )
        if "fecha_fin" in self.fields:
            self.fields["fecha_fin"].widget = forms.SelectDateWidget(
                years=years_last(30)
            )

        if "total_horas" in self.fields:
            self.fields["total_horas"].widget = forms.NumberInput(
                attrs={"min": 0, "step": 1}
            )


@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    form = CursoRealizadoAdminForm
    ordering = ("-fecha_fin", "-fecha_inicio")

    class Media:
        js = ("tasks/admin/js/curso_fechas.js",)


# ----------------- FORMACION -----------------
@admin.register(Formacion)
class FormacionAdmin(admin.ModelAdmin):
    list_display = ("perfil", "tipo", "titulo", "activarparaqueseveaenfront")
    list_filter = ("tipo", "activarparaqueseveaenfront")
    search_fields = ("titulo", "descripcion", "perfil__nombres", "perfil__apellidos")

    fields = (
        "perfil",
        "tipo",
        "titulo",
        "descripcion",
        "activarparaqueseveaenfront",
    )


# ----------------- VentaGarage -----------------
class VentaGarageAdminForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "valordelbien" in self.fields:
            self.fields["valordelbien"].widget = forms.NumberInput(
                attrs={"min": 0, "step": "0.01"}
            )

        # ✅ NUEVO: Placeholder para pegar la URL de la imagen
        if "imagen_url" in self.fields:
            self.fields["imagen_url"].widget.attrs.update({
                "placeholder": "https://ejemplo.com/imagen.jpg"
            })


@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    form = VentaGarageAdminForm

    # ✅ Mostrar el campo imagen_url en el formulario del admin
    fields = (
        "perfil",
        "nombreproducto",
        "estadoproducto",
        "descripcion",
        "imagen_url",
        "valordelbien",
        "activarparaqueseveaenfront",
    )

    # ✅ Listado más útil
    list_display = (
        "nombreproducto",
        "estadoproducto",
        "valordelbien",
        "activarparaqueseveaenfront",
    )
    list_filter = ("estadoproducto", "activarparaqueseveaenfront")
    search_fields = ("nombreproducto", "descripcion")


# ----------------- ProductoAcademico -----------------
admin.site.register(ProductoAcademico)
