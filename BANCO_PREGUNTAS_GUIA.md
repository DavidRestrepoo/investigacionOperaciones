# 📚 Guía: Banco de Preguntas Integrado

## 🎯 ¿Qué es el Banco de Preguntas?

El **Banco de Preguntas (40-preguntas-etapa-2-IO)** es una colección de 40 preguntas de Investigación de Operaciones con respuestas detalladas que ahora está **integrada en el sistema** como base de conocimiento.

### 📊 Contenido del Banco

El banco contiene **40 preguntas** organizadas en **6 secciones**:

| Sección | Preguntas | Temas |
|---------|-----------|-------|
| **Ruta Crítica** | 1-7 | CPM/PERT, holgura, crashing |
| **Flujos en Redes** | 8-14 | Flujo máximo, Ford-Fulkerson, redes residuales |
| **Logística y Transporte** | 15-21 | Método Vogel, balanceo, transbordo |
| **Inventarios** | 22-28 | EOQ, ROP, nivel de servicio |
| **Teoría de Colas** | 29-35 | Kendall, intensidad de tráfico, M/M/s |
| **Programación No Lineal** | 36-40 | Óptimos locales, Lagrange, optimización |

---

## 🚀 Cómo Funciona la Integración

### 1️⃣ **Carga Automática**

Al iniciar el programa, el sistema:
- ✅ Lee el archivo `banco_preguntas_io.txt`
- ✅ Divide las 40 preguntas en documentos individuales
- ✅ Las convierte a embeddings (vectores numéricos)
- ✅ Las almacena en **ChromaDB** (base de datos vectorial)

```python
# Función que se ejecuta automáticamente:
agregar_banco_preguntas_a_chroma()
```

### 2️⃣ **Búsqueda Inteligente (RAG)**

Cuando haces una pregunta, el sistema:
1. Convierte tu pregunta a vector
2. Busca preguntas similares en ChromaDB
3. Recupera las 6 preguntas más relevantes
4. Las usa como **contexto de referencia** para mejorar la respuesta

**Ejemplo:**
```
Tu pregunta: "¿Cómo se calcula el tiempo esperado en PERT?"
↓
ChromaDB busca y encuentra: Pregunta 2 del banco (tiempo esperado PERT)
↓
El agente LLM usa esa respuesta como modelo para su explicación
```

### 3️⃣ **Formato de Respuesta Mejorado**

El agente ahora responde siguiendo el patrón del banco:

```
┌─────────────────────────────────────────────────────────┐
│ CLASIFICACIÓN: [Tipo de problema]                       │
│                                                          │
│ OPCIONES:                                                │
│ A) ... | B) ... | C) ... | D) ...                       │
│                                                          │
│ RESPUESTA CORRECTA: B                                    │
│                                                          │
│ EXPLICACIÓN DETALLADA:                                   │
│ • Fundamentación teórica                                 │
│ • Fórmulas clave                                         │
│ • Desarrollo paso a paso                                 │
│ • Ejemplo numérico                                       │
│ • Interpretación práctica                                │
│                                                          │
│ CONCLUSIÓN:                                              │
│ [Síntesis educativa]                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Pregunta sobre PERT

**Tu entrada:**
```
¿Cuándo tengo optimista=2, probable=5, pesimista=14, 
cuál es el tiempo esperado en PERT?
```

**Respuesta del sistema (siguiendo modelo del banco):**
```
CLASIFICACIÓN: Teoría de Proyectos / PERT

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

La fórmula da mayor peso (coeficiente 4) al tiempo más probable...
```

### Ejemplo 2: Pregunta sobre EOQ

**Tu entrada:**
```
Si el costo de mantener aumenta, ¿qué pasa con el lote óptimo Q?
```

**Respuesta (siguiendo modelo del banco):**
```
CLASIFICACIÓN: Gestión de Inventarios / EOQ

EXPLICACIÓN DETALLADA:
La fórmula de Wilson (EOQ) es:
Q = √(2DS / H)

Análisis matemático:
H está en el DENOMINADOR. Cuando H aumenta:
- El término (2DS / H) disminuye
- Por lo tanto √(2DS / H) disminuye
- Conclusión: Q disminuye

Ejemplo numérico:
Si D=1000, S=50:
- Si H=10: Q = √(10000) = 100 unidades
- Si H=20: Q = √(5000) = 70.7 unidades
- Mayor H → Menor Q

