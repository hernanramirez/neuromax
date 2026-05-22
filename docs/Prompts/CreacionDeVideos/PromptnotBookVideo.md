# Prompts para Videos Instruccionales (NotebookML)

A partir de la base de datos de problemas, se han agrupado los ejercicios por tema (Fracciones y Exponenciación) dado que guardan mucha similitud y pertenecen al mismo hilo conductor. 

El objetivo es usar estos prompts en **NotebookML** (o herramientas de generación de video/audio derivadas) para crear material orientado a **estudiantes de 10 años**, asegurando que el contenido sea muy breve, dinámico y concreto.

---

## 1. Tema: Fracciones (Equivalencia y Operaciones)
**Problemas cubiertos:** Equivalencia (2/4 = 1/2), División (3/4 ÷ 1/8), Fracción de una fracción (1/2 de 2/3) y Suma con distinto denominador (5/6 + 7/4).

**Prompt para NotebookML:**

```text
Actúa como un profesor divertido y experto en explicar matemáticas a niños de 10 años. Necesito que generes un guion muy corto (máximo 1 minuto y medio) para un video instruccional sobre las Fracciones. 

El tono debe ser enérgico, concreto y usar ejemplos del mundo real, sin usar palabras complicadas. 

Estructura el video así:
1. **El gancho (15 seg):** Empieza hablando de pizza o barras de chocolate. Explica de forma visual y rápida que "2 de 4 pedazos" es exactamente lo mismo que "la mitad" (1/2). Esto se llama fracción equivalente.
2. **El reto de dividir (20 seg):** Usa el ejemplo de un club de ciencias: Tienes 3/4 de litro de una poción mágica y quieres llenar frascos pequeñitos de 1/8. Explica que dividir fracciones es como "darle la vuelta" a la segunda y multiplicar. ¡Magia! Obtienes 6 frasquitos.
3. **Multiplicar y sumar (30 seg):** Explica que la palabra "DE" en matemáticas significa multiplicar (ej: "la mitad DE mi patio"). Y para terminar, diles el secreto para sumar fracciones distintas (como 5/6 + 7/4): buscar un número amigo en común en la parte de abajo (el mínimo común múltiplo, que es 12).
4. **Cierre (10 seg):** Un mensaje motivador recordando que las fracciones son solo partes de un todo.

Por favor, incluye notas sobre qué imágenes, animaciones o elementos visuales sencillos deben aparecer en pantalla mientras hablas.
```

---

## 2. Tema: Exponenciación (El Poder de las Potencias)
**Problemas cubiertos:** Concepto base (2⁴), Producto de igual base (a³ × a⁴), Potencia de potencia ((2³)²) y División de potencias ((a³b²)/(ab)).

**Prompt para NotebookML:**

```text
Actúa como un profesor de ciencias y tecnología muy divertido, experto en explicar conceptos a niños de 10 años. Necesito un guion ultracorto (máximo 1 minuto y medio) para un video instruccional sobre la Exponenciación (Las Potencias).

Usa un tono emocionante, como si estuvieras revelando el secreto de un superpoder, usando un lenguaje sencillo y concreto.

Estructura el video de la siguiente manera:
1. **El gancho - La multiplicación rápida (20 seg):** Empieza con una bacteria de laboratorio que se duplica cada hora. Explica que en lugar de escribir 2x2x2x2, los científicos usan un superpoder llamado "exponente" y escriben 2⁴, lo que da 16. ¡Cuidado! Aclara que NO es 2x4=8.
2. **Las dos reglas de oro (30 seg):** 
   - *Regla 1 (Sumar):* Cuando multiplicas bases iguales (como a³ x a⁴), solo tienes que sumar los numeritos de arriba: ¡Boom! a⁷. 
   - *Regla 2 (Multiplicar):* Si tienes un "cubo dentro de un cubo", es decir, una potencia sobre otra potencia como (2³)², los exponentes se multiplican: 3x2=6, dando 2⁶.
3. **El truco de dividir (25 seg):** Imagina que estás reduciendo el tamaño de un compuesto químico (a³ / a). Explica que al dividir, es una pelea donde los numeritos de arriba se restan. Si tienes 3 arriba y 1 abajo (3-1), te quedan 2. ¡Fácil!
4. **Cierre (10 seg):** Despídete animándolos a usar estos superpoderes matemáticos para calcular cosas gigantes sin esfuerzo.

Incluye instrucciones sobre qué tipo de animaciones visuales (como bacterias multiplicándose o números fusionándose) deben mostrarse en el video para mantener la atención de un niño.
```

