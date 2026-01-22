"""
FICEM Watch - Asistente Ejecutivo de Posicionamiento

Interface Streamlit para consultas RAG sobre documentos FICEM.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

# Configuracion
CHROMA_DB_PATH = Path(os.getenv("CHROMA_DB_PATH", "./chroma_db"))
MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-5-sonnet-20241022")

# System prompt con placeholder de estrategia comunicacional
SYSTEM_PROMPT = """Eres el asistente ejecutivo de posicionamiento de FICEM (Federacion Interamericana del Cemento).

Tu rol es ayudar a directivos de FICEM a responder consultas basandote en la documentacion oficial de la organizacion.

## REGLAS CRITICAS

1. **SIEMPRE cita tus fuentes**: Cada afirmacion debe incluir [Fuente: nombre_documento]
2. **NUNCA inventes informacion**: Si no encuentras datos en los documentos, di "No tengo informacion oficial sobre esto"
3. **Prioriza documentos recientes**: Si hay conflicto entre fechas, usa la informacion mas reciente
4. **Formato ejecutivo**: Respuestas concisas, estructuradas, listas para usar

## LINEAMIENTOS COMUNICACIONALES (Placeholder - Version Prototipo)

Tono: Profesional, tecnico, propositivo
Enfoque: Sostenibilidad, innovacion, compromiso ambiental
Evitar: Lenguaje defensivo, minimizar problemas ambientales

## CONTEXTO RELEVANTE

{context}

## PREGUNTA

{question}

## RESPUESTA

Proporciona una respuesta estructurada con:
1. Respuesta directa a la pregunta
2. Datos de soporte con citas [Fuente: documento]
3. Contexto adicional si es relevante
"""

PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"]
)


@st.cache_resource
def load_vectorstore():
    """Carga el vectorstore de ChromaDB."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embeddings
    )

    return vectorstore


@st.cache_resource
def load_qa_chain(_vectorstore):
    """Crea la cadena de QA con el LLM."""
    llm = ChatAnthropic(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=2000
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=_vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa_chain


def format_sources(source_docs):
    """Formatea los documentos fuente para mostrar."""
    sources = []
    seen = set()

    for doc in source_docs:
        source = doc.metadata.get("source", "Desconocido")
        if source not in seen:
            seen.add(source)
            categoria = doc.metadata.get("categoria", "")
            descripcion = doc.metadata.get("descripcion", "")
            sources.append({
                "archivo": source,
                "categoria": categoria,
                "descripcion": descripcion
            })

    return sources


def main():
    st.set_page_config(
        page_title="FICEM Watch",
        page_icon="🏭",
        layout="wide"
    )

    st.title("🏭 FICEM Watch")
    st.caption("Asistente Ejecutivo de Posicionamiento - Prototipo")

    # Sidebar con info
    with st.sidebar:
        st.header("Acerca de")
        st.markdown("""
        **FICEM Watch** es un asistente que permite consultar
        la documentacion oficial de FICEM para:

        - Consultar historial de posiciones
        - Obtener datos para interpelaciones
        - Generar respuestas informadas

        ---
        **Prototipo v0.1**

        Documentos cargados:
        - Coprocesamiento
        - Emisiones CO2/GEI
        - Institucional FICEM
        """)

        st.warning("⚠️ Las respuestas requieren validacion humana antes de uso publico")

    # Verificar que existe el vectorstore
    if not CHROMA_DB_PATH.exists():
        st.error("❌ Base de datos no encontrada. Ejecuta primero: `python src/ingest.py`")
        return

    # Cargar recursos
    with st.spinner("Cargando base de conocimiento..."):
        vectorstore = load_vectorstore()
        qa_chain = load_qa_chain(vectorstore)

    # Input de consulta
    st.markdown("### Consulta")

    # Ejemplos de preguntas
    col1, col2 = st.columns(2)
    with col1:
        if st.button("¿Que es el coprocesamiento?"):
            st.session_state.query = "¿Que es el coprocesamiento y cual es la posicion de FICEM al respecto?"
    with col2:
        if st.button("Emisiones de CO2 en cemento"):
            st.session_state.query = "¿Cuales son las principales fuentes de emisiones de CO2 en la industria del cemento?"

    query = st.text_area(
        "Escribe tu pregunta:",
        value=st.session_state.get("query", ""),
        height=100,
        placeholder="Ej: ¿Cual ha sido la posicion de FICEM sobre el impuesto al carbono?"
    )

    if st.button("Consultar", type="primary"):
        if not query.strip():
            st.warning("Por favor, escribe una pregunta")
            return

        with st.spinner("Buscando en documentos FICEM..."):
            try:
                result = qa_chain.invoke({"query": query})

                # Mostrar respuesta
                st.markdown("### Respuesta")
                st.markdown(result["result"])

                # Mostrar fuentes
                st.markdown("### Fuentes Consultadas")
                sources = format_sources(result["source_documents"])

                for src in sources:
                    with st.expander(f"📄 {src['archivo']}"):
                        st.markdown(f"**Categoria:** {src['categoria']}")
                        if src['descripcion']:
                            st.markdown(f"**Descripcion:** {src['descripcion']}")

            except Exception as e:
                st.error(f"Error al procesar consulta: {str(e)}")

    # Footer
    st.markdown("---")
    st.caption("FICEM Watch - Prototipo | Los datos provienen de documentacion oficial FICEM")


if __name__ == "__main__":
    main()
