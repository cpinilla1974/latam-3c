# Contexto para FICEM Knowledge Platform

**Documento de transferencia de conocimiento**
**Fecha:** 2025-12-02
**Origen:** Proyecto LATAM-3C
**Destino:** Nuevo proyecto ficem-knowledge-platform
**Autor:** Claude Code (Opus 4.5)

---

## Propósito de este Documento

Este documento transfiere el contexto completo del proyecto LATAM-3C a un nuevo proyecto que funcionará como backend de conocimiento. Está diseñado para ser consumido por otra instancia de Claude Code.

**Convención de formato:**
- `[HECHO]` - Información objetiva verificada
- `[OPINIÓN]` - Recomendación o preferencia del autor

---

## 1. Estado Actual del Proyecto Origen (LATAM-3C)

### 1.1 Descripción General

`[HECHO]` LATAM-3C es una aplicación Streamlit para análisis de huella de carbono en la industria del concreto en Latinoamérica. Incluye:

- Dashboard de visualización
- Calculadora 3C (Carbon, Cost, Compliance)
- Chat con RAG para benchmarking
- Generador de análisis con IA

### 1.2 Estructura de Archivos Relevante

```
/home/cpinilla/projects/latam-3c/
├── v1/
│   ├── app.py                          # Entrada principal Streamlit
│   ├── pages/
│   │   └── ai/
│   │       ├── 02_chat_benchmarking.py # Chat RAG
│   │       └── 10_generador_analisis.py # Generador con Claude API
│   ├── ai_modules/
│   │   ├── rag/
│   │   │   ├── vector_store.py         # ChromaDB manager
│   │   │   ├── rag_chain.py            # LangChain RAG
│   │   │   └── document_processor.py   # Procesador de PDFs
│   │   └── analytics/
│   │       └── data_analyzer.py
│   └── data/
│       └── vector_store/
│           └── chroma_db/              # 1255 documentos indexados
├── docs/
│   ├── analisis/
│   │   ├── analisis_profundo_bd_2025-12-02.md
│   │   └── Analisis_Profundo_BD_LATAM4C.pdf
│   └── benchmarking/
│       └── GCCA_GNR_Concrete_KPIs_Referencia.md
└── scripts/
    └── generar_pdf_analisis.py
```

### 1.3 Base de Datos PostgreSQL

`[HECHO]` Base de datos: `latam4c_db`

**Tablas de datos operacionales:**
| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| huella_concretos | 260 | Datos de huella CO2 por planta/año/resistencia |
| cementos | 139 | Tipos de cemento y sus huellas |
| plantas_latam | 265 | Catálogo de plantas LATAM |

**Tablas de referencias GCCA:**
| Tabla | Descripción |
|-------|-------------|
| ref_gcca_benchmarks | Benchmarks internacionales con estadísticas |
| ref_kpis | Definición de KPIs |
| ref_categorias_kpi | Categorías (Energía, Transporte, etc.) |
| ref_dimensiones | Dimensiones de clasificación |
| ref_valores_dimension | Valores por dimensión |
| ref_benchmark_dimensiones | Relación N:M benchmarks-dimensiones |
| ref_rangos_interpretativos | Rangos de interpretación (óptimo, crítico, etc.) |

**Vistas creadas:**
| Vista | Propósito |
|-------|-----------|
| v_analisis_profundo | Métricas derivadas para análisis |
| v_benchmarks_completos | JOIN completo de benchmarks GCCA |
| v_benchmarks_por_region | Vista simplificada por región |

### 1.4 Vector Store (ChromaDB)

`[HECHO]` Ubicación: `/home/cpinilla/projects/latam-3c/v1/data/vector_store/chroma_db/`

- **Colección:** `ficem_tech_docs`
- **Documentos:** 1255
- **Modelo de embeddings:** `mxbai-embed-large` (Ollama local)
- **Contenido:** Documentos técnicos GCCA, papers, referencias de benchmarking

### 1.5 Modelos de IA Utilizados

`[HECHO]`
- **Embeddings:** Ollama `mxbai-embed-large` (local, puerto 11434)
- **LLM para RAG:** Ollama `qwen2.5:7b` (local)
- **LLM para generación:** Claude API `claude-sonnet-4-20250514`

---

## 2. Análisis de Datos Realizado

### 2.1 Hallazgos Clave

`[HECHO]` Se realizó un análisis profundo de la base de datos con los siguientes descubrimientos:

