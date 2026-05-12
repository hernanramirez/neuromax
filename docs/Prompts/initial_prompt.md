# Prompt de Desarrollo: Plataforma Neurodidáctica en Django (Modo Plan)

**Rol del Sistema:**
Actúa como un Desarrollador Full-Stack Senior experto en Django (Python) y Arquitecto de Software EdTech basado en Neurociencia Cognitiva. Vas a utilizar un enfoque de "Modo Plan" paso a paso para ayudarme a construir una aplicación educativa.

## Contexto del Proyecto y Arquitectura
El proyecto ya cuenta con una estructura básica en Django. Es fundamental que todas las vistas rendericen los templates asumiendo que los archivos HTML (basados en Bootstrap) se ubican en el directorio `apps/templates/pages`. 

La arquitectura lógica se compone de dos motores principales:
1. **Motor KST (Teoría de Espacios de Conocimiento):** Un algoritmo que utiliza jerarquías de habilidades y redes bayesianas para determinar la "frontera de conocimiento" del estudiante, mapeando lo que sabe y adaptando la ruta de aprendizaje.
2. **Tutor Socrático (API de Gemini):** Un sistema de diálogo inteligente basado en la metodología de "Expectativa-Idea Errónea" (EMT, por sus siglas en inglés) que evalúa las respuestas del alumno frente a expectativas de éxito y errores comunes, proporcionando retroalimentación dinámica y preguntas guiadas en lugar de respuestas directas. 

**Requisito Nuevo:** El sistema debe ser capaz de **manejar múltiples clases** (multi-tenant a nivel de profesor), permitiendo que un docente administre diferentes grupos de estudiantes de manera independiente.

---

## Instrucciones de Trabajo (Modo Plan)
Por favor, estructura el desarrollo en los siguientes 4 pasos secuenciales. **No escribas todo el código de inmediato.** Primero preséntame este plan, confirma que comprendes la arquitectura, el directorio de los templates y el uso de la API de Gemini, y espera mi confirmación para iniciar el "Paso 1".

### Paso 1: Modelos de Base de Datos (`models.py` - Multi-clase y KST)
* Genera las entidades `Profesor`, `Clase` (con un código de unión único) y `Estudiante` (relacionado con la clase mediante llave foránea).
* Genera la entidad `InteraccionIA` para registrar el estudiante, la clase, el tema, los intentos y las pistas (hints) dadas por Gemini, datos esenciales para alimentar el Motor KST.
* Genera los modelos `DiarioMetacognitivo` y `EvaluacionIadov`.

### Paso 2: Lógica del Motor KST y Controladores (`views.py`)
* Crea un "Dashboard Multi-clase" para el docente, donde pueda seleccionar una de sus clases y ver el estado de conocimiento de ese grupo en específico.
* Estructura la vista del estudiante que actúe como el Motor KST, evaluando silenciosamente los prerrequisitos visuales antes de permitirle avanzar al problema principal. Todas estas vistas deben utilizae los demos a `apps/templates/pages/`.

### Paso 3: Integración de la API de Gemini (`services.py` y Tutor Socrático)
* Crea un servicio utilizando el SDK `google-generativeai`.
* La llamada a la API debe incluir un *System Prompt* estructurado estrictamente en JSON que contenga las llaves `"Expectations"` (lo que el alumno debe deducir) y `"Misconceptions"` (errores esperados).
* Si la respuesta del alumno coincide con un *Misconception*, la API de Gemini debe generar y devolver una `"Seed_Question"` (pregunta semilla mayéutica) para provocar disonancia cognitiva en el estudiante.

### Paso 4: Integración del Front-End (Templates de Bootstrap)
* Proporcióname los esquemas HTML con clases de Bootstrap que coincidan con la ruta `apps/templates/pages/`.
* Necesitaremos un esquema para `dashboard_docente.html` (con tarjetas o tablas para las múltiples clases) y `tutor_interactivo.html` (con el componente visual del problema y el componente de chat de Gemini).


Adicinalmente tenemoos 3 demos en la carpeta `docs/CodeDemo` que se pueden utilizar comoo referencia para la generación de este proyecto
