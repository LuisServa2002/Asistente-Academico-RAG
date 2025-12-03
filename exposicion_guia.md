# Flujo de la exposición
## 1. Introducción
Se presenta el proyecto , una descripción y como lo logramos.
## 2.RAG
1. Una teoría sobre RAG.
2. Como se aplico en nuestro proyecto
```
Usuario hace pregunta
    ↓
1. RECUPERACIÓN
   - Convierte la pregunta en un vector (embedding)
   - Busca en la base de datos los fragmentos más relevantes
   - Recupera los top-k documentos similares
    ↓
2. CONTEXTO
   - Combina la pregunta + fragmentos relevantes
    ↓
3. GENERACIÓN
   - El LLM genera respuesta basada en el contexto
    ↓
Respuesta con citas de fuentes
```
- Carga documentos
PyPDFLoader extrae texto de los PDFs
- División en fragmentos (Chunking)
```
# Divide documentos en pedazos manejables
RecursiveCharacterTextSplitter
- Tamaño: 1000-1500 caracteres
- Overlap: 200 caracteres (para mantener contexto)
```