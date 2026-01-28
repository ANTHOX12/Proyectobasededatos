from django.contrib import admin
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimiento,
    CursoRealizado,
    ProductoAcademico,
    VentaGarage,   
)

admin.site.register(DatosPersonales)
admin.site.register(ExperienciaLaboral)
admin.site.register(Reconocimiento)
admin.site.register(CursoRealizado)
admin.site.register(ProductoAcademico)
admin.site.register(VentaGarage)   
