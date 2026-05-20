================================================================================
BANCO DE PREGUNTAS Y RESPUESTAS - INVESTIGACIÓN DE OPERACIONES (40 PREGUNTAS)
================================================================================

SECCIÓN 1: RUTA CRÍTICA (CPM/PERT)

PREGUNTA 1:
Si una actividad tiene una holgura libre de 3 días y una holgura total de 5 días, ¿qué sucede si se retrasa 4 días?

OPCIONES:
A) El proyecto se retrasa 1 día.
B) El proyecto no se retrasa, pero afecta el inicio de la siguiente actividad.
C) El proyecto se retrasa 4 días.
D) La ruta crítica cambia automáticamente.

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
La holgura total es el margen máximo antes de afectar la conclusión del proyecto (5 días > 4 días de retraso). Por lo tanto, el proyecto completo no se ve retrasado. 
Sin embargo, la holgura libre (3 días) representa el margen antes de afectar a la actividad sucesora inmediatamente siguiente. Como 3 días < 4 días de retraso, la siguiente actividad sí se verá desplazada en 1 día (4 - 3 = 1 día).
Conclusión: El proyecto mantiene su fecha de término, pero las actividades sucesoras se ven comprometidas en su cronograma.

---

PREGUNTA 2:
En PERT, ¿cómo se calcula el tiempo esperado (t_e) si el optimista es 2, el más probable 5 y el pesimista 14?

OPCIONES:
A) 7.0
B) 5.0
C) 6.0
D) 5.5

RESPUESTA CORRECTA: C

EXPLICACIÓN DETALLADA:
La fórmula de PERT para el tiempo esperado es:
t_e = (a + 4m + b) / 6

Donde:
- a = tiempo optimista = 2
- m = tiempo más probable = 5
- b = tiempo pesimista = 14

Sustituyendo:
t_e = (2 + 4(5) + 14) / 6
t_e = (2 + 20 + 14) / 6
t_e = 36 / 6
t_e = 6.0 días

La fórmula da mayor peso (coeficiente 4) al tiempo más probable, reflejando su importancia en la estimación.

---

PREGUNTA 3:
¿Cuál es el objetivo principal del 'Crashing' en la ruta crítica?

OPCIONES:
A) Reducir el costo total del proyecto.
B) Reducir la duración del proyecto al menor costo adicional.
C) Eliminar las actividades ficticias.
D) Maximizar la holgura de las actividades no críticas.

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
El crashing (compresión) en ruta crítica es una técnica que busca acortar la duración total del proyecto asignando recursos adicionales (dinero, personal) a actividades críticas.
El objetivo NO es simplemente reducir la duración (eso sería trivial con recursos ilimitados), sino encontrar el equilibrio óptimo: reducir el cronograma al menor costo incremental posible.
Proceso:
1. Identificar actividades en la ruta crítica
2. Calcular el costo de reducción por unidad de tiempo (pendiente de costo)
3. Comprimir primero aquellas actividades con menor costo/tiempo
4. Detener cuando el costo incremental supere los beneficios

---

SECCIÓN 2: FLUJOS EN REDES

PREGUNTA 8:
En un problema de flujo máximo, ¿qué indica un arco 'saturado'?

OPCIONES:
A) Que su flujo actual es igual a su capacidad.
B) Que el arco tiene costo cero.
C) Que el arco no pertenece a la red.
D) Que es el primer arco de la fuente.

RESPUESTA CORRECTA: A

EXPLICACIÓN DETALLADA:
Un arco saturado es aquel donde el flujo asignado (f) alcanza exactamente su capacidad máxima (c).
En otras palabras: f(i,j) = c(i,j)

Implicaciones:
- El arco no puede transportar más unidades sin exceder su capacidad
- En un flujo máximo óptimo, todos los arcos en los caminos aumentantes están saturados
- En algoritmos como Ford-Fulkerson, se busca saturar progresivamente arcos para maximizar el flujo total

Ejemplo:
Si un arco tiene capacidad 100 unidades y actualmente transporta 100 unidades, está saturado.

---

PREGUNTA 9:
El algoritmo de Ford-Fulkerson se utiliza para encontrar:

