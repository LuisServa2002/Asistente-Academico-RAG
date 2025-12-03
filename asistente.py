import os
from typing import List

from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


class AsistenteAcademico:
    """
    Asistente académico RAG con LLaMA local
    """

    def __init__(self, modelo_llama="llama2:7b", persist_directory="./chroma_db", temperatura=0.3, top_k=3):
        """
        Inicializa el asistente

        Args:
            modelo_llama: Nombre del modelo en Ollama
            persist_directory: Directorio para persistir vectores
            temperatura: Control de creatividad (0.0 - 1.0)
            top_k: Número de fragmentos a recuperar
        """
        print("🚀 Inicializando Asistente Académico...")

        # Guardar parámetros configurables
        self.modelo_llama = modelo_llama
        self.temperatura = temperatura
        self.top_k = top_k

        # Configurar embeddings (gratuito y en español)
        print("📊 Cargando modelo de embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={"device": "cpu"},  # Cambiar a 'cuda' si tienen GPU
        )

        # Configurar LLaMA local
        print(f"🦙 Conectando con LLaMA ({modelo_llama})...")
        self.llm = Ollama(
            model=modelo_llama,
            temperature=temperatura,
            num_ctx=4096,  # Contexto grande para documentos largos
            request_timeout=300.0,  # Agregar esto (5 minutos)
        )

        # Base de datos vectorial
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.qa_chain = None

        print("✅ Asistente inicializado correctamente")

    def cargar_documentos(self, rutas_pdf: List[str]):
        """
        Carga y procesa documentos PDF

        Args:
            rutas_pdf: Lista de rutas a archivos PDF
        """
        print(f"\n📚 Cargando {len(rutas_pdf)} documentos...")

        documentos = []
        for ruta in rutas_pdf:
            print(f"  - Procesando: {os.path.basename(ruta)}")
            loader = PyPDFLoader(ruta)
            documentos.extend(loader.load())

        print(f"✅ {len(documentos)} páginas cargadas")

        # Dividir en chunks
        print("✂️  Dividiendo documentos en fragmentos...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Tamaño de cada fragmento
            chunk_overlap=200,  # Solapamiento entre fragmentos
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )

        chunks = text_splitter.split_documents(documentos)
        print(f"✅ {len(chunks)} fragmentos creados")

        # Crear vectorstore
        print("🔢 Generando embeddings y almacenando vectores...")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
        )

        print("💾 Base de datos vectorial persistida")
        self._crear_qa_chain()

    def cargar_vectorstore_existente(self):
        """
        Carga vectorstore previamente guardado
        """
        try:
            print("📂 Cargando base de datos existente...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory, embedding_function=self.embeddings
            )
            self._crear_qa_chain()
            print("✅ Base de datos cargada")
        except Exception as e:
            print(f"❌ Error al cargar base de datos: {str(e)}")
            print("💡 Asegúrate de haber cargado documentos primero")
            raise

    def _crear_qa_chain(self, top_k=None):
        """
        Crea la cadena de pregunta-respuesta
        
        Args:
            top_k: Número de fragmentos a recuperar (usa self.top_k si no se especifica)
        """
        if top_k is None:
            top_k = self.top_k
            
        # Prompt en español optimizado para contexto académico
        template = """Eres un asistente académico experto. Usa el siguiente contexto para responder la pregunta del estudiante.

Si no sabes la respuesta con base en el contexto proporcionado, di claramente "No tengo suficiente información en los documentos para responder esa pregunta".

Contexto:
{context}

Pregunta: {question}

Respuesta detallada y académica:"""

        PROMPT = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

        # Crear chain con retrieval
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": top_k}  # Recuperar top_k fragmentos
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True,
        )
    
    def actualizar_parametros(self, temperatura=None, top_k=None):
        """
        Actualiza parámetros del modelo y recrea la cadena QA si es necesario
        
        Args:
            temperatura: Nueva temperatura (requiere recrear LLM)
            top_k: Nuevo número de fragmentos (requiere recrear QA chain)
        """
        if temperatura is not None and temperatura != self.temperatura:
            self.temperatura = temperatura
            self.llm = Ollama(
                model=self.modelo_llama,
                temperature=temperatura,
                num_ctx=4096,
            )
            if self.qa_chain is not None:
                self._crear_qa_chain()
        
        if top_k is not None and top_k != self.top_k:
            self.top_k = top_k
            if self.qa_chain is not None:
                self._crear_qa_chain(top_k=top_k)

    def consultar(self, pregunta: str):
        """
        Realiza una consulta al asistente

        Args:
            pregunta: Pregunta del estudiante

        Returns:
            dict con 'respuesta' y 'fuentes'
        """
        if self.qa_chain is None:
            return {"respuesta": "❌ Primero debes cargar documentos", "fuentes": []}

        print(f"\n❓ Pregunta: {pregunta}")
        print("🔍 Buscando información relevante...")

        resultado = self.qa_chain({"query": pregunta})

        respuesta = resultado["result"]
        fuentes = resultado["source_documents"]

        return {"respuesta": respuesta, "fuentes": fuentes}

    def mostrar_fuentes(self, fuentes):
        """
        Muestra las fuentes utilizadas
        """
        if not fuentes:
            print("\n📌 No se encontraron fuentes")
            return

        print(f"\n📌 Fuentes consultadas ({len(fuentes)}):")
        for i, doc in enumerate(fuentes, 1):
            source = doc.metadata.get("source", "Desconocido")
            page = doc.metadata.get("page", "?")
            print(f"\n  [{i}] {os.path.basename(source)} - Página {page}")
            print(f"      {doc.page_content[:200]}...")


# ========== EJEMPLO DE USO ==========

if __name__ == "__main__":
    # Crear asistente
    asistente = AsistenteAcademico(modelo_llama="llama2:7b")

    # Opción 1: Cargar documentos por primera vez
    pdfs = [
        "documentos/RAG.pdf"
        # Agregar más PDFs aquí
    ]
    asistente.cargar_documentos(pdfs)

    # Opción 2: Cargar vectorstore existente (para ejecuciones posteriores)
    # asistente.cargar_vectorstore_existente()

    # Realizar consultas
    preguntas = [
        "¿Qué es RAG y cómo funciona?",
        "¿Qué técnicas de IA se utilizan en el proyecto?",
        "¿Cuáles son los objetivos específicos del asistente académico?",
    ]

    for pregunta in preguntas:
        resultado = asistente.consultar(pregunta)

        print("\n" + "=" * 60)
        print(f"💬 Respuesta:\n{resultado['respuesta']}")
        asistente.mostrar_fuentes(resultado["fuentes"])
        print("=" * 60)
