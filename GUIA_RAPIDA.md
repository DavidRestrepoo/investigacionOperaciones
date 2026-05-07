# 🚀 GUÍA DE INICIO RÁPIDO

## Paso 1: Instalación (Primera vez)

```powershell
# En PowerShell, dentro del directorio del proyecto:
python -m pip install -r requirements.txt
```

Esto puede tomar 5-10 minutos dependiendo de tu conexión.

## Paso 2: Verificar la instalación

```powershell
python verificador.py --diagnose
```

Deberías ver:
- ✅ PDF encontrado
- ✅ ChromaDB funcionando
- ✅ API Groq configurada
- ✅ Herramientas matemáticas disponibles

## Paso 3: Ejecutar la aplicación

### Opción A: Interfaz Web (Recomendada)

```powershell
streamlit run app_ui.py
```

Se abrirá automáticamente en tu navegador.

### Opción B: Línea de comandos

```powershell
python prueba.py
```

## ¿Qué puedo hacer?

### 1. Resolver Problemas de Programación Lineal

**Ejemplo:**
```
Maximizar: Z = 40x + 30y
Sujeto a:
  - 2x + y ≤ 100
  - x + 2y ≤ 80
  - x, y ≥ 0

¿Cuál es la solución óptima?
```

### 2. Encontrar Rutas Más Cortas

**Ejemplo:**
```
Tengo ciudades conectadas:
A-B: 4, A-C: 2, B-C: 1, B-D: 5, C-D: 8, C-E: 10, D-E: 2

¿Cuál es la ruta más corta de A a E?
```

### 3. Aprender Conceptos de Investigación de Operaciones

**Ejemplo:**
```
¿Qué es el método Simplex? ¿Cómo funciona?
```

## Troubleshooting

### Error: "No module named 'langchain_chroma'"

```powershell
# Instalar solo lo necesario:
python -m pip install langchain langchain-community langchain-groq langchain-chroma chromadb
```

### Error: "GROQ_API_KEY no configurada"

Verifica que el archivo `.env` existe y contiene:
```
GROQ_API_KEY=tu_api_key_de_groq
GROQ_MODEL=llama-3.1-70b-versatile
```

### ChromaDB no funciona

```powershell
# Regenerar la base de datos desde el PDF:
python verificador.py --regenerate-db
```

Esto procesará el PDF y creará la base de datos nuevamente.

## Estructura de Archivos

```
inteligencia-en-operaciones/
├── app_ui.py                    ← Interfaz web (Streamlit)
├── prueba.py                    ← Script principal
├── verificador.py               ← Diagnóstico del sistema
├── .env                         ← Configuración (API keys)
├── requirements.txt             ← Dependencias
├── chroma_db/                   ← Base de datos vectorial
└── README.md                    ← Documentación completa
```

## Componentes del Sistema

| Componente | Función |
|---|---|
| **prueba.py** | Core: Agentes LLM, Herramientas, Solucionadores |
| **app_ui.py** | Interfaz web tipo ChatGPT |
| **verificador.py** | Diagnóstico e instalación |
| **ChromaDB** | Base de conocimiento vectorial del libro |
| **Groq API** | LLM (LLaMA 3.1 70B) |

## Capacidades Principales

✅ **Programación Lineal Continua** (SciPy)
✅ **Programación Lineal Entera** (PuLP)
✅ **Rutas Más Cortas** (Dijkstra)
✅ **Búsqueda Teórica** (RAG)

## Tips

1. **Para problemas complejos**: Describe el problema de forma clara y estruturada
2. **Copia y pega**: Puedes copiar ecuaciones directamente
3. **Historial**: La interfaz web guarda historial de consultas
4. **Ejemplos**: Usa los ejemplos predefinidos como referencia

## ¿Necesitas ayuda?

- Revisa el `README.md` para documentación completa
- Ejecuta `python verificador.py --diagnose` para ver el estado del sistema
- Revisa los ejemplos en la pestaña "Ejemplos" de la interfaz web

---

**¡Listo para resolver problemas de Investigación de Operaciones! 🧮**