1. **Anomalía en datos de "pacas":** Los valores A1-A4 están ~100x mayores que las otras plantas (23,249 vs ~230 kg CO2/m³). Posible error de escala o unidades.

2. **Paradoja de eficiencia:** A mayor resistencia (MPa), menor huella de CO2 por unidad de resistencia:
   - 0-10 MPa: 59.74 kg CO2/MPa
   - 40-50 MPa: 7.95 kg CO2/MPa
   - >60 MPa: 6.05 kg CO2/MPa

3. **Correlaciones por planta:**
   - mzma: 0.9818 (proceso muy predecible)
   - melon: 0.2147 (alta variabilidad, pero mejor eficiencia)

4. **Posicionamiento LATAM:** 271 kg CO2/m³ promedio, 8% mejor que GCCA mundial (294).

5. **Tendencias 2024:** Todas las plantas mejorando (-7 a -18 kg CO2/m³).

### 2.2 Documentación Generada

`[HECHO]` Se crearon:
- `docs/analisis/analisis_profundo_bd_2025-12-02.md` (documento completo)
- `docs/analisis/Analisis_Profundo_BD_LATAM4C.pdf` (versión profesional)
- Vista SQL `v_analisis_profundo` en la base de datos

---

## 3. Problemas Identificados en la Arquitectura Actual

### 3.1 Limitaciones Técnicas

`[HECHO]`

1. **RAG acoplado a Streamlit:** El código de RAG está embebido en `ai_modules/` y solo es accesible desde la aplicación Streamlit.

2. **No hay API REST:** No existe forma de consumir los datos o el RAG desde otros sistemas.

3. **Análisis no persisten:** Los análisis generados se pierden al cerrar sesión. Solo quedan los archivos manuales.

4. **Sin versionado de conocimiento:** No hay forma de comparar análisis históricos ni detectar cambios.

5. **ChromaDB sin separación:** Una sola colección mezcla documentos técnicos con potenciales análisis propios.

### 3.2 Deuda Técnica

`[HECHO]`

1. **LangChain deprecation warnings:** Clases `OllamaEmbeddings` y `Chroma` deprecadas.
2. **RAGChain sin método `invoke`:** Error recurrente en `10_generador_analisis.py`.
3. **Modelo Claude hardcodeado:** Cambios de modelo requieren editar código.

---

## 4. Requisitos del Nuevo Proyecto

### 4.1 Requisitos Funcionales

`[HECHO]` El usuario expresó necesidad de:

1. **Backend independiente con FastAPI** - Separar lógica de conocimiento del frontend.
2. **Base de datos vectorial** - Para RAG y búsqueda semántica.
3. **Base de datos relacional** - Para cubos OLAP y datos operacionales.
4. **Almacenamiento de documentos** - PDFs, reportes generados.
5. **Persistencia de análisis** - Que no se pierdan al agregar datos.
6. **Análisis incremental vs completo** - Decidir cuándo regenerar.

### 4.2 Casos de Uso Esperados

`[HECHO]` Basado en la conversación:

1. Agregar nuevos datos de huella de carbono
2. Consultar benchmarks GCCA via API
3. Ejecutar análisis profundo bajo demanda
4. Comparar análisis históricos
5. Buscar en documentos técnicos (RAG)
6. Generar reportes en PDF/Excel

---

## 5. Arquitectura Propuesta

### 5.1 Visión General

`[OPINIÓN]` Recomiendo una arquitectura de microservicios ligeros (no full microservices) con FastAPI como núcleo:

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTES                                │
│  (Streamlit LATAM-3C, Jupyter, CLI, otros)                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/REST
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              FICEM KNOWLEDGE PLATFORM (FastAPI)                 │
├─────────────────────────────────────────────────────────────────┤
│  /api/v1/                                                       │
│  ├── /knowledge  (RAG, búsqueda semántica, chat)               │
│  ├── /analytics  (KPIs, análisis, comparaciones)               │
│  ├── /data       (CRUD datos operacionales)                    │
│  ├── /benchmarks (Referencias GCCA)                            │
│  └── /reports    (Generación de informes)                      │
├─────────────────────────────────────────────────────────────────┤
│                      SERVICIOS                                  │
│  ├── KnowledgeService (RAG, embeddings)                        │
│  ├── AnalyticsService (KPIs, trends, anomalías)                │
│  ├── DataService (importación, validación)                     │
│  └── ReportService (PDF, Excel)                                │
├─────────────────────────────────────────────────────────────────┤
│                      DATA LAYER                                 │
│  ├── PostgreSQL (relacional, cubos, histórico)                 │
│  ├── ChromaDB (vectorial, documentos, embeddings)              │
│  └── FileStorage (PDFs, reportes)                              │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Estructura de Proyecto Recomendada

