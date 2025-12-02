# Asistente Académico con RAG 🎓

Sistema de asistente académico basado en Retrieval-Augmented Generation (RAG) que responde preguntas sobre documentos académicos usando LLaMA y búsqueda vectorial.

## 👥 Equipo

- Iman Noriega Melissa (20224041G)
- Trujillo Serva Luis Andre (20220428D)
- Orrego Torrejón Diego A. (20204161G)
- Méndez Gonzalo Miguel (20220264A)
- Pineda García Diego (20222117F)

**Universidad Nacional de Ingeniería**  
Facultad de Ciencias - Ciencia de la Computación  
Curso: Inteligencia Artificial - 2025-2

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.10+
- Ollama instalado (para LLaMA local)
- 8GB+ RAM recomendado
- ~10GB espacio libre en disco

### Instalación Rápida

**Para Windows (VSCode):** Ver guía detallada en [`GUIA_EJECUCION_WINDOWS.md`](GUIA_EJECUCION_WINDOWS.md)

**Pasos generales:**

1. **Instalar Ollama:**
   - Windows: Descargar desde https://ollama.com/download
   - Linux/Mac: `curl -fsSL https://ollama.com/install.sh | sh`
   - Descargar modelo: `ollama pull llama2:7b`

2. **Configurar proyecto:**
   ```bash
   # Crear entorno virtual
   python -m venv venv
   
   # Activar entorno virtual
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Instalar dependencias
   pip install -r requirements.txt
   ```

3. **Verificar instalación:**
   ```bash
   python verificar_setup.py
   ```

---

## 📖 Uso

### Opción 1: Interfaz Streamlit (Recomendado) ⭐

**1. Iniciar servidor Ollama (en terminal separada):**
```bash
ollama serve
```

**2. Ejecutar aplicación:**
```bash
streamlit run app.py
```

**3. Usar la aplicación:**
- Abre `http://localhost:8501` en tu navegador
- Sube PDFs académicos en la barra lateral
- Configura modelo, temperatura y top-k
- Haz clic en "🚀 Inicializar Asistente"
- Espera el procesamiento (primera vez puede tardar)
- ¡Comienza a hacer preguntas!

**4. Sesiones posteriores:**
- Usa "📂 Cargar Base de Datos Existente" para cargar documentos ya procesados (más rápido)

### Opción 2: Script Python

```python
from asistente import AsistenteAcademico

# Inicializar con parámetros personalizados
asistente = AsistenteAcademico(
    modelo_llama="llama2:7b",
    temperatura=0.3,
    top_k=3
)

# Cargar documentos (primera vez)
asistente.cargar_documentos([
    "documentos/apuntes_ia.pdf",
    "documentos/libro_ml.pdf"
])

# O cargar base de datos existente (más rápido)
# asistente.cargar_vectorstore_existente()

# Consultar
resultado = asistente.consultar("¿Qué es RAG?")
print(resultado["respuesta"])

# Ver fuentes
asistente.mostrar_fuentes(resultado["fuentes"])
```

---

## 📁 Estructura del Proyecto

```
Proyecto-IA/
├── app.py                      # Interfaz Streamlit
├── asistente.py               # Clase principal del RAG
├── requirements.txt           # Dependencias
├── README.md                  # Este archivo
│
├── documentos/                # PDFs de entrada
│   └── README.md
│
├── chroma_db/                 # Base de datos vectorial (auto-generado)
│
├── evaluacion/               
│   ├── metricas.py           # Scripts de evaluación
│   └── test_preguntas.json   # Conjunto de pruebas
│
└── notebooks/
    └── experimentacion.ipynb  # Jupyter para pruebas
```

---

## 🛠️ Tecnologías Utilizadas

- **LLM**: LLaMA 2/3 (vía Ollama)
- **Embeddings**: sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2)
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **Interfaz**: Streamlit
- **PDF Processing**: PyPDF2

---

## 📊 Evaluación

Ejecutar evaluaciones automáticas:

```bash
python -c "from evaluacion.metricas import EvaluadorAsistente; from asistente import AsistenteAcademico; a = AsistenteAcademico(); a.cargar_vectorstore_existente(); e = EvaluadorAsistente(a); r = e.evaluar_conjunto_completo(e.cargar_conjunto_prueba('evaluacion/test_preguntas.json')); e.generar_reporte(r)"
```

Métricas incluidas:
- ROUGE (calidad de generación)
- Latencia de respuesta
- Evaluación manual de relevancia

---

## ⚙️ Configuración

### Parámetros Configurables

**En la interfaz Streamlit:**
- **Modelo**: llama2:7b, llama3:8b, mistral:7b
- **Temperatura**: Control de creatividad (0.0 - 1.0)
  - 0.0-0.3: Respuestas más determinísticas y precisas
  - 0.4-0.7: Balance entre precisión y creatividad
  - 0.8-1.0: Respuestas más creativas y variadas
- **Top-K**: Número de fragmentos a recuperar (1 - 10)
  - Menor valor: Respuestas más específicas pero menos contexto
  - Mayor valor: Más contexto pero puede incluir información menos relevante

**En código Python:**
```python
# Actualizar parámetros dinámicamente
asistente.actualizar_parametros(temperatura=0.5, top_k=5)
```

---

## 🔍 Arquitectura RAG

```
1. Indexación:
   Documentos → Chunking → Embeddings → ChromaDB

2. Consulta:
   Pregunta → Búsqueda Semántica → Contexto → LLaMA → Respuesta
```

---

## ⚠️ Limitaciones Conocidas

- Requiere Ollama instalado localmente
- Modelos LLaMA necesitan ~8GB RAM mínimo
- Respuestas limitadas al contenido de los documentos cargados
- No guarda historial entre sesiones

---

## 🤝 Consideraciones Éticas

- Las respuestas están limitadas al contenido de los documentos
- Se muestran fuentes para verificar información
- Sistema indica cuando no tiene suficiente información
- Respeta derechos de autor (solo documentos propios)

---

## 📝 Licencia

Proyecto académico - Universidad Nacional de Ingeniería

---

## 📧 Contacto

Coordinador: Luis Andre Trujillo Serva  
Email: luis.trujillo.s@uni.edu.pe
