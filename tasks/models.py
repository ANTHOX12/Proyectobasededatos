from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db.models import Q


# ---------- Validadores ----------
def no_futuro(value):
    if value and value > timezone.localdate():
        raise ValidationError("No se permiten fechas futuras.")


# ---------- Modelos ----------
class DatosPersonales(models.Model):
    SEXO_CHOICES = [
        ("H", "Hombre"),
        ("M", "Mujer"),
    ]

    descripcion_de_perfil = models.CharField(max_length=50, blank=True)
    perfil_activo = models.IntegerField(default=1)

    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)

    nacionalidad = models.CharField(max_length=20, blank=True)
    lugar_de_nacimiento = models.CharField(max_length=60, blank=True)

    fechana_de_nacimiento = models.DateField(null=True, blank=True, validators=[no_futuro])

    numero_de_cedula = models.CharField(max_length=10, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    estado_civil = models.CharField(max_length=50, blank=True)
    licencia_de_conducir = models.CharField(max_length=6, blank=True)

    telefono_convencional = models.CharField(max_length=15, blank=True)
    telefono_fijo = models.CharField(max_length=15, blank=True)

    direccion_de_trabajo = models.CharField(max_length=50, blank=True)
    direccion_domiciliaria = models.CharField(max_length=50, blank=True)

    sitioweb = models.CharField(max_length=60, blank=True)
    foto_url = models.URLField(blank=True)

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

    fecha_de_inicio_de_gestion = models.DateField(null=True, blank=True, validators=[no_futuro])
    fecha_fin_de_gestion = models.DateField(null=True, blank=True, validators=[no_futuro])

    descripcion_de_funciones = models.CharField(max_length=100, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    ruta_certificado = models.CharField(max_length=100, blank=True)

    def clean(self):
        super().clean()
        if self.fecha_de_inicio_de_gestion and self.fecha_fin_de_gestion:
            if self.fecha_fin_de_gestion < self.fecha_de_inicio_de_gestion:
                raise ValidationError({
                    "fecha_fin_de_gestion": "La fecha fin no puede ser menor que la fecha inicio."
                })

    # ✅ Blindaje: valida siempre (admin, scripts, etc.)
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cargo_desempenado} - {self.nombre_de_la_empresa}"


class Reconocimiento(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="reconocimientos"
    )

    tipo_reconocimiento = models.CharField(max_length=100)
    fecha_reconocimiento = models.DateField(null=True, blank=True, validators=[no_futuro])
    descripcion_reconocimiento = models.CharField(max_length=100, blank=True)

    entidad_patrocinadora = models.CharField(max_length=100, blank=True)
    nombre_contacto_auspicia = models.CharField(max_length=100, blank=True)
    telefono_contacto_auspicia = models.CharField(max_length=60, blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.tipo_reconocimiento


class CursoRealizado(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="cursos"
    )

    nombrecurso = models.CharField(max_length=100)

    fecha_inicio = models.DateField(null=True, blank=True, validators=[no_futuro])
    fecha_fin = models.DateField(null=True, blank=True, validators=[no_futuro])

    # ✅ AQUÍ ESTABA EL HUECO: ahora no permite negativos
    total_horas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    descripcion_curso = models.CharField(max_length=100, blank=True)

    entidad_patrocinadora = models.CharField(max_length=100, blank=True)
    nombre_contacto_auspicia = models.CharField(max_length=100, blank=True)
    telefono_contactoauspicia = models.CharField(max_length=60, blank=True)
    email_empresapatrocinadora = models.EmailField(blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.CharField(max_length=100, blank=True)

    def clean(self):
        super().clean()
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({
                "fecha_fin": "La fecha fin no puede ser menor que la fecha inicio."
            })

    # ✅ Blindaje: valida siempre
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            # ✅ Extra blindaje DB: total_horas >= 0 (si es null, no molesta)
            models.CheckConstraint(
                check=Q(total_horas__gte=0) | Q(total_horas__isnull=True),
                name="curso_total_horas_no_negativo"
            ),
        ]

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

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombrerecurso


class VentaGarage(models.Model):
    ESTADO_CHOICES = [
        ("Bueno", "Bueno"),
        ("Regular", "Regular"),
    ]

    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        db_column="idperfilconqueestaactivo",
        related_name="ventas_garage",
    )

    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40, choices=ESTADO_CHOICES)
    descripcion = models.CharField(max_length=100, blank=True)

    # ✅ NUEVO: Imagen por URL (para mostrar miniatura en el front)
    imagen_url = models.URLField(blank=True)

    valordelbien = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = "venta_garage"
        constraints = [
            models.CheckConstraint(check=Q(valordelbien__gte=0), name="venta_valor_no_negativo"),
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombreproducto


class Formacion(models.Model):
    perfil = models.ForeignKey(
        DatosPersonales, on_delete=models.CASCADE, related_name="formacion_items"
    )

    TIPO_CHOICES = [
        ("PROYECTO", "PROYECTO"),
        ("CURSO", "CURSO"),
        ("CERTIFICACION", "CERTIFICACIÓN"),
        ("TITULO", "TÍTULO"),
        ("OTRO", "OTRO"),
    ]

    titulo = models.CharField(max_length=160)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="PROYECTO")
    descripcion = models.TextField(blank=True)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo} - {self.titulo}"