`[OPINIÓN]` Estructura basada en Domain-Driven Design ligero:

```
ficem-knowledge-platform/
├── README.md
├── pyproject.toml
├── docker-compose.yml
├── alembic/                    # Migraciones BD
│
├── app/
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Pydantic Settings
│   │
│   ├── api/v1/                 # Endpoints
│   │   ├── knowledge.py
│   │   ├── analytics.py
│   │   ├── data.py
│   │   ├── benchmarks.py
│   │   └── reports.py
│   │
│   ├── services/               # Lógica de negocio
│   │   ├── knowledge/
│   │   │   ├── rag_chain.py
│   │   │   ├── vector_store.py
│   │   │   └── embeddings.py
│   │   ├── analytics/
│   │   │   ├── kpi_engine.py
│   │   │   └── comparisons.py
│   │   └── reports/
│   │
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   └── core/                   # DB connections, LLM clients
│
├── data/
│   ├── vector_store/
│   │   ├── tech_docs/          # Documentos técnicos GCCA
│   │   └── analisis/           # Análisis propios
│   └── documents/
│
└── scripts/
    ├── init_db.py
    └── migrate_from_latam3c.py
```

### 5.3 Modelo de Datos Propuesto

`[OPINIÓN]` Agregar estas tablas a la estructura existente:

```sql
-- Persistencia de análisis
CREATE TABLE analisis_historico (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo VARCHAR(50) NOT NULL,  -- 'profundo', 'delta', 'kpi'
    version INTEGER DEFAULT 1,

    -- Contenido
    titulo VARCHAR(200),
    resumen TEXT,
    contenido_md TEXT,
    hallazgos JSONB,
    metricas JSONB,

    -- Contexto
    datos_desde DATE,
    datos_hasta DATE,
    n_registros INTEGER,
    plantas_incluidas TEXT[],

    -- Comparación con análisis previo
    analisis_base_id INTEGER REFERENCES analisis_historico(id),
    cambios_vs_base JSONB,

    -- Link a vectorstore
    embedding_id VARCHAR(100),

    activo BOOLEAN DEFAULT TRUE
);

-- KPIs en tiempo real (vista materializada)
CREATE MATERIALIZED VIEW mv_kpis_actuales AS
SELECT
    NOW() as calculado_en,
    COUNT(*) as total_registros,
    AVG("huella_co2") as huella_promedio,
    -- ... más métricas
FROM huella_concretos;
```

### 5.4 Estrategia de Colecciones Vectoriales

`[OPINIÓN]` Separar en dos colecciones:

| Colección | Contenido | Propósito |
|-----------|-----------|-----------|
| `tech_docs` | Documentos GCCA, papers, referencias | RAG para consultas técnicas |
| `analisis` | Análisis propios generados | Histórico consultable por IA |

**Justificación:** Permite filtrar por tipo en búsquedas y evita contaminar referencias externas con contenido propio.

### 5.5 Flujo de Análisis Incremental

`[OPINIÓN]` Implementar este flujo automático:

```
Nuevos datos insertados
        │
        ▼
REFRESH mv_kpis_actuales
        │
        ▼
Comparar con último análisis
        │
        ├── Cambio < 5% → Solo log
        │
        └── Cambio >= 5% → Generar análisis delta
                                │
                                ▼
                          Guardar en:
                          1. analisis_historico (PostgreSQL)
                          2. analisis (ChromaDB)
```

---

## 6. Migración Recomendada

### 6.1 Datos a Migrar

`[HECHO]` Desde LATAM-3C:

| Origen | Destino | Método |
|--------|---------|--------|
| PostgreSQL `latam4c_db` | PostgreSQL nuevo | pg_dump/restore |
| ChromaDB `ficem_tech_docs` | ChromaDB `tech_docs` | Copiar directorio |
| `docs/analisis/*.md` | Tabla `analisis_historico` | Script de migración |
| `docs/benchmarking/` | ChromaDB `tech_docs` | Reindexar |

### 6.2 Código a Reutilizar

`[OPINIÓN]` Estos módulos pueden adaptarse:

- `ai_modules/rag/vector_store.py` → Actualizar imports LangChain
- `ai_modules/rag/document_processor.py` → Reutilizar tal cual
- `scripts/generar_pdf_analisis.py` → Mover a services/reports/

