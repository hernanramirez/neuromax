# NeuroMax: Plataforma Neurodidáctica en Django
## Contexto Institucional
**Institución:** Colegio Sagrada Familia — COSAFAM  
**Nivel educativo objetivo:** 1er Año de Bachillerato  
**Asignaturas cubiertas:** Matemáticas — Fracciones y Exponenciación

## Descripción del Proyecto

Construcción de una aplicación EdTech sobre la base Django existente (cookie-cutter), integando dos motores pedagógicos: el **Motor KST** (Knowledge Space Theory) para mapear la frontera de conocimiento del estudiante, y el **Tutor Socrático powered by Gemini** que aplica la metodología EMT (Expectativa-Malentendido). El sistema soporta múltiples clases por docente (multi-tenant a nivel de profesor).

Los demos en `docs/CodeDemo/` (fracciones.html, fracciones2.html) definen el patrón de 4 fases pedagógicas que replicaremos en Django:
- **Fase 1 — Activación Cognitiva:** Prerrequisito visual con feedback inmediato (Motor KST)
- **Fase 2 — El Desafío:** Problema contextualizado con representación visual (Codificación Dual)
- **Fase 3 — Laboratorio Socrático:** Chat con Gemini usando EMT (API Gemini)
- **Fase 4 — Cierre Metacognitivo:** Diario + Escala de Iadov

---

## Arquitectura General

```
neuromax/
├── apps/
│   ├── tutor/              # [NEW] App principal pedagógica
│   │   ├── models.py       # Entidades KST + Interacciones
│   │   ├── views.py        # Dashboard Docente + Vistas Estudiante
│   │   ├── services.py     # Integración API Gemini (EMT)
│   │   ├── urls.py         # Rutas de la app
│   │   ├── admin.py        # Panel de administración
│   │   ├── migrations/
│   │   └── management/
│   │       └── commands/
│   │           └── seed_pruebas.py   # [NEW] Datos de prueba
│   ├── templates/
│   │   └── pages/
│   │       ├── dashboard_docente.html    # [NEW]
│   │       └── tutor_interactivo.html   # [NEW]
│   └── users/              # [EXISTING] User model via allauth
├── config/
│   └── urls.py             # [MODIFY] Incluir rutas de tutor
└── pyproject.toml          # [MODIFY] Añadir google-generativeai
```

---

## User Review Required

> [!NOTE]
> El modelo `User` existente usa **email como USERNAME_FIELD** (sin `username`), autenticado via django-allauth. El rol se asignará automáticamente por la URL de registro utilizada (`/registro/profesor/` o `/registro/estudiante/`), no requiere selección manual del usuario.

> [!NOTE]
> `GEMINI_API_KEY` confirmada en `.env` ✅


## Decisiones de Diseño — Confirmadas ✅

| # | Decisión | Definición |
|---|----------|------------|
| 1 | **Flujo de registro** | **Registros separados**: `/registro/profesor/` y `/registro/estudiante/`. Cada URL usa su propio formulario y adaptador de allauth. El campo `rol` en `PerfilUsuario` se asigna automáticamente según la URL usada al registrarse. |
| 2 | **Contenido pedagógico** | **100% en base de datos** — Política estricta de cero hardcoding. Los enunciados, `Expectations`, `Misconceptions` y `Seed_Questions` se administran únicamente desde Django Admin. Los demos de `docs/CodeDemo/` son la referencia de diseño, pero su contenido se migra como fixtures al modelo `Problema`. |
| 3 | **SDK de Gemini** | **`google-generativeai`** (SDK clásico) — se instala vía `uv add google-generativeai`. |

> [!NOTE]
> `GEMINI_API_KEY` confirmada en `.env` ✅ — lista para el Paso 3.

---

## Impacto en la Arquitectura por las Decisiones

### Registro Separado (Decisión 1)

Se añaden dos URLs y dos vistas al módulo `tutor`:
- `GET/POST /registro/profesor/` → `RegistroProfesorView` → crea `User` + `PerfilUsuario(rol='PROFESOR')`
- `GET/POST /registro/estudiante/` → `RegistroEstudianteView` → crea `User` + `PerfilUsuario(rol='ESTUDIANTE')` + solicita `codigo_union` para unirse a una `Clase`

