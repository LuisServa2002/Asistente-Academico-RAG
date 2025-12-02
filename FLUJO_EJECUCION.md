# 🔄 Flujo de Ejecución - Asistente Académico RAG

## Diagrama de Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    INICIO - Configuración Inicial                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. Verificar Entorno                                            │
│     python verificar_setup.py                                    │
│     ✓ Python 3.10+                                               │
│     ✓ Ollama instalado                                           │
│     ✓ Modelo LLaMA descargado                                    │
│     ✓ Dependencias instaladas                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Iniciar Servidor Ollama (Terminal 1)                        │
│     ollama serve                                                 │
│     → Servidor corriendo en http://localhost:11434              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. Activar Entorno Virtual (Terminal 2)                        │
│     .\venv\Scripts\Activate.ps1                                  │
│     → (venv) aparece en el prompt                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Ejecutar Streamlit (Terminal 2)                             │
│     streamlit run app.py                                         │
│     → Aplicación abierta en http://localhost:8501               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌──────────────────┐  ┌──────────────────┐
        │  Primera Vez     │  │  Sesión Anterior │
        │  (Nuevos PDFs)   │  │  (Base Existente)│
        └──────────────────┘  └──────────────────┘
                    │                   │
                    ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  5A. Cargar Documentos (Primera Vez)                            │
│     • Subir PDFs en la barra lateral                            │
│     • Configurar modelo, temperatura, top-k                      │
│     • Clic en "🚀 Inicializar Asistente"                        │
│     • Esperar procesamiento (5-15 min)                          │
│     → Base de datos guardada en chroma_db/                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  5B. Cargar Base Existente (Más Rápido)                         │
│     • Clic en "📂 Cargar Base de Datos Existente"               │
│     • Esperar carga (10-30 seg)                                 │
│     → Base de datos cargada desde chroma_db/                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. Sistema Listo ✅                                            │
│     • Mensaje: "✅ Sistema listo"                                │
│     • Chat habilitado                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  7. Hacer Consultas                                             │
│     • Escribir pregunta en el chat                               │
│     • Presionar Enter                                             │
│     • Esperar respuesta (5-30 seg)                               │
│     • Ver respuesta y fuentes                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌──────────────────┐  ┌──────────────────┐
        │  Continuar        │  │  Reiniciar        │
        │  Consultando      │  │  Sistema          │
        └──────────────────┘  └──────────────────┘
```

---

## 📋 Pasos Detallados para Windows/VSCode

### Preparación (Una sola vez)

```powershell
# 1. Abrir VSCode en la carpeta del proyecto
# File → Open Folder → asistente-academico-rag

# 2. Abrir terminal integrada
# Terminal → New Terminal (Ctrl + `)

# 3. Crear entorno virtual
python -m venv venv

# 4. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Verificar instalación
python verificar_setup.py
```

### Ejecución Diaria

#### Paso 1: Iniciar Ollama (Terminal 1)
```powershell
# Abrir nueva terminal en VSCode
# Terminal → New Terminal

# Iniciar servidor Ollama
ollama serve

# Dejar esta terminal abierta
# Deberías ver: "Ollama is running"
```

#### Paso 2: Ejecutar Streamlit (Terminal 2)
```powershell
# En otra terminal (o la misma si Ollama ya está corriendo)

# Activar entorno virtual (si no está activo)
.\venv\Scripts\Activate.ps1

# Ejecutar Streamlit
streamlit run app.py

# Esperar mensaje:
# "You can now view your Streamlit app in your browser."
# "Local URL: http://localhost:8501"
```

#### Paso 3: Usar la Aplicación

1. **Abrir navegador**: `http://localhost:8501` (se abre automáticamente)

2. **Primera vez (cargar documentos)**:
   - Ir a la barra lateral izquierda
   - En "📚 Documentos", hacer clic en "Browse files"
   - Seleccionar PDFs académicos
   - Configurar parámetros:
     - Modelo: `llama2:7b`
     - Temperatura: `0.3` (recomendado)
     - Fragmentos: `3` (recomendado)
   - Clic en "🚀 Inicializar Asistente"
   - Esperar procesamiento (puede tardar varios minutos)
   - Ver mensaje: "✅ X documentos cargados correctamente"

