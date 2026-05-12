"""
NeuroMax — Modelos de Base de Datos
=====================================
Motor KST (Knowledge Space Theory) + Tutor Socrático con metodología EMT.
Institución: Colegio Sagrada Familia (COSAFAM)
Nivel: 1er Año de Bachillerato
"""

import secrets
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def _generar_codigo_union(longitud: int = 8) -> str:
    """Genera un código alfanumérico único en mayúsculas para unirse a una Clase."""
    alfabeto = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alfabeto) for _ in range(longitud))


# ---------------------------------------------------------------------------
# PERFILES DE USUARIO
# ---------------------------------------------------------------------------

class PerfilUsuario(models.Model):
    """
    Extensión del User base de allauth.
    El rol se asigna automáticamente según la URL de registro utilizada:
      - /registro/profesor/   → rol='PROFESOR'
      - /registro/estudiante/ → rol='ESTUDIANTE'
    """

    class Rol(models.TextChoices):
        PROFESOR = "PROFESOR", _("Profesor")
        ESTUDIANTE = "ESTUDIANTE", _("Estudiante")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil",
        verbose_name=_("Usuario"),
    )
    rol = models.CharField(
        _("Rol"),
        max_length=10,
        choices=Rol.choices,
        default=Rol.ESTUDIANTE,
    )
    nombre_completo = models.CharField(_("Nombre completo"), max_length=200, blank=True)
    institucion = models.CharField(
        _("Institución"),
        max_length=200,
        default="Colegio Sagrada Familia — COSAFAM",
    )

    class Meta:
        verbose_name = _("Perfil de Usuario")
        verbose_name_plural = _("Perfiles de Usuarios")

    def __str__(self) -> str:
        return f"{self.get_rol_display()}: {self.nombre_completo or self.user.email}"

    @property
    def es_profesor(self) -> bool:
        return self.rol == self.Rol.PROFESOR

    @property
    def es_estudiante(self) -> bool:
        return self.rol == self.Rol.ESTUDIANTE


# ---------------------------------------------------------------------------
# CLASES (MULTI-TENANT A NIVEL DE PROFESOR)
# ---------------------------------------------------------------------------

class Clase(models.Model):
    """
    Grupo de estudiantes administrado por un Profesor.
    Soporta múltiples clases por docente (multi-tenant).
    """

    profesor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="clases",
        verbose_name=_("Profesor"),
        limit_choices_to={"perfil__rol": "PROFESOR"},
    )
    nombre = models.CharField(_("Nombre de la clase"), max_length=150)
    descripcion = models.TextField(_("Descripción"), blank=True)
    codigo_union = models.CharField(
        _("Código de unión"),
        max_length=8,
        unique=True,
        help_text=_("Código único para que los estudiantes se unan a la clase."),
    )
    activa = models.BooleanField(_("Activa"), default=True)
    fecha_creacion = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)

    class Meta:
        verbose_name = _("Clase")
        verbose_name_plural = _("Clases")
        ordering = ["-fecha_creacion"]

    def __str__(self) -> str:
        return f"{self.nombre} [{self.codigo_union}]"

    def save(self, *args, **kwargs):
        # Auto-generar código de unión si no fue asignado manualmente
        if not self.codigo_union:
            codigo = _generar_codigo_union()
            while Clase.objects.filter(codigo_union=codigo).exists():
                codigo = _generar_codigo_union()
            self.codigo_union = codigo
        super().save(*args, **kwargs)

    @property
    def total_estudiantes(self) -> int:
        return self.inscripciones.filter(activa=True).count()


class Inscripcion(models.Model):
    """
    Relación entre un Estudiante y una Clase.
    Un estudiante puede estar inscrito en múltiples clases.
    """

    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inscripciones",
        verbose_name=_("Estudiante"),
        limit_choices_to={"perfil__rol": "ESTUDIANTE"},
    )
    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name="inscripciones",
        verbose_name=_("Clase"),
    )
    fecha_ingreso = models.DateTimeField(_("Fecha de ingreso"), auto_now_add=True)
    activa = models.BooleanField(_("Activa"), default=True)

    class Meta:
        verbose_name = _("Inscripción")
        verbose_name_plural = _("Inscripciones")
        unique_together = [("estudiante", "clase")]
        ordering = ["clase", "fecha_ingreso"]

    def __str__(self) -> str:
        return f"{self.estudiante.email} → {self.clase.nombre}"


