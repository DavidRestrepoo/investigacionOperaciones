# ============================================================================
# SISTEMA DE INTELIGENCIA EN OPERACIONES - VERSIÓN MEJORADA
# Solves: Linear Programming (Continuous/Integer), Shortest Paths, Optimization
# ============================================================================

import os
import sys
import json
import logging
import re
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

# Data Science & Math
import pandas as pd
import numpy as np
from scipy.optimize import linprog
import heapq
from collections import defaultdict

# LangChain core & LLM (optional)
LANGCHAIN_AVAILABLE = True
LANGCHAIN_IMPORT_ERROR = ""
RAG_AVAILABLE = True
RAG_IMPORT_ERROR = ""
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_groq import ChatGroq
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage
    from langgraph.prebuilt import create_react_agent
except Exception as e:
    LANGCHAIN_AVAILABLE = False
    LANGCHAIN_IMPORT_ERROR = str(e)

    Chroma = Any  # type: ignore

    def tool(func):
        func.name = func.__name__
        return func

if LANGCHAIN_AVAILABLE:
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_chroma import Chroma
    except Exception as e:
        RAG_AVAILABLE = False
        RAG_IMPORT_ERROR = str(e)
        Chroma = Any  # type: ignore
else:
    RAG_AVAILABLE = False

# Optimization
import pulp
from dotenv import load_dotenv

# Setup console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")


if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY no configurada. Define la variable en .env")

logger.info(f"✅ Usando modelo: {GROQ_MODEL}")
if not LANGCHAIN_AVAILABLE:
    logger.warning(f"⚠️ Modo limitado activo (sin núcleo LangChain): {LANGCHAIN_IMPORT_ERROR}")
elif not RAG_AVAILABLE:
    logger.warning(f"⚠️ Modo sin RAG (agente activo): {RAG_IMPORT_ERROR}")

# ============================================================================
# VERIFICACIÓN E INICIALIZACIÓN DE BASE DE DATOS VECTORIAL (ChromaDB)
# ============================================================================

CHROMA_PATH = Path("./chroma_db")
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") if RAG_AVAILABLE else None
vector_store = None

def verify_and_init_vectordb() -> Optional[Any]:
    """Verifica integridad de ChromaDB y la inicializa"""
    global vector_store

    if not RAG_AVAILABLE:
        return None
    
    if CHROMA_PATH.exists() and any(CHROMA_PATH.iterdir()):
        try:
            logger.info("🔍 Verificando base de datos vectorial...")
            vector_store = Chroma(
                persist_directory=str(CHROMA_PATH), 
                embedding_function=embeddings_model
            )
            # Verificar contenido
            count = vector_store._collection.count()
            logger.info(f"✅ ChromaDB verificada: {count} documentos encontrados")
            return vector_store
        except Exception as e:
            logger.warning(f"⚠️ Error al cargar ChromaDB: {e}. Regenerando...")
            return None
    return None

def init_vectordb_from_pdf() -> Optional[Any]:
    """Inicializa ChromaDB desde PDF si no existe"""
    global vector_store

    if not RAG_AVAILABLE:
        return None
    
    pdf_paths = [
        "./Investigacion-Operaciones10Edicion-Frederick-S-Hillier.pdf",
        "./documentos/Investigacion-Operaciones10Edicion-Frederick-S-Hillier.pdf"
    ]
    
    documentos_pdf = []
    for path in pdf_paths:
        if Path(path).exists():
            try:
                logger.info(f"📖 Cargando PDF: {path}")
                loader = PyPDFLoader(path)
                documentos_pdf = loader.load()
                logger.info(f"✅ PDF cargado: {len(documentos_pdf)} páginas")
                break
            except Exception as e:
                logger.error(f"❌ Error al cargar PDF: {e}")
    
    if not documentos_pdf:
        logger.error("❌ No se pudo cargar el PDF. Usando modo limitado.")
        return None
    
    try:
        logger.info("🔄 Creando embeddings y fragmentos...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " "]
        )
        chunks = text_splitter.split_documents(documentos_pdf)
        logger.info(f"✅ {len(chunks)} fragmentos creados")
        
        logger.info("💾 Guardando en ChromaDB...")
        vector_store = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings_model, 
            persist_directory=str(CHROMA_PATH)
        )
        logger.info("✅ Base de datos vectorial persistida")
        return vector_store
    except Exception as e:
        logger.error(f"❌ Error creando ChromaDB: {e}")
        return None

