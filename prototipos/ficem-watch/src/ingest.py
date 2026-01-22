"""
FICEM Watch - Document Ingestion Script

Carga documentos FICEM a ChromaDB para busqueda semantica.
"""

import os
import csv
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# Configuracion
DOCUMENTS_PATH = Path(os.getenv("DOCUMENTS_PATH", "/mnt/c/Users/cpini/OneDrive/RAG_DocumentosFICEM"))
CHROMA_DB_PATH = Path(os.getenv("CHROMA_DB_PATH", "./chroma_db"))
INDEX_FILE = DOCUMENTS_PATH / "_indice_documentos.csv"

# Categorias a cargar para el prototipo (subset)
PROTOTYPE_CATEGORIES = [
    "03_Coprocesamiento",
    "04_Emisiones_CO2_GEI",
    "07_Institucional_FICEM",
]


def load_index() -> dict:
    """Carga el indice CSV con metadatos de documentos."""
    index = {}
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row['Categoria']}/{row.get('Subcategoria', '')}/{row['Archivo']}".replace("//", "/")
                index[row['Archivo']] = {
                    "categoria": row['Categoria'],
                    "subcategoria": row.get('Subcategoria', ''),
                    "descripcion": row.get('Descripcion', ''),
                    "tipo": row.get('Tipo', '')
                }
    return index


def load_document(file_path: Path) -> list:
    """Carga un documento segun su tipo."""
    suffix = file_path.suffix.lower()

    try:
        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
            return loader.load()
        elif suffix in [".docx", ".doc"]:
            loader = Docx2txtLoader(str(file_path))
            return loader.load()
        else:
            print(f"  Tipo no soportado: {suffix}")
            return []
    except Exception as e:
        print(f"  Error cargando {file_path.name}: {e}")
        return []


def process_documents(categories: list = None) -> list:
    """Procesa documentos de las categorias especificadas."""
    if categories is None:
        categories = PROTOTYPE_CATEGORIES

    index = load_index()
    all_docs = []

    for category in categories:
        category_path = DOCUMENTS_PATH / category
        if not category_path.exists():
            print(f"Categoria no encontrada: {category}")
            continue

        print(f"\n=== Procesando: {category} ===")

        for file_path in category_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in [".pdf", ".docx", ".doc"]:
                print(f"  Cargando: {file_path.name}")
                docs = load_document(file_path)

                # Agregar metadatos
                metadata = index.get(file_path.name, {})
                for doc in docs:
                    doc.metadata.update({
                        "source": file_path.name,
                        "categoria": metadata.get("categoria", category),
                        "subcategoria": metadata.get("subcategoria", ""),
                        "descripcion": metadata.get("descripcion", ""),
                        "full_path": str(file_path)
                    })

                all_docs.extend(docs)
                print(f"    -> {len(docs)} paginas/secciones")

    return all_docs


def split_documents(docs: list) -> list:
    """Divide documentos en chunks para embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(docs)
    print(f"\nTotal chunks generados: {len(chunks)}")
    return chunks


def create_vectorstore(chunks: list) -> Chroma:
    """Crea la base de datos vectorial con ChromaDB."""
    print("\nCreando embeddings y vectorstore...")

    # Usar embeddings locales (no requiere API)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Crear vectorstore
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_PATH)
    )

    print(f"Vectorstore creado en: {CHROMA_DB_PATH}")
    return vectorstore


def main():
    """Proceso principal de ingesta."""
    print("=" * 50)
    print("FICEM Watch - Ingesta de Documentos")
    print("=" * 50)

    print(f"\nRuta documentos: {DOCUMENTS_PATH}")
    print(f"Categorias a procesar: {PROTOTYPE_CATEGORIES}")

    # Verificar que existe la ruta
    if not DOCUMENTS_PATH.exists():
        print(f"\nERROR: No se encuentra la ruta de documentos: {DOCUMENTS_PATH}")
        return

    # Cargar documentos
    docs = process_documents()
    print(f"\nTotal documentos cargados: {len(docs)}")

    if not docs:
        print("No se cargaron documentos. Verificar rutas y formatos.")
        return

    # Dividir en chunks
    chunks = split_documents(docs)

    # Crear vectorstore
    vectorstore = create_vectorstore(chunks)

    print("\n" + "=" * 50)
    print("Ingesta completada exitosamente!")
    print("=" * 50)


if __name__ == "__main__":
    main()