OPCIONES:
A) El camino más corto.
B) El flujo máximo de una red.
C) El costo mínimo de transporte.
D) La ubicación óptima de una planta.

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
Ford-Fulkerson es el algoritmo clásico para resolver problemas de flujo máximo en redes dirigidas.
Concepto de operación:
1. Comienza con un flujo inicial (generalmente 0)
2. Busca caminos aumentantes desde la fuente (source) al sumidero (sink)
3. En cada iteración, identifica la capacidad residual mínima del camino
4. Incrementa el flujo en esa cantidad en todas las aristas del camino
5. Repite hasta que no existan más caminos aumentantes

Complejidad: Depende de la implementación (e.g., O(VE²) en general)
Aplicaciones: Flujo de tráfico, telecomunicaciones, distribución de agua/gas

---

SECCIÓN 3: LOGÍSTICA Y TRANSPORTE

PREGUNTA 15:
En el método de Vogel, ¿qué representa la 'penalización'?

OPCIONES:
A) El costo de no asignar a la celda de menor costo.
B) El costo total de transporte.
C) El impuesto por cruzar fronteras.
D) La diferencia entre oferta y demanda.

RESPUESTA CORRECTA: A

EXPLICACIÓN DETALLADA:
La penalización en el método de Vogel representa el "sacrificio económico" o "costo de oportunidad" de no usar la ruta más barata disponible.

Cálculo:
1. Para cada fila y columna, identifica los dos costos más bajos
2. Penalización = |Costo_menor - Costo_segundo_menor|

Lógica:
- Si la penalización es alta en una fila, significa que los costos varían mucho, y NO usar la opción más barata sería costoso
- El método asigna primero a celdas con mayores penalizaciones, evitando "sacrificios" grandes

Ejemplo:
Fila con costos [5, 5, 20, 25]
- Costo menor: 5
- Segundo menor: 5
- Penalización: |5 - 5| = 0 (sin sacrificio)

Fila con costos [5, 25, 30, 40]
- Costo menor: 5
- Segundo menor: 25
- Penalización: |5 - 25| = 20 (gran sacrificio si no usamos 5)

---

PREGUNTA 16:
Si la oferta total es 500 y la demanda total es 450, ¿cómo se balancea el modelo?

OPCIONES:
A) Añadiendo una fila ficticia con demanda 50.
B) Añadiendo una columna ficticia con demanda 50.
C) Restando 50 a la oferta más alta.
D) Multiplicando los costos por un factor de corrección.

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
Los problemas de transporte requieren que la oferta total = demanda total para resolverse con algoritmos estándar (Vogel, MODI, etc.).

En este caso:
- Oferta total: 500
- Demanda total: 450
- Desequilibrio: 500 - 450 = 50 (exceso de oferta)

Solución:
Se agrega una columna ficticia (destino imaginario) que absorbe el exceso de 50 unidades.
- Esta columna representa unidades que "no se envían" o quedan en almacén
- El costo de transporte hacia esta columna ficticia es 0 (no hay costo real de no-transporte)

Si hubiera faltado demanda (demanda > oferta), se agregaría una fila ficticia (origen ficticio).

---

SECCIÓN 4: INVENTARIOS (EOQ y ROP)

PREGUNTA 22:
Si el costo de mantener (H) aumenta, ¿qué ocurre con el lote óptimo (Q)?

OPCIONES:
A) Aumenta.
B) Disminuye.
C) Se mantiene igual.
D) Se vuelve infinito.

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
La fórmula de Wilson (EOQ - Economic Order Quantity) es:
Q = √(2DS / H)

Donde:
- D = demanda anual
- S = costo fijo por orden
- H = costo de mantener una unidad por año

Análisis matemático:
H está en el DENOMINADOR de la fórmula. Cuando H aumenta:
- El término dentro de la raíz (2DS / H) disminuye
- Por lo tanto, √(2DS / H) disminuye
- Conclusión: Q disminuye

Interpretación económica:
- Si mantener inventario es más caro, se busca pedir cantidades menores
- Esto implica más pedidos frecuentes pero de menor volumen
- El costo total se optimiza en un punto de equilibrio