---

## Anexo: Listado de Desafíos por Problema

A continuación, se detallan los desafíos (problemas) disponibles en la base de datos, desglosados por tema. Para cada desafío se incluye el enunciado que se le presenta al estudiante y las **dificultades o errores comunes (misconceptions)** que el tutor virtual está preparado para manejar.

### Tema 1: Fracciones

**Desafío 1: Fracciones Equivalentes (FR-1)**
*   **Situación:** En el laboratorio tienes un vaso con 2/4 de litro de solución y otro con 1/2 de litro. La profesora dice que tienen la misma cantidad.
*   **El Reto:** Demostrar por qué 2/4 es igual a 1/2 sin usar calculadora.
*   **Dificultades/Errores esperados:**
    *   Creer que 2/4 es mayor que 1/2 simplemente porque los números (2 y 4) son más grandes.
    *   Intentar sumar numeradores y denominadores (ej. 2/4 + 1/2 = 3/6) en lugar de simplificar.

**Desafío 2: División de Fracciones (FR-2)**
*   **Situación:** El club de Ciencias tiene 3/4 de litro de reactivo para llenar frascos pequeños de 1/8 de litro.
*   **El Reto:** Calcular cuántos frascos completos se pueden llenar (3/4 ÷ 1/8).
*   **Dificultades/Errores esperados:**
    *   Dividir los numeradores entre sí y los denominadores entre sí de forma directa.
    *   Multiplicar directamente las dos fracciones sin "invertir" la segunda (3/4 × 1/8).

**Desafío 3: Fracción de una Fracción (FR-3)**
*   **Situación:** El huerto ocupa 2/3 del patio. Las lechugas ocupan 1/2 de ese huerto.
*   **El Reto:** Determinar qué fracción del patio total representan las lechugas (1/2 de 2/3).
*   **Dificultades/Errores esperados:**
    *   Sumar las fracciones en lugar de multiplicarlas (1/2 + 2/3).
    *   Interpretar mal el texto y restar las cantidades (2/3 - 1/2).

**Desafío 4: Suma de Fracciones Heterogéneas (FR-4)**
*   **Situación:** Para un proyecto unes 5/6 de metro de una manguera y 7/4 de metro de otra.
*   **El Reto:** Calcular el total de metros de manguera (5/6 + 7/4).
*   **Dificultades/Errores esperados:**
    *   Sumar el numerador con el numerador y el denominador con el denominador de forma lineal (5+7=12, 6+4=10).
    *   Intentar sumar usando un denominador común que es incorrecto (que no sea el Mínimo Común Múltiplo).

---

### Tema 2: Exponenciación

**Desafío 5: Potenciación: Concepto y Cálculo (EX-1)**
*   **Situación:** Una bacteria se duplica cada hora. Empiezas con 1 bacteria.
*   **El Reto:** Calcular cuántas bacterias habrá en 4 horas usando potencias (2⁴).
*   **Dificultades/Errores esperados:**
    *   Multiplicar la base por el exponente directamente (2 × 4 = 8).
    *   Creer que el exponente significa sumar la base varias veces (2 + 2 + 2 + 2 = 8).

**Desafío 6: Producto de Potencias de Igual Base (EX-2)**
*   **Situación:** Al combinar dos sistemas de energía, tienes que multiplicar a³ joules por a⁴ joules.
*   **El Reto:** Simplificar la expresión de energía total (a³ × a⁴).
*   **Dificultades/Errores esperados:**
    *   Multiplicar los exponentes en lugar de sumarlos (a¹²).
    *   Mantener los exponentes separados sin realizar la operación (a³⁴).

**Desafío 7: Potencia de una Potencia (EX-3)**
*   **Situación:** Almacenamiento organizado en cubos. Cada cubo tiene 2³ celdas y hay 2³ cubos.
*   **El Reto:** Expresar el total de celdas como la potencia de una potencia ((2³)²).
*   **Dificultades/Errores esperados:**
    *   Sumar los exponentes en vez de multiplicarlos (2⁵).
    *   Elevar la base dos veces en lugar de multiplicar los exponentes, lo que causa confusión en los pasos matemáticos aunque a veces coincida el resultado.