3. **Sesiones posteriores (cargar base existente)**:
   - Clic en "📂 Cargar Base de Datos Existente"
   - Esperar carga (más rápido, ~10-30 segundos)
   - Ver mensaje: "✅ Base de datos cargada correctamente"

4. **Hacer preguntas**:
   - Escribir pregunta en el chat (parte inferior)
   - Presionar Enter o clic en el botón de enviar
   - Esperar respuesta (5-30 segundos)
   - Ver respuesta y fuentes utilizadas

5. **Ver fuentes**:
   - Clic en "📌 Ver fuentes" debajo de la respuesta
   - Ver documentos y páginas utilizadas
   - Ver fragmentos de texto relevantes

---

## 🔄 Flujo de Datos

```
┌─────────────┐
│   PDFs      │
│  (Input)    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  PyPDFLoader    │ → Extrae texto de PDFs
└──────┬──────────┘
       │
       ▼
┌──────────────────────┐
│  TextSplitter         │ → Divide en chunks
│  (chunk_size=1000)    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  HuggingFaceEmbeddings│ → Genera vectores
│  (sentence-transformers)│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  ChromaDB            │ → Almacena vectores
│  (chroma_db/)        │   (persistente)
└──────┬───────────────┘
       │
       │
       │  ┌──────────────┐
       │  │   Pregunta   │
       │  │   (Usuario)  │
       │  └──────┬───────┘
       │         │
       ▼         ▼
┌──────────────────────┐
│  Búsqueda Semántica  │ → Encuentra chunks relevantes
│  (Similarity Search)  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  LLaMA (Ollama)       │ → Genera respuesta
│  (llama2:7b)          │
└──────┬───────────────┘
       │
       ▼
┌─────────────┐
│  Respuesta  │
│  + Fuentes  │
└─────────────┘
```

---

## ⚡ Comandos Rápidos

### Verificación Rápida
```powershell
python verificar_setup.py
```

### Iniciar Todo (Script de ayuda)
```powershell
# Crear archivo iniciar.ps1 con:
# Terminal 1
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ollama serve"

# Terminal 2 (esperar 3 segundos)
Start-Sleep -Seconds 3
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

### Detener Todo
```powershell
# Cerrar terminales de Ollama y Streamlit
# O presionar Ctrl+C en cada terminal
```

---

## 🎯 Checklist de Ejecución

### Antes de Ejecutar
- [ ] Python 3.10+ instalado
- [ ] Ollama instalado y modelo descargado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] PDFs en carpeta `documentos/` (opcional, primera vez)

### Durante Ejecución
- [ ] Terminal 1: Ollama corriendo (`ollama serve`)
- [ ] Terminal 2: Streamlit ejecutándose (`streamlit run app.py`)
- [ ] Navegador abierto en `http://localhost:8501`
- [ ] Documentos cargados o base de datos existente cargada

### Después de Ejecutar
- [ ] Base de datos guardada en `chroma_db/`
- [ ] Respuestas coherentes obtenidas
- [ ] Fuentes mostradas correctamente

---

## 🐛 Solución Rápida de Problemas

### Ollama no inicia
```powershell
# Verificar instalación
ollama --version

# Si no funciona, reinstalar desde: https://ollama.com/download
```

### Streamlit no se abre
```powershell
# Verificar que está instalado
pip show streamlit

# Si no, reinstalar
pip install streamlit

# Abrir manualmente: http://localhost:8501
```

### Error al cargar documentos
```powershell
# Verificar que los PDFs existen
ls documentos/

# Verificar permisos de escritura
# Asegurarse de que chroma_db/ no esté bloqueado
```

---

**¡Listo para ejecutar! 🚀**

Para más detalles, consulta `GUIA_EJECUCION_WINDOWS.md`