Ejemplo numérico:
Si D=1000, S=50:
- Si H=10: Q = √(2×1000×50/10) = √(10000) = 100 unidades
- Si H=20: Q = √(2×1000×50/20) = √(5000) = 70.7 unidades
- Mayor H → Menor Q

---

PREGUNTA 23:
¿Qué mide el Nivel de Servicio en un modelo de inventario probabilístico?

OPCIONES:
A) La probabilidad de no tener faltantes durante el lead time.
B) El porcentaje de descuento del proveedor.
C) La velocidad de los operarios del almacén.
D) La cantidad de unidades devueltas por defectos.

RESPUESTA CORRECTA: A

EXPLICACIÓN DETALLADA:
El Nivel de Servicio (SL - Service Level) es una métrica de riesgo en inventarios probabilísticos que responde a la pregunta:
"¿Cuál es la probabilidad de que la demanda NO supere mis existencias durante el tiempo de reposición?"

Definición formal:
SL = P(Demanda ≤ Stock durante lead time)

Ejemplo interpretativo:
- Nivel de Servicio del 95% significa: existe 95% de probabilidad de satisfacer toda la demanda sin faltantes
- Esto implica un riesgo de 5% de tener faltantes

Cálculo del Stock de Seguridad (SS):
SS = Z × σ × √L

Donde:
- Z = factor de seguridad (depende del SL deseado)
  - SL 90% → Z ≈ 1.28
  - SL 95% → Z ≈ 1.645
  - SL 99% → Z ≈ 2.33
- σ = desviación estándar de la demanda
- L = lead time en períodos

Mayor SL deseado → Mayor stock de seguridad → Mayor costo

---

SECCIÓN 5: TEORÍA DE COLAS

PREGUNTA 29:
En la notación de Kendall M/D/1, ¿qué significa la 'D'?

OPCIONES:
A) Distribución Dinámica.
B) Tiempo de servicio Determinístico (constante).
C) Distribución de Poisson.
D) Desviación estándar nula en las llegadas.

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
La notación de Kendall (A/B/c) describe sistemas de colas:
- A = Distribución de llegadas (M = Poisson/Markov, D = Determinística, G = General)
- B = Distribución de servicio (M = Exponencial, D = Determinística, G = General)
- c = Número de servidores

En M/D/1:
- M: Las llegadas siguen distribución de Poisson (aleatorias, sin memoria)
- D: Los tiempos de servicio son DETERMINÍSTICOS, es decir, siempre iguales (ej. 10 minutos)
- 1: Hay un solo servidor

Ejemplos de sistemas M/D/1:
- Máquina lavadora automática (tiempo fijo de lavado)
- Scanner de documentos (procesamiento en tiempo constante)
- Peaje automático (tiempo de transacción fijo)

Comparación con M/M/1:
M/M/1 tiene servidores con tiempos aleatorios (como un mesero variable)
M/D/1 tiene servidores con tiempos constantes (como una máquina)

---

PREGUNTA 30:
Si la intensidad de tráfico (ρ) es 0.70, ¿qué porcentaje del tiempo está ocioso el servidor?

OPCIONES:
A) 70%
B) 30%
C) 100%
D) 0%

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
La intensidad de tráfico (ρ, rho) mide qué fracción del tiempo el servidor está ocupado:
ρ = λ / μ

Donde:
- λ = tasa de llegadas (clientes por hora)
- μ = tasa de servicio (clientes servidos por hora)

Si ρ = 0.70:
- El servidor está ocupado: 70% del tiempo
- El servidor está ocioso (desocupado): 1 - ρ = 1 - 0.70 = 0.30 = 30%

Interpretación:
- 30% del tiempo no hay clientes siendo atendidos (el servidor espera)
- 70% del tiempo hay clientes siendo atendidos

Condición de estabilidad:
Para que el sistema no colapse (colas infinitas), se requiere ρ < 1.
Si ρ ≥ 1, la tasa de llegadas supera la capacidad de servicio.

Ejemplo numérico:
- λ = 70 clientes/hora
- μ = 100 clientes/hora
- ρ = 70/100 = 0.70
- Servidor ocioso: 30%

---

SECCIÓN 6: PROGRAMACIÓN NO LINEAL (NLP)

