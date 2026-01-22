# FICEM Watch - Prototipo

Prueba de concepto del asistente ejecutivo de posicionamiento.

## Objetivo del Prototipo

Validar la arquitectura RAG con documentos FICEM reales antes de desarrollar el sistema completo.

## Estructura

```
ficem-watch/
├── src/
│   ├── ingest.py      # Carga documentos a ChromaDB
│   └── app.py         # Interface Streamlit
├── data/              # Symlink a documentos FICEM
├── chroma_db/         # Base de datos vectorial
├── requirements.txt
└── .env.example
```

## Alcance del Prototipo

**Incluye:**
- Chat simple para consultas
- Busqueda semantica en documentos FICEM
- Respuestas con citas verificables
- Subset de documentos (15-20 docs)

**No incluye (para version completa):**
- Capa 2 de estrategia comunicacional (usa placeholder)
- Autenticacion
- Exportacion PDF
- Acceso movil

## Documentos Fuente

Ubicacion: `/mnt/c/Users/cpini/OneDrive/RAG_DocumentosFICEM/`

## Requisitos

- Python 3.10+
- API Key Anthropic

## Instalacion

```bash
cd prototipos/ficem-watch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tu API key
```

## Uso

```bash
# Paso 1: Ingestar documentos
python src/ingest.py

# Paso 2: Ejecutar app
streamlit run src/app.py
```

## Especificacion Completa

Ver: [proyectos/ficem-cognos/ficem-watch/README.md](../../proyectos/ficem-cognos/ficem-watch/README.md)