# ---------------------------------------------------------------------------
# CONTENIDO PEDAGÓGICO (100% EN BASE DE DATOS — CERO HARDCODING)
# ---------------------------------------------------------------------------

class Problema(models.Model):
    """
    Unidad pedagógica completa.
    Contiene el enunciado, la representación visual (HTML), y los datos EMT
    (Expectations + Misconceptions) que alimentan el System Prompt de Gemini.
    La cadena KST se define mediante el campo `prerequisito`.
    """

    class Tema(models.TextChoices):
        FRACCIONES = "FRACCIONES", _("Fracciones")
        EXPONENCIACION = "EXPONENCIACION", _("Exponenciación")

    titulo = models.CharField(_("Título"), max_length=200)
    tema = models.CharField(_("Tema"), max_length=20, choices=Tema.choices)
    nivel_kst = models.PositiveIntegerField(
        _("Nivel KST"),
        default=1,
        help_text=_("Posición en la jerarquía de conocimiento (1 = base)."),
    )
    prerequisito = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dependientes",
        verbose_name=_("Problema prerrequisito"),
        help_text=_("El estudiante debe superar este problema antes de acceder al actual."),
    )

    # --- Enunciado y contexto ---
    enunciado = models.TextField(_("Enunciado del problema"))

    # --- Fase 1: Activación Cognitiva (Motor KST — evaluación silenciosa) ---
    activacion_cognitiva_json = models.JSONField(
        _("Activación cognitiva"),
        help_text=_(
            'JSON con la estructura: {"pregunta": "...", "opciones": ["A","B","C"], "correcta": "C"}'
        ),
    )
    # HTML/SVG del componente visual interactivo (vasos, chocolates, barras, etc.)
    # Administrable desde Django Admin con editor de texto enriquecido.
    visualizacion_html = models.TextField(
        _("HTML de visualización"),
        help_text=_("Fragmento HTML con el componente visual animado de la Fase 1."),
        blank=True,
    )

    # --- Datos EMT para el System Prompt de Gemini ---
    # {"Expectations": ["El alumno identifica que...", "Aplica la regla..."]}
    expectations_json = models.JSONField(
        _("Expectations (EMT)"),
        help_text=_('JSON: {"Expectations": ["Lo que el alumno debe deducir..."]}'),
    )
    # {"Misconceptions": [{"error": "...", "Seed_Question": "..."}, ...]}
    misconceptions_json = models.JSONField(
        _("Misconceptions (EMT)"),
        help_text=_(
            'JSON: {"Misconceptions": [{"error": "...", "Seed_Question": "Pregunta mayéutica..."}]}'
        ),
    )

    # --- Respuesta esperada (para validación de Motor KST) ---
    respuesta_correcta = models.CharField(
        _("Respuesta correcta"),
        max_length=200,
        help_text=_("Valor(es) aceptados como respuesta correcta, separados por coma."),
    )

    activo = models.BooleanField(_("Activo"), default=True)
    fecha_creacion = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)

    class Meta:
        verbose_name = _("Problema")
        verbose_name_plural = _("Problemas")
        ordering = ["tema", "nivel_kst"]

    def __str__(self) -> str:
        return f"[{self.get_tema_display()} — Nivel {self.nivel_kst}] {self.titulo}"

    @property
    def respuestas_aceptadas(self) -> list[str]:
        """Retorna la lista de respuestas aceptadas como strings normalizados."""
        return [r.strip().lower() for r in self.respuesta_correcta.split(",")]


# ---------------------------------------------------------------------------
# INTERACCIONES IA (ALIMENTA EL MOTOR KST)
# ---------------------------------------------------------------------------

