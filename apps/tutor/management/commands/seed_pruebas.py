"""
Comando de Seeding — NeuroMax COSAFAM
Uso: python manage.py seed_pruebas [--reset]
Crea: 1 profesor + 32 estudiantes, 1 clase, 8 problemas con datos EMT.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.tutor.models import Clase, Inscripcion, PerfilUsuario, Problema

User = get_user_model()

ESTUDIANTES = [
    ("Ana Sofía Pérez", "estudiante01"), ("Carlos Mendoza", "estudiante02"),
    ("Valentina Ruiz", "estudiante03"), ("Diego Fuentes", "estudiante04"),
    ("Isabella Torres", "estudiante05"), ("Mateo García", "estudiante06"),
    ("Luciana Castro", "estudiante07"), ("Sebastián Vargas", "estudiante08"),
    ("Camila Herrera", "estudiante09"), ("Tomás Jiménez", "estudiante10"),
    ("Renata Morales", "estudiante11"), ("Andrés Salazar", "estudiante12"),
    ("María José León", "estudiante13"), ("Felipe Ortiz", "estudiante14"),
    ("Daniela Ramos", "estudiante15"), ("Javier Reyes", "estudiante16"),
    ("Sofía Guerrero", "estudiante17"), ("Emilio Flores", "estudiante18"),
    ("Natalia Rojas", "estudiante19"), ("Samuel Cruz", "estudiante20"),
    ("Alejandra Vega", "estudiante21"), ("Ricardo Ponce", "estudiante22"),
    ("Melissa Aguilar", "estudiante23"), ("Esteban Cortés", "estudiante24"),
    ("Andrea Lozano", "estudiante25"), ("Nicolás Delgado", "estudiante26"),
    ("Gabriela Rios", "estudiante27"), ("Martín Serrano", "estudiante28"),
    ("Paola Medina", "estudiante29"), ("Luis Carrillo", "estudiante30"),
    ("Valeria Espinoza", "estudiante31"), ("Rodrigo Naranjo", "estudiante32"),
]

ACT_FR1 = {
    "pregunta": "Tienes una barra de chocolate dividida en 4 partes iguales y comes 2. ¿Qué fracción comiste?",
    "opciones": ["1/4", "2/4", "3/4", "4/2"],
    "correcta": "2/4",
    "feedback_correcto": "¡Exacto! 2 de 4 partes es 2/4. Ahora verás por qué también se puede escribir como 1/2.",
    "feedback_incorrecto": "Observa cuántas partes tiene la barra en total y cuántas comiste.",
}
ACT_FR2 = {
    "pregunta": "Si tienes 3/4 de un litro de jugo y lo divides en partes de 1/8 litro, ¿cuántas partes obtienes?",
    "opciones": ["3", "4", "6", "8"],
    "correcta": "6",
    "feedback_correcto": "¡Correcto! 3/4 ÷ 1/8 = 6 partes.",
    "feedback_incorrecto": "Piensa: ¿cuántas veces cabe 1/8 dentro de 3/4?",
}
ACT_FR3 = {
    "pregunta": "¿Qué operación representa 'la mitad de las tres cuartas partes'?",
    "opciones": ["1/2 + 3/4", "1/2 × 3/4", "3/4 ÷ 2", "3/4 - 1/2"],
    "correcta": "1/2 × 3/4",
    "feedback_correcto": "¡Sí! 'La mitad de algo' siempre es una multiplicación.",
    "feedback_incorrecto": "La palabra 'de' en matemáticas generalmente indica multiplicación.",
}
ACT_FR4 = {
    "pregunta": "¿Cuánto es 5/6 + 7/4 expresado con denominador común?",
    "opciones": ["10/12 + 21/12", "5/12 + 7/12", "10/6 + 7/6", "5/24 + 7/24"],
    "correcta": "10/12 + 21/12",
    "feedback_correcto": "¡Perfecto! El MCM de 6 y 4 es 12.",
    "feedback_incorrecto": "Busca el mínimo común múltiplo de 6 y 4.",
}
ACT_EX1 = {
    "pregunta": "¿Cuánto es 2³?",
    "opciones": ["6", "8", "9", "12"],
    "correcta": "8",
    "feedback_correcto": "¡Correcto! 2³ = 2 × 2 × 2 = 8.",
    "feedback_incorrecto": "Recuerda: el exponente indica cuántas veces multiplicas la base por sí misma.",
}
ACT_EX2 = {
    "pregunta": "¿Qué es a³ × a⁴ usando propiedades de exponentes?",
    "opciones": ["a⁷", "a¹²", "a", "2a⁷"],
    "correcta": "a⁷",
    "feedback_correcto": "¡Exacto! Al multiplicar potencias de igual base, se suman los exponentes.",
    "feedback_incorrecto": "¿Qué pasa con los exponentes cuando multiplicas potencias de la misma base?",
}
ACT_EX3 = {
    "pregunta": "¿Cuánto es (2³)²?",
    "opciones": ["2⁵", "2⁶", "2⁹", "6²"],
    "correcta": "2⁶",
    "feedback_correcto": "¡Correcto! Potencia de una potencia: se multiplican los exponentes. 3×2=6.",
    "feedback_incorrecto": "Cuando una potencia está elevada a otro exponente, ¿qué operación harías con los exponentes?",
}
ACT_EX4 = {
    "pregunta": "¿Cómo se simplifica (a³b²)/(ab)?",
    "opciones": ["a²b", "a³b²", "ab²", "a²b²"],
    "correcta": "a²b",
    "feedback_correcto": "¡Excelente! a³/a = a² y b²/b = b.",
    "feedback_incorrecto": "Aplica la regla de división de potencias para cada variable por separado.",
}

VIS_FRACCIONES = """
<div class="text-center py-3">
  <svg viewBox="0 0 200 60" width="200" height="60" xmlns="http://www.w3.org/2000/svg">
    <rect x="5" y="10" width="45" height="40" rx="4" fill="#818cf8" opacity=".9"/>
    <rect x="55" y="10" width="45" height="40" rx="4" fill="#818cf8" opacity=".9"/>
    <rect x="105" y="10" width="45" height="40" rx="4" fill="#e2e8f0"/>
    <rect x="155" y="10" width="45" height="40" rx="4" fill="#e2e8f0"/>
    <text x="27" y="35" text-anchor="middle" font-size="11" fill="white" font-weight="bold">1/4</text>
    <text x="77" y="35" text-anchor="middle" font-size="11" fill="white" font-weight="bold">2/4</text>
    <text x="127" y="35" text-anchor="middle" font-size="11" fill="#94a3b8">3/4</text>
    <text x="177" y="35" text-anchor="middle" font-size="11" fill="#94a3b8">4/4</text>
  </svg>
  <p class="small text-muted mt-2">Barra dividida en 4 partes iguales — las azules fueron comidas</p>