# Inicializar o verificar ChromaDB
vector_store = verify_and_init_vectordb()
if not vector_store:
    vector_store = init_vectordb_from_pdf()

retriever = vector_store.as_retriever(search_kwargs={"k": 6}) if vector_store else None

# ============================================================================
# HERRAMIENTAS (TOOLS) - SOLUCIONADORES NUMÉRICOS
# ============================================================================

@tool
def tool_buscar_teoria(query: str) -> str:
    """
    Busca conceptos teóricos de Investigación de Operaciones en el libro.
    Úsalo para definiciones, métodos, teoremas y fundamentación matemática.
    """
    if not retriever:
        return "⚠️ Base de conocimiento no disponible"
    try:
        docs = retriever.invoke(query)
        if not docs:
            return "❌ No se encontraron documentos relevantes"
        return "\n---\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"❌ Error en búsqueda: {str(e)}"

@tool
def tool_resolver_lp_continua(c: list, A_ub: Optional[list] = None, b_ub: Optional[list] = None,
                               A_eq: Optional[list] = None, b_eq: Optional[list] = None,
                               bounds: Optional[list] = None) -> str:
    """
    Resuelve Programación Lineal CONTINUA con scipy.optimize.linprog.
    IMPORTANTE: linprog minimiza por defecto. Para maximizar, multiplica c por -1.
    
    Args:
        c: coeficientes función objetivo (lista)
        A_ub: matriz restricciones <= (lista de listas)
        b_ub: vector derecho restricciones <= (lista)
        A_eq: matriz restricciones = (lista de listas)
        b_eq: vector derecho restricciones = (lista)
        bounds: limites variables [(min,max), ...], None=sin límite
    """
    try:
        c = np.array(c, dtype=float)
        A_ub = np.array(A_ub, dtype=float) if A_ub else None
        b_ub = np.array(b_ub, dtype=float) if b_ub else None
        A_eq = np.array(A_eq, dtype=float) if A_eq else None
        b_eq = np.array(b_eq, dtype=float) if b_eq else None
        
        result = linprog(
            c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, 
            bounds=bounds, method='highs'
        )
        
        if result.success:
            sol_dict = {f"x{i+1}": float(result.x[i]) for i in range(len(result.x))}
            return f"✅ ÓPTIMO ENCONTRADO\nSolución: {sol_dict}\nValor Objetivo: {float(result.fun):.4f}"
        else:
            return f"❌ Sin solución óptima: {result.message}"
    except Exception as e:
        return f"❌ Error en PL Continua: {str(e)}"

@tool
def tool_resolver_lp_entera(problema_json: str) -> str:
    """
    Resuelve Programación Lineal ENTERA/MIXTA usando PuLP.
    
    Args:
        problema_json: JSON con estructura:
        {
            "tipo": "maximizar" o "minimizar",
            "variables": [{"nombre": "x1", "tipo": "Continuous/Integer/Binary"}],
            "objetivo": "3*x1 + 2*x2",
            "restricciones": [
                {"expr": "2*x1 + x2 <= 100"},
                {"expr": "x1 + 2*x2 <= 80"}
            ]
        }
    """
    try:
        config = json.loads(problema_json)
        
        prob = pulp.LpProblem(
            "ProblemaIO", 
            pulp.LpMaximize if config.get("tipo", "maximizar") == "maximizar" else pulp.LpMinimize
        )
        
        # Crear variables
        variables = {}
        for var in config.get("variables", []):
            cat = var.get("tipo", "Continuous")
            if cat == "Binary":
                cat = pulp.LpBinary
            elif cat == "Integer":
                cat = pulp.LpInteger
            else:
                cat = pulp.LpContinuous
            
            variables[var["nombre"]] = pulp.LpVariable(var["nombre"], lowBound=0, cat=cat)
        
        # Objetivo
        obj_expr = config.get("objetivo", "")
        prob += eval(obj_expr, {"__builtins__": {}}, variables)
        
        # Restricciones
        for constr in config.get("restricciones", []):
            prob += eval(constr["expr"], {"__builtins__": {}}, variables)
        
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        if pulp.LpStatus[prob.status] == 'Optimal':
            solucion = {v.name: float(v.varValue) for v in prob.variables()}
            return f"✅ ÓPTIMO ENCONTRADO\nSolución: {solucion}\nValor Objetivo: {float(pulp.value(prob.objective)):.4f}"
        else:
            return f"❌ Sin solución óptima: {pulp.LpStatus[prob.status]}"
    except Exception as e:
        return f"❌ Error en PL Entera: {str(e)}"