**Desafío 8: División de Potencias y Simplificación (EX-4)**
*   **Situación:** Trabajas con la fórmula de concentración de un compuesto químico: (a³b²) / (ab).
*   **El Reto:** Simplificar la fórmula aplicando propiedades de los exponentes.
*   **Dificultades/Errores esperados:**
    *   Restar todos los exponentes pero equivocarse al evaluar qué pasa con variables elevadas a la potencia 0 o 1 (ej. creer que b¹ desaparece u olvidarlo).
    *   Creer que al dividir letras sin exponente (a/a) el resultado es 0 en lugar de 1.

---

## 3. Prompts Específicos para Desafíos (Modo Pista)

### Prompt para Desafío 1: Fracciones Equivalentes (FR-1)
**Objetivo del video:** Dar pistas matemáticas para que el estudiante descubra cómo demostrar que 2/4 = 1/2 sin que el video le dé la respuesta final.

**Prompt para NotebookML:**

```text
Actúa como un profesor guía muy divertido y motivador. Estás ayudando a estudiantes de 10 años a resolver un misterio en el laboratorio de Ciencias: "Demostrar matemáticamente por qué un vaso con 2/4 de litro de poción tiene exactamente la misma cantidad que uno con 1/2 litro".

Tu objetivo en este video ultracorto (máximo 1 minuto) NO es darles la respuesta final, sino darles pistas matemáticas para que ellos lo descubran. 

Usa un tono intrigante, como si les estuvieras dando las pistas de un mapa del tesoro.

Estructura el video así:
1. **El misterio inicial (15 seg):** Presenta el problema del laboratorio. "Tienen 2/4 de litro y 1/2 de litro. ¿Parece diferente, verdad? 2 y 4 son números más grandes que 1 y 2... ¡pero los vasos están igual de llenos!".
2. **Primera pista - El truco del dibujo (15 seg):** Diles: "Pista número uno: ¿Qué pasa si dibujan un rectángulo, lo parten en 4 y pintan 2 pedazos? Ahora, dibujen otro igual, pártanlo a la mitad y pinten 1 pedazo. Miren bien sus dibujos... ¿Notan algo mágico?".
3. **Segunda pista - La regla de oro matemática (20 seg):** Diles: "Pista número dos: En las fracciones, si divides el número de arriba (numerador) y el número de abajo (denominador) por el MISMÍSIMO número, la cantidad no cambia, ¡solo cambian los números!". Pregúntales: "¿Qué número usarían para dividir al 2 y al 4 al mismo tiempo?".
4. **El desafío final (10 seg):** Despídete desafiándolos a usar esa pista matemática en su cuaderno para atrapar la respuesta. "¡Atrévete a dividir ambos números y descubre el secreto! ¡Tú puedes, científico!".

Incluye notas sobre las visualizaciones: pide mostrar los vasos llenos al mismo nivel para generar curiosidad, y signos de interrogación gigantes al hablar de qué número usar para dividir.
```

---

### Prompt para Desafío 2: División de Fracciones (FR-2)
**Objetivo del video:** Dar pistas matemáticas para que el estudiante calcule cuántos frascos de 1/8 caben en 3/4 de litro sin darle la respuesta.

**Prompt para NotebookML:**

```text
Actúa como un profesor guía muy divertido y motivador. Estás ayudando a estudiantes de 10 años a resolver un misterio: "Tienen 3/4 de litro de reactivo mágico y deben repartirlo en frascos pequeñitos de 1/8 de litro. ¿Cuántos frascos llenarán?".

Tu objetivo en este video ultracorto (máximo 1 minuto) NO es darles la respuesta final, sino darles pistas matemáticas.

Estructura el video así:
1. **El misterio inicial (15 seg):** "¡Científicos! Tenemos 3/4 de litro y frasquitos de 1/8. Muchos intentan dividir cruzado y terminan con un desastre en el laboratorio. ¡Peligro!".
2. **Primera pista - La magia de voltear (15 seg):** "Pista número uno: Dividir fracciones tiene un truco secreto. En lugar de dividir, ¡podemos multiplicar! Pero, oh, oh... para hacer eso tienes que darle la vuelta a la segunda fracción. El 1/8 se voltea y se convierte en... ¡8/1!".
3. **Segunda pista - Multiplicación en línea recta (20 seg):** "Pista número dos: Una vez que le diste la vuelta a la segunda fracción, simplemente multiplicas en línea recta: el de arriba con el de arriba (3x8) y el de abajo con el de abajo (4x1). Luego ves qué pasa con ese resultado.".
4. **El desafío final (10 seg):** "¡Ahora te toca a ti! Voltea la segunda, multiplica recto y descubre cuántos frascos llenamos. ¡A calcular!".

Visuales: Mostrar una fracción dándose una voltereta acrobática (1/8 a 8/1) y flechas rectas para la multiplicación.
```

