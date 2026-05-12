"""
NeuroMax — Formularios del Tutor Socrático
==========================================
Formularios para registro de Profesor/Estudiante y gestión de Clases.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Clase, PerfilUsuario

User = get_user_model()


# ---------------------------------------------------------------------------
# REGISTRO DE PROFESOR
# ---------------------------------------------------------------------------

class RegistroProfesorForm(forms.Form):
    """Formulario de registro para docentes. El rol se asigna automáticamente."""

    nombre_completo = forms.CharField(
        label=_("Nombre completo"),
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Ej: Prof. Hernán Ramírez"),
            "autocomplete": "name",
        }),
    )
    email = forms.EmailField(
        label=_("Correo electrónico institucional"),
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "profesor@cosafam.edu.ec",
            "autocomplete": "email",
        }),
    )
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "autocomplete": "new-password",
        }),
    )
    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "autocomplete": "new-password",
        }),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Este correo ya está registrado."))
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError({"password2": _("Las contraseñas no coinciden.")})
        return cleaned

    def save(self) -> User:
        data = self.cleaned_data
        user = User.objects.create_user(
            email=data["email"],
            password=data["password1"],
            name=data["nombre_completo"],
        )
        PerfilUsuario.objects.create(
            user=user,
            rol=PerfilUsuario.Rol.PROFESOR,
            nombre_completo=data["nombre_completo"],
        )
        return user


# ---------------------------------------------------------------------------
# REGISTRO DE ESTUDIANTE
# ---------------------------------------------------------------------------

class RegistroEstudianteForm(forms.Form):
    """
    Formulario de registro para estudiantes.
    Incluye el campo `codigo_union` para vincularse a una Clase.
    """

    nombre_completo = forms.CharField(
        label=_("Nombre completo"),
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Ej: Ana Sofía Pérez"),
            "autocomplete": "name",
        }),
    )
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "estudiante@cosafam.edu.ec",
            "autocomplete": "email",
        }),
    )
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "autocomplete": "new-password",
        }),
    )
    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "autocomplete": "new-password",
        }),
    )
    codigo_union = forms.CharField(
        label=_("Código de clase"),
        max_length=8,
        widget=forms.TextInput(attrs={
            "class": "form-control text-uppercase",
            "placeholder": _("Ej: COSAFAM1"),
            "autocomplete": "off",
            "style": "letter-spacing: 0.15em; font-family: monospace; font-size: 1.1rem;",
        }),
        help_text=_("El código lo proporciona tu profesor/a."),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Este correo ya está registrado."))
        return email

    def clean_codigo_union(self):
        codigo = self.cleaned_data["codigo_union"].strip().upper()
        try:
            self._clase = Clase.objects.get(codigo_union=codigo, activa=True)
        except Clase.DoesNotExist:
            raise ValidationError(_("El código de clase no es válido o la clase está inactiva."))
        return codigo

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError({"password2": _("Las contraseñas no coinciden.")})
        return cleaned

    def save(self) -> User:
        from .models import Inscripcion
        data = self.cleaned_data
        user = User.objects.create_user(
            email=data["email"],
            password=data["password1"],
            name=data["nombre_completo"],
        )
        PerfilUsuario.objects.create(
            user=user,
            rol=PerfilUsuario.Rol.ESTUDIANTE,
            nombre_completo=data["nombre_completo"],
        )
        # Inscribir al estudiante en la clase
        Inscripcion.objects.create(estudiante=user, clase=self._clase)
        return user


# ---------------------------------------------------------------------------
# CREACIÓN DE CLASE (DASHBOARD DOCENTE)
# ---------------------------------------------------------------------------

class CrearClaseForm(forms.ModelForm):
    """Formulario para que el profesor cree una nueva Clase."""

    class Meta:
        model = Clase
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Ej: 1er Año de Bachillerato A — COSAFAM 2026"),
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": _("Descripción opcional del grupo..."),
            }),
        }
        labels = {
            "nombre": _("Nombre de la clase"),
            "descripcion": _("Descripción"),
        }
