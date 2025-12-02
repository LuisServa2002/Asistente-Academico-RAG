"""
Script de verificación del entorno para Asistente Académico RAG
Ejecutar antes de usar el sistema para verificar que todo esté configurado correctamente.
"""

import sys
import subprocess
import importlib
from pathlib import Path

def verificar_python():
    """Verifica versión de Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - Se requiere Python 3.10+")
        return False

def verificar_ollama():
    """Verifica que Ollama esté instalado"""
    print("\n🦙 Verificando Ollama...")
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   ✅ Ollama instalado - {result.stdout.strip()}")
            return True
        else:
            print("   ❌ Ollama no responde correctamente")
            return False
    except FileNotFoundError:
        print("   ❌ Ollama no encontrado. Instalar desde: https://ollama.com/download")
        return False
    except Exception as e:
        print(f"   ⚠️  Error al verificar Ollama: {str(e)}")
        return False

def verificar_modelo_llama():
    """Verifica que el modelo LLaMA esté disponible"""
    print("\n📦 Verificando modelo LLaMA...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            modelos = result.stdout
            if "llama2" in modelos.lower() or "llama3" in modelos.lower():
                print("   ✅ Modelo LLaMA encontrado")
                print(f"   Modelos disponibles:\n{modelos}")
                return True
            else:
                print("   ⚠️  No se encontró modelo LLaMA")
                print("   Ejecutar: ollama pull llama2:7b")
                return False
        else:
            print("   ⚠️  No se pudo listar modelos")
            return False
    except Exception as e:
        print(f"   ⚠️  Error al verificar modelos: {str(e)}")
        return False

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("\n📚 Verificando dependencias...")
    
    dependencias_requeridas = [
        "langchain",
        "chromadb",
        "streamlit",
        "sentence_transformers",
        "pypdf2",
    ]
    
    faltantes = []
    instaladas = []
    
    for dep in dependencias_requeridas:
        try:
            # Intentar importar
            if dep == "sentence_transformers":
                importlib.import_module("sentence_transformers")
            elif dep == "pypdf2":
                importlib.import_module("PyPDF2")
            else:
                importlib.import_module(dep)
            instaladas.append(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            faltantes.append(dep)
            print(f"   ❌ {dep} - NO INSTALADO")
    
    if faltantes:
        print(f"\n   ⚠️  Faltan {len(faltantes)} dependencias")
        print("   Ejecutar: pip install -r requirements.txt")
        return False
    else:
        print(f"\n   ✅ Todas las dependencias instaladas ({len(instaladas)})")
        return True

def verificar_estructura():
    """Verifica estructura de carpetas"""
    print("\n📁 Verificando estructura de carpetas...")
    
    carpetas_requeridas = [
        "documentos",
        "evaluacion",
    ]
    
    archivos_requeridos = [
        "app.py",
        "asistente.py",
        "requirements.txt",
        "README.md",
    ]
    
    todo_ok = True
    
    for carpeta in carpetas_requeridas:
        if Path(carpeta).exists():
            print(f"   ✅ Carpeta '{carpeta}' existe")
        else:
            print(f"   ⚠️  Carpeta '{carpeta}' no existe (se creará automáticamente)")
    
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"   ✅ Archivo '{archivo}' existe")
        else:
            print(f"   ❌ Archivo '{archivo}' NO EXISTE")
            todo_ok = False
    
    return todo_ok

def verificar_ollama_servidor():
    """Verifica que el servidor Ollama esté corriendo"""
    print("\n🖥️  Verificando servidor Ollama...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("   ✅ Servidor Ollama está corriendo")
            return True
        else:
            print("   ⚠️  Servidor Ollama no responde correctamente")
            return False
    except ImportError:
        print("   ⚠️  'requests' no instalado (opcional)")
        print("   💡 Para verificar servidor: ollama serve")
        return None
    except Exception:
        print("   ⚠️  Servidor Ollama no está corriendo")
        print("   💡 Ejecutar en otra terminal: ollama serve")
        return False

def main():
    """Función principal de verificación"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DEL ENTORNO - Asistente Académico RAG")
    print("=" * 60)
    
    resultados = {
        "Python": verificar_python(),
        "Ollama": verificar_ollama(),
        "Modelo LLaMA": verificar_modelo_llama(),
        "Dependencias": verificar_dependencias(),
        "Estructura": verificar_estructura(),
        "Servidor Ollama": verificar_ollama_servidor(),
    }
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    total = len(resultados)
    exitosos = sum(1 for v in resultados.values() if v is True)
    opcionales = sum(1 for v in resultados.values() if v is None)
    
    for componente, estado in resultados.items():
        if estado is True:
            print(f"✅ {componente}")
        elif estado is None:
            print(f"⚠️  {componente} (opcional)")
        else:
            print(f"❌ {componente}")
    
    print("\n" + "=" * 60)
    
    if exitosos == total:
        print("🎉 ¡Todo está configurado correctamente!")
        print("   Puedes ejecutar: streamlit run app.py")
    elif exitosos + opcionales >= total - 1:
        print("✅ Configuración casi completa")
        print("   Revisa los elementos marcados con ❌")
    else:
        print("⚠️  Hay problemas que resolver")
        print("   Revisa los elementos marcados con ❌")
        print("\n💡 Siguiente paso: Revisar GUIA_EJECUCION_WINDOWS.md")
    
    print("=" * 60)
    
    return exitosos == total

if __name__ == "__main__":
    try:
        exit_code = 0 if main() else 1
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante verificación: {str(e)}")
        sys.exit(1)

