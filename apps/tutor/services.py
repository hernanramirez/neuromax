"""
NeuroMax — Servicio de IA Multi-Proveedor: Tutor Socrático con Metodología EMT
================================================================================
Proveedores soportados:
  - groq    : Llama 3.3 70B (GRATUITO, recomendado para uso educativo)
  - gemini  : Gemini 2.0 Flash (requiere plan de pago o cuota activa)

Selección via settings.TUTOR_AI_PROVIDER ("groq" | "gemini").

El System Prompt se construye dinámicamente desde la BD — cero hardcoding.
"""

import json
import logging
import warnings

logger = logging.getLogger(__name__)


# ── System Prompt base compartido por todos los proveedores ──────────────────

SYSTEM_PROMPT_TEMPLATE = """Eres un Tutor Socrático experto en neuroeducación para estudiantes de \
1er Año de Bachillerato del Colegio Sagrada Familia (COSAFAM, Ecuador).
Tu misión es guiar al estudiante para que construya el conocimiento por sí mismo, \
aplicando la metodología EMT (Expectativa-Malentendido).

## PROBLEMA ACTUAL
Título: {titulo}
Tema: {tema}
Enunciado: {enunciado}

## EXPECTATIONS (lo que el alumno debe deducir/comprender)
{expectations}

## MISCONCEPTIONS (errores frecuentes + pregunta mayéutica)
{misconceptions}

## REGLAS ESTRICTAS
1. NUNCA revelar la respuesta directamente.
2. Si la respuesta coincide con un Misconception → usa su Seed_Question para provocar disonancia cognitiva.
3. Si la respuesta es correcta → confirmar con entusiasmo (tipo: "correcto").
4. SIEMPRE responder en español, tono amigable y motivador.
5. Responde ÚNICAMENTE con el siguiente JSON (sin markdown, sin texto extra):

{{"tipo": "seed_question" | "correcto" | "guia", "mensaje": "<texto>", "seed_question": "<solo si tipo==seed_question>"}}"""


def _construir_system_prompt(problema) -> str:
    """Construye el system prompt EMT desde los campos JSON del modelo Problema."""
    expectations = "\n".join(
        f"- {e}" for e in problema.expectations_json.get("Expectations", [])
    )
    misconceptions = "\n".join(
        f"- Error: {m.get('error','')}\n  Seed_Question: {m.get('Seed_Question','')}"
        for m in problema.misconceptions_json.get("Misconceptions", [])
    )
    return SYSTEM_PROMPT_TEMPLATE.format(
        titulo=problema.titulo,
        tema=problema.get_tema_display(),
        enunciado=problema.enunciado,
        expectations=expectations or "(no especificadas)",
        misconceptions=misconceptions or "(no especificados)",
    )


def _parsear_json_respuesta(raw: str) -> dict:
    """Extrae el JSON de la respuesta del modelo, limpiando markdown si existe."""
    texto = raw.strip()
    if texto.startswith("```"):
        lineas = texto.split("\n")
        texto = "\n".join(lineas[1:-1])
    try:
        data = json.loads(texto)
        return {
            "tipo": data.get("tipo", "guia"),
            "mensaje": data.get("mensaje", "¿Puedes explicar tu razonamiento con más detalle?"),
            "seed_question": data.get("seed_question", ""),
        }
    except (json.JSONDecodeError, AttributeError) as exc:
        logger.warning("JSON inválido del modelo: %s | raw: %.200s", exc, raw)
        return {
            "tipo": "guia",
            "mensaje": "Interesante. Describe paso a paso tu razonamiento. ¿Por dónde empezarías?",
            "seed_question": "",
        }


FALLBACK = {
    "tipo": "guia",
    "mensaje": (
        "El tutor está tomando un respiro ☕. "
        "Mientras tanto, relee el enunciado e intenta describir tu razonamiento paso a paso."
    ),
    "seed_question": "",
}


# ── Proveedor GROQ (Llama 3.3 70B) ──────────────────────────────────────────

