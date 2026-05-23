"""
NeuroMax — Vistas del Tutor Socrático y Motor KST
===================================================
Flujo pedagógico de 4 fases:
  Fase 1 — Activación Cognitiva (Motor KST silencioso: verifica prerrequisitos)
  Fase 2 — El Desafío (problema contextualizado)
  Fase 3 — Laboratorio Socrático (Chat con Gemini vía AJAX)
  Fase 4 — Cierre Metacognitivo (Diario + Iadov)

Registro:
  /registro/profesor/   → RegistroProfesorView
  /registro/estudiante/ → RegistroEstudianteView

Dashboard:
  /tutor/               → DashboardDocenteView
  /tutor/clase/<pk>/    → DetalleClaseView
  /tutor/problema/<pk>/ → TutorInteractivoView
  /tutor/chat/          → ChatAjaxView (endpoint AJAX)
  /tutor/guardar-cierre/<pk>/ → GuardarCierreView
"""

import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import CrearClaseForm, RegistroEstudianteForm, RegistroProfesorForm
from .models import (
    Clase,
    DiarioMetacognitivo,
    EvaluacionIadov,
    Inscripcion,
    InteraccionIA,
    PerfilUsuario,
    Problema,
)
from .services import get_tutor_service


# ---------------------------------------------------------------------------
# MIXINS DE ROL
# ---------------------------------------------------------------------------

class ProfesorRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restringe el acceso a usuarios con rol PROFESOR."""

    def test_func(self):
        return (
            hasattr(self.request.user, "perfil")
            and self.request.user.perfil.es_profesor
        )

    def handle_no_permission(self):
        messages.error(self.request, _("Acceso restringido a docentes."))
        return redirect("tutor:login_redirect")


class EstudianteRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restringe el acceso a usuarios con rol ESTUDIANTE."""

    def test_func(self):
        return (
            hasattr(self.request.user, "perfil")
            and self.request.user.perfil.es_estudiante
        )

    def handle_no_permission(self):
        messages.error(self.request, _("Acceso restringido a estudiantes."))
        return redirect("tutor:login_redirect")


# ---------------------------------------------------------------------------
# REGISTRO SEPARADO POR ROL
# ---------------------------------------------------------------------------

class RegistroProfesorView(View):
    """
    GET/POST /registro/profesor/
    Crea un User + PerfilUsuario(rol='PROFESOR') automáticamente.
    """

    template_name = "pages/registro_profesor.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("tutor:dashboard")
        return render(request, self.template_name, {"form": RegistroProfesorForm()})

    def post(self, request):
        form = RegistroProfesorForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(
                request,
                _("¡Bienvenido, Profesor! Tu cuenta ha sido creada. Crea tu primera clase."),
            )
            return redirect("tutor:dashboard")
        return render(request, self.template_name, {"form": form})


class RegistroEstudianteView(View):
    """
    GET/POST /registro/estudiante/
    Crea un User + PerfilUsuario(rol='ESTUDIANTE') e inscribe al estudiante
    en la Clase correspondiente al código ingresado.
    """

    template_name = "pages/registro_estudiante.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("tutor:mi_clase")
        codigo_url = request.GET.get("codigo", "")
        form = RegistroEstudianteForm(initial={"codigo_union": codigo_url})
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegistroEstudianteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(
                request,
                _("¡Bienvenido! Ya estás inscrito en tu clase. ¡A aprender!"),
            )
            return redirect("tutor:mi_clase")
        return render(request, self.template_name, {"form": form})


# ---------------------------------------------------------------------------
# REDIRECCIÓN SEGÚN ROL (POST-LOGIN)
# ---------------------------------------------------------------------------

class LoginRedirectView(LoginRequiredMixin, View):
    """Redirige al usuario al dashboard correcto según su rol."""

    def get(self, request):
        if not hasattr(request.user, "perfil"):
            messages.warning(request, _("Tu cuenta no tiene un perfil asignado."))
            return redirect("account_logout")
        if request.user.perfil.es_profesor:
            return redirect("tutor:dashboard")
        return redirect("tutor:mi_clase")


# ---------------------------------------------------------------------------
# DASHBOARD MULTI-CLASE DEL DOCENTE
# ---------------------------------------------------------------------------