class InteraccionIA(models.Model):
    """
    Registro de cada sesión de un estudiante con el Tutor Socrático.
    Es la tabla central que alimenta el Motor KST:
    guarda intentos, pistas (Seed Questions) entregadas y nivel alcanzado.
    """

    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interacciones",
        verbose_name=_("Estudiante"),
    )
    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name="interacciones",
        verbose_name=_("Clase"),
    )
    problema = models.ForeignKey(
        Problema,
        on_delete=models.CASCADE,
        related_name="interacciones",
        verbose_name=_("Problema"),
    )
    timestamp_inicio = models.DateTimeField(_("Inicio de sesión"), auto_now_add=True)
    timestamp_fin = models.DateTimeField(_("Fin de sesión"), null=True, blank=True)

    # Datos KST
    intentos = models.PositiveIntegerField(_("Intentos"), default=0)
    pistas_dadas = models.JSONField(
        _("Pistas dadas"),
        default=list,
        help_text=_("Lista de Seed_Questions entregadas durante la sesión."),
    )
    respondio_correctamente = models.BooleanField(
        _("Respondió correctamente"), default=False
    )
    fase_kst_alcanzada = models.PositiveIntegerField(
        _("Fase KST alcanzada"),
        default=1,
        help_text=_("Fase pedagógica máxima alcanzada (1-4)."),
    )

    # Historial completo del chat para contexto de Gemini
    historial_chat = models.JSONField(
        _("Historial del chat"),
        default=list,
        help_text=_('Lista de mensajes: [{"rol": "user"|"model", "texto": "..."}]'),
    )

    class Meta:
        verbose_name = _("Interacción IA")
        verbose_name_plural = _("Interacciones IA")
        ordering = ["-timestamp_inicio"]
        unique_together = [("estudiante", "problema")]  # Una sesión por problema

    def __str__(self) -> str:
        estado = "✓" if self.respondio_correctamente else "…"
        return f"{estado} {self.estudiante.email} | {self.problema.titulo} | {self.intentos} intentos"


# ---------------------------------------------------------------------------
# CIERRE METACOGNITIVO (FASE 4)
# ---------------------------------------------------------------------------

class DiarioMetacognitivo(models.Model):
    """
    Reflexión del estudiante al finalizar la sesión (Fase 4).
    Registra el aprendizaje declarativo y el análisis del error del compañero virtual.
    """

    interaccion = models.OneToOneField(
        InteraccionIA,
        on_delete=models.CASCADE,
        related_name="diario",
        verbose_name=_("Interacción"),
    )
    reflexion_texto = models.TextField(
        _("Reflexión"),
        help_text=_("¿Qué descubriste hoy sobre el tema?"),
    )
    analisis_error_texto = models.TextField(
        _("Análisis del error del compañero virtual"),
        blank=True,
        help_text=_("Explicación del error presentado en la Fase 4."),
    )
    timestamp = models.DateTimeField(_("Fecha de registro"), auto_now_add=True)

    class Meta:
        verbose_name = _("Diario Metacognitivo")
        verbose_name_plural = _("Diarios Metacognitivos")
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"Diario: {self.interaccion.estudiante.email} | {self.interaccion.problema.titulo}"


class EvaluacionIadov(models.Model):
    """
    Escala de satisfacción de Iadov (1-5 emojis).
    Mide el estado afectivo del estudiante al finalizar la sesión.
    """

    class Puntuacion(models.IntegerChoices):
        MUY_INSATISFECHO = 1, "😞 Muy insatisfecho"
        INSATISFECHO = 2, "😕 Insatisfecho"
        NEUTRAL = 3, "😐 Neutral"
        SATISFECHO = 4, "🙂 Satisfecho"
        MUY_SATISFECHO = 5, "🤩 Muy satisfecho"

    interaccion = models.OneToOneField(
        InteraccionIA,
        on_delete=models.CASCADE,
        related_name="iadov",
        verbose_name=_("Interacción"),
    )
    puntuacion = models.PositiveSmallIntegerField(
        _("Puntuación Iadov"),
        choices=Puntuacion.choices,
    )
    timestamp = models.DateTimeField(_("Fecha de registro"), auto_now_add=True)

    class Meta:
        verbose_name = _("Evaluación Iadov")
        verbose_name_plural = _("Evaluaciones Iadov")
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return (
            f"Iadov {self.puntuacion}/5 — "
            f"{self.interaccion.estudiante.email} | "
            f"{self.interaccion.problema.titulo}"
        )
