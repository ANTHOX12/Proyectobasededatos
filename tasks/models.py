from django.db import models


class DatosPersonales(models.Model):
    SEXO_CHOICES = [
        ("H", "Hombre"),
        ("M", "Mujer"),
    ]

    # Perfil
    descripcionperfil = models.CharField(max_length=50, blank=True)
    perfilactivo = models.IntegerField(default=1)

    # Datos básicos
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)

    nacionalidad = models.CharField(max_length=20, blank=True)
    lugarnacimiento = models.CharField(max_length=60, blank=True)
    fechanacimiento = models.DateField(null=True, blank=True)

    numerocedula = models.CharField(max_length=10, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    estadocivil = models.CharField(max_length=50, blank=True)
    licenciaconducir = models.CharField(max_length=6, blank=True)

    telefonoconvencional = models.CharField(max_length=15, blank=True)
    telefonofijo = models.CharField(max_length=15, blank=True)

    direcciontrabajo = models.CharField(max_length=50, blank=True)
    direcciondomiciliaria = models.CharField(max_length=50, blank=True)

    sitioweb = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="experiencias"
    )

    cargodesempenado = models.CharField(max_length=100)
    nombrempresa = models.CharField(max_length=50)
    lugarempresa = models.CharField(max_length=50, blank=True)

    emailempresa = models.EmailField(blank=True)
    sitiowebempresa = models.CharField(max_length=100, blank=True)

    nombrecontactoempresarial = models.CharField(max_length=100, blank=True)
    telefonocontactoempresarial = models.CharField(max_length=60, blank=True)

    fechainiciogestion = models.DateField(null=True, blank=True)
    fechafingestion = models.DateField(null=True, blank=True)

    descripcionfunciones = models.CharField(max_length=100, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.cargodesempenado} - {self.nombrempresa}"


class Reconocimiento(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="reconocimientos"
    )

    tiporeconocimiento = models.CharField(max_length=100)
    fechareconocimiento = models.DateField(null=True, blank=True)
    descripcionreconocimiento = models.CharField(max_length=100, blank=True)

    entidadpatrocinadora = models.CharField(max_length=100, blank=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.tiporeconocimiento


class CursoRealizado(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="cursos"
    )

    nombrecurso = models.CharField(max_length=100)
    fechainicio = models.DateField(null=True, blank=True)
    fechafin = models.DateField(null=True, blank=True)

    totalhoras = models.IntegerField(null=True, blank=True)
    descripcioncurso = models.CharField(max_length=100, blank=True)

    entidadpatrocinadora = models.CharField(max_length=100, blank=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True)
    emailempresapatrocinadora = models.EmailField(blank=True)

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