Interpretación económica:
Si mantener inventario es más caro, se piden cantidades menores 
pero más frecuentemente...
```

---

## 🔍 Búsqueda Directa en el Banco

### Opción 1: Pregunta Similar
Si tu pregunta es similar a alguna del banco, el sistema:
- La encontrará automáticamente
- Usará esa respuesta como referencia
- Adaptará la explicación a tu contexto específico

### Opción 2: Pregunta el Número Directamente
```
"Pregunta 15 del banco: En el método de Vogel..."
"¿Cuál es la respuesta de la pregunta 22?"
```

### Opción 3: Por Tema
```
"¿Qué preguntas tienes sobre flujo máximo?"
"Explícame las preguntas de teoría de colas"
```

---

## 📈 Ventajas de la Integración

| Ventaja | Beneficio |
|---------|-----------|
| **Contexto enriquecido** | El sistema "conoce" 40 ejemplos de examen |
| **Respuestas consistentes** | Sigue un formato probado de examen |
| **Explicaciones detalladas** | No solo responde, enseña paso a paso |
| **Ejemplos concretos** | Cada tema tiene un caso de estudio |
| **Búsqueda inteligente** | Recupera automáticamente preguntas relevantes |
| **Mejor para estudiantes** | Aprenden metodología de respuesta correcta |

---

## ⚙️ Detalles Técnicos

### Estructura del Archivo

```
banco_preguntas_io.txt
├── SECCIÓN 1: RUTA CRÍTICA
│   ├── PREGUNTA 1: [enunciado]
│   │   ├── OPCIONES: A), B), C), D)
│   │   ├── RESPUESTA CORRECTA: [letra]
│   │   └── EXPLICACIÓN DETALLADA: [desarrollo]
│   ├── PREGUNTA 2: ...
│   └── ...
├── SECCIÓN 2: FLUJOS EN REDES
│   └── ...
└── ...
```

### Cómo se Indexa en ChromaDB

```
Cada pregunta se convierte en:
{
  "page_content": "[Pregunta + Opciones + Respuesta + Explicación]",
  "metadata": {
    "source": "banco_preguntas_io",
    "pregunta_numero": 15,
    "tipo": "examen_io"
  }
}
```

### Búsqueda RAG

Cuando haces una pregunta:
```
1. Tu pregunta se convierte a vector (embedding)
2. Se compara con los 40 vectores del banco
3. ChromaDB retorna las 6 preguntas más similares
4. El agente LLM utiliza esas como contexto
5. Genera respuesta en el formato del banco
```

---

## 🛠️ Regenerar el Banco

Si necesitas regenerar la base de datos vectorial:

```python
# En prueba.py:
python -c "from prueba import agregar_banco_preguntas_a_chroma; agregar_banco_preguntas_a_chroma()"
```

O simplemente:
```bash
# Elimina la carpeta chroma_db y reinicia
rm -r ./chroma_db
python app_ui.py
```

---

## 📝 Preguntas Frecuentes

### P: ¿Qué pasa si hago una pregunta que no está exactamente en el banco?

**R:** El sistema busca preguntas *similares* usando similitud vectorial. Por ejemplo:
- Si preguntas sobre "lote óptimo", encontrará la pregunta 22 (EOQ)
- Si preguntas sobre "ruta crítica", encontrará preguntas 1-7

### P: ¿Las respuestas son exactas al banco?

**R:** No necesariamente. El sistema usa el banco como **referencia de estilo y contenido**, pero adapta la respuesta a tu pregunta específica. Así aprenderás mejor.

### P: ¿Puedo agregar más preguntas al banco?

**R:** Sí, simplemente:
1. Agrega más preguntas al archivo `banco_preguntas_io.txt`
2. Llama `agregar_banco_preguntas_a_chroma()` 
3. O reconstruye ChromaDB

### P: ¿El banco se actualiza automáticamente?

**R:** El sistema carga el banco cada vez que inicia. Si cambias el archivo, se usará la versión nueva en el siguiente reinicio.

---

## 🎓 Recomendaciones para Estudiantes

1. **Estudia el banco** antes de usarlo
2. **Intenta resolver preguntas** sin consultarlo
3. **Usa el sistema** para verificar y entender tu error
4. **Lee las explicaciones** paso a paso
5. **Practica con variaciones** de las preguntas
6. **Genera tus propias preguntas** y verifica con el sistema

---

## 📞 Soporte

Si el banco no se carga:
```bash
python verificador.py --diagnose
```

Esto mostrará el estado de:
- ✅ Archivo del banco (`banco_preguntas_io.txt`)
- ✅ ChromaDB e inicialización
- ✅ Embeddings
- ✅ API de Groq

---

**¡Ahora tu sistema educativo es más potente! 🚀**