### Cero Hardcoding (Decisión 2)

El campo `VisualizacionHTML` se agrega al modelo `Problema`:
```python
class Problema(models.Model):
    ...
    # Componente visual de la Fase 1 (Activación Cognitiva) en HTML puro
    # Administrable desde Django Admin con un editor de texto enriquecido
    visualizacion_html = models.TextField(
        help_text="HTML del componente visual interactivo (vasos, chocolates, etc.)"
    )
    # Alternativa de activación cognitiva: pregunta y opciones en JSON
    activacion_cognitiva_json = models.JSONField(
        help_text='Ej: {"pregunta": "...", "opciones": [...], "correcta": "iguales"}'
    )
```
Esto garantiza que **todo** el contenido (incluidas las animaciones de los demos) sea editable sin tocar código.

---

## Proposed Changes

### Paso 1: Modelos de Base de Datos (`models.py`)

#### [MODIFY] `pyproject.toml`
- Añadir `google-generativeai` a las dependencias del proyecto.

#### [NEW] `apps/tutor/` — Django App completa

#### [NEW] `apps/tutor/models.py`

Entidades a crear:

```python
# Perfil que extiende al User base (OneToOne)
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    rol = models.CharField(choices=[('PROFESOR','Profesor'),('ESTUDIANTE','Estudiante')])
    avatar_url = models.URLField(blank=True)

# Docente administra múltiples clases (multi-tenant)
class Clase(models.Model):
    profesor = models.ForeignKey(User, related_name='clases')
    nombre = models.CharField(max_length=100)         # "5to Año A - 2026"
    codigo_union = models.CharField(unique=True, max_length=8)  # Auto-generado, ej: "XK9P2R"
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

# Estudiante pertenece a una Clase
class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    clase = models.ForeignKey(Clase, related_name='estudiantes', null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

# Contenido pedagógico (Problema + EMT data para Gemini)
class Problema(models.Model):
    titulo = models.CharField(max_length=200)
    tema = models.CharField(max_length=100)           # "Fracciones - División"
    nivel_kst = models.PositiveIntegerField(default=1) # Nivel en la jerarquía KST
    enunciado = models.TextField()
    # Datos EMT para el System Prompt de Gemini (almacenados como JSON)
    expectations_json = models.JSONField()    # {"Expectations": [...]}
    misconceptions_json = models.JSONField()  # {"Misconceptions": [...]}
    respuesta_correcta = models.CharField(max_length=100)
    # Metadatos para el Motor KST
    prerequisito = models.ForeignKey('self', null=True, blank=True, on_delete=SET_NULL)

# Registro de cada interacción IA (alimenta el Motor KST)
class InteraccionIA(models.Model):
    estudiante = models.ForeignKey(User, on_delete=CASCADE)
    clase = models.ForeignKey(Clase, on_delete=CASCADE)
    problema = models.ForeignKey(Problema, on_delete=CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    intentos = models.PositiveIntegerField(default=0)
    pistas_dadas = models.JSONField(default=list)     # Lista de Seed_Questions entregadas
    respondio_correctamente = models.BooleanField(default=False)
    fase_kst_alcanzada = models.PositiveIntegerField(default=1)

# Diario Metacognitivo (Fase 4 del ciclo pedagógico)
class DiarioMetacognitivo(models.Model):
    interaccion = models.OneToOneField(InteraccionIA, on_delete=CASCADE)
    reflexion_texto = models.TextField()              # "¿Qué descubriste hoy?"
    analisis_error_texto = models.TextField(blank=True)  # Explicación del error del compañero virtual

# Evaluación de Iadov (Satisfacción del estudiante - Fase 4)
class EvaluacionIadov(models.Model):
    ESCALA = [(1,'😞'),(2,'😕'),(3,'😐'),(4,'🙂'),(5,'🤩')]
    interaccion = models.OneToOneField(InteraccionIA, on_delete=CASCADE)
    puntuacion = models.PositiveSmallIntegerField(choices=ESCALA)
    timestamp = models.DateTimeField(auto_now_add=True)
```