</div>"""

VIS_EXPONENCIACION = """
<div class="text-center py-3">
  <svg viewBox="0 0 180 60" width="180" height="60" xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="20" width="30" height="30" rx="4" fill="#f472b6"/>
    <rect x="50" y="10" width="30" height="40" rx="4" fill="#f472b6"/>
    <rect x="90" y="5" width="30" height="45" rx="4" fill="#f472b6"/>
    <rect x="130" y="0" width="30" height="50" rx="4" fill="#f472b6"/>
    <text x="25" y="62" text-anchor="middle" font-size="9" fill="#64748b">2¹=2</text>
    <text x="65" y="62" text-anchor="middle" font-size="9" fill="#64748b">2²=4</text>
    <text x="105" y="62" text-anchor="middle" font-size="9" fill="#64748b">2³=8</text>
    <text x="145" y="62" text-anchor="middle" font-size="9" fill="#64748b">2⁴=16</text>
  </svg>
  <p class="small text-muted mt-2">Crecimiento exponencial de potencias de 2</p>
</div>"""

PROBLEMAS_DATA = [
    {
        "id_ref": "FR-1", "titulo": "Fracciones Equivalentes", "tema": "FRACCIONES", "nivel_kst": 1,
        "prerequisito_ref": None,
        "enunciado": (
            "En el laboratorio de Química del COSAFAM, tienes un vaso con 2/4 de litro de solución "
            "y otro con 1/2 de litro. Tu profesora dice que tienen la misma cantidad. "
            "¿Puedes demostrar por qué 2/4 = 1/2 sin usar una calculadora?"
        ),
        "activacion": ACT_FR1,
        "visualizacion": VIS_FRACCIONES,
        "respuesta_correcta": "2/4, 1/2, son iguales, equivalentes",
        "expectations": {"Expectations": [
            "El alumno identifica que multiplicar o dividir numerador y denominador por el mismo número no cambia el valor.",
            "El alumno relaciona 2/4 con 1/2 dividiendo ambos términos entre 2.",
            "Comprende el concepto de fracción equivalente como igual valor, diferente representación.",
        ]},
        "misconceptions": {"Misconceptions": [
            {"error": "Cree que 2/4 es mayor que 1/2 porque tiene más números.",
             "Seed_Question": "Si partes una pizza en 4 y comes 2 trozos, ¿o si la partes en 2 y comes 1 trozo... ¿comiste diferente cantidad? ¿Por qué?"},
            {"error": "Suma numeradores y denominadores: 2/4 + 1/2 = 3/6.",
             "Seed_Question": "¿Por qué no puedes sumar 2 manzanas y 4 naranjas y decir que tienes 6 frutas del mismo tipo?"},
        ]},
    },
    {
        "id_ref": "FR-2", "titulo": "División de Fracciones", "tema": "FRACCIONES", "nivel_kst": 2,
        "prerequisito_ref": "FR-1",
        "enunciado": (
            "El club de Ciencias del COSAFAM tiene 3/4 de litro de reactivo para llenar frascos "
            "de 1/8 de litro cada uno. ¿Cuántos frascos completos pueden llenar?"
        ),
        "activacion": ACT_FR2,
        "visualizacion": VIS_FRACCIONES,
        "respuesta_correcta": "6, seis frascos",
        "expectations": {"Expectations": [
            "El alumno aplica la regla de 'invertir y multiplicar': a/b ÷ c/d = a/b × d/c.",
            "Comprende que dividir por 1/8 equivale a multiplicar por 8.",
            "Verifica el resultado: 6 × 1/8 = 6/8 = 3/4.",
        ]},
        "misconceptions": {"Misconceptions": [
            {"error": "Divide numeradores entre sí y denominadores entre sí: (3÷1)/(4÷8) = 3/0.5.",
             "Seed_Question": "Si divides 3 pizzas entre 1/2 pizza, ¿obtienes menos pizzas o más grupos de media pizza?"},
            {"error": "Multiplica directamente sin invertir: 3/4 × 1/8 = 3/32.",
             "Seed_Question": "¿Dividir entre un número menor que 1 debería darte un resultado mayor o menor que lo que dividiste?"},
        ]},
    },
    {
        "id_ref": "FR-3", "titulo": "Fracción de una Fracción", "tema": "FRACCIONES", "nivel_kst": 3,
        "prerequisito_ref": "FR-2",
        "enunciado": (
            "El huerto escolar del COSAFAM ocupa 2/3 del patio. El área de lechugas representa "
            "1/2 de ese huerto. ¿Qué fracción del patio total son las lechugas?"
        ),
        "activacion": ACT_FR3,
        "visualizacion": VIS_FRACCIONES,
        "respuesta_correcta": "1/3, un tercio",
        "expectations": {"Expectations": [
            "El alumno reconoce que 'fracción de fracción' implica multiplicación.",
            "Multiplica 1/2 × 2/3 = 2/6 y simplifica a 1/3.",
            "Interpreta el resultado: las lechugas ocupan 1/3 del patio total.",
        ]},
        "misconceptions": {"Misconceptions": [
            {"error": "Suma las fracciones: 1/2 + 2/3 = 7/6.",
             "Seed_Question": "Si tomas 'la mitad DE algo', ¿obtienes más de ese algo o menos?"},
            {"error": "Interpreta mal el enunciado y calcula 2/3 - 1/2.",
             "Seed_Question": "La palabra 'de' en '1/2 de 2/3' indica una operación. ¿Cuál crees que es, suma o producto?"},
        ]},
    },
    {
        "id_ref": "FR-4", "titulo": "Suma de Fracciones Heterogéneas", "tema": "FRACCIONES", "nivel_kst": 4,
        "prerequisito_ref": "FR-3",
        "enunciado": (
            "Para el proyecto de Biología del COSAFAM usas 5/6 de metro de manguera de un tipo "
            "y 7/4 de metro de otro tipo. ¿Cuántos metros de manguera usaste en total?"
        ),
        "activacion": ACT_FR4,
        "visualizacion": VIS_FRACCIONES,
        "respuesta_correcta": "31/12, 2 y 7/12",
        "expectations": {"Expectations": [
            "El alumno encuentra el MCM de 6 y 4, que es 12.",
            "Convierte: 5/6 = 10/12 y 7/4 = 21/12.",
            "Suma: 10/12 + 21/12 = 31/12 = 2 y 7/12.",
        ]},
        "misconceptions": {"Misconceptions": [
            {"error": "Suma numeradores y denominadores: 5+7=12 y 6+4=10, resultado 12/10.",
             "Seed_Question": "Si tienes 1/2 litro y agregas 1/2 litro más, ¿obtienes 2/4 litros o 1 litro completo?"},
            {"error": "Usa denominador incorrecto distinto del MCM.",
             "Seed_Question": "¿Cuál es el número más pequeño que es divisible exactamente tanto por 6 como por 4?"},
        ]},
    },
    {
        "id_ref": "EX-1", "titulo": "Potenciación: Concepto y Cálculo", "tema": "EXPONENCIACION", "nivel_kst": 1,
        "prerequisito_ref": None,
        "enunciado": (
            "Una bacteria del laboratorio de Biología del COSAFAM se duplica cada hora. "
            "Si empiezas con 1 bacteria, ¿cuántas habrá después de 4 horas? "
            "Expresa el resultado usando potencias."
        ),
        "activacion": ACT_EX1,
        "visualizacion": VIS_EXPONENCIACION,
        "respuesta_correcta": "16, 2^4, dieciséis",
        "expectations": {"Expectations": [
            "El alumno identifica que la base es 2 (duplicación) y el exponente es 4 (horas).",
            "Calcula 2⁴ = 2×2×2×2 = 16.",
            "Diferencia entre multiplicación (2×4=8) y potenciación (2⁴=16).",
        ]},
        "misconceptions": {"Misconceptions": [
            {"error": "Multiplica base por exponente: 2×4 = 8.",
             "Seed_Question": "Si la bacteria se duplica cada hora, ¿al final de la hora 2 tienes 2 bacterias o 4? Haz el conteo hora por hora."},
            {"error": "Suma repetida: 2+2+2+2 = 8.",
             "Seed_Question": "¿Duplicar significa sumar 2 o multiplicar por 2? ¿Cuál es la diferencia entre 'añadir 2' y 'el doble de lo que había'?"},
        ]},
    },
    {
        "id_ref": "EX-2", "titulo": "Producto de Potencias de Igual Base", "tema": "EXPONENCIACION", "nivel_kst": 2,
        "prerequisito_ref": "EX-1",
        "enunciado": (
            "En el club de Física del COSAFAM calculas la energía de dos sistemas. "
            "El primero tiene a³ joules y el segundo a⁴ joules. "
            "Si combinas los sistemas, la energía total es a³ × a⁴. Simplifica."
        ),
        "activacion": ACT_EX2,
        "visualizacion": VIS_EXPONENCIACION,
        "respuesta_correcta": "a^7, a7",
        "expectations": {"Expectations": [
            "El alumno identifica que la base es la misma (a) en ambas potencias.",
            "Aplica la propiedad: aⁿ × aᵐ = aⁿ⁺ᵐ.",
            "Suma los exponentes: 3+4=7, resultado a⁷.",
        ]},
        "misconceptions": {"Misconceptions": [
            {"error": "Multiplica los exponentes: a³ × a⁴ = a¹².",
             "Seed_Question": "Escribe a³ × a⁴ expandido como (a×a×a) × (a×a×a×a). ¿Cuántas 'a' multiplicas en total?"},
            {"error": "Mantiene los exponentes separados: a³⁴.",
             "Seed_Question": "¿Qué significa a³ escrito sin exponente? ¿Cuántos factores 'a' tiene?"},
        ]},
    },
    {
        "id_ref": "EX-3", "titulo": "Potencia de una Potencia", "tema": "EXPONENCIACION", "nivel_kst": 3,
        "prerequisito_ref": "EX-2",
        "enunciado": (
            "En el proyecto de Cómputo del COSAFAM, el almacenamiento se organiza en cubos de "
            "cubos: cada cubo tiene 2³ celdas, y hay 2³ cubos. "
            "¿Cuántas celdas totales hay? Expresa como (2³)²."
        ),
        "activacion": ACT_EX3,
        "visualizacion": VIS_EXPONENCIACION,
        "respuesta_correcta": "2^6, 64, sesenta y cuatro",
        "expectations": {"Expectations": [
            "El alumno aplica la propiedad: (aⁿ)ᵐ = aⁿ×ᵐ.",
            "Multiplica los exponentes: 3×2=6.",
            "Calcula 2⁶=64 y verifica que coincide con 8×8=64.",
        ]},
        "misconceptions": {"Misconceptions": [
            {"error": "Suma los exponentes: (2³)² = 2⁵.",
             "Seed_Question": "Expande (2³)² como 2³ × 2³. Ahora aplica la regla del producto de potencias que ya conoces."},
            {"error": "Eleva la base dos veces: 2³ al cuadrado = 4³ = 64 (resultado correcto por casualidad).",
             "Seed_Question": "Tu respuesta final es correcta, pero ¿puedes explicar por qué el procedimiento de elevar la base no es el camino general correcto?"},
        ]},
    },
    {
        "id_ref": "EX-4", "titulo": "División de Potencias y Simplificación", "tema": "EXPONENCIACION", "nivel_kst": 4,
        "prerequisito_ref": "EX-3",
        "enunciado": (
            "El equipo de Química del COSAFAM trabaja con concentraciones. "
            "La fórmula simplificada de un compuesto es (a³b²)/(ab). "
            "Simplifica la expresión aplicando propiedades de exponentes."
        ),
        "activacion": ACT_EX4,
        "visualizacion": VIS_EXPONENCIACION,
        "respuesta_correcta": "a^2 b, a2b",
        "expectations": {"Expectations": [
            "El alumno aplica aⁿ/aᵐ = aⁿ⁻ᵐ para cada variable.",
            "Calcula a³/a = a² y b²/b = b¹ = b.",
            "Combina el resultado: a²b.",
        ]},
        "misconceptions": {"Misconceptions": [
            {"error": "Resta todos los exponentes directamente: a³⁻¹b²⁻¹ pero escribe a²b⁰ = a².",
             "Seed_Question": "¿b⁰ vale 0 o vale 1? ¿Desaparece o se convierte en otro número?"},
            {"error": "Divide los coeficientes numéricos que no existen: a/a=0.",
             "Seed_Question": "Si tienes a³/a¹, escríbelo expandido: (a×a×a)/(a). ¿Qué se cancela y qué queda?"},
        ]},
    },
]


class Command(BaseCommand):
    help = "Genera datos de prueba COSAFAM: 33 usuarios, 1 clase, 8 problemas EMT."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Elimina datos previos antes de sembrar.")

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write("🗑  Eliminando datos previos...")
            Problema.objects.all().delete()
            Inscripcion.objects.all().delete()
            Clase.objects.all().delete()
            PerfilUsuario.objects.all().delete()
            User.objects.filter(email__endswith="@cosafam.test").delete()
            self.stdout.write(self.style.WARNING("   Datos anteriores eliminados."))

        # ── 1. PROFESOR ──
        self.stdout.write("👤 Creando profesor...")
        prof_user, created = User.objects.get_or_create(
            email="profesor@cosafam.test",
            defaults={"name": "Prof. Hernán Ramírez", "is_active": True},
        )
        if created:
            prof_user.set_password("Cosafam2026!")
            prof_user.save()
        PerfilUsuario.objects.get_or_create(
            user=prof_user,
            defaults={"rol": "PROFESOR", "nombre_completo": "Prof. Hernán Ramírez"},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("   ✓ profesor@cosafam.test"))

        # ── 2. CLASE ──
        self.stdout.write("🏫 Creando clase COSAFAM1...")
        clase, _ = Clase.objects.get_or_create(
            codigo_union="COSAFAM1",
            defaults={
                "profesor": prof_user,
                "nombre": "1er Año de Bachillerato — COSAFAM 2026",
                "descripcion": "Grupo piloto del Colegio Sagrada Familia para prueba cerrada de NeuroMax.",
                "activa": True,
            },
        )
        self.stdout.write(self.style.SUCCESS(f"   ✓ Clase: {clase.nombre}"))

        # ── 3. ESTUDIANTES ──
        self.stdout.write(f"👥 Creando {len(ESTUDIANTES)} estudiantes...")
        for nombre, username in ESTUDIANTES:
            email = f"{username}@cosafam.test"
            num = username.replace("estudiante", "")
            password = f"Est{num}-2026!"
            est_user, created = User.objects.get_or_create(
                email=email, defaults={"name": nombre, "is_active": True}
            )
            if created:
                est_user.set_password(password)
                est_user.save()
            PerfilUsuario.objects.get_or_create(
                user=est_user,
                defaults={"rol": "ESTUDIANTE", "nombre_completo": nombre},
            )
            Inscripcion.objects.get_or_create(
                estudiante=est_user, clase=clase, defaults={"activa": True}
            )
        self.stdout.write(self.style.SUCCESS(f"   ✓ {len(ESTUDIANTES)} estudiantes inscritos en COSAFAM1"))

        # ── 4. PROBLEMAS ──
        self.stdout.write("📚 Creando 8 problemas con datos EMT...")
        ref_map = {}
        for pd in PROBLEMAS_DATA:
            prereq = ref_map.get(pd["prerequisito_ref"]) if pd["prerequisito_ref"] else None
            problema, created = Problema.objects.get_or_create(
                titulo=pd["titulo"],
                defaults={
                    "tema": pd["tema"],
                    "nivel_kst": pd["nivel_kst"],
                    "prerequisito": prereq,
                    "enunciado": pd["enunciado"],
                    "activacion_cognitiva_json": pd["activacion"],
                    "visualizacion_html": pd["visualizacion"],
                    "respuesta_correcta": pd["respuesta_correcta"],
                    "expectations_json": pd["expectations"],
                    "misconceptions_json": pd["misconceptions"],
                    "activo": True,
                },
            )
            ref_map[pd["id_ref"]] = problema
            icon = "✓ [NUEVO]" if created else "~ [ya existía]"
            self.stdout.write(f"   {icon} {pd['id_ref']}: {pd['titulo']}")

        self.stdout.write(self.style.SUCCESS(
            "\n✅ Seed completado: 33 usuarios COSAFAM (1 profesor + 32 estudiantes), "
            "1 clase de 1er Bachillerato, 8 problemas con datos EMT completos.\n"
            "🔑 Profesor:    profesor@cosafam.test  /  Cosafam2026!\n"
            "🎓 Estudiantes: estudiante01-32@cosafam.test  /  EstNN-2026!\n"
            "🏫 Código clase: COSAFAM1\n"
            "💡 Usa --reset para limpiar y re-sembrar datos."
        ))
