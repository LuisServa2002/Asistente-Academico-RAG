# 🪟 Guía de Ejecución - Windows (VSCode)

Esta guía te ayudará a ejecutar el Asistente Académico con RAG en Windows usando Visual Studio Code.

---

## 📋 Prerrequisitos

### 1. Python 3.10 o superior

**Verificar instalación:**
```powershell
python --version
```

**Si no está instalado:**
- Descargar desde: https://www.python.org/downloads/
- ⚠️ **IMPORTANTE**: Marcar la opción "Add Python to PATH" durante la instalación

### 2. Visual Studio Code

**Instalar VSCode:**
- Descargar desde: https://code.visualstudio.com/
- Instalar extensión "Python" desde el marketplace

### 3. Ollama (Modelo LLaMA)

**Instalación en Windows:**

1. **Descargar Ollama:**
   - Visitar: https://ollama.com/download
   - Descargar el instalador para Windows
   - Ejecutar el instalador

2. **Verificar instalación:**
   ```powershell
   ollama --version
   ```

3. **Descargar modelo LLaMA:**
   ```powershell
   ollama pull llama2:7b
   ```
   
   ⚠️ **Nota**: Este proceso puede tardar varios minutos y requiere ~4GB de espacio libre.

4. **Verificar modelo descargado:**
   ```powershell
   ollama list
   ```

5. **Probar modelo:**
   ```powershell
   ollama run llama2:7b "Hola, ¿cómo estás?"
   ```

---

## 🚀 Configuración del Proyecto

### Paso 1: Abrir el proyecto en VSCode

1. Abrir Visual Studio Code
2. File → Open Folder → Seleccionar la carpeta del proyecto
3. Asegurarse de que VSCode detecta Python (ver esquina inferior derecha)

### Paso 2: Crear entorno virtual

**En la terminal integrada de VSCode (Terminal → New Terminal):**

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1
```

⚠️ **Si aparece error de ejecución de scripts:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Alternativa (si PowerShell no funciona):**
```cmd
venv\Scripts\activate.bat
```

### Paso 3: Instalar dependencias

```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

**Verificar instalación:**
```powershell
pip list
```

Deberías ver: `langchain`, `chromadb`, `streamlit`, `sentence-transformers`, etc.

---

## 🎯 Ejecución del Sistema

### Opción 1: Interfaz Streamlit (Recomendado)

**1. Verificar que Ollama esté corriendo:**

Abre una nueva terminal y ejecuta:
```powershell
ollama serve
```

⚠️ **IMPORTANTE**: Deja esta terminal abierta. Ollama debe estar corriendo en segundo plano.

**2. En otra terminal (con el entorno virtual activado):**

```powershell
# Asegúrate de estar en el directorio del proyecto
cd "C:\Users\luisa\Desktop\UNI\7-CICLO\IA\PC's\PC 05\asistente-academico-rag"

# Activar entorno virtual si no está activo
.\venv\Scripts\Activate.ps1

# Ejecutar Streamlit
streamlit cache clear
streamlit run app.py
```

**3. Abrir en navegador:**

- Streamlit abrirá automáticamente: `http://localhost:8501`
- Si no se abre, copiar la URL que aparece en la terminal

**4. Usar la aplicación:**

- Subir PDFs académicos en la barra lateral
- Configurar modelo, temperatura y top-k
- Clic en "🚀 Inicializar Asistente"
- Esperar a que procese los documentos (puede tardar varios minutos)
- ¡Hacer preguntas!

### Opción 2: Script Python directo

**1. Preparar documentos:**

Colocar PDFs en la carpeta `documentos/`:
```
documentos/
  ├── apuntes_ia.pdf
  └── libro_ml.pdf
```

**2. Ejecutar script:**

```powershell
# Con entorno virtual activado
python asistente.py
```

**3. Modificar el script:**

Editar `asistente.py` (líneas 178-183) para especificar tus PDFs:
```python
pdfs = [
    "documentos/tu_documento1.pdf",
    "documentos/tu_documento2.pdf",
]
```

---

## 🔧 Solución de Problemas Comunes

### Error: "Ollama no se encuentra"

**Solución:**
```powershell
# Verificar que Ollama esté en PATH
ollama --version

# Si no funciona, agregar manualmente al PATH:
# 1. Buscar "Variables de entorno" en Windows
# 2. Agregar ruta de Ollama (normalmente: C:\Users\<usuario>\AppData\Local\Programs\Ollama)
```

### Error: "No se puede conectar a Ollama"

