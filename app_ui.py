# ============================================================================
# INTERFAZ WEB - INTELIGENCIA EN OPERACIONES
# Similar a ChatGPT/Gemini interface
# ============================================================================

import streamlit as st
import sys
import logging
from pathlib import Path
from typing import Optional

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from prueba import (
    resolver_problema_io, 
    diagnosticar_sistema,
    vector_store,
    GROQ_API_KEY,
    GROQ_MODEL,
    logger
)

# ============================================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="🧮 Inteligencia en Operaciones",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS PERSONALIZADOS
# ============================================================================

st.markdown("""
<style>
    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 12px;
    }
    .stTextArea > div > div > textarea {
        font-size: 14px;
        padding: 12px;
    }
    .message-box {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid;
    }
    .user-message {
        border-left-color: #0084ff;
        background-color: #e3f2fd;
    }
    .assistant-message {
        border-left-color: #34a853;
        background-color: #f1f8e9;
    }
    .error-message {
        border-left-color: #d32f2f;
        background-color: #ffebee;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZACIÓN DE SESIÓN
# ============================================================================

if "historial" not in st.session_state:
    st.session_state.historial = []
    
if "api_ready" not in st.session_state:
    st.session_state.api_ready = bool(GROQ_API_KEY)


def separar_respuesta_y_sugerencia(respuesta: str) -> tuple[str, Optional[str]]:
    """Separa la respuesta principal de la sugerencia final, si existe."""
    marcador = "💡 SUGERENCIA DE SOLUCIÓN"
    if marcador in respuesta:
        principal, sugerencia = respuesta.split(marcador, 1)
        return principal.strip(), sugerencia.strip()
    return respuesta, None

# ============================================================================
# HEADER
# ============================================================================

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🧮 Inteligencia en Operaciones")
    st.caption("Resolvedor inteligente de problemas de Investigación de Operaciones")

# ============================================================================
# SIDEBAR - INFORMACIÓN Y DIAGNOSTICO
# ============================================================================

with st.sidebar:
    st.header("📊 Sistema")
    
    # Estado del sistema
    col1, col2 = st.columns(2)
    with col1:
        st.metric("API Groq", "✅" if GROQ_API_KEY else "❌")
    with col2:
        st.metric("ChromaDB", "✅" if vector_store else "❌")
    
    st.divider()
    
    # Información técnica
    st.subheader("⚙️ Configuración")
    st.text(f"Modelo: {GROQ_MODEL}")
    
    if vector_store:
        try:
            doc_count = vector_store._collection.count()
            st.text(f"Documentos: {doc_count}")
        except:
            st.text("Documentos: N/A")
    
    st.divider()
    
    # Historial
    st.subheader("📝 Historial")
    if st.button("🗑️ Limpiar historial", use_container_width=True):
        st.session_state.historial = []
        st.rerun()
    
    if st.session_state.historial:
        st.text(f"Consultas: {len(st.session_state.historial)}")
    else:
        st.info("Sin historial aún")
    
    st.divider()
    
    # Ayuda
    st.subheader("❓ Tipos de problemas")
    tipos = [
        "Programación Lineal Continua",
        "Programación Lineal Entera",
        "Rutas y Grafos",
        "Teoría y Conceptos"
    ]
    for tipo in tipos:
        st.caption(f"• {tipo}")

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

# Verificar API
if not GROQ_API_KEY:
    st.error("❌ **API Key de Groq no configurada**")
    st.info("Define GROQ_API_KEY en el archivo .env")
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📚 Ejemplos", "🔍 Diagnóstico"])

# ============================================================================
# TAB 1: CHAT (MAIN)
# ============================================================================

with tab1:
    st.subheader("Describe tu problema de Investigación de Operaciones")
    
    # Input del usuario
    problema = st.text_area(
        "📝 Ingresa tu problema:",
        placeholder="""Ejemplo: Una empresa fabrica dos productos A y B.
- Ganancia: A=$40/unidad, B=$30/unidad  
- Restricciones:
  * Máquina: 2A + 1B ≤ 100 horas
  * Mano de obra: 1A + 2B ≤ 80 horas
¿Cuál es el plan óptimo de producción?""",
        height=150,
        key="problema_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        resolver_btn = st.button("🚀 Resolver", use_container_width=True, type="primary")
    with col2:
        ejemplo_btn = st.button("📋 Cargar Ejemplo", use_container_width=True)
    with col3:
        limpiar_btn = st.button("🗑️ Limpiar", use_container_width=True)
    
    # Acciones
    if limpiar_btn:
        st.session_state.problema_input = ""
        st.rerun()

    if ejemplo_btn:
        st.session_state.problema_input = (
            "Una empresa fabrica dos productos A y B. "
            "Ganancias: A=$40/unidad, B=$30/unidad. "
            "Restricciones: 2A + B <= 100, A + 2B <= 80, A,B >= 0. "
            "Encuentra el plan óptimo de producción."
        )
        st.rerun()
    
    if resolver_btn and problema.strip():
        with st.spinner("🤔 Procesando..."):
            try:
                respuesta = resolver_problema_io(problema)
                
                # Guardar en historial
                st.session_state.historial.append({
                    "problema": problema,
                    "respuesta": respuesta
                })
                
                # Mostrar resultado
                st.success("✅ Problema resuelto")

                respuesta_principal, sugerencia = separar_respuesta_y_sugerencia(respuesta)
                
                with st.container(border=True):
                    st.markdown("### 📤 Resultado:")
                    st.markdown(respuesta_principal)

                if sugerencia:
                    st.success(f"✅ Recomendación final\n\n{sugerencia}")
                
                # Opciones
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Descargar respuesta",
                        data=respuesta,
                        file_name="solucion_io.txt",
                        mime="text/plain"
                    )
                with col2:
                    if st.button("💾 Guardar en historial"):
                        st.info("✅ Guardado en historial")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif resolver_btn:
        st.warning("⚠️ Por favor ingresa un problema")
    
    # Mostrar historial si existe
    if st.session_state.historial:
        st.divider()
        st.subheader("📜 Historial de esta sesión")
        
        for i, item in enumerate(st.session_state.historial):
            with st.expander(f"Consulta #{i+1}: {item['problema'][:50]}..."):
                st.markdown("**Problema:**")
                st.text(item['problema'])
                st.markdown("**Respuesta:**")
                respuesta_principal, sugerencia = separar_respuesta_y_sugerencia(item['respuesta'])
                st.markdown(respuesta_principal)
                if sugerencia:
                    st.success(f"✅ Recomendación final\n\n{sugerencia}")

# ============================================================================
# TAB 2: EJEMPLOS
# ============================================================================

with tab2:
    st.subheader("📚 Ejemplos Predefinidos")
    
    ejemplos = {
        "PL Continua - Producción": """
        Una fábrica produce dos tipos de mesas: M1 y M2.
        
        **Ganancias:**
        - M1: $80 por unidad
        - M2: $60 por unidad
        
        **Recursos disponibles:**
        - Madera: 300 unidades
        - Mano de obra: 240 horas
        
        **Requerimientos por unidad:**
        - M1: 6 unidades madera, 8 horas trabajo
        - M2: 8 unidades madera, 6 horas trabajo
        
        Encontrar el plan óptimo de producción que maximice ganancias.
        """,
        
        "PL Entera - Asignación": """
        Una empresa necesita asignar 3 trabajadores a 3 proyectos.
        
        **Costos de asignación (en miles):**
        - Trabajador 1: Proyecto A=$10, B=$12, C=$11
        - Trabajador 2: Proyecto A=$14, B=$10, C=$9
        - Trabajador 3: Proyecto A=$11, B=$13, C=$10
        
        Cada trabajador debe asignarse a exactamente un proyecto.
        Minimizar costo total de asignación.
        """,
        
        "Ruta Más Corta": """
        Tienes una red de ciudades con las siguientes conexiones:
        
        - Madrid ↔ Barcelona: 620 km
        - Madrid ↔ Sevilla: 540 km
        - Barcelona ↔ Valencia: 360 km
        - Sevilla ↔ Valencia: 720 km
        - Valencia ↔ Bilbao: 420 km
        - Sevilla ↔ Bilbao: 780 km
        
        ¿Cuál es la ruta más corta de Madrid a Bilbao?
        """,
        
        "Teoría - Simplex": """
        Explícame en detalle el método simplex: 
        - Qué es y para qué sirve
        - Pasos del algoritmo
        - Cuándo es más eficiente
        - Comparación con otros métodos
        """
    }
    
    col1, col2 = st.columns(2)
    
    for idx, (titulo, contenido) in enumerate(ejemplos.items()):
        with (col1 if idx % 2 == 0 else col2):
            if st.button(f"📌 {titulo}", use_container_width=True):
                st.session_state.problema_input = contenido
                st.success("✅ Ejemplo cargado. Ve a la pestaña '💬 Chat' y pulsa '🚀 Resolver'.")
                st.rerun()

# ============================================================================
# TAB 3: DIAGNÓSTICO
# ============================================================================

with tab3:
    st.subheader("🔍 Diagnóstico del Sistema")
    
    if st.button("🔄 Ejecutar diagnóstico completo", use_container_width=True):
        with st.spinner("Diagnosticando..."):
            try:
                # Capturar output
                import io
                from contextlib import redirect_stdout
                
                f = io.StringIO()
                with redirect_stdout(f):
                    diagnosticar_sistema()
                
                diagnostico = f.getvalue()
                st.code(diagnostico, language="text")
                st.success("✅ Diagnóstico completado")
                
            except Exception as e:
                st.error(f"Error en diagnóstico: {e}")

    if st.button("🧪 Ejecutar autoprueba end-to-end", use_container_width=True):
        with st.spinner("Ejecutando autoprueba..."):
            try:
                prueba_prompt = (
                    "Resuelve: Maximizar Z=40x1+30x2 sujeto a "
                    "2x1+x2<=100, x1+2x2<=80, x1,x2>=0"
                )
                respuesta_prueba = resolver_problema_io(prueba_prompt)

                st.markdown("### Resultado de autoprueba")
                st.code(respuesta_prueba, language="text")

                if "❌ Error" in respuesta_prueba or "ERROR" in respuesta_prueba.upper():
                    st.error("❌ La autoprueba falló: el agente devolvió un error.")
                elif all(token in respuesta_prueba for token in ["40", "20", "2200"]):
                    st.success("✅ Autoprueba aprobada: flujo completo operativo (modelo + tools + resolución).")
                else:
                    st.warning("⚠️ La autoprueba respondió, pero el formato no coincide exactamente con el esperado.")
            except Exception as e:
                st.error(f"❌ Error en autoprueba: {e}")
    
    st.divider()
    
    st.subheader("📋 Estado de Componentes")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("API Groq", "🟢" if GROQ_API_KEY else "🔴")
    with col2:
        st.metric("ChromaDB", "🟢" if vector_store else "🔴")
    with col3:
        st.metric("Modelo", GROQ_MODEL.split("/")[-1][:10])
    with col4:
        st.metric("Historial", len(st.session_state.historial))
    
    st.divider()
    
    st.subheader("🛠️ Herramientas disponibles")
    
    herramientas_info = {
        "🔍 Búsqueda Teórica": "Busca conceptos en el libro de Investigación de Operaciones",
        "📊 PL Continua": "Resuelve problemas de programación lineal continua (SciPy)",
        "🔢 PL Entera": "Resuelve problemas de programación lineal entera/mixta (PuLP)",
        "🗺️ Dijkstra": "Encuentra rutas más cortas en grafos"
    }
    
    for herramienta, desc in herramientas_info.items():
        with st.expander(herramienta):
            st.write(desc)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🧮 **Inteligencia en Operaciones**")
    st.caption("Powered by LangChain + Groq")
with col2:
    st.caption("📚 Base de conocimiento: Hillier & Lieberman")
with col3:
    st.caption("✨ Versión 1.0")