---

### Prompt para Desafío 3: Fracción de una Fracción (FR-3)
**Objetivo del video:** Dar pistas para que el estudiante resuelva qué fracción es "1/2 de 2/3" sin darle la respuesta.

**Prompt para NotebookML:**

```text
Actúa como un profesor guía aventurero. Estás ayudando a estudiantes de 10 años con un enigma agrícola: "Si el huerto ocupa 2/3 del patio, y las lechugas ocupan 1/2 de ese huerto... ¿Qué parte de todo el patio son las lechugas?".

Tu objetivo es dar pistas (máximo 1 minuto), sin dar la respuesta.

Estructura el video así:
1. **El misterio (15 seg):** "¿Lechugas en 1/2 de 2/3? Algunos piensan que deben sumar... ¡pero deténganse! Si sacan la mitad de algo, ¿obtienen más o menos? ¡Menos, claro!".
2. **Primera pista - El secreto de la palabra 'DE' (15 seg):** "Pista clave: En el lenguaje secreto de las matemáticas, cuando decimos 'una fracción DE otra fracción', la palabra 'DE' significa... ¡MULTIPLICAR!".
3. **Segunda pista - La técnica de multiplicar y achicar (20 seg):** "Pista número dos: Ya sabes que es multiplicar (1/2 x 2/3). Se multiplica el de arriba con el de arriba y el de abajo con el de abajo. Y ojo, tu resultado se podrá hacer más pequeño si lo divides por el mismo número, ¡como hicimos antes!".
4. **El desafío (10 seg):** "¡Transforma ese 'DE' en un 'POR' y descubre el terreno de las lechugas! ¡Adelante!".

Visuales: Mostrar la palabra "DE" transformándose mágicamente en un signo "×".
```

---

### Prompt para Desafío 4: Suma de Fracciones Heterogéneas (FR-4)
**Objetivo del video:** Dar pistas para sumar 5/6 + 7/4.

**Prompt para NotebookML:**

```text
Actúa como un profesor guía constructor. Ayudas a estudiantes de 10 años a sumar 5/6 de metro de manguera con 7/4 de metro.

Tu objetivo es dar pistas matemáticas (máximo 1 minuto), sin dar la respuesta.

Estructura el video así:
1. **El misterio (15 seg):** "¡Ingenieros! Queremos unir 5/6 y 7/4 de manguera. ¡Alerta! No pueden sumar 5+7 y 6+4. ¡Esa manguera se rompería y el agua saldría por todos lados!".
2. **Primera pista - El idioma común (15 seg):** "Pista uno: Para sumar fracciones, los números de abajo (los denominadores) deben ser IDÉNTICOS. El 6 y el 4 hablan idiomas distintos. Necesitamos un número que esté en la tabla del 6 y en la tabla del 4 al mismo tiempo.".
3. **Segunda pista - El mínimo común (20 seg):** "Pista dos: Busquen el Mínimo Común Múltiplo. Pista extra: ¡Piensen en el número 12! Si convierten los de abajo en 12 multiplicando, ¡recuerden multiplicar también a los de arriba por el mismo número para que no lloren!".
4. **El desafío (10 seg):** "Encuentren cómo transformar ambas fracciones para que tengan un 12 abajo y sumen solo los de arriba. ¡A construir!".

Visuales: Mostrar los números 6 y 4 buscando un "amigo en común" y abrazando al número 12.
```

---

Actúa como un experto en pedagogía infantil y director de arte de un canal de ciencia para niños (estilo "Beakman" o "Bill Nye"). Tu objetivo es generar el guion para un video ultracorto (máximo 1 minuto) muy dinámico, gráfico e instruccional en español latino americano.


Estás ayudando a estudiantes de 10 años a resolver este misterio matemático: "¡Peligro biológico! Una bacteria se duplica. Tenemos la expresión 2⁴ (dos a la cuarta). ¡Cuidado! Muchos científicos novatos dicen que es 2x4=8... ¡Error fatal!". NO debes darles la respuesta final, solo guiarlos gráficamente.


