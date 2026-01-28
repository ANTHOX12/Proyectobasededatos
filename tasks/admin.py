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

        # Fechas
        if "fecha_inicio" in self.fields:
            self.fields["fecha_inicio"].widget = forms.SelectDateWidget(
                years=years_last(30)
            )
        if "fecha_fin" in self.fields:
            self.fields["fecha_fin"].widget = forms.SelectDateWidget(
                years=years_last(30)
            )

        # 🔒 NO negativos (UI)
        if "total_horas" in self.fields:
            self.fields["total_horas"].widget = forms.NumberInput(
                attrs={"min": 0, "step": 1}
            )


@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    form = CursoRealizadoAdminForm

    # 👉 ORDEN POR FECHA (más reciente primero)
    ordering = ("-fecha_fin", "-fecha_inicio")

    class Media:
        js = ("tasks/admin/js/curso_fechas.js",)



# ----------------- VentaGarage -----------------
class VentaGarageAdminForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔒 NO negativos (UI)
        if "valordelbien" in self.fields:
            self.fields["valordelbien"].widget = forms.NumberInput(
                attrs={"min": 0, "step": "0.01"}
            )


@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    form = VentaGarageAdminForm


# ----------------- ProductoAcademico -----------------
admin.site.register(ProductoAcademico)