---

### Paso 2: Lógica del Motor KST y Vistas (`views.py`)

#### [NEW] `apps/tutor/views.py`

**Vista: `DashboardDocenteView`** → `apps/templates/pages/dashboard_docente.html`
- Lista las clases del profesor autenticado (`Clase.objects.filter(profesor=request.user)`)
- Para cada clase: nombre, código de unión, cantidad de estudiantes, progreso KST agregado
- Permite crear nueva clase y ver detalle de clase individual

**Vista: `DetalleClaseView`** → reutiliza `dashboard_docente.html` con sección de detalle
- Tabla de estudiantes con columnas: Nombre, Nivel KST, Último intento, Iadov promedio
- Gráfico de distribución de fases KST del grupo (via `InteraccionIA`)

**Vista: `TutorInteractivoView`** → `apps/templates/pages/tutor_interactivo.html`
- **Motor KST silencioso:** Verifica si el estudiante aprobó los prerrequisitos (`InteraccionIA.respondio_correctamente` del problema padre). Si no, redirige a la Fase 1 del prerrequisito.
- Renderiza el problema y el contexto EMT via `context['problema']`
- Recibe `POST` desde el chat → llama a `GeminiService` → retorna JSON con respuesta del tutor

**Vista: `ChatAjaxView`** → endpoint AJAX `/tutor/chat/` (retorna JSON)
- Recibe respuesta del estudiante
- Llama a `GeminiService.evaluar_respuesta()`
- Actualiza `InteraccionIA` (intentos, pistas)
- Retorna `{"tipo": "seed_question" | "correcto" | "guia", "mensaje": "..."}`

---

### Paso 3: Servicio Gemini (`services.py`)

#### [NEW] `apps/tutor/services.py`

```python
# Estructura del System Prompt (JSON estricto)
SYSTEM_PROMPT_TEMPLATE = {
    "Rol": "Eres un Tutor Socrático...",
    "Metodologia": "EMT (Expectativa-Malentendido)...",
    "Reglas": ["No dar respuestas directas", "Generar disonancia cognitiva"],
    "Expectations": [],      # Se inyecta desde Problema.expectations_json
    "Misconceptions": [],    # Se inyecta desde Problema.misconceptions_json
    "Formato_Respuesta": {
        "tipo": "seed_question | correcto | guia",
        "Seed_Question": "...",  # Solo si tipo == seed_question
        "mensaje": "..."
    }
}

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def evaluar_respuesta(self, problema: Problema, respuesta_estudiante: str, historial: list) -> dict:
        """
        1. Construye el system_prompt con EMT data del Problema
        2. Envía historial + respuesta al modelo
        3. Si detecta Misconception → genera Seed_Question (pregunta mayéutica)
        4. Si detecta match con Expectations → tipo='correcto'
        5. Retorna dict con tipo + mensaje
        """
        system_prompt = self._build_system_prompt(problema)
        # ... llamada a API con chat history
        return self._parse_response(raw_response)
```

---

### Paso 4: Templates HTML con Bootstrap

#### [NEW] `apps/templates/pages/dashboard_docente.html`
- Extiende `layout_vertical.html` (usa la barra lateral y topbar del admin existente)
- **Sección superior:** Stats cards (Total clases, Total estudiantes, Promedio KST, Iadov promedio)
- **Cuerpo:** Grid de tarjetas Bootstrap (`card`) por cada `Clase`, con:
  - Nombre de clase + badge de código de unión (copyable)
  - Barra de progreso KST del grupo
  - Botón "Ver Detalle" y "Nuevo Problema"
- **Modal:** Formulario para crear nueva `Clase`