Genera el contenido respetando estrictamente esta estructura de Guion Técnico, incluyendo indicaciones de voz (tono) y visuales precisas en cada paso:

### Prompt para Desafío 5: Potenciación: Concepto y Cálculo (EX-1)
**Objetivo del video:** Dar pistas para calcular 2⁴.

**Prompt para NotebookML:**

```text
Actúa como un científico loco y divertido. Ayudas a estudiantes de 10 años a calcular bacterias que se duplican 4 veces (2⁴).

Tu objetivo es dar pistas (máximo 1 minuto), sin dar la respuesta.

Estructura el video así:
1. **El misterio (15 seg):** "¡Peligro biológico! Una bacteria se duplica. Tenemos la expresión 2⁴ (dos a la cuarta). ¡Cuidado! Muchos científicos novatos dicen que es 2x4=8... ¡Error fatal!".
2. **Primera pista - El clonador (15 seg):** "Pista uno: El número pequeñito de arriba (el exponente) te dice CUÁNTAS VECES vas a escribir el número grande (la base) para multiplicarlo por sí mismo.".
3. **Segunda pista - Cadena de multiplicación (20 seg):** "Pista dos: No es sumar. Es multiplicar en cadena. Escribe el número 2 cuatro veces en tu papel (2 x 2 x 2 x 2) y empieza a resolver de izquierda a derecha. Primero 2x2, a ese resultado lo multiplicas por 2, y luego otra vez.".
4. **El desafío (10 seg):** "Multiplica en cadena con cuidado y dime, ¿cuántas bacterias gigantes tendremos? ¡A multiplicar!".

Visuales: Mostrar una bacteria clonándose, y una gran "X" roja tachando un "2x4".
```

---

Actúa como un experto en pedagogía infantil y director de arte de un canal de ciencia para niños (estilo "Beakman" o "Bill Nye"). Tu objetivo es generar el guion para un video ultracorto (máximo 1 minuto) muy dinámico, gráfico e instruccional en español latino americano.


Estás ayudando a estudiantes de 10 años a resolver este misterio matemático: "¡Sistemas de energía listos! Tenemos la energía a³ multiplicándose por a⁴. ¡Alerta de cortocircuito! Algunos multiplican el 3 por el 4 y les da 12. ¡Eso haría explotar la máquina!". NO debes darles la respuesta final, solo guiarlos gráficamente.


Genera el contenido respetando estrictamente esta estructura de Guion Técnico, incluyendo indicaciones de voz (tono) y visuales precisas en cada paso:


### Prompt para Desafío 6: Producto de Potencias de Igual Base (EX-2)
**Objetivo del video:** Dar pistas para calcular a³ × a⁴.

**Prompt para NotebookML:**

```text
Actúa como un profesor guía de superhéroes. Ayudas a estudiantes de 10 años a combinar a³ y a⁴.

Tu objetivo es dar pistas (máximo 1 minuto), sin dar la respuesta.

Estructura el video así:
1. **El misterio (15 seg):** "¡Sistemas de energía listos! Tenemos la energía a³ multiplicándose por a⁴. ¡Alerta de cortocircuito! Algunos multiplican el 3 por el 4 y les da 12. ¡Eso haría explotar la máquina!".
2. **Primera pista - Expandiendo el poder (15 seg):** "Pista uno: Imagina qué es a³. Es simplemente (a x a x a). Y a⁴ es (a x a x a x a). Si los juntas todos en una sola línea de multiplicación...".
3. **Segunda pista - La regla rápida (20 seg):** "Pista dos: Cuenta cuántas 'a' tienes en total. Para no escribir tanto siempre, hay un truco mágico de los matemáticos: Cuando multiplicas letras iguales, ¡solo tienes que SUMAR los numeritos de arriba!".
4. **El desafío (10 seg):** "¿Cuánto es 3 más 4? Aplica la regla rápida y obtén la energía total. ¡Enciende la máquina!".

Visuales: Mostrar las 'a' multiplicándose y los numeritos 3 y 4 bajando para sumarse con un signo "+".
```

---


Actúa como un experto en pedagogía infantil y director de arte de un canal de ciencia para niños (estilo "Beakman" o "Bill Nye"). Tu objetivo es generar el guion para un video ultracorto (máximo 1 minuto) muy dinámico, gráfico e instruccional en español latino americano.


