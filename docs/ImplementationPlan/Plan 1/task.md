# NeuroMax — Task Tracker

## Paso 1: Modelos + Migraciones
- [x] Instalar `google-generativeai` via `uv add` → v0.8.6 instalado
- [x] Crear `apps/tutor/` como Django app
- [x] Crear `apps/tutor/models.py` con las 7 entidades (PerfilUsuario, Clase, Inscripcion, Problema, InteraccionIA, DiarioMetacognitivo, EvaluacionIadov)
- [x] Registrar app en `config/settings/base.py` + añadir `GEMINI_API_KEY`
- [x] Crear `apps/tutor/admin.py` con fieldsets, badges e inlines
- [x] Ejecutar `makemigrations` → `0001_initial.py` generado ✅

## Paso 2: Vistas + Motor KST
- [x] Crear `apps/tutor/forms.py` (RegistroProfesor, RegistroEstudiante, CrearClase)
- [x] Crear `apps/tutor/urls.py` con namespace `tutor`
- [x] Crear `apps/tutor/views.py` (Dashboard, DetalleClase, MiClase, TutorInteractivo, ChatAjax, GuardarCierre)
- [x] Registrar rutas en `config/urls.py`
- [x] `python manage.py check` → 0 errores ✅

## Paso 3: Servicio Gemini
- [x] Crear `apps/tutor/services.py`
- [x] Implementar `GeminiService` con EMT + Seed Questions
- [x] System Prompt 100% dinámico desde BD (cero hardcoding)
- [x] Fallback de emergencia cuando API no responde

## Paso 4: Templates Bootstrap
- [x] `pages/dashboard_docente.html` — Stats, grid de clases, código copiable, modal nueva clase
- [x] `pages/tutor_interactivo.html` — 4 fases: activación cognitiva, desafío, chat AJAX, Iadov
- [x] `pages/registro_profesor.html` — Fondo degradado púrpura, badge de rol
- [x] `pages/registro_estudiante.html` — Fondo degradado verde, campo código monoespaciado
- [x] `pages/detalle_clase.html` — Tabla de estudiantes con progreso KST, gráfico de distribución
- [x] `pages/mi_clase.html` — Cards por tema con estado KST (bloqueado/pendiente/en progreso/completado)
- [x] `python manage.py check` → 0 issues ✅

## Paso 5: Seed de Prueba COSAFAM
- [x] Crear `apps/tutor/management/__init__.py`
- [x] Crear `apps/tutor/management/commands/__init__.py`
- [x] Crear `apps/tutor/management/commands/seed_pruebas.py`
  - 33 usuarios (1 profesor + 32 estudiantes)
  - 1 clase con código fijo `COSAFAM1`
  - 8 problemas EMT completos: FR-1→FR-2→FR-3→FR-4 + EX-1→EX-2→EX-3→EX-4
  - Soporte `--reset` para limpiar y re-sembrar
- [x] `python manage.py check` → 0 issues ✅

## 🎉 PROYECTO COMPLETO
Ejecutar para poblar la BD: `python manage.py seed_pruebas`
Re-sembrar limpio: `python manage.py seed_pruebas --reset`