#### [NEW] `apps/templates/pages/tutor_interactivo.html`
- Extiende `layout_vertical.html`
- **Columna izquierda (7 cols):** Panel del problema visual (replica estética de los demos con animaciones CSS dentro del template Django)
  - Fase 1 (Activación Cognitiva): componente visual interactivo
  - Fase 2 (El Desafío): enunciado del problema desde `{{ problema.enunciado }}`
- **Columna derecha (5 cols):** Chat del Tutor Socrático
  - Header verde con avatar 🤖 y status "Online"
  - Ventana de mensajes con scroll
  - Input + botón enviar → AJAX `POST` a `/tutor/chat/`
- **Fase 4** (oculta, aparece al resolver): Diario + Escala Iadov con formulario POST

---

## Verification Plan

### Automated Tests
- `python manage.py makemigrations tutor && python manage.py migrate`
- `python manage.py test apps.tutor` — Tests unitarios para `GeminiService._build_system_prompt()`
- Verificar admin: `python manage.py createsuperuser` → ingresar al panel y crear `Clase` + `Problema`

### Manual Verification
1. Registrar usuario Profesor → crear Clase → compartir código
2. Registrar usuario Estudiante → unirse a Clase con código
3. Ingresar a `tutor_interactivo` → verificar que Motor KST bloquea sin prerrequisitos
4. Interactuar con el chat → verificar Seed Question con un Misconception
5. Completar Fase 4 → verificar que `DiarioMetacognitivo` e `InteraccionIA` se guardan en DB

---

### Paso 5: Datos de Prueba Cerrada (`seed_pruebas`)

#### [NEW] `apps/tutor/management/commands/seed_pruebas.py`

Comando Django: `python manage.py seed_pruebas`

Pobla la base de datos con un conjunto de datos reproducible para pruebas cerradas de la aplicación completa.

---

#### 👤 Usuarios de Prueba

| Rol | Email | Contraseña | Nombre |
|-----|-------|-----------|--------|
| Profesor | `profesor@cosafam.test` | `Cosafam2026!` | Prof. Hernán Ramírez |
| Estudiante 01 | `estudiante01@cosafam.test` | `Est01-2026!` | Ana Sofía Pérez |
| Estudiante 02 | `estudiante02@cosafam.test` | `Est02-2026!` | Carlos Mendoza |
| Estudiante 03 | `estudiante03@cosafam.test` | `Est03-2026!` | Valentina Ruiz |
| Estudiante 04 | `estudiante04@cosafam.test` | `Est04-2026!` | Diego Fuentes |
| Estudiante 05 | `estudiante05@cosafam.test` | `Est05-2026!` | Isabella Torres |
| Estudiante 06 | `estudiante06@cosafam.test` | `Est06-2026!` | Mateo García |
| Estudiante 07 | `estudiante07@cosafam.test` | `Est07-2026!` | Luciana Castro |
| Estudiante 08 | `estudiante08@cosafam.test` | `Est08-2026!` | Sebastián Vargas |
| Estudiante 09 | `estudiante09@cosafam.test` | `Est09-2026!` | Camila Herrera |
| Estudiante 10 | `estudiante10@cosafam.test` | `Est10-2026!` | Tomás Jiménez |
| Estudiante 11 | `estudiante11@cosafam.test` | `Est11-2026!` | Renata Morales |
| Estudiante 12 | `estudiante12@cosafam.test` | `Est12-2026!` | Andrés Salazar |
| Estudiante 13 | `estudiante13@cosafam.test` | `Est13-2026!` | María José León |
| Estudiante 14 | `estudiante14@cosafam.test` | `Est14-2026!` | Felipe Ortiz |
| Estudiante 15 | `estudiante15@cosafam.test` | `Est15-2026!` | Daniela Ramos |
| Estudiante 16 | `estudiante16@cosafam.test` | `Est16-2026!` | Javier Reyes |
| Estudiante 17 | `estudiante17@cosafam.test` | `Est17-2026!` | Sofía Guerrero |
| Estudiante 18 | `estudiante18@cosafam.test` | `Est18-2026!` | Emilio Flores |
| Estudiante 19 | `estudiante19@cosafam.test` | `Est19-2026!` | Natalia Rojas |
| Estudiante 20 | `estudiante20@cosafam.test` | `Est20-2026!` | Samuel Cruz |
| Estudiante 21 | `estudiante21@cosafam.test` | `Est21-2026!` | Alejandra Vega |
| Estudiante 22 | `estudiante22@cosafam.test` | `Est22-2026!` | Ricardo Ponce |
| Estudiante 23 | `estudiante23@cosafam.test` | `Est23-2026!` | Melissa Aguilar |
| Estudiante 24 | `estudiante24@cosafam.test` | `Est24-2026!` | Esteban Cortés |
| Estudiante 25 | `estudiante25@cosafam.test` | `Est25-2026!` | Andrea Lozano |
| Estudiante 26 | `estudiante26@cosafam.test` | `Est26-2026!` | Nicolás Delgado |
| Estudiante 27 | `estudiante27@cosafam.test` | `Est27-2026!` | Gabriela Rios |
| Estudiante 28 | `estudiante28@cosafam.test` | `Est28-2026!` | Martín Serrano |
| Estudiante 29 | `estudiante29@cosafam.test` | `Est29-2026!` | Paola Medina |
| Estudiante 30 | `estudiante30@cosafam.test` | `Est30-2026!` | Luis Carrillo |
| Estudiante 31 | `estudiante31@cosafam.test` | `Est31-2026!` | Valeria Espinoza |
| Estudiante 32 | `estudiante32@cosafam.test` | `Est32-2026!` | Rodrigo Naranjo |