Estás ayudando a estudiantes de 10 años a resolver este misterio matemático: "¡Ingenieros espaciales! Tenemos cubos dentro de cubos. La fórmula es ((2³)²). Algunos creen que deben sumar el 3 y el 2 para tener 2⁵... ¡Cuidado, la nave se caería!". NO debes darles la respuesta final, solo guiarlos gráficamente.


Genera el contenido respetando estrictamente esta estructura de Guion Técnico, incluyendo indicaciones de voz (tono) y visuales precisas en cada paso:

### Prompt para Desafío 7: Potencia de una Potencia (EX-3)
**Objetivo del video:** Dar pistas para resolver ((2³)²).

**Prompt para NotebookML:**

```text
Actúa como un arquitecto espacial divertido. Ayudas a resolver el misterio de ((2³)²).

Tu objetivo es dar pistas (máximo 1 minuto), sin dar la respuesta.

Estructura el video así:
1. **El misterio (15 seg):** "¡Ingenieros espaciales! Tenemos cubos dentro de cubos. La fórmula es ((2³)²). Algunos creen que deben sumar el 3 y el 2 para tener 2⁵... ¡Cuidado, la nave se caería!".
2. **Primera pista - ¿Qué significa el 2 de afuera? (15 seg):** "Pista uno: El número 2 de afuera significa que tienes DOS bloques idénticos de 2³. Es decir, (2³) multiplicado por (2³).".
3. **Segunda pista - El atajo supremo (20 seg):** "Pista dos: Ya sabes que cuando multiplicas bases iguales, sumas los exponentes (3+3). PERO, el atajo supremo dice que cuando tienes un exponente tocando a otro exponente con un paréntesis en el medio... ¡ellos se MULTIPLICAN entre sí!".
4. **El desafío (10 seg):** "¿Cuánto es 3 por 2? Aplica el atajo supremo y calcula cuántas celdas tiene la nave. ¡Despegue en 3, 2, 1!".

Visuales: Mostrar exponentes chocando a través de un paréntesis y convirtiéndose en un signo "×".
```

---


Actúa como un experto en pedagogía infantil y director de arte de un canal de ciencia para niños (estilo "Beakman" o "Bill Nye"). Tu objetivo es generar el guion para un video ultracorto (máximo 1 minuto) muy dinámico, gráfico e instruccional en español latino americano.


Estás ayudando a estudiantes de 10 años a resolver este misterio matemático: "¡Científicos, a los laboratorios! Queremos simplificar la fórmula (a³b²) dividida entre (ab). ¡Peligro! Algunos creen que si dividen letras iguales desaparecen en un gran cero. ¡No!". NO debes darles la respuesta final, solo guiarlos gráficamente.


Genera el contenido respetando estrictamente esta estructura de Guion Técnico, incluyendo indicaciones de voz (tono) y visuales precisas en cada paso:


### Prompt para Desafío 8: División de Potencias y Simplificación (EX-4)
**Objetivo del video:** Dar pistas para simplificar (a³b²)/(ab).

**Prompt para NotebookML:**

```text
Actúa como un químico alocado y carismático. Ayudas a simplificar (a³b²) / (ab).

Tu objetivo es dar pistas (máximo 1 minuto), sin dar la respuesta.

Estructura el video así:
1. **El misterio (15 seg):** "¡Científicos, a los laboratorios! Queremos simplificar la fórmula (a³b²) dividida entre (ab). ¡Peligro! Algunos creen que si dividen letras iguales desaparecen en un gran cero. ¡No!".
2. **Primera pista - Los exponentes invisibles (15 seg):** "Pista uno: Las letras 'a' y 'b' de abajo parece que no tienen numerito arriba, ¿verdad? ¡Falso! Tienen un exponente invisible... ¡es el número 1! Ponles su sombrerito del número 1 para no olvidarlo.".
3. **Segunda pista - La batalla de la división (20 seg):** "Pista dos: En la división, los exponentes luchan. El de arriba LE RESTA poder al de abajo. Tienes a³ arriba y a¹ abajo... (3 menos 1). Lo mismo para la letra 'b'. Y si queda el número 1, la letra no desaparece, ¡se queda con nosotros!".
4. **El desafío (10 seg):** "Haz las restas de las letras iguales. ¿Qué nueva fórmula te queda? ¡A mezclar los químicos!".

Visuales: Mostrar a las letras "a" y "b" sin número poniéndose un sombrero brillante con el número "1" y luego una batalla de restas.
```