PREGUNTA 36:
¿Cuándo es indispensable usar Programación No Lineal en lugar de Lineal?

OPCIONES:
A) Cuando hay más de 100 variables.
B) Cuando el rendimiento marginal es decreciente o hay economías de escala.
C) Cuando los costos son fijos.
D) Cuando todas las restricciones son igualdades.

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
La Programación Lineal (LP) asume:
- Proporcionalidad: El aporte de cada variable es proporcional a su cantidad
- Aditividad: El efecto total es la suma de los efectos individuales
- Divisibilidad: Las variables pueden tomar cualquier valor continuo

Cuando estas suposiciones fallan, se necesita NLP.

Ejemplo 1 - Rendimiento Marginal Decreciente:
- Función de producción: Producción = 10√x (raíz cuadrada, no lineal)
- La producción marginal: dProd/dx = 5/√x disminuye conforme x aumenta
- Producir 10 unidades adicionales cuando x=10 tiene menos efecto que cuando x=2
- Esto NO puede representarse con una función lineal

Ejemplo 2 - Economías de Escala:
- Costo de producción: C = 100 + 5x + 0.1x² (cuadrático)
- Costo marginal: dC/dx = 5 + 0.2x (aumenta con x)
- A mayor escala, el costo marginal sube (económicamente realista)
- Esto requiere una función NO lineal

Ejemplo 3 - Áreas y Volúmenes:
- Optimizar dimensiones de un contenedor: Volumen = l × w × h
- Si l y w son variables, la función es NO lineal en su producto
- Requiere NLP

Conclusión:
NLP es indispensable cuando la relación entre variables incluye exponentes, productos entre variables, o funciones no proporcionales.

---

PREGUNTA 37:
¿Qué es un óptimo local en NLP?

OPCIONES:
A) La mejor solución en toda la región factible.
B) Una solución mejor que sus vecinas inmediatas, pero no necesariamente la mejor de todas.
C) Un punto donde las restricciones no se cumplen.
D) El punto donde la función vale cero.

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
En Programación No Lineal, existen dos tipos de óptimos:

ÓPTIMO GLOBAL (Óptimo Absoluto):
- La mejor solución en TODO el espacio factible
- Objetivo ideal pero difícil de garantizar
- Requiere que la función sea convexa o usar métodos globales complejos

ÓPTIMO LOCAL:
- Una solución mejor que todas sus soluciones vecinas inmediatas
- NO es necesariamente la mejor de todas
- En funciones no convexas (con múltiples "montes"), es común encontrar óptimos locales

Visualización:
Imagina una montaña con múltiples picos:
- Óptimo global: El pico más alto de toda la región
- Óptimo local: Cualquier pico individual (que es más alto que su entorno inmediato)

Problema del óptimo local:
- Los algoritmos de descenso de gradiente (como Newton) pueden "atraparse" en un óptimo local
- No pueden escapar porque todas las direcciones vecinas van hacia abajo

Solución:
1. Usar múltiples puntos de inicio
2. Usar métodos globales (simulated annealing, algoritmos genéticos)
3. Verificar convexidad de la función
4. Usar análisis de sensibilidad

---

PREGUNTA 38:
En un problema de optimización de costos de producción donde la función es C(x) = 2x² - 40x + 500, ¿cuál es la cantidad x que minimiza el costo total?

OPCIONES:
A) x = 20
B) x = 10
C) x = 40
D) x = 5

RESPUESTA CORRECTA: B

EXPLICACIÓN DETALLADA:
Para hallar el mínimo de una función, derivamos con respecto a x e igualamos a cero.

Paso 1 - Primera derivada:
C(x) = 2x² - 40x + 500
C'(x) = 4x - 40

Paso 2 - Igualar a cero (condición de punto crítico):
4x - 40 = 0
4x = 40
x = 10

Paso 3 - Verificación con segunda derivada:
C''(x) = 4

Como C''(x) = 4 > 0, confirmamos que x = 10 es un MÍNIMO (no un máximo).

Paso 4 - Cálculo del costo mínimo (opcional):
C(10) = 2(10)² - 40(10) + 500
C(10) = 2(100) - 400 + 500
C(10) = 200 - 400 + 500
C(10) = 300