**1 Clase de prueba:**
- Nombre: `"1er Año de Bachillerato — COSAFAM 2026"`
- Descripción: `"Grupo piloto del Colegio Sagrada Familia para prueba cerrada de la plataforma NeuroMax"`
- Código de unión: `COSAFAM1` (fijo para reproducibilidad)
- Los **32 estudiantes** inscritos en esta clase

---

#### 📚 Problemas — Fracciones (4 niveles KST encadenados)

La cadena KST garantiza que el Motor bloquee automáticamente al estudiante si no superó el prerrequisito.

```
FR-1 (nivel 1) → FR-2 (nivel 2) → FR-3 (nivel 3) → FR-4 (nivel 4)
```

| ID | Título | Operación | Nivel KST | Prerrequisito |
|----|--------|-----------|-----------|---------------|
| FR-1 | Fracciones Equivalentes | Reconocimiento visual (1/2 vs 2/4) | 1 | — |
| FR-2 | División de Fracciones | 3/4 ÷ 1/8 = 6 frascos | 2 | FR-1 |
| FR-3 | Fracción de una Fracción | 1/2 × 2/3 del huerto | 3 | FR-2 |
| FR-4 | Suma con Denominador Diferente | 1/3 + 1/4 en receta de cocina | 4 | FR-3 |

**EMT Data por problema (ejemplo FR-2):**
```json
{
  "Expectations": [
    "El estudiante identifica que repartir implica dividir",
    "Aplica la regla: invertir la segunda fracción y multiplicar (3/4 × 8/1 = 6)",
    "Interpreta el resultado 6 como la cantidad de frascos completos"
  ],
  "Misconceptions": [
    {"error": "Multiplicar directo (3/4 × 1/8 = 3/32)",
     "Seed_Question": "Si tienes una jarra y la repartes en vasos, ¿estás multiplicando el líquido o dividiéndolo en partes? ¿Qué pasa con la cantidad total?"},
    {"error": "Sumar las fracciones (3/4 + 1/8 = 7/8)",
     "Seed_Question": "¿Sumar te dice cuántos frascos CABEN? Si agregas más líquido, ¿sabes cuántos frascos necesitas?"},
    {"error": "Restar fracciones (3/4 - 1/8 = 5/8)",
     "Seed_Question": "La resta te dice cuánto sobra, no cuántas veces cabe algo dentro de otro. ¿Cuál operación usamos para saber cuántas veces cabe un número en otro?"}
  ]
}
```

---

#### ⚡ Problemas — Exponenciación (4 niveles KST encadenados)

