#!/usr/bin/env python
# ============================================================================
# VERIFICADOR DE INTEGRIDAD - ChromaDB
# Verifica que la base de datos vectorial esté correcta y disponible
# ============================================================================

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ============================================================================
# VERIFICACIONES
# ============================================================================

def verificar_archivo_pdf() -> Tuple[bool, str]:
    """Verifica que el PDF esté disponible"""
    pdf_paths = [
        "./Investigacion-Operaciones10Edicion-Frederick-S-Hillier.pdf",
        "./documentos/Investigacion-Operaciones10Edicion-Frederick-S-Hillier.pdf"
    ]
    
    for path in pdf_paths:
        if Path(path).exists():
            size_mb = Path(path).stat().st_size / (1024 * 1024)
            return True, f"PDF encontrado: {path} ({size_mb:.1f} MB)"
    
    return False, "PDF no encontrado en rutas esperadas"

def verificar_chromadb() -> Tuple[bool, Dict]:
    """Verifica la integridad de ChromaDB"""
    try:
        from langchain_chroma import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
        
        chroma_path = Path("./chroma_db")
        
        if not chroma_path.exists():
            return False, {"mensaje": "Directorio ChromaDB no existe"}
        
        # Intentar cargar
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma(
            persist_directory=str(chroma_path),
            embedding_function=embeddings
        )
        
        # Verificar contenido
        try:
            count = vector_store._collection.count()
            return True, {
                "documentos": count,
                "path": str(chroma_path),
                "embeddings": "all-MiniLM-L6-v2"
            }
        except:
            return False, {"mensaje": "No se pudo contar documentos"}
            
    except Exception as e:
        return False, {"error": str(e)}

def verificar_api_groq() -> Tuple[bool, Dict]:
    """Verifica configuración de API Groq"""
    try:
        from dotenv import load_dotenv
        
        load_dotenv()
        
        api_key = os.environ.get("GROQ_API_KEY")
        model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        if not api_key:
            return False, {"mensaje": "GROQ_API_KEY no configurada"}
        
        # Verificar formato
        if not api_key.startswith("gsk_"):
            return False, {"mensaje": "API Key con formato inválido"}
        
        return True, {
            "modelo": model,
            "key_presente": True,
            "key_inicio": api_key[:10] + "..."
        }
        
    except Exception as e:
        return False, {"error": str(e)}

def verificar_herramientas() -> Tuple[bool, Dict]:
    """Verifica que todas las herramientas se importen correctamente"""
    try:
        from scipy.optimize import linprog
        from collections import defaultdict
        import heapq
        import pulp
        
        return True, {
            "scipy": "✅",
            "heapq": "✅",
            "collections": "✅",
            "pulp": "✅"
        }
    except Exception as e:
        return False, {"error": str(e)}

# ============================================================================
# DIAGNOSTICO COMPLETO
# ============================================================================

def diagnostico_completo():
    """Ejecuta diagnóstico completo del sistema"""
    
    print("\n" + "="*80)
    print("🔍 DIAGNÓSTICO COMPLETO - SISTEMA DE INTELIGENCIA EN OPERACIONES")
    print("="*80 + "\n")
    
    diagnosticos = {
        "📖 PDF (Libro Hillier)": verificar_archivo_pdf,
        "💾 ChromaDB (Base Vectorial)": verificar_chromadb,
        "🔑 API Groq": verificar_api_groq,
        "🛠️ Herramientas Matemáticas": verificar_herramientas
    }
    
    resultados = {}
    
    for nombre, verificador in diagnosticos.items():
        print(f"\n{nombre}")
        print("-" * 80)
        
        try:
            ok, datos = verificador()
            resultados[nombre] = (ok, datos)
            
            if ok:
                print(f"✅ OK")
                if isinstance(datos, dict):
                    for clave, valor in datos.items():
                        print(f"   • {clave}: {valor}")
            else:
                print(f"❌ FALLO")
                if isinstance(datos, dict) and datos:
                    for clave, valor in datos.items():
                        print(f"   • {clave}: {valor}")
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            resultados[nombre] = (False, {"error": str(e)})
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN")
    print("="*80)
    
    total = len(resultados)
    ok_count = sum(1 for ok, _ in resultados.values() if ok)
    
    print(f"\n✅ Pasadas: {ok_count}/{total}")
    
    if ok_count == total:
        print("\n🟢 **SISTEMA LISTO PARA USAR**")
        return 0
    else:
        print("\n🟡 **REQUIERE ATENCIÓN**")
        print("\nProblemas detectados:")
        for nombre, (ok, datos) in resultados.items():
            if not ok:
                print(f"  • {nombre}")
        return 1

# ============================================================================
# ACTIONS - REPARACIÓN/GENERACIÓN
# ============================================================================

def regenerar_chromadb():
    """Regenera ChromaDB desde el PDF"""
    print("\n" + "="*80)
    print("🔄 REGENERANDO ChromaDB...")
    print("="*80 + "\n")
    
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_chroma import Chroma
        import shutil
        
        # Buscar PDF
        pdf_path = None
        pdf_paths = [
            "./Investigacion-Operaciones10Edicion-Frederick-S-Hillier.pdf",
            "./documentos/Investigacion-Operaciones10Edicion-Frederick-S-Hillier.pdf"
        ]
        
        for path in pdf_paths:
            if Path(path).exists():
                pdf_path = path
                break
        
        if not pdf_path:
            print("❌ PDF no encontrado")
            return False
        
        print(f"📖 Cargando PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        documentos = loader.load()
        print(f"✅ Cargadas {len(documentos)} páginas")
        
        print("✂️ Dividiendo en fragmentos...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " "]
        )
        chunks = text_splitter.split_documents(documentos)
        print(f"✅ {len(chunks)} fragmentos creados")
        
        print("🤖 Generando embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Limpiar ChromaDB viejo
        chroma_path = Path("./chroma_db")
        if chroma_path.exists():
            print("🗑️ Limpiando ChromaDB anterior...")
            shutil.rmtree(chroma_path)
        
        print("💾 Creando nueva base de datos...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(chroma_path)
        )
        
        print("✅ ChromaDB regenerada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Verificador de integridad - Sistema I/O")
    parser.add_argument("--diagnose", action="store_true", help="Ejecutar diagnóstico completo")
    parser.add_argument("--regenerate-db", action="store_true", help="Regenerar ChromaDB desde PDF")
    parser.add_argument("--full-repair", action="store_true", help="Reparación completa del sistema")
    
    args = parser.parse_args()
    
    if args.regenerate_db or args.full_repair:
        regenerar_chromadb()
    
    if args.diagnose or args.full_repair or not args.regenerate_db:
        exit_code = diagnostico_completo()
        sys.exit(exit_code)