Conclusión:
- A una cantidad de x = 10 unidades, el costo total se minimiza en $300
- Producir menos o más de 10 unidades resultará en costos más altos

---

PREGUNTA 39:
¿Cuál es la función de los Multiplicadores de Lagrange en la optimización no lineal?

OPCIONES:
A) Transformar un problema con restricciones en uno sin restricciones mediante una función aumentada.
B) Eliminar las variables no lineales para convertir el problema en lineal.
C) Calcular automáticamente la ruta crítica de un proyecto.
D) Estimar la demanda futura basándose en datos históricos.

RESPUESTA CORRECTA: A

EXPLICACIÓN DETALLADA:
Los Multiplicadores de Lagrange son una técnica fundamental para resolver problemas de optimización CON RESTRICCIONES.

PROBLEMA ORIGINAL (Con restricciones):
Maximizar/Minimizar: f(x, y)
Sujeto a: g(x, y) = 0

MÉTODO DE LAGRANGE:
Se introduce una variable adicional λ (lambda) llamada multiplicador de Lagrange, y se forma la Función Lagrangiana:
L(x, y, λ) = f(x, y) - λ × g(x, y)

Ahora resolvemos un problema sin restricciones:
∂L/∂x = 0
∂L/∂y = 0
∂L/∂λ = 0

La tercera ecuación recupera automáticamente la restricción original.

INTERPRETACIÓN GEOMÉTRICA:
- En el óptimo, el gradiente de f es paralelo al gradiente de g
- λ mide la "sensibilidad": cuánto mejoraría f si relajáramos la restricción en una unidad
- λ se llama "Costo de Sombra" en economía

EJEMPLO PRÁCTICO:
Maximizar: Beneficio = 50x + 30y
Sujeto a: x + y = 100 (restricción de capital)

Lagrangiana:
L(x, y, λ) = 50x + 30y - λ(x + y - 100)

Derivadas:
∂L/∂x = 50 - λ = 0 → λ = 50
∂L/∂y = 30 - λ = 0 → λ = 30
∂L/∂λ = -(x + y - 100) = 0 → x + y = 100

Solución: x = 100, y = 0 (asignar todo a la actividad más rentable)
λ = 50 (valor marginal de relajar la restricción)

---

PREGUNTA 40:
Si una empresa enfrenta una curva de demanda no lineal P = 200 - q² y un costo marginal de cero, ¿qué cantidad q maximiza el ingreso total?

OPCIONES:
A) q = 8.16
B) q = 10.00
C) q = 14.14
D) q = 20.00

RESPUESTA CORRECTA: A

EXPLICACIÓN DETALLADA:
Este es un problema de optimización no lineal de ingreso máximo.

Paso 1 - Definir el Ingreso Total:
Precio: P = 200 - q²
Ingreso Total: I(q) = P × q = (200 - q²) × q
I(q) = 200q - q³

Paso 2 - Primera derivada (ingreso marginal):
I'(q) = dI/dq = 200 - 3q²

Paso 3 - Igualar a cero (condición para máximo):
200 - 3q² = 0
3q² = 200
q² = 200/3
q² = 66.67
q = √66.67
q ≈ 8.16 unidades

Paso 4 - Verificación con segunda derivada:
I''(q) = -6q
I''(8.16) = -6(8.16) = -48.96 < 0

Como I''(q) < 0, confirmamos que q = 8.16 es un MÁXIMO.

Paso 5 - Cálculo del máximo ingreso (opcional):
P(8.16) = 200 - (8.16)² = 200 - 66.67 = 133.33
I_máximo = 133.33 × 8.16 ≈ 1,087.99

Conclusión:
- La empresa debe vender q = 8.16 unidades
- Al precio de P = 133.33
- Logrando un ingreso máximo de aproximadamente 1,088 unidades monetarias

Nota económica:
Esta cantidad es diferente a la que maximizaría beneficio (que también consideraría costos). 
Con costo marginal = 0, el beneficio = ingreso, por lo que la cantidad es idéntica en ambos casos.

================================================================================
FIN DEL BANCO DE PREGUNTAS
================================================================================