@tool
def tool_ruta_mas_corta_dijkstra(aristas: list, nodo_inicio: str, nodo_fin: str) -> str:
    """
    Encuentra ruta más corta usando algoritmo de Dijkstra.
    
    Args:
        aristas: lista de dicts {"origen": "A", "destino": "B", "peso": 5}
        nodo_inicio: nodo de partida
        nodo_fin: nodo destino
    """
    try:
        grafo = defaultdict(list)
        nodos = set()
        
        for a in aristas:
            origen = str(a.get('origen', ''))
            destino = str(a.get('destino', ''))
            peso = float(a.get('peso', 1))
            
            nodos.add(origen)
            nodos.add(destino)
            grafo[origen].append((destino, peso))
            grafo[destino].append((origen, peso))  # No dirigido
        
        if nodo_inicio not in nodos or nodo_fin not in nodos:
            return f"❌ Nodos no válidos. Disponibles: {nodos}"
        
        distancias = {nodo: float('inf') for nodo in nodos}
        distancias[nodo_inicio] = 0
        parents = {nodo: None for nodo in nodos}
        pq = [(0, nodo_inicio)]
        visited = set()
        
        while pq:
            dist_actual, nodo_actual = heapq.heappop(pq)
            if nodo_actual in visited:
                continue
            visited.add(nodo_actual)
            
            if nodo_actual == nodo_fin:
                break
            
            for vecino, peso in grafo[nodo_actual]:
                dist_nueva = dist_actual + peso
                if dist_nueva < distancias[vecino]:
                    distancias[vecino] = dist_nueva
                    parents[vecino] = nodo_actual
                    heapq.heappush(pq, (dist_nueva, vecino))
        
        # Reconstruir ruta
        ruta = []
        nodo = nodo_fin
        while nodo is not None:
            ruta.insert(0, nodo)
            nodo = parents[nodo]
        
        if distancias[nodo_fin] == float('inf'):
            return f"❌ No existe ruta entre {nodo_inicio} y {nodo_fin}"
        
        distancia = distancias[nodo_fin]
        ruta_str = " → ".join(ruta)
        return f"✅ RUTA MÁS CORTA ENCONTRADA\nDistancia: {distancia}\nRuta: {ruta_str}"
    except Exception as e:
        return f"❌ Error en Dijkstra: {str(e)}"

@tool
def tool_calcular_ruta_critica_cpm(actividades: list) -> str:
    """
    Calcula la Ruta Crítica (CPM/PERT) para un proyecto dado un conjunto de actividades.
    
    Args:
        actividades: Lista de diccionarios. Ejemplo:
        [
            {"nombre": "A", "duracion": 4, "predecesores": []},
            {"nombre": "B", "duracion": 6, "predecesores": ["A"]},
            {"nombre": "C", "duracion": 2, "predecesores": ["A"]},
            {"nombre": "D", "duracion": 3, "predecesores": ["B", "C"]},
            {"nombre": "E", "duracion": 2, "predecesores": ["D"]}
        ]
    """
    try:
        # 1. Preparar datos
        info = {a['nombre']: a for a in actividades}
        nombres = list(info.keys())
        
        # 2. Forward Pass (ES, EF)
        es = {n: 0 for n in nombres}
        ef = {n: 0 for n in nombres}
        
        # Necesitamos procesar en orden topológico o iterativo
        procesados = set()
        while len(procesados) < len(nombres):
            cambio = False
            for n in nombres:
                if n in procesados: continue
                preds = info[n].get('predecesores', [])
                if not preds or all(p in procesados for p in preds):
                    es[n] = max([ef[p] for p in preds]) if preds else 0
                    ef[n] = es[n] + info[n]['duracion']
                    procesados.add(n)
                    cambio = True
            if not cambio: break # Ciclo detectado o error
            
        # Duración total del proyecto
        duracion_total = max(ef.values()) if ef else 0
        
        # 3. Backward Pass (LS, LF)
        lf = {n: duracion_total for n in nombres}
        ls = {n: 0 for n in nombres}
        
        procesados_back = set()
        while len(procesados_back) < len(nombres):
            cambio = False
            # Nodos que no son predecesores de nadie aún no procesado
            for n in nombres:
                if n in procesados_back: continue
                es_predecesor_de = [m for m in nombres if n in info[m].get('predecesores', [])]
                if not es_predecesor_de or all(m in procesados_back for m in es_predecesor_de):
                    lf[n] = min([ls[m] for m in es_predecesor_de]) if es_predecesor_de else duracion_total
                    ls[n] = lf[n] - info[n]['duracion']
                    procesados_back.add(n)
                    cambio = True
            if not cambio: break
            
        # 4. Calcular Holgura (Slack)
        holgura = {n: lf[n] - ef[n] for n in nombres}
        ruta_critica = [n for n in nombres if holgura[n] == 0]
        
        # Ordenar ruta crítica por ES
        ruta_critica.sort(key=lambda x: es[x])
        
        # 5. Formatear salida
        res = [f"✅ ANÁLISIS DE RUTA CRÍTICA (CPM) COMPLETADO"]
        res.append(f"Duración total del proyecto: {duracion_total} unidades de tiempo")
        res.append(f"Ruta Crítica: {' → '.join(ruta_critica)}")
        res.append("\nDetalle de Actividades:")
        res.append(f"{'Actividad':<12} | {'ES':<4} | {'EF':<4} | {'LS':<4} | {'LF':<4} | {'Holgura':<7}")
        res.append("-" * 55)
        for n in nombres:
            res.append(f"{n:<12} | {es[n]:<4} | {ef[n]:<4} | {ls[n]:<4} | {lf[n]:<4} | {holgura[n]:<7}")
            
        return "\n".join(res)
    except Exception as e:
        return f"❌ Error en cálculo CPM: {str(e)}"

# ============================================================================
# ORQUESTADOR - AGENTE LLM
# ============================================================================

tools = [
    tool_buscar_teoria, 
    tool_resolver_lp_continua, 
    tool_resolver_lp_entera,
    tool_ruta_mas_corta_dijkstra,
    tool_calcular_ruta_critica_cpm
]


def _parsear_json_desde_texto(texto: str) -> Optional[Dict[str, Any]]:
    """Extrae un objeto JSON desde texto libre (con o sin bloque markdown)."""
    try:
        limpio = texto.strip()
        if "```" in limpio:
            limpio = limpio.replace("```json", "").replace("```", "").strip()
        inicio = limpio.find("{")
        fin = limpio.rfind("}")
        if inicio == -1 or fin == -1 or fin <= inicio:
            return None
        return json.loads(limpio[inicio:fin + 1])
    except Exception:
        return None


def _invocar_tool(tool_obj: Any, kwargs: Dict[str, Any]) -> str:
    """Invoca tools LangChain (invoke) o funciones planas en modo limitado."""
    if hasattr(tool_obj, "invoke"):
        return tool_obj.invoke(kwargs)
    return tool_obj(**kwargs)


def _aplicar_fallback_sin_tool_call(llm: Any, pregunta_usuario: str) -> str:
    """Resuelve por ruta estructurada cuando el proveedor falla en tool-calling."""
    prompt_fallback = f"""
Analiza el problema y devuelve SOLO un JSON válido sin texto adicional.

Esquema:
{{
  "tipo": "lp_continua|lp_entera|ruta|cpm|teoria|desconocido",
  "query": "texto breve",
  "maximize": false,
  "c": [0],
  "A_ub": [[0]],
  "b_ub": [0],
  "A_eq": [],
  "b_eq": [],
  "bounds": [],
  "aristas": [{{"origen":"A","destino":"B","peso":1}}],
  "nodo_inicio": "A",
  "nodo_fin": "B",
  "actividades": [{{"nombre":"A","duracion":1,"predecesores":[]}}],
  "problema_json": {{}}
}}

Reglas:
- Si es ruta crítica, CPM o PERT, usa tipo=cpm y llena actividades.
- Si es teoría, usa tipo=teoria y llena query.
- Si no puedes extraer parámetros confiables, usa tipo=teoria.
- Para LP continua, devuelve c, A_ub, b_ub, y maximize.
- IMPORTANTE: Para problemas de MAXIMIZACIÓN en LP, pon maximize=true.

Problema:
{pregunta_usuario}
"""

    try:
        crudo = llm.invoke(prompt_fallback).content
        plan = _parsear_json_desde_texto(crudo) or {"tipo": "teoria", "query": pregunta_usuario}
    except Exception:
        plan = {"tipo": "teoria", "query": pregunta_usuario}

    tipo = str(plan.get("tipo", "teoria")).lower()

    if tipo == "cpm":
        actividades = plan.get("actividades") or []
        if actividades:
            return _invocar_tool(tool_calcular_ruta_critica_cpm, {"actividades": actividades})
        return "❌ No fue posible extraer una lista de actividades válida para CPM"

    if tipo == "ruta":
        aristas = plan.get("aristas") or []
        inicio = str(plan.get("nodo_inicio") or "")
        fin = str(plan.get("nodo_fin") or "")
        if aristas and inicio and fin:
            return _invocar_tool(
                tool_ruta_mas_corta_dijkstra,
                {"aristas": aristas, "nodo_inicio": inicio, "nodo_fin": fin}
            )
        return "❌ No fue posible extraer una red válida para Dijkstra"

    if tipo == "lp_continua":
        c = plan.get("c") or []
        A_ub = plan.get("A_ub") or None
        b_ub = plan.get("b_ub") or None
        A_eq = plan.get("A_eq") or None
        b_eq = plan.get("b_eq") or None
        bounds = plan.get("bounds") or None
        maximize = bool(plan.get("maximize", False))

        if not c:
            return "❌ No fue posible extraer coeficientes para LP continua"

        c_solver = [-float(v) for v in c] if maximize else c
        salida = _invocar_tool(
            tool_resolver_lp_continua,
            {
                "c": c_solver,
                "A_ub": A_ub,
                "b_ub": b_ub,
                "A_eq": A_eq,
                "b_eq": b_eq,
                "bounds": bounds,
            }
        )

        if maximize and "Valor Objetivo:" in salida:
            m = re.search(r"Valor Objetivo:\s*([-+]?[0-9]*\.?[0-9]+)", salida)
            if m:
                valor_min = float(m.group(1))
                valor_max = -valor_min
                salida = re.sub(
                    r"Valor Objetivo:\s*[-+]?[0-9]*\.?[0-9]+",
                    f"Valor Objetivo: {valor_max:.4f}",
                    salida
                )
        return salida

    if tipo == "lp_entera":
        problema = plan.get("problema_json")
        if isinstance(problema, dict) and problema:
            return _invocar_tool(
                tool_resolver_lp_entera,
                {"problema_json": json.dumps(problema, ensure_ascii=False)}
            )
        return "❌ No fue posible construir el JSON para PL entera"

    query = str(plan.get("query") or pregunta_usuario)
    return _invocar_tool(tool_buscar_teoria, {"query": query})

def generar_sugerencia_solucion(pregunta_usuario: str, resultado: str) -> str:
    """Genera una sugerencia accionable según el tipo de problema."""
    texto = f"{pregunta_usuario} {resultado}".lower()

    if "❌" in resultado or "error" in texto:
        return (
            "Revisa primero los datos de entrada y las restricciones. "
            "Luego vuelve a ejecutar el problema validando unidades, signos (<=, >=, =) "
            "y que no falten parámetros clave."
        )

    if any(k in texto for k in ["cpm", "ruta crítica", "holgura", "actividad"]):
        return (
            "Identifica las actividades con holgura cero para gestionar el riesgo del proyecto. "
            "Cualquier retraso en ellas afectará la fecha final de entrega."
        )

    if any(k in texto for k in ["ruta", "dijkstra", "grafo", "camino más corto", "distancia"]):
        return (
            "Representa tu red en una tabla Origen-Destino-Peso, verifica que todos los pesos "
            "sean no negativos y compara la ruta óptima con 1-2 rutas alternativas para validar el resultado."
        )

    if any(k in texto for k in ["entera", "binary", "binaria", "integer", "asignación", "asignacion"]):
        return (
            "Define claramente qué variables deben ser enteras o binarias, ejecuta el modelo y luego "
            "haz una prueba de sensibilidad simple cambiando un recurso o costo para ver la robustez de la solución."
        )

    if any(k in texto for k in ["lineal", "simplex", "maximizar", "minimizar", "restricciones"]):
        return (
            "Convierte el enunciado a modelo matemático (función objetivo + restricciones), "
            "resuelve y valida que la solución cumpla todas las restricciones antes de implementarla."
        )

    return (
        "Descompón el problema en: datos, objetivo y restricciones. Luego selecciona el método adecuado "
        "(PL, entera, rutas o CPM), resuelve y verifica el resultado con un caso pequeño de prueba."
    )

def resolver_problema_io(pregunta_usuario: str) -> str:
    """
    Resuelve problemas de Investigación de Operaciones usando agentes LLM.
    El agente selecciona automáticamente la mejor herramienta.
    """
    if not GROQ_API_KEY:
        return "❌ API Key de Groq no configurada"

    if not LANGCHAIN_AVAILABLE:
        return (
            "⚠️ El sistema está en modo limitado porque faltan dependencias del núcleo LangChain.\n"
            "Instala los paquetes faltantes para habilitar el agente LLM.\n"
            f"Detalle técnico: {LANGCHAIN_IMPORT_ERROR}"
        )
    
    llm = None
    try:
        llm = ChatGroq(model=GROQ_MODEL, temperature=0.1, timeout=40)

        # Flujo principal robusto: extrae estructura y ejecuta herramientas locales.
        resultado_estructurado = _aplicar_fallback_sin_tool_call(llm, pregunta_usuario)
        if not resultado_estructurado.startswith("❌"):
            sugerencia = generar_sugerencia_solucion(pregunta_usuario, resultado_estructurado)
            logger.info("✅ Respuesta generada (flujo estructurado)")
            return f"{resultado_estructurado}\n\n💡 SUGERENCIA DE SOLUCIÓN\n{sugerencia}"
        
        system_prompt = """Eres un EXPERTO en Investigación de Operaciones (IO) especializado en:
- Programación Lineal Continua (método Simplex) - Minimización y MAXIMIZACIÓN.
- Programación Lineal Entera/Mixta.
- Problemas de Rutas (Dijkstra, caminos más cortos).
- Gestión de Proyectos (CPM/PERT, Ruta Crítica).
- Teoría de Operaciones.

INSTRUCCIONES CRÍTICAS:
1. SIEMPRE analiza el problema matemáticamente.
2. Identifica si es un problema de minimización o MAXIMIZACIÓN.
3. SIEMPRE BUSCA TEORÍA primero usando la herramienta tool_buscar_teoria.
4. Para Gestión de Proyectos/Tiempos: USA tool_calcular_ruta_critica_cpm.
5. Para PL Continua: USA tool_resolver_lp_continua (Recuerda: si es maximizar, el parámetro 'c' debe invertirse).
6. Para PL Entera: CONSTRUYE JSON y USA tool_resolver_lp_entera.
7. Para grafos/rutas: USA tool_ruta_mas_corta_dijkstra.
8. NUNCA intentes resolver matemáticamente sin herramientas.
9. Presenta siempre: FORMULACIÓN → RESOLUCIÓN → RESULTADO FINAL.

Cuando recibas un problema:
1. Clasifica el tipo (LP, Entera, Ruta, CPM, Teoría).
2. Busca teoría relevante.
3. Formula correctamente (especifica si es Max o Min).
4. Invoca herramienta adecuada.
5. Explica resultados claramente."""
        
        agent = create_react_agent(llm, tools, debug=False)
        
        logger.info(f"🚀 Procesando: {pregunta_usuario[:100]}...")
        response = agent.invoke({
            "messages": [
                HumanMessage(content=system_prompt + f"\n\nPROBLEMA DEL USUARIO:\n{pregunta_usuario}")
            ]
        })
        
        resultado = response["messages"][-1].content
        sugerencia = generar_sugerencia_solucion(pregunta_usuario, resultado)
        resultado_final = f"{resultado}\n\n💡 SUGERENCIA DE SOLUCIÓN\n{sugerencia}"
        logger.info("✅ Respuesta generada")
        return resultado_final
        
    except Exception as e:
        if llm is not None and "tool_use_failed" in str(e).lower():
            logger.warning("⚠️ Tool-calling falló en proveedor; activando fallback estructurado")
            try:
                resultado = _aplicar_fallback_sin_tool_call(llm, pregunta_usuario)
                sugerencia = generar_sugerencia_solucion(pregunta_usuario, resultado)
                return (
                    "⚠️ Modo de respaldo activado por incompatibilidad temporal de tool-calling.\n"
                    f"{resultado}\n\n💡 SUGERENCIA DE SOLUCIÓN\n{sugerencia}"
                )
            except Exception as fallback_error:
                logger.error(f"❌ Fallback también falló: {fallback_error}")

        error_msg = f"❌ Error en agente: {str(e)}"
        logger.error(error_msg)
        return error_msg

# ============================================================================
# FUNCIÓN DE DIAGNOSTICO
# ============================================================================

def diagnosticar_sistema():
    """Realiza diagnóstico completo del sistema"""
    print("\n" + "="*70)
    print("🔍 DIAGNÓSTICO DEL SISTEMA")
    print("="*70)
    
    # 1. API
    print(f"\n✅ Groq API: {GROQ_MODEL}")
    print(f"   Key presente: {'✅ Sí' if GROQ_API_KEY else '❌ No'}")
    
    # 2. ChromaDB
    if vector_store:
        count = vector_store._collection.count()
        print(f"\n✅ ChromaDB: {count} documentos")
    else:
        print("\n❌ ChromaDB: No disponible")

    # 2.1 Modo LangChain
    if LANGCHAIN_AVAILABLE:
        print("✅ LangChain: Disponible")
    else:
        print("⚠️ LangChain: No disponible (modo limitado)")

    # 2.2 Modo RAG
    if RAG_AVAILABLE:
        print("✅ RAG (Chroma/Embeddings): Disponible")
    else:
        print("⚠️ RAG (Chroma/Embeddings): No disponible")
    
    # 3. Herramientas
    print(f"\n✅ Herramientas disponibles: {len(tools)}")
    for tool in tools:
        print(f"   - {tool.name}")
    
    print("\n" + "="*70 + "\n")

# ============================================================================
# MAIN - EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    diagnosticar_sistema()
    
    print("\n" + "🔷"*35)
    print("EJEMPLO 1: Programación Lineal Continua")
    print("🔷"*35)
    problema1 = """
    Una empresa fabrica dos productos: A y B.
    - Ganancias: A=$40/unidad, B=$30/unidad
    - Restricciones: 
      * Máquina: 2A + 1B ≤ 100 horas
      * Mano de obra: 1A + 2B ≤ 80 horas
    - Encontrar plan óptimo de producción (maximizar ganancia)
    """
    resultado = resolver_problema_io(problema1)
    print(resultado)
    
    print("\n" + "🔷"*35)
    print("EJEMPLO 2: Rutas Más Cortas")
    print("🔷"*35)
    problema2 = """
    Tengo una red de ciudades:
    - A↔B: 4km, A↔C: 2km, B↔C: 1km, B↔D: 5km, C↔D: 8km, C↔E: 10km, D↔E: 2km
    ¿Cuál es la ruta más corta de A a E?
    """
    resultado = resolver_problema_io(problema2)
    print(resultado)
    
    print("\n" + "🔷"*35)
    print("EJEMPLO 3: Teoría")
    print("🔷"*35)
    problema3 = "Explícame qué es el método simplex y sus aplicaciones"
    resultado = resolver_problema_io(problema3)
    print(resultado[:500] + "...\n")