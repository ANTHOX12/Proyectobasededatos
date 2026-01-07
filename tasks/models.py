from django.db import models


class DatosPersonales(models.Model):
    SEXO_CHOICES = [
        ("H", "Hombre"),
        ("M", "Mujer"),
    ]

    # Perfil
    descripcion_de_perfil = models.CharField(max_length=50, blank=True)
    perfil_activo = models.IntegerField(default=1)

    # Datos básicos
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)

    nacionalidad = models.CharField(max_length=20, blank=True)
    lugar_de_nacimiento = models.CharField(max_length=60, blank=True)
    fechana_de_nacimiento = models.DateField(null=True, blank=True)

    numero_de_cedula = models.CharField(max_length=10, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    estado_civil = models.CharField(max_length=50, blank=True)
    licencia_de_conducir = models.CharField(max_length=6, blank=True)

    telefono_convencional = models.CharField(max_length=15, blank=True)
    telefono_fijo = models.CharField(max_length=15, blank=True)

    direccion_de_trabajo = models.CharField(max_length=50, blank=True)
    direccion_domiciliaria = models.CharField(max_length=50, blank=True)

    sitioweb = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="experiencias"
    )

    cargo_desempenado = models.CharField(max_length=100)
    nombre_de_la_empresa = models.CharField(max_length=50)
    lugarempresa = models.CharField(max_length=50, blank=True)

    email_empresa = models.EmailField(blank=True)
    sitio_web_empresa = models.CharField(max_length=100, blank=True)

    nombre_contacto_empresarial = models.CharField(max_length=100, blank=True)
    telefono_contacto_empresarial = models.CharField(max_length=60, blank=True)

    fecha_de_inicio_de_gestion = models.DateField(null=True, blank=True)
    fecha_fin_de_gestion = models.DateField(null=True, blank=True)

    descripcion_de_funciones = models.CharField(max_length=100, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    ruta_certificado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.cargo_desempenado} - {self.nombre_de_la_empresa}"


class Reconocimiento(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="reconocimientos"
    )

    tipo_reconocimiento = models.CharField(max_length=100)
    fecha_reconocimiento = models.DateField(null=True, blank=True)
    descripcion_reconocimiento = models.CharField(max_length=100, blank=True)

    entidad_patrocinadora = models.CharField(max_length=100, blank=True)
    nombre_contacto_auspicia = models.CharField(max_length=100, blank=True)
    telefono_contacto_auspicia = models.CharField(max_length=60, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.tipo_reconocimiento


class CursoRealizado(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="cursos"
    )

    nombrecurso = models.CharField(max_length=100)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    total_horas = models.IntegerField(null=True, blank=True)
    descripcion_curso = models.CharField(max_length=100, blank=True)

    entidad_patrocinadora = models.CharField(max_length=100, blank=True)
    nombre_contacto_auspicia = models.CharField(max_length=100, blank=True)
    telefono_contactoauspicia = models.CharField(max_length=60, blank=True)
    email_empresapatrocinadora = models.EmailField(blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombrecurso


class ProductoAcademico(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="productos_academicos"
    )

    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100, blank=True)
    descripcion = models.CharField(max_length=100, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombrerecurso
