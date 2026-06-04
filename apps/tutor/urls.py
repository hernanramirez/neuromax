"""
NeuroMax — URLs del Tutor Socrático
=====================================
namespace: tutor
"""

from django.urls import path

from . import views

app_name = "tutor"

urlpatterns = [
    # --- Registro separado por rol ---
    path("registro/profesor/", views.RegistroProfesorView.as_view(), name="registro_profesor"),
    path("registro/estudiante/", views.RegistroEstudianteView.as_view(), name="registro_estudiante"),

    # --- Redirección post-login según rol ---
    path("inicio/", views.LoginRedirectView.as_view(), name="login_redirect"),

    # --- Dashboard del Docente (multi-clase) ---
    path("tutor/", views.DashboardDocenteView.as_view(), name="dashboard"),
    path("tutor/clase/<int:pk>/", views.DetalleClaseView.as_view(), name="detalle_clase"),
    path("tutor/clase/<int:pk>/csv/", views.ExportarClaseCSVView.as_view(), name="exportar_clase_csv"),

    # --- Espacio del Estudiante ---
    path("tutor/mi-clase/", views.MiClaseView.as_view(), name="mi_clase"),
    path("tutor/problema/<int:pk>/", views.TutorInteractivoView.as_view(), name="tutor_interactivo"),

    # --- AJAX: Chat con Gemini (Fase 3) ---
    path("tutor/chat/", views.ChatAjaxView.as_view(), name="chat_ajax"),

    # --- Guardar Cierre Metacognitivo (Fase 4) ---
    path("tutor/guardar-cierre/<int:pk>/", views.GuardarCierreView.as_view(), name="guardar_cierre"),
]