class DashboardDocenteView(ProfesorRequeridoMixin, View):
    """
    GET  /tutor/
    Dashboard principal del docente: lista sus clases con métricas KST.
    POST /tutor/ → Crea una nueva Clase.
    """

    template_name = "pages/dashboard_docente.html"

    def get(self, request):
        clases = (
            Clase.objects.filter(profesor=request.user, activa=True)
            .annotate(
                num_estudiantes=Count("inscripciones", filter=Q(inscripciones__activa=True)),
                promedio_kst=Avg(
                    "interacciones__fase_kst_alcanzada",
                    filter=Q(interacciones__respondio_correctamente=True),
                ),
            )
            .order_by("-fecha_creacion")
        )

        # Estadísticas globales del profesor
        total_estudiantes = sum(c.num_estudiantes for c in clases)
        total_interacciones = InteraccionIA.objects.filter(clase__profesor=request.user).count()
        promedio_iadov = (
            EvaluacionIadov.objects.filter(interaccion__clase__profesor=request.user)
            .aggregate(prom=Avg("puntuacion"))["prom"]
        ) or 0

        context = {
            "clases": clases,
            "form_clase": CrearClaseForm(),
            "total_clases": clases.count(),
            "total_estudiantes": total_estudiantes,
            "total_interacciones": total_interacciones,
            "promedio_iadov": round(promedio_iadov, 1),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CrearClaseForm(request.POST)
        if form.is_valid():
            clase = form.save(commit=False)
            clase.profesor = request.user
            clase.save()
            messages.success(
                request,
                _(f"Clase «{clase.nombre}» creada. Código de unión: {clase.codigo_union}"),
            )
            return redirect("tutor:dashboard")
        # Re-renderizar con errores
        return self.get(request)


class DetalleClaseView(ProfesorRequeridoMixin, View):
    """
    GET /tutor/clase/<pk>/
    Vista detallada de una clase: lista de estudiantes con progreso KST individual.
    """

    template_name = "pages/detalle_clase.html"

    def get(self, request, pk):
        clase = get_object_or_404(Clase, pk=pk, profesor=request.user)

        inscripciones = (
            Inscripcion.objects.filter(clase=clase, activa=True)
            .select_related("estudiante", "estudiante__perfil")
        )

        # Enriquecer cada inscripción con datos KST del estudiante en esta clase
        estudiantes_data = []
        for ins in inscripciones:
            interacciones = InteraccionIA.objects.filter(
                estudiante=ins.estudiante, clase=clase
            )
            max_kst = interacciones.aggregate(max=Avg("fase_kst_alcanzada"))["max"] or 0
            resueltos = interacciones.filter(respondio_correctamente=True).count()
            iadov = (
                EvaluacionIadov.objects.filter(interaccion__estudiante=ins.estudiante, interaccion__clase=clase)
                .aggregate(prom=Avg("puntuacion"))["prom"]
            ) or None

            estudiantes_data.append({
                "inscripcion": ins,
                "interacciones": interacciones.count(),
                "problemas_resueltos": resueltos,
                "nivel_kst": round(max_kst, 1),
                "iadov_promedio": round(iadov, 1) if iadov else "—",
                "ultimo_acceso": interacciones.order_by("-timestamp_inicio").values_list(
                    "timestamp_inicio", flat=True
                ).first(),
            })

        # Distribución KST para gráfico
        distribucion_kst = [0, 0, 0, 0]
        for ed in estudiantes_data:
            nivel = int(ed["nivel_kst"])
            if 1 <= nivel <= 4:
                distribucion_kst[nivel - 1] += 1

        context = {
            "clase": clase,
            "estudiantes_data": estudiantes_data,
            "distribucion_kst": distribucion_kst,
            "problemas": Problema.objects.filter(activo=True).order_by("tema", "nivel_kst"),
        }
        return render(request, self.template_name, context)


# ---------------------------------------------------------------------------
# VISTA DEL ESTUDIANTE (MI CLASE)
# ---------------------------------------------------------------------------

class MiClaseView(EstudianteRequeridoMixin, View):
    """
    GET /tutor/mi-clase/
    Vista del estudiante: lista los problemas disponibles con su estado KST.
    """

    template_name = "pages/mi_clase.html"

    def get(self, request):
        # Obtener la clase activa del estudiante
        inscripcion = (
            Inscripcion.objects.filter(estudiante=request.user, activa=True)
            .select_related("clase")
            .first()
        )
        if not inscripcion:
            messages.warning(request, _("No estás inscrito en ninguna clase activa."))
            return redirect("tutor:registro_estudiante")

        clase = inscripcion.clase
        problemas = Problema.objects.filter(activo=True).order_by("tema", "nivel_kst")

        # Estado KST por problema para este estudiante
        interacciones_map = {
            ia.problema_id: ia
            for ia in InteraccionIA.objects.filter(
                estudiante=request.user, clase=clase
            ).select_related("problema")
        }

        problemas_data = []
        for problema in problemas:
            ia = interacciones_map.get(problema.pk)
            # Motor KST: verificar si el prerrequisito está aprobado
            prereq_ok = True
            if problema.prerequisito:
                prereq_ia = interacciones_map.get(problema.prerequisito_id)
                prereq_ok = prereq_ia is not None and prereq_ia.respondio_correctamente

            problemas_data.append({
                "problema": problema,
                "estado": _obtener_estado_kst(ia),
                "bloqueado": not prereq_ok,
                "interaccion": ia,
            })

        context = {
            "clase": clase,
            "problemas_data": problemas_data,
            "inscripcion": inscripcion,
        }
        return render(request, self.template_name, context)


def _obtener_estado_kst(interaccion: InteraccionIA | None) -> str:
    """Retorna el estado visual de un problema según la interacción del estudiante."""
    if interaccion is None:
        return "pendiente"
    if interaccion.respondio_correctamente:
        return "completado"
    if interaccion.intentos > 0:
        return "en_progreso"
    return "pendiente"


# ---------------------------------------------------------------------------
# TUTOR INTERACTIVO (4 FASES PEDAGÓGICAS)
# ---------------------------------------------------------------------------

class TutorInteractivoView(EstudianteRequeridoMixin, View):
    """
    GET /tutor/problema/<pk>/
    Renderiza el problema con el ciclo completo de 4 fases.

    Motor KST silencioso:
      Verifica si el prerrequisito está aprobado antes de permitir el acceso.
      Si no, redirige al prerrequisito con un mensaje informativo.
    """

    template_name = "pages/tutor_interactivo.html"

    def get(self, request, pk):
        problema = get_object_or_404(Problema, pk=pk, activo=True)

        # Obtener clase activa del estudiante
        inscripcion = get_object_or_404(
            Inscripcion, estudiante=request.user, activa=True
        )
        clase = inscripcion.clase

        # === MOTOR KST: VERIFICACIÓN SILENCIOSA DE PRERREQUISITOS ===
        if problema.prerequisito:
            prereq_aprobado = InteraccionIA.objects.filter(
                estudiante=request.user,
                clase=clase,
                problema=problema.prerequisito,
                respondio_correctamente=True,
            ).exists()

            if not prereq_aprobado:
                messages.warning(
                    request,
                    _(
                        f"Primero debes completar «{problema.prerequisito.titulo}» "
                        "para acceder a este problema."
                    ),
                )
                return redirect("tutor:tutor_interactivo", pk=problema.prerequisito.pk)
        # ============================================================

        # Obtener o crear la InteraccionIA para esta sesión
        interaccion, created = InteraccionIA.objects.get_or_create(
            estudiante=request.user,
            problema=problema,
            defaults={"clase": clase},
        )

        # Si ya fue resuelto, mostrar un mensaje pero permitir ver la resolución
        if interaccion.respondio_correctamente:
            messages.info(
                request,
                _(f"Estás viendo la resolución de «{problema.titulo}». Este ejercicio ya fue completado."),
            )

        import json as _json
        from .models import EvaluacionIadov

        # Preparar datos de activación cognitiva para el template
        activacion_raw = problema.activacion_cognitiva_json or {}
        activacion = {
            "pregunta": activacion_raw.get("pregunta", "¿Qué observas en este problema?"),
            "opciones": activacion_raw.get("opciones", []),
            "correcta": activacion_raw.get("correcta", ""),
            "feedback_correcto": activacion_raw.get("feedback_correcto", ""),
            "feedback_incorrecto": activacion_raw.get("feedback_incorrecto", ""),
        }

        video_mapping = {
            ("EXPONENCIACION", 1): "Exp_01_Peligro_Exponencial.mp4",
            ("EXPONENCIACION", 2): "Exp_02_Poder_de_los_Exponentes.mp4",
            ("EXPONENCIACION", 3): "Exp_03_Misterio_del_Exponente.mp4",
            ("EXPONENCIACION", 4): "Exp_04_Simplifica.mp4",
            ("FRACCIONES", 1): "Frac_01_Misterio_de_fracciones.mp4",
            ("FRACCIONES", 2): "Frac_02_Magia_con_Fracciones.mp4",
            ("FRACCIONES", 3): "Frac_03_El_enigma_de_la_lechuga.mp4",
            ("FRACCIONES", 4): "Frac_04_Fracciones_heterogéneas.mp4",
        }
        video_filename = video_mapping.get((problema.tema, problema.nivel_kst))

        context = {
            "problema": problema,
            "interaccion": interaccion,
            "clase": clase,
            "historial_json": json.dumps(interaccion.historial_chat, ensure_ascii=False),
            "activacion": activacion,
            "activacion_json": json.dumps(activacion, ensure_ascii=False),
            "iadov_choices": EvaluacionIadov.Puntuacion.choices,
            "video_filename": video_filename,
        }
        return render(request, self.template_name, context)


# ---------------------------------------------------------------------------
# ENDPOINT AJAX — CHAT CON GEMINI (FASE 3)
# ---------------------------------------------------------------------------

class ChatAjaxView(EstudianteRequeridoMixin, View):
    """
    POST /tutor/chat/
    Endpoint AJAX del chat socrático.

    Payload: {"problema_id": int, "respuesta": "texto del estudiante"}
    Response: {"tipo": "seed_question"|"correcto"|"guia", "mensaje": "..."}
    """

    def post(self, request):
        try:
            data = json.loads(request.body)
            problema_id = int(data["problema_id"])
            respuesta_estudiante = str(data["respuesta"]).strip()
        except (KeyError, ValueError, json.JSONDecodeError):
            return JsonResponse({"error": "Payload inválido"}, status=400)

        if not respuesta_estudiante:
            return JsonResponse({"error": "Respuesta vacía"}, status=400)

        problema = get_object_or_404(Problema, pk=problema_id, activo=True)
        inscripcion = get_object_or_404(Inscripcion, estudiante=request.user, activa=True)

        interaccion, created = InteraccionIA.objects.get_or_create(
            estudiante=request.user,
            problema=problema,
            defaults={"clase": inscripcion.clase},
        )

        # Llamada al Tutor Socrático (proveedor configurado en TUTOR_AI_PROVIDER)
        tutor = get_tutor_service()
        resultado = tutor.evaluar_respuesta(
            problema=problema,
            respuesta_estudiante=respuesta_estudiante,
            historial=interaccion.historial_chat,
        )

        # Actualizar historial en BD
        interaccion.historial_chat.append({"rol": "user", "texto": respuesta_estudiante})
        interaccion.historial_chat.append({"rol": "model", "texto": resultado["mensaje"]})
        interaccion.intentos += 1
        interaccion.fase_kst_alcanzada = max(interaccion.fase_kst_alcanzada, 3)

        # Registrar pista si fue una Seed Question
        if resultado["tipo"] == "seed_question" and resultado.get("seed_question"):
            interaccion.pistas_dadas.append(resultado["seed_question"])

        # Marcar como correcto si Gemini lo confirma
        if resultado["tipo"] == "correcto":
            interaccion.respondio_correctamente = True
            interaccion.timestamp_fin = timezone.now()
            interaccion.fase_kst_alcanzada = 3  # Llegó a Fase 3

        interaccion.save()

        return JsonResponse(resultado)


# ---------------------------------------------------------------------------
# GUARDAR CIERRE METACOGNITIVO (FASE 4)
# ---------------------------------------------------------------------------

class GuardarCierreView(EstudianteRequeridoMixin, View):
    """
    POST /tutor/guardar-cierre/<interaccion_pk>/
    Guarda el Diario Metacognitivo y la Evaluación Iadov al finalizar la sesión.
    """

    def post(self, request, pk):
        interaccion = get_object_or_404(
            InteraccionIA,
            pk=pk,
            estudiante=request.user,
            respondio_correctamente=True,
        )

        reflexion = request.POST.get("reflexion", "").strip()
        analisis_error = request.POST.get("analisis_error", "").strip()
        puntuacion_raw = request.POST.get("puntuacion", "")

        # Guardar diario
        if reflexion:
            DiarioMetacognitivo.objects.update_or_create(
                interaccion=interaccion,
                defaults={
                    "reflexion_texto": reflexion,
                    "analisis_error_texto": analisis_error,
                },
            )

        # Guardar Iadov
        try:
            puntuacion = int(puntuacion_raw)
            if 1 <= puntuacion <= 5:
                EvaluacionIadov.objects.update_or_create(
                    interaccion=interaccion,
                    defaults={"puntuacion": puntuacion},
                )
                # Actualizar fase KST al máximo (completó las 4 fases)
                interaccion.fase_kst_alcanzada = 4
                interaccion.save(update_fields=["fase_kst_alcanzada"])
        except (ValueError, TypeError):
            pass

        messages.success(
            request,
            _(
                f"¡Sesión completada! Has superado «{interaccion.problema.titulo}». "
                "Tu reflexión ha sido guardada."
            ),
        )
        return redirect("tutor:mi_clase")