**Solución:**
```powershell
# Iniciar servidor Ollama manualmente
ollama serve

# En otra terminal, verificar:
curl http://localhost:11434/api/tags
```

### Error: "Modelo no encontrado"

**Solución:**
```powershell
# Listar modelos disponibles
ollama list

# Si llama2:7b no está, descargarlo:
ollama pull llama2:7b

# Alternativas más pequeñas (si tienes poca RAM):
ollama pull llama2:7b-chat-q4_0  # Versión cuantizada (menos RAM)
```

### Error: "Out of memory" o sistema lento

**Soluciones:**
1. Usar modelo más pequeño:
   ```powershell
   ollama pull llama2:7b-chat-q4_0
   ```
2. Reducir tamaño de chunks en `asistente.py`:
   ```python
   chunk_size=500  # En lugar de 1000
   ```
3. Procesar menos documentos a la vez

### Error: "ModuleNotFoundError"

**Solución:**
```powershell
# Asegurarse de que el entorno virtual está activado
# Deberías ver (venv) al inicio de la línea de comandos

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "ChromaDB lock" o "Database locked"

**Solución:**
```powershell
# Cerrar todas las instancias de Python/Streamlit
# Eliminar carpeta chroma_db si es necesario (se regenerará)
Remove-Item -Recurse -Force chroma_db
```

### Streamlit no se abre automáticamente

**Solución:**
- Copiar la URL que aparece en la terminal (ej: `http://localhost:8501`)
- Abrir manualmente en el navegador

---

## 📊 Verificación del Sistema

### Script de verificación rápida

Ejecutar `verificar_setup.py`:
```powershell
python verificar_setup.py
```

Este script verificará:
- ✅ Python instalado
- ✅ Ollama instalado y corriendo
- ✅ Modelo LLaMA disponible
- ✅ Dependencias instaladas
- ✅ Estructura de carpetas correcta

---

## 🎓 Flujo de Trabajo Recomendado

### Primera vez:

1. ✅ Instalar Ollama y descargar modelo
2. ✅ Crear entorno virtual e instalar dependencias
3. ✅ Colocar PDFs en carpeta `documentos/`
4. ✅ Ejecutar `streamlit run app.py`
5. ✅ Subir PDFs y hacer clic en "Inicializar Asistente"
6. ✅ Esperar procesamiento (primera vez puede tardar)
7. ✅ ¡Hacer preguntas!

### Sesiones posteriores:

1. ✅ Activar entorno virtual
2. ✅ Iniciar Ollama (`ollama serve`)
3. ✅ Ejecutar Streamlit
4. ✅ Opción A: Subir nuevos PDFs
5. ✅ Opción B: Clic en "Cargar Base de Datos Existente" (más rápido)

---

## 📝 Notas Importantes

### Rendimiento:

- **Primera carga de documentos**: Puede tardar 5-15 minutos dependiendo del tamaño
- **Consultas**: 5-30 segundos por pregunta (depende del hardware)
- **RAM recomendada**: Mínimo 8GB, ideal 16GB

### Almacenamiento:

- **Modelo LLaMA**: ~4GB
- **Base de datos vectorial**: ~100-500MB por documento (depende del tamaño)
- **Espacio total recomendado**: ~10GB libres

### Mejores Prácticas:

1. **Procesar documentos una vez**: La base de datos se guarda en `chroma_db/`
2. **Reutilizar base de datos**: Usar "Cargar Base de Datos Existente" en sesiones posteriores
3. **PDFs pequeños**: Para pruebas, usar documentos de 10-50 páginas
4. **Guardar trabajo**: La base de datos se persiste automáticamente

---

## 🆘 Soporte Adicional

Si encuentras problemas:

1. Revisar logs en la terminal de VSCode
2. Verificar que Ollama esté corriendo: `ollama list`
3. Probar modelo directamente: `ollama run llama2:7b "test"`
4. Verificar versión de Python: `python --version` (debe ser 3.10+)
5. Revisar `requirements.txt` y versiones instaladas: `pip list`

---

## ✅ Checklist de Verificación

Antes de ejecutar, verifica:

- [ ] Python 3.10+ instalado
- [ ] VSCode instalado con extensión Python
- [ ] Ollama instalado y funcionando
- [ ] Modelo LLaMA descargado (`ollama list`)
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip list`)
- [ ] Ollama corriendo (`ollama serve`)
- [ ] PDFs en carpeta `documentos/` (opcional para primera ejecución)

---

**¡Listo para comenzar! 🚀**

Si tienes dudas, revisa la sección de "Solución de Problemas" o consulta el README.md principal.

