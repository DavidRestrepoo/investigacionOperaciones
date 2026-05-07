#!/usr/bin/env python
"""
Script de instalación interactivo y diagnóstico
Instala dependencias de forma segura y verifica el sistema
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Ejecuta comando y maneja errores"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - FALLÓ")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ {description} - TIMEOUT (puede estar en progreso)")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("🔧 INSTALADOR INTELIGENCIA EN OPERACIONES")
    print("="*80)
    
    # Verificar Python
    print(f"\n✅ Python: {sys.version.split()[0]}")
    
    # Paquetes por prioridad
    paquetes = {
        "CRÍTICOS": [
            "python-dotenv",
            "scipy",
            "numpy",
            "pandas",
            "pulp"
        ],
        "LangChain": [
            "langchain==0.1.20",
            "langchain-community",
            "langchain-groq",
        ],
        "Vector DB": [
            "chromadb",
            "sentence-transformers",
            "langchain-chroma",
        ],
        "PDF": [
            "pymupdf",
            "pypdf"
        ],
        "UI": [
            "streamlit",
            "langgraph"
        ]
    }
    
    # Menú
    print("\n" + "="*80)
    print("INSTALACIÓN POR CATEGORÍAS")
    print("="*80)
    
    for i, categoria in enumerate(paquetes.keys(), 1):
        print(f"{i}. {categoria} ({len(paquetes[categoria])} paquetes)")
    
    print(f"{len(paquetes)+1}. Instalar TODO")
    print(f"{len(paquetes)+2}. Salir")
    
    try:
        opcion = int(input("\nSelecciona una opción: "))
        
        if opcion == len(paquetes) + 2:
            print("Hasta luego!")
            return
        elif opcion == len(paquetes) + 1:
            # Todo
            categorias_a_instalar = list(paquetes.values())
        elif 1 <= opcion <= len(paquetes):
            # Categoría específica
            categoria = list(paquetes.keys())[opcion - 1]
            categorias_a_instalar = [paquetes[categoria]]
        else:
            print("❌ Opción inválida")
            return
        
        # Instalar
        print("\n" + "="*80)
        total_paquetes = sum(len(cat) for cat in categorias_a_instalar)
        print(f"📦 Instalando {total_paquetes} paquetes...")
        print("="*80)
        
        for categoria_list in categorias_a_instalar:
            paquetes_str = " ".join(categoria_list)
            cmd = f'python -m pip install {paquetes_str} -q'
            run_command(cmd, f"Instalando {len(categoria_list)} paquetes")
        
        print("\n" + "="*80)
        print("✅ INSTALACIÓN COMPLETADA")
        print("="*80)
        
        # Verificar
        print("\n🔍 Verificando instalación...")
        run_command("python verificador.py --diagnose", "Diagnóstico del sistema")
        
    except ValueError:
        print("❌ Entrada inválida")
    except KeyboardInterrupt:
        print("\n\n⚠️ Instalación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
