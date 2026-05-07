# 🧮 Inteligencia en Operaciones

Sistema inteligente basado en IA para resolver problemas de **Investigación de Operaciones** usando LLM, RAG y solucionadores numéricos.

## ✨ Características

- **🤖 Agente LLM** basado en Groq (LLaMA-3.1-70B)
- **📚 RAG** con base de datos vectorial (ChromaDB)
- **🔢 Solucionadores numéricos**:
  - Programación Lineal Continua (SciPy)
  - Programación Lineal Entera/Mixta (PuLP)
  - Rutas más cortas (Dijkstra)
- **💬 Interfaz web** tipo ChatGPT (Streamlit)
- **📖 Base de conocimiento** extraída del libro Hillier & Lieberman

## 🚀 Quick Start

## 🌐 Publicar Enlace Desde GitHub (Para Tus Compañeros)

Este proyecto se publica de forma sencilla con **Streamlit Community Cloud** usando tu repositorio de GitHub.

1. Entra a: https://share.streamlit.io
2. Inicia sesión con GitHub.
3. Clic en **New app**.
4. Selecciona:
   - **Repository**: `DavidRestrepoo/investigacionOperaciones`
   - **Branch**: `main`
   - **Main file path**: `app_ui.py`
5. Ve a **Advanced settings > Secrets** y agrega:

```toml
GROQ_API_KEY = "tu_api_key_de_groq"
GROQ_MODEL = "llama-3.1-70b-versatile"
```

6. Clic en **Deploy**.
7. Copia el enlace público generado (por ejemplo: `https://tu-app.streamlit.app`) y compártelo.

Notas:
- El archivo `runtime.txt` fija la versión de Python para el deploy.
- No subas claves reales al repositorio. Usa Secrets del panel de Streamlit.

### 1. Instalación

```bash
# Clonar/descargar el proyecto
cd inteligencia-en-operaciones

# Crear entorno virtual (opcional pero recomendado)
python -m venv .venv

# Activar entorno (Windows)
.\.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración

Crear archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=tu_api_key_de_groq
GROQ_MODEL=llama-3.1-70b-versatile
```

### 3. Verificar Sistema

```bash
python verificador.py --diagnose
```

Si hay problemas con ChromaDB:
```bash
python verificador.py --regenerate-db
```

### 4. Ejecutar Aplicación

**Opción A: Interfaz Web (Recomendado)**
```bash
streamlit run app_ui.py
```
Se abre automáticamente en `http://localhost:8501`

**Opción B: Script de Prueba**
```bash
python prueba.py
```

## 📋 Ejemplos de Uso

### Programación Lineal Continua

```
Una empresa fabrica dos productos: A y B
- Ganancias: A=$40/unidad, B=$30/unidad
- Restricciones:
  * Máquina: 2A + 1B ≤ 100 horas
  * Mano de obra: 1A + 2B ≤ 80 horas
¿Cuál es el plan óptimo de producción?
```

### Rutas Más Cortas

```
Tengo ciudades: A-B: 4km, A-C: 2km, B-C: 1km, B-D: 5km, C-D: 8km, C-E: 10km, D-E: 2km
¿Cuál es la ruta más corta de A a E?
```

### Consultas Teóricas

```
Explícame el método Simplex y sus aplicaciones en programación lineal
```

## 📁 Estructura del Proyecto

```
.
├── prueba.py                 # Core del sistema (agentes, herramientas, solucionadores)
├── app_ui.py                 # Interfaz web con Streamlit
├── verificador.py            # Diagnóstico e integridad del sistema
├── requirements.txt          # Dependencias Python
├── .env                      # Configuración (API keys)
├── chroma_db/               # Base de datos vectorial
│   ├── chroma.sqlite3
│   └── [embeddings...]
├── README.md                # Este archivo
└── Investigacion-Operaciones10Edicion-Frederick-S-Hillier.pdf  # Libro base
```

## 🔧 Componentes Técnicos

### Herramientas Disponibles

| Herramienta | Función | Entrada | Salida |
|---|---|---|---|
| `tool_buscar_teoria` | Búsqueda semántica en libro | Query (str) | Fragmentos relevantes |
| `tool_resolver_lp_continua` | PL continua (SciPy) | c, A_ub, b_ub, bounds | Solución óptima |
| `tool_resolver_lp_entera` | PL entera (PuLP) | JSON con problema | Solución óptima |
| `tool_ruta_mas_corta_dijkstra` | Caminos mínimos | Aristas, nodos | Ruta y distancia |

### Stack Tecnológico

- **LLM**: Groq (LLaMA 3.1 70B)
- **Framework**: LangChain + LanggGraph
- **Vector DB**: ChromaDB
- **Embeddings**: all-MiniLM-L6-v2 (HuggingFace)
- **Solucionadores**: SciPy, PuLP, NumPy
- **UI**: Streamlit
- **Lenguaje**: Python 3.10+

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY no configurada"
- Verificar archivo `.env`
- Usar: `python verificador.py --diagnose`

### Error: "ChromaDB no disponible"
- Ejecutar: `python verificador.py --regenerate-db`
- Asegurarse de que el PDF esté en la raíz del proyecto

### Error: "Modelo no encontrado"
- Verificar que el modelo esté disponible en Groq
- Por defecto: `llama-3.1-70b-versatile`

### Streamlit no inicia
```bash
# Limpiar caché
streamlit cache clear

# Ejecutar con flags
streamlit run app_ui.py --logger.level=debug
```

## 📊 Capacidades Soportadas

✅ Implementado:
- [x] Programación Lineal Continua
- [x] Programación Lineal Entera/Mixta
- [x] Problemas de Rutas (Dijkstra)
- [x] Búsqueda Teórica (RAG)
- [x] Interfaz interactiva

🟡 Parcial:
- [ ] Análisis de Sensibilidad
- [ ] Visualización de resultados

❌ Futuro:
- [ ] Colas (M/M/1, M/M/c)
- [ ] PERT/CPM
- [ ] Simulación Montecarlo
- [ ] Exportación de reportes

## 🎓 Conceptos de I/O Soportados

1. **Programación Lineal**
   - Método Simplex
   - Variables continuas
   - Restricciones ≤, ≥, =

2. **Programación Entera**
   - Variables enteras (Integer)
   - Variables binarias (Binary)
   - Problemas de asignación

3. **Teoría de Grafos**
   - Caminos más cortos (Dijkstra)
   - Rutas óptimas
   - Redes de transporte

4. **Conceptos Teóricos**
   - Método Simplex
   - Región factible
   - Variables de holgura
   - Dualidad

## 📝 Uso Programático

```python
from prueba import resolver_problema_io

problema = "Maximizar Z = 3x + 2y sujeto a: x + y <= 10, x >= 0, y >= 0"
resultado = resolver_problema_io(problema)
print(resultado)
```

## 🤝 Contribuciones

Se aceptan mejoras, nuevas herramientas y extensiones.

## 📄 Licencia

Proyecto de investigación académica.

## 👤 Autor

Desarrollado para el curso de **Investigación de Operaciones**

## 🔗 Referencias

- Hillier, F. S., & Lieberman, G. J. (2010). **Introduction to Operations Research** (10th ed.)
- LangChain Documentation: https://python.langchain.com
- Groq API: https://console.groq.com

---

**Versión**: 1.0  
**Estado**: ✅ Funcional y listo para usar  
**Última actualización**: 2024
# investigacionOperaciones
# investigacionOperaciones
