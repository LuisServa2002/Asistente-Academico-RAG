import os
import tempfile
from pathlib import Path

import streamlit as st

# Importar la clase del asistente
from asistente import AsistenteAcademico

# Configuración de la página
st.set_page_config(
    page_title="Asistente Académico RAG - UNI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados basados en la plataforma UNI
st.markdown(
    """
<style>
    /* Colores principales UNI */
    :root {
        --uni-red: #8B2332;
        --uni-red-dark: #6B1825;
        --uni-red-light: #A83145;
        --uni-beige: #F5F5F0;
        --uni-gray: #E8E8E8;
        --uni-text: #2C2C2C;
    }
    
    /* Header principal */
    .main-header {
        font-size: 2rem;
        color: var(--uni-red);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1rem;
        color: var(--uni-text);
        margin-bottom: 2rem;
    }
    
    /* Sidebar personalizado */
    [data-testid="stSidebar"] {
        background-color: var(--uni-red);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Headers en sidebar */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Labels y texto en sidebar */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Valores de sliders */
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] + div {
        color: white !important;
    }
    
    /* Selectbox */
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }
    
    /* File uploader */
    [data-testid="stSidebar"] .stFileUploader label,
    [data-testid="stSidebar"] .stFileUploader section {
        color: white !important;
    }
    
    /* Divider en sidebar */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Botones en sidebar */
    [data-testid="stSidebar"] button {
        background-color: white !important;
        color: var(--uni-red) !important;
        border: 2px solid white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background-color: var(--uni-beige) !important;
        border: 2px solid white !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Asegurar que el texto de los botones sea visible */
    [data-testid="stSidebar"] button p,
    [data-testid="stSidebar"] button span,
    [data-testid="stSidebar"] button div {
        color: var(--uni-red) !important;
    }
    
    /* Área de drag and drop en sidebar */
    [data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed rgba(255, 255, 255, 0.5) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploadDropzone"]:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 2px dashed white !important;
    }
    
    /* Texto dentro del file uploader */
    [data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] label,
    [data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] small,
    [data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] span {
        color: white !important;
    }
    
    /* Mensajes de chat */
    .stChatMessage {
        background-color: var(--uni-beige);
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid var(--uni-red);
    }
    
    /* Cards de bienvenida */
    .welcome-card {
        background-color: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-top: 4px solid var(--uni-red);
        height: 100%;
    }
    
    .welcome-card h3 {
        color: var(--uni-red);
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .welcome-card p {
        color: #2C2C2C;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Botones principales */
    .stButton > button {
        background-color: var(--uni-red);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: var(--uni-red-dark);
        box-shadow: 0 4px 8px rgba(139, 35, 50, 0.3);
    }
    
    /* Expander de fuentes */
    .streamlit-expanderHeader {
        background-color: var(--uni-beige);
        color: var(--uni-red);
        font-weight: 600;
    }
    
    /* Info boxes */
    .stAlert {
        border-left: 4px solid var(--uni-red);
    }
    
    /* Dividers */
    hr {
        border-color: var(--uni-gray);
    }
    
    /* Input de chat */
    .stChatInputContainer {
        border-top: 2px solid var(--uni-gray);
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #E8F5E9;
        color: #2E7D32;
        border-left: 4px solid #4CAF50;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #FFF3E0;
        color: #E65100;
        border-left: 4px solid #FF9800;
    }
    
    /* Texto dentro de mensajes de warning */
    .stWarning p {
        color: #E65100 !important;
    }
    
    /* Error messages */
    .stError {
        background-color: #FFEBEE;
        color: #C62828;
        border-left: 4px solid #F44336;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Inicializar estado de sesión
if "asistente" not in st.session_state:
    st.session_state.asistente = None
if "historial" not in st.session_state:
    st.session_state.historial = []
if "documentos_cargados" not in st.session_state:
    st.session_state.documentos_cargados = False

# Header
st.markdown('<p class="main-header">Asistente Académico con RAG</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Universidad Nacional de Ingeniería - Inteligencia Artificial</p>',
    unsafe_allow_html=True
)

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración")

    # Selección de modelo
    modelo = st.selectbox(
        "Modelo LLaMA",
        ["llama2:7b", "llama3:8b", "mistral:7b"],
        help="Selecciona el modelo de Ollama a utilizar",
    )

    temperatura = st.slider(
        "Temperatura", 
        0.0, 
        1.0, 
        0.3, 
        help="Controla la creatividad de las respuestas"
    )

    top_k = st.slider(
        "Fragmentos a recuperar",
        1,
        10,
        3,
        help="Número de fragmentos relevantes a usar",
    )

    st.divider()

    # Sección de carga de documentos
    st.header("Documentos")

    uploaded_files = st.file_uploader(
        "Cargar PDFs del curso",
        type=["pdf"],
        accept_multiple_files=True,
        help="Sube los apuntes, libros o documentos del curso",
    )

    if st.button("Inicializar Asistente", type="primary", use_container_width=True):
        if uploaded_files:
            with st.spinner("Inicializando asistente y procesando documentos..."):
                try:
                    # Guardar archivos temporalmente
                    temp_paths = []
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".pdf"
                        ) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            temp_paths.append(tmp_file.name)

                    # Inicializar asistente
                    st.session_state.asistente = AsistenteAcademico(
                        modelo_llama=modelo,
                        temperatura=temperatura,
                        top_k=top_k
                    )
                    st.session_state.asistente.cargar_documentos(temp_paths)

                    # Limpiar archivos temporales
                    for path in temp_paths:
                        try:
                            os.unlink(path)
                        except Exception:
                            pass

                    st.session_state.documentos_cargados = True
                    st.success(f"{len(uploaded_files)} documentos cargados correctamente")

                except Exception as e:
                    st.error(f"Error al cargar documentos: {str(e)}")
        else:
            st.warning("Por favor, sube al menos un documento PDF")

    # Mostrar estado
    if st.session_state.documentos_cargados:
        st.success("Sistema listo")
        
        # Opción para cargar base de datos existente
        if st.button("Cargar Base de Datos Existente", use_container_width=True):
            try:
                with st.spinner("Cargando base de datos..."):
                    st.session_state.asistente = AsistenteAcademico(
                        modelo_llama=modelo,
                        temperatura=temperatura,
                        top_k=top_k
                    )
                    st.session_state.asistente.cargar_vectorstore_existente()
                    st.session_state.documentos_cargados = True
                    st.success("Base de datos cargada correctamente")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        if st.button("Reiniciar", use_container_width=True):
            st.session_state.asistente = None
            st.session_state.historial = []
            st.session_state.documentos_cargados = False
            st.rerun()

    st.divider()

    # Información del proyecto
    with st.expander("Sobre el proyecto"):
        st.markdown("""
        **Asistente Académico con RAG**
        
        Desarrollado por:
        - Iman Noriega Melissa
        - Méndez Gonzalo Miguel
        - Orrego Torrejón Diego
        - Pineda García Diego
        - Trujillo Serva Luis Andre
        
        **Tecnologías:**
        - LLaMA (Ollama)
        - LangChain
        - ChromaDB
        - Sentence Transformers
        """)

# Área principal
if not st.session_state.documentos_cargados:
    # Pantalla de bienvenida
    st.info("Por favor, carga documentos PDF en la barra lateral para comenzar")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="welcome-card">
            <h3>Búsqueda Inteligente</h3>
            <p>Encuentra información específica en tus documentos usando búsqueda semántica avanzada</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="welcome-card">
            <h3>Respuestas Contextuales</h3>
            <p>Obtén respuestas precisas basadas en el contenido de tus materiales académicos</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="welcome-card">
            <h3>Citas de Fuentes</h3>
            <p>Verifica la información con referencias directas a las páginas originales</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Interfaz de chat

    # Mostrar historial
    for mensaje in st.session_state.historial:
        with st.chat_message(mensaje["rol"]):
            st.markdown(mensaje["contenido"])

            # Mostrar fuentes si es una respuesta del asistente
            if mensaje["rol"] == "assistant" and "fuentes" in mensaje:
                with st.expander("Ver fuentes"):
                    for i, fuente in enumerate(mensaje["fuentes"], 1):
                        source = fuente.metadata.get("source", "Desconocido")
                        page = fuente.metadata.get("page", "?")
                        st.markdown(f"**[{i}]** {Path(source).name} - Página {page}")
                        st.text(fuente.page_content[:300] + "...")
                        st.divider()

    # Input del usuario
    if pregunta := st.chat_input("Escribe tu pregunta aquí..."):
        # Agregar pregunta al historial
        st.session_state.historial.append({"rol": "user", "contenido": pregunta})

        # Mostrar pregunta
        with st.chat_message("user"):
            st.markdown(pregunta)

        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # Actualizar parámetros si cambiaron
                    if st.session_state.asistente:
                        st.session_state.asistente.actualizar_parametros(
                            temperatura=temperatura,
                            top_k=top_k
                        )
                    
                    # Consultar al asistente
                    resultado = st.session_state.asistente.consultar(pregunta)

                    st.markdown(resultado["respuesta"])

                    # Agregar respuesta al historial
                    st.session_state.historial.append(
                        {
                            "rol": "assistant",
                            "contenido": resultado["respuesta"],
                            "fuentes": resultado["fuentes"],
                        }
                    )

                    # Mostrar fuentes
                    if resultado["fuentes"]:
                        with st.expander("Ver fuentes"):
                            for i, fuente in enumerate(resultado["fuentes"], 1):
                                source = fuente.metadata.get("source", "Desconocido")
                                page = fuente.metadata.get("page", "?")
                                st.markdown(f"**[{i}]** {Path(source).name} - Página {page}")
                                st.text(fuente.page_content[:300] + "...")
                                st.divider()

                except Exception as e:
                    error_msg = str(e)
                    st.error(f"Error: {error_msg}")
                    # Agregar mensaje de error al historial
                    st.session_state.historial.append(
                        {
                            "rol": "assistant",
                            "contenido": f"Lo siento, ocurrió un error: {error_msg}",
                            "fuentes": [],
                        }
                    )

# Footer
st.divider()
st.caption("Desarrollado por el equipo de IA - UNI FC 2025-2")