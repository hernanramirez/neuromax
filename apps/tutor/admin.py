"""
NeuroMax — Admin para el Tutor Socrático.
Configuración del panel Django Admin para gestionar todos los modelos pedagógicos.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    Clase,
    DiarioMetacognitivo,
    EvaluacionIadov,
    Inscripcion,
    InteraccionIA,
    PerfilUsuario,
    Problema,
)


# ---------------------------------------------------------------------------
# PERFIL DE USUARIO
# ---------------------------------------------------------------------------

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ["user", "nombre_completo", "rol", "institucion"]
    list_filter = ["rol", "institucion"]
    search_fields = ["user__email", "nombre_completo"]
    list_select_related = ["user"]


# ---------------------------------------------------------------------------
# CLASES
# ---------------------------------------------------------------------------

class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    fields = ["estudiante", "fecha_ingreso", "activa"]
    readonly_fields = ["fecha_ingreso"]
    autocomplete_fields = ["estudiante"]


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ["nombre", "profesor", "codigo_union_badge", "total_estudiantes", "activa", "fecha_creacion"]
    list_filter = ["activa", "fecha_creacion"]
    search_fields = ["nombre", "codigo_union", "profesor__email"]
    readonly_fields = ["codigo_union", "fecha_creacion"]
    inlines = [InscripcionInline]
    list_select_related = ["profesor"]

    @admin.display(description=_("Código"))
    def codigo_union_badge(self, obj):
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:4px;font-family:monospace">{}</span>',
            obj.codigo_union,
        )

    @admin.display(description=_("Estudiantes"))
    def total_estudiantes(self, obj):
        return obj.total_estudiantes

    fieldsets = (
        (_("Información de la Clase"), {
            "fields": ("nombre", "descripcion", "profesor", "activa"),
        }),
        (_("Acceso"), {
            "fields": ("codigo_union",),
            "description": _("El código se genera automáticamente al crear la clase."),
        }),
        (_("Fechas"), {
            "fields": ("fecha_creacion",),
        }),
    )


# ---------------------------------------------------------------------------
# PROBLEMAS (CONTENIDO PEDAGÓGICO)
# ---------------------------------------------------------------------------

@admin.register(Problema)
class ProblemaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "tema", "nivel_kst", "prerequisito", "activo", "fecha_creacion"]
    list_filter = ["tema", "nivel_kst", "activo"]
    search_fields = ["titulo", "enunciado"]
    readonly_fields = ["fecha_creacion"]
    list_select_related = ["prerequisito"]

    fieldsets = (
        (_("Identificación y KST"), {
            "fields": ("titulo", "tema", "nivel_kst", "prerequisito", "activo"),
        }),
        (_("Enunciado"), {
            "fields": ("enunciado",),
        }),
        (_("Fase 1 — Activación Cognitiva"), {
            "fields": ("activacion_cognitiva_json", "visualizacion_html"),
            "description": _("Componente visual y pregunta de activación previa al problema principal."),
        }),
        (_("Datos EMT para Gemini"), {
            "fields": ("expectations_json", "misconceptions_json", "respuesta_correcta"),
            "description": _(
                "Expectations: lo que el alumno debe deducir. "
                "Misconceptions: errores esperados con su Seed_Question (pregunta mayéutica)."
            ),
        }),
        (_("Metadatos"), {
            "fields": ("fecha_creacion",),
        }),
    )


# ---------------------------------------------------------------------------
# INTERACCIONES IA
# ---------------------------------------------------------------------------

@admin.register(InteraccionIA)
class InteraccionIAAdmin(admin.ModelAdmin):
    list_display = [
        "estudiante", "problema", "clase", "intentos",
        "respondio_correctamente", "fase_kst_alcanzada", "timestamp_inicio",
    ]
    list_filter = ["respondio_correctamente", "fase_kst_alcanzada", "problema__tema"]
    search_fields = ["estudiante__email", "problema__titulo", "clase__nombre"]
    readonly_fields = ["timestamp_inicio", "timestamp_fin", "historial_chat", "pistas_dadas"]
    list_select_related = ["estudiante", "problema", "clase"]

    def has_add_permission(self, request):
        return False  # Las interacciones se crean solo via la plataforma


# ---------------------------------------------------------------------------
# CIERRE METACOGNITIVO
# ---------------------------------------------------------------------------

@admin.register(DiarioMetacognitivo)
class DiarioMetacognitivoAdmin(admin.ModelAdmin):
    list_display = ["get_estudiante", "get_problema", "timestamp"]
    search_fields = ["interaccion__estudiante__email", "interaccion__problema__titulo"]
    readonly_fields = ["timestamp"]
    list_select_related = ["interaccion__estudiante", "interaccion__problema"]

    @admin.display(description=_("Estudiante"))
    def get_estudiante(self, obj):
        return obj.interaccion.estudiante.email

    @admin.display(description=_("Problema"))
    def get_problema(self, obj):
        return obj.interaccion.problema.titulo


@admin.register(EvaluacionIadov)
class EvaluacionIadovAdmin(admin.ModelAdmin):
    list_display = ["get_estudiante", "get_problema", "puntuacion_display", "timestamp"]
    list_filter = ["puntuacion"]
    readonly_fields = ["timestamp"]
    list_select_related = ["interaccion__estudiante", "interaccion__problema"]

    @admin.display(description=_("Estudiante"))
    def get_estudiante(self, obj):
        return obj.interaccion.estudiante.email

    @admin.display(description=_("Problema"))
    def get_problema(self, obj):
        return obj.interaccion.problema.titulo

    @admin.display(description=_("Satisfacción"))
    def puntuacion_display(self, obj):
        emojis = {1: "😞", 2: "😕", 3: "😐", 4: "🙂", 5: "🤩"}
        return format_html("{} {}/5", emojis.get(obj.puntuacion, "?"), obj.puntuacion)