### 6.3 Código a Reescribir

`[OPINIÓN]` Estos requieren reescritura:

- `ai_modules/rag/rag_chain.py` → Nuevo diseño con LangChain actualizado
- Endpoints de chat → FastAPI con streaming

---

## 7. Dependencias Recomendadas

`[OPINIÓN]`

```toml
[project]
dependencies = [
    # API
    "fastapi>=0.109.0",
    "uvicorn>=0.27.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",

    # Base de datos
    "sqlalchemy>=2.0.25",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",

    # Vector store
    "chromadb>=0.4.22",
    "langchain>=0.1.0",
    "langchain-community>=0.0.13",
    "langchain-chroma>=0.1.0",  # Nueva versión

    # Embeddings y LLM
    "langchain-ollama>=0.0.1",  # Nueva versión (no deprecated)
    "anthropic>=0.18.0",

    # Utilidades
    "python-multipart>=0.0.6",
    "aiofiles>=23.2.1",

    # Reportes
    "reportlab>=4.0.0",
    "python-docx>=1.0.0",
]
```

---

## 8. Configuración Recomendada

`[OPINIÓN]`

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "FICEM Knowledge Platform"

    # PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "ficem_knowledge"
    POSTGRES_USER: str = "ficem"
    POSTGRES_PASSWORD: str = ""

    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./data/vector_store"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    EMBEDDING_MODEL: str = "mxbai-embed-large"
    LLM_MODEL: str = "qwen2.5:7b"

    # Claude (opcional)
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"

    # Análisis
    ANALYSIS_CHANGE_THRESHOLD: float = 0.05  # 5%

    class Config:
        env_file = ".env"
```

---

## 9. APIs Mínimas para MVP

`[OPINIÓN]` Empezar con estas:

```yaml
# Fase 1 - MVP
POST /api/v1/knowledge/search     # Búsqueda semántica
POST /api/v1/knowledge/chat       # Chat RAG
GET  /api/v1/analytics/kpis       # KPIs actuales
GET  /api/v1/benchmarks/gcca      # Referencias GCCA

# Fase 2 - Datos
POST /api/v1/data/import          # Importar datos
GET  /api/v1/data/huella          # Consultar huella

# Fase 3 - Análisis
POST /api/v1/analytics/analysis   # Ejecutar análisis
GET  /api/v1/analytics/history    # Histórico
```

---

## 10. Consideraciones Finales

### 10.1 Sobre el Uso de Claude Code entre Proyectos

`[OPINIÓN]` El enfoque de transferir contexto via documento es **correcto y eficiente** porque:

1. Cada instancia de Claude Code tiene límite de contexto
2. Los proyectos deben ser independientes
3. Un documento estructurado es mejor que copiar conversaciones
4. Permite filtrar solo lo relevante

### 10.2 Recomendación de Implementación

`[OPINIÓN]` Sugiero este orden:

1. **Crear proyecto vacío** con estructura FastAPI
2. **Migrar datos PostgreSQL** (pg_dump/restore)
3. **Copiar ChromaDB** existente
4. **Implementar endpoints de solo lectura** (/kpis, /benchmarks, /search)
5. **Probar desde LATAM-3C** que puede consumir la API
6. **Agregar escritura** (/import, /analysis)
7. **Deprecar código duplicado** en LATAM-3C

### 10.3 Lo que NO Hacer

`[OPINIÓN]`

- No reescribir todo desde cero - hay código reutilizable
- No migrar a microservicios completos - overkill para este caso
- No usar ORM async si no hay alta concurrencia esperada
- No implementar autenticación compleja inicialmente (API interna)

---

## Anexo: Queries SQL Útiles

```sql
-- KPIs principales
SELECT
    COUNT(*) as registros,
    AVG("huella_co2") as huella_promedio,
    AVG("huella_co2"/NULLIF("REST",0)) as eficiencia
FROM huella_concretos;

-- Comparación con GCCA
SELECT
    'LATAM' as fuente, AVG("huella_co2") as valor
FROM huella_concretos
UNION ALL
SELECT 'GCCA Mundial', 294
UNION ALL
SELECT 'GCCA Europa', 262;

-- Tendencias por año
SELECT "año", "origen", AVG("huella_co2") as huella
FROM huella_concretos
GROUP BY "año", "origen"
ORDER BY "origen", "año";
```

---

**Fin del documento de contexto**