class GroqService:
    """
    Tutor Socrático usando Groq + Llama 3.3 70B.
    Gratuito para proyectos educativos — https://console.groq.com
    Rate limit generoso: 6.000 req/min, 500.000 tokens/día.
    """

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        from groq import Groq
        self.client = Groq(api_key=api_key)
        self.model = model

    def evaluar_respuesta(self, problema, respuesta_estudiante: str, historial: list) -> dict:
        system_prompt = _construir_system_prompt(problema)

        # Convertir historial interno al formato OpenAI/Groq
        messages = [{"role": "system", "content": system_prompt}]
        for msg in historial:
            rol = "user" if msg.get("rol") == "user" else "assistant"
            messages.append({"role": rol, "content": msg.get("texto", "")})
        messages.append({"role": "user", "content": respuesta_estudiante})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.4,
                max_tokens=512,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or ""
            return _parsear_json_respuesta(raw)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Error en GroqService.evaluar_respuesta: %s", exc)
            return FALLBACK


# ── Proveedor GEMINI ─────────────────────────────────────────────────────────

class GeminiService:
    """
    Tutor Socrático usando Google Gemini 2.0 Flash.
    Requiere cuota activa o plan de pago en Google AI Studio.
    """

    MODEL_NAME = "gemini-2.0-flash"

    def __init__(self, api_key: str):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=self.MODEL_NAME,
            generation_config=genai.GenerationConfig(
                temperature=0.4,
                top_p=0.85,
                max_output_tokens=512,
                response_mime_type="application/json",
            ),
        )

    def evaluar_respuesta(self, problema, respuesta_estudiante: str, historial: list) -> dict:
        system_prompt = _construir_system_prompt(problema)

        # Convertir historial al formato Gemini
        gemini_history = []
        for msg in historial:
            gemini_history.append({
                "role": msg.get("rol", "user"),
                "parts": [msg.get("texto", "")],
            })

        prompt_completo = (
            f"SYSTEM:\n{system_prompt}\n\n"
            f"Respuesta del estudiante: \"{respuesta_estudiante}\"\n"
            "Responde SOLO con el JSON indicado."
        )

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", FutureWarning)
                import google.generativeai as genai  # noqa: F811
            chat = self.model.start_chat(history=gemini_history)
            response = chat.send_message(prompt_completo)
            return _parsear_json_respuesta(response.text)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Error en GeminiService.evaluar_respuesta: %s", exc)
            return FALLBACK


# ── FACTORY: selecciona el proveedor según settings ──────────────────────────

def get_tutor_service():
    """
    Retorna la instancia del servicio de IA configurado en settings.TUTOR_AI_PROVIDER.

    Uso en views.py:
        from .services import get_tutor_service
        tutor = get_tutor_service()
        resultado = tutor.evaluar_respuesta(problema, respuesta, historial)
    """
    from django.conf import settings

    provider = getattr(settings, "TUTOR_AI_PROVIDER", "groq").lower()

    if provider == "groq":
        api_key = getattr(settings, "GROQ_API_KEY", "")
        model = getattr(settings, "GROQ_MODEL", "llama-3.3-70b-versatile")
        if not api_key:
            logger.error(
                "GROQ_API_KEY no configurada. Obtén tu clave gratuita en https://console.groq.com"
            )
            return _DummyService()
        return GroqService(api_key=api_key, model=model)

    if provider == "gemini":
        api_key = getattr(settings, "GEMINI_API_KEY", "")
        if not api_key:
            logger.error("GEMINI_API_KEY no configurada.")
            return _DummyService()
        return GeminiService(api_key=api_key)

    logger.error("TUTOR_AI_PROVIDER='%s' no reconocido. Usa 'groq' o 'gemini'.", provider)
    return _DummyService()


class _DummyService:
    """Servicio nulo que activa cuando no hay API key — evita crashes en desarrollo."""

    def evaluar_respuesta(self, problema, respuesta_estudiante: str, historial: list) -> dict:
        return {
            "tipo": "guia",
            "mensaje": (
                "⚠️ El tutor no está configurado. "
                "Agrega GROQ_API_KEY en tu archivo .env (obtén una gratis en console.groq.com)."
            ),
            "seed_question": "",
        }