```
EXP-1 (nivel 1) → EXP-2 (nivel 2) → EXP-3 (nivel 3) → EXP-4 (nivel 4)
```

| ID | Título | Concepto | Nivel KST | Prerrequisito |
|----|--------|----------|-----------|---------------|
| EXP-1 | ¿Qué significa una potencia? | Notación base-exponente vs multiplicación repetida | 1 | — |
| EXP-2 | Producto de Potencias | a^m × a^n = a^(m+n) — bacterias duplicándose | 2 | EXP-1 |
| EXP-3 | Potencia de Potencia | (a^m)^n = a^(m×n) — zoom de imagen | 3 | EXP-2 |
| EXP-4 | Potencia de Exponente Cero | a^0 = 1 — dilemas de la nada | 4 | EXP-3 |

**EMT Data por problema (ejemplo EXP-2):**
```json
{
  "Expectations": [
    "El estudiante reconoce que al multiplicar potencias de igual base se suman los exponentes",
    "Calcula 2^3 × 2^4 = 2^7 = 128 correctamente",
    "Conecta el crecimiento bacteriano con el crecimiento exponencial"
  ],
  "Misconceptions": [
    {"error": "Multiplicar los exponentes (2^3 × 2^4 = 2^12)",
     "Seed_Question": "Si cuentas 2×2×2 y luego 2×2×2×2, y los juntas en una sola fila, ¿cuántos doses multiplicas en total? ¿Los exponentes se suman o se multiplican?"},
    {"error": "Multiplicar las bases (2^3 × 2^4 = 4^7)",
     "Seed_Question": "Si usas el mismo tipo de bacteria (base 2) en dos frascos, al juntarlos ¿cambia el tipo de bacteria o solo la cantidad de generaciones (el exponente)?"},
    {"error": "Sumar base y exponente (2^3 × 2^4 = 2^3+4 = 2^7 pero escrito como 14)",
     "Seed_Question": "Obtuviste el exponente correcto (7), pero ¿cuál es el valor numérico de 2 elevado a la 7? Calcula 2×2×2×2×2×2×2."}
  ]
}
```

---

#### 🔧 Estructura del Management Command

```python
# apps/tutor/management/commands/seed_pruebas.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Pobla la BD con datos de prueba cerrada: 1 profesor, 10 estudiantes, 8 problemas'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true',
                            help='Elimina datos previos de tutor antes de seedear')

    def handle(self, *args, **options):
        if options['flush']:
            # Limpia solo las tablas de tutor, no users
            InteraccionIA.objects.all().delete()
            Problema.objects.all().delete()
            Clase.objects.all().delete()
            self.stdout.write('🗑️  Datos anteriores eliminados.')

        # 1. Crear/obtener Profesor
        # 2. Crear Clase con codigo_union='NEURO01'
        # 3. Crear 10 Estudiantes y asociarlos a la Clase
        # 4. Crear 4 Problemas de Fracciones con cadena KST
        # 5. Crear 4 Problemas de Exponenciación con cadena KST
        self.stdout.write(self.style.SUCCESS('✅ Seed completado: 33 usuarios COSAFAM (1 profesor + 32 estudiantes), 1 clase de 1er Bachillerato, 8 problemas.'))
```

> [!TIP]
> El flag `--flush` permite resetear y re-seedear en cada ciclo de prueba sin tocar los usuarios de producción.

---

## Secuencia de Ejecución

| Paso | Componentes | Archivos Principales |
|------|-------------|---------------------|
| **1** | Modelos + Migraciones | `apps/tutor/models.py`, `pyproject.toml`, `config/settings/` |
| **2** | Vistas + Motor KST | `apps/tutor/views.py`, `apps/tutor/urls.py`, `config/urls.py` |
| **3** | Servicio Gemini | `apps/tutor/services.py`, `.env` (GEMINI_API_KEY) |
| **4** | Templates Bootstrap | `dashboard_docente.html`, `tutor_interactivo.html` |
| **5** | Datos de Prueba | `management/commands/seed_pruebas.py` → `python manage.py seed_pruebas` |
