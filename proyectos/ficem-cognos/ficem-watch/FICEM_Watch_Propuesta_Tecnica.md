# FICEM Watch - Propuesta Técnica de Implementación

**Asistente Ejecutivo de Posicionamiento Estratégico**

**Fecha**: Enero 2026
**Versión**: 1.1
**Preparado para**: FICEM (Federación Interamericana del Cemento)

---

## Resumen Ejecutivo

FICEM Watch es un sistema de **posicionamiento estratégico** diseñado para directivos de FICEM. No es simplemente un buscador de documentos ni un chatbot genérico: es una herramienta que combina el conocimiento institucional de FICEM con su estrategia comunicacional para generar respuestas alineadas con la voz de la organización.

**FICEM Watch NO es un buscador de documentos; es una herramienta de comunicación política y técnica.**

### Problema que Resuelve

Los directivos de FICEM enfrentan diariamente:
- Solicitudes de posicionamiento urgente ante noticias del sector
- Necesidad de consultar historial de posiciones anteriores
- Requerimientos de datos duros para interpelaciones de gobiernos/medios
- Preparación de briefings ejecutivos en tiempos reducidos

### Solución Propuesta

Un asistente inteligente que en minutos proporciona:
- Respuestas **informadas** (basadas en ~94 documentos institucionales)
- Respuestas **alineadas** (con la estrategia comunicacional de FICEM)
- Con **citas verificables** (nunca inventa información)
- Con **alertas** sobre temas sensibles que requieren validación humana

---

## Arquitectura de Dos Capas

El diferenciador clave de FICEM Watch es su arquitectura de dos capas que garantiza respuestas no solo correctas, sino estratégicamente alineadas.

### Capa 1: Conocimiento (Qué sabe FICEM)

| Componente | Descripción |
|------------|-------------|
| **Base documental** | ~94 documentos en 10 categorías |
| **Tecnología** | RAG (Retrieval-Augmented Generation) |
| **Almacenamiento** | Base de datos vectorial (Qdrant) |
| **Búsqueda** | Híbrida (semántica + palabras clave) |

**Categorías de documentos disponibles:**
- Coprocesamiento
- Emisiones CO2/GEI
- Institucional FICEM
- Reportes de Sostenibilidad
- Buenas Prácticas
- Actas de Congresos
- Documentos internos
- Referencias GCCA, BID, CAF

### Capa 2: Estrategia Comunicacional (Cómo comunica FICEM)

El sistema no solo busca información; **filtra y formula respuestas** según:

| Elemento | Función |
|----------|---------|
| **Tono institucional** | Formal, técnico, propositivo (no reactivo/defensivo) |
| **Mensajes clave** | Pilares comunicacionales que FICEM siempre refuerza |
| **Públicos objetivo** | Adapta mensaje según audiencia (gobierno, industria, medios) |
| **Temas sensibles** | Identifica temas que requieren validación humana |
| **Posicionamiento diferencial** | Lo que distingue a FICEM de otras voces del sector |

### Flujo de Generación de Respuesta

```
Pregunta del usuario
        |
        v
[Capa 1: Conocimiento]
   Busca información relevante en base de datos
   Recupera documentos con Re-ranking
        |
        v
[Capa 2: Estrategia]
   Filtra según lineamientos comunicacionales
   Formula respuesta con tono institucional
        |
        v
Respuesta alineada + citas verificables + alertas si aplica
```

---

## Casos de Uso

### 1. Respuesta Rápida a Noticias

**Escenario**: "Salió una noticia sobre impuestos al carbono en Colombia, ¿qué debemos decir?"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Posición histórica de FICEM + contexto regional + datos relevantes |
| **Estrategia** | Formulación con tono institucional + alineación con mensajes clave |

**Output**: Respuesta sugerida lista para usar, con citas verificables

### 2. Consulta de Historial

**Escenario**: "¿Qué hemos dicho sobre factores clínker en los últimos 3 años?"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Línea de tiempo de posiciones + documentos clave + evolución |
| **Estrategia** | Identificación de cambios de postura + coherencia con lineamientos actuales |

**Output**: Resumen ejecutivo de evolución del discurso + alertas si hay inconsistencias

### 3. Datos Duros para Interpelaciones

**Escenario**: "Gobierno pregunta cuántas empresas cumplen con X norma"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Estadísticas precisas + fuentes verificables + comparación regional |
| **Estrategia** | Contexto narrativo (enfatizar logros, reconocer desafíos) |

**Output**: Datos con narrativa alineada a posicionamiento FICEM

### 4. Reporte Ejecutivo Urgente

**Escenario**: "Necesito briefing completo sobre co-procesamiento para reunión en 1 hora"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Datos técnicos + posiciones históricas + referencias documentales |
| **Estrategia** | Estructura y tono según audiencia de la reunión |

**Output**: Reporte ejecutivo de 2 páginas con voz institucional FICEM

### 5. Tema Sensible

**Escenario**: "¿Qué responder sobre el caso de contaminación en planta X?"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Información disponible sobre el caso + contexto |
| **Estrategia** | **ALERTA**: Tema sensible - requiere validación humana |

**Output**: Borrador de respuesta + flag de revisión obligatoria

---

## Por qué los RAG Tradicionales Fallan

### Investigación de Mercado

El 72-80% de los proyectos RAG empresariales fallan en producción. La investigación académica (Barnett et al., 2024/2025) identifica 7 puntos de falla:

| # | Punto de Falla | Descripción |
|---|----------------|-------------|
| 1 | **Contenido Faltante** | La respuesta no está en los documentos, pero el sistema inventa |
| 2 | **Fallo en Ranking** | El fragmento correcto existe pero no llega al Top K |
| 3 | **Fuera de Contexto** | Se recuperó pero no entró al prompt por límites |
| 4 | **No Extraído** | Está en el prompt pero el LLM no lo "ve" entre el ruido |
| 5 | **Formato Incorrecto** | El modelo no sigue las reglas de salida |
| 6 | **Especificidad Incorrecta** | Respuesta demasiado general o técnica |
| 7 | **Incompleto** | Solo recupera parte de la respuesta distribuida |

### El Fenómeno "Lost in the Middle"

Los modelos de lenguaje leen bien el inicio y final del contexto, pero **ignoran información en el medio**. Si la respuesta está en el fragmento 5 de 10, hay alta probabilidad de fallo.

### El Problema de los PDFs

Los PDFs son el **peor formato para RAG** porque "pintan" texto en coordenadas en lugar de mantener una estructura lógica. Si se corta una tabla por la mitad, se pierde la relación entre columnas.

> **Nota Crítica**: El fallo principal de los prototipos corporativos suele ser la **extracción**. Si el texto que entra a la base de datos es basura (tablas rotas, encabezados mezclados), el mejor LLM del mundo fallará. **Invertir el 60% del tiempo en el Parsing.**

### Solución: RAG Avanzado

FICEM Watch implementa técnicas de RAG Avanzado que mitigan estos fallos:

| Técnica | Problema que Resuelve |
|---------|----------------------|
| **Layout-aware Parsing (Docling)** | Extracción correcta de tablas y estructura |
| **Indexación en Markdown** | Preserva relación estructural de tablas |
| **Chunking semántico** | Fragmentos coherentes por tema, no por caracteres |
| **Búsqueda híbrida (Vectores + BM25)** | Encuentra tanto conceptos como datos exactos |
| **Re-ranking (Cohere)** | Elimina ruido, prioriza relevancia real |
| **Small-to-Big Retrieval** | Búsqueda precisa + contexto expandido |
| **Filtros de metadatos** | Si pregunta por "2024", filtra antes de buscar |

---

## Análisis ROI: GraphRAG vs RAG Avanzado

| Característica | Advanced RAG (Vectores + Re-ranker + Metadata) | GraphRAG (Nodos y Relaciones) |
|----------------|------------------------------------------------|-------------------------------|
| **Tiempo de implementación** | 3-5 días | 3-6 semanas |
| **Complejidad** | Media | Muy Alta |
| **Precisión en datos técnicos** | Muy Alta (con Re-ranker) | Superior en relaciones complejas |
| **Costo de inferencia** | Bajo / Medio | Muy Alto |

**Decisión para prototipo de 2 semanas**: No implementar GraphRAG desde cero (quedaría atrapado en limpieza de datos). El mejor ROI es **Hybrid RAG + Re-ranking**.

---

## Plan de Implementación

### Visión General

| Fase | Duración | Objetivo |
|------|----------|----------|
| **Fase 1: Prototipo** | 2 semanas | Demostrar valor y diferenciación |
| **Fase 2: Producción** | 2-3 meses | Sistema robusto y evaluado |

---

## FASE 1: Prototipo Diferenciador (2 Semanas)

### Objetivo

Construir un prototipo funcional que demuestre:
1. Capacidad de respuesta basada en documentos FICEM
2. Diferencia tangible respecto a RAG básicos que no funcionan
3. Potencial de la arquitectura de dos capas

El enfoque **NO es "más documentos"**, sino **"extracción de altísima calidad + inteligencia en la recuperación"**.

### Cronograma Detallado

| Días | Actividad Crítica | Entregable |
|------|-------------------|------------|
| **1-3** | **Parsing de Oro**: Procesar 94 docs con Docling | Carpeta de archivos `.md` limpios |
| **4-6** | **Indexación Híbrida**: BM25 + Vectores con metadatos | Base de datos Qdrant funcional |
| **7-9** | **Capa 2 (Estrategia)**: System Prompt y Re-ranking | Pipeline funcional con tono FICEM |
| **10-12** | **Evaluación Sintética**: Correr RAGAS sobre 40-50 preguntas | Reporte de precisión inicial |
| **13-14** | **Demo UI**: Interfaz que muestre Fuente y Pilar Estratégico | Prototipo funcional para directivos |

### Stack Tecnológico Fase 1

| Componente | Tecnología | Justificación |
|------------|------------|---------------|
| **Parsing** | Docling (IBM) | Superior para tablas técnicas, convierte a Markdown preservando estructura |
| **Alternativas parsing** | Unstructured.io, Marker | Unstructured usa visión para bounding boxes; Marker es rápido para fórmulas |
| **Vector DB** | Qdrant | Mejor soporte para búsqueda híbrida, fácil de levantar en Docker |
| **Búsqueda** | Híbrida (Vectores + BM25) | Encuentra conceptos Y datos exactos |
| **Re-ranker** | Cohere Rerank v3 Multilingual | Estándar de oro, drásticamente superior en español técnico |
| **Alternativas re-ranker** | Jina Reranker v2, BGE-M3, Mixedbread.ai | Jina para chunks largos; BGE-M3 si se requiere open-source |
| **Chunking** | SemanticChunker (LangChain) | Detecta rupturas de cohesión, fragmentos coherentes por tema |
| **Embeddings** | paraphrase-multilingual-MiniLM-L12-v2 | Buen rendimiento en español técnico |
| **LLM** | Claude 3.5 Sonnet | Redacción matizada, ideal para comunicaciones políticas |
| **Orquestador** | LangChain o LlamaIndex | Ambos soportan Hybrid Search out-of-the-box |
| **UI** | Streamlit | Desarrollo rápido, familiar para directivos |

### Detalle Técnico de Cada Etapa

#### Días 1-3: Parsing de Documentos (60% del éxito)

**Principio crítico**: Si la extracción de texto es deficiente, el mejor LLM fallará.

**Herramientas de Layout-aware Parsing**:

| Herramienta | Fortaleza |
|-------------|-----------|
| **Docling (IBM)** | Mejor para convertir PDFs complejos a Markdown, preserva tablas perfectamente |
| **Unstructured.io** | Usa modelos de visión para detectar bounding boxes (títulos, tablas, imágenes) |
| **Marker** | Muy rápido, alta fidelidad en fórmulas y tablas |

**Proceso**:
1. Procesar 94 PDFs con Docling
2. Convertir a Markdown (preserva tablas como texto estructurado)
3. Validar calidad con muestra aleatoria (5%) usando LLM "auditor"
4. Verificar especialmente: números, porcentajes, datos de emisiones

**Estrategia clave**: No indexar texto plano. **Indexar Markdown**. Las tablas en Markdown mantienen la relación estructural y son fácilmente "entendibles" por embeddings y LLM.

**Manejo de tablas complejas**:
- Docling normaliza celdas fusionadas (repite valores o usa estructura plana)
- El título de la tabla se adjunta a cada chunk
- Formato Markdown permite al LLM razonar sobre filas/columnas

#### Días 4-6: Indexación Híbrida

**Small-to-Big Retrieval**:
- Guardar chunks pequeños (oraciones) con su embedding
- En metadatos: ID del párrafo padre
- **Búsqueda**: encontrar oración precisa (mayor precisión)
- **Recuperación**: traer párrafo completo para contexto al LLM

**Metadatos por documento**:
```json
{
  "categoria": "coprocesamiento",
  "subcategoria": "normativa",
  "fecha": "2024-03-15",
  "year": 2024,
  "fuente": "Reporte_Sostenibilidad_2024.pdf",
  "pagina": 45,
  "nivel_acceso": "interno"
}
```

**Filtros de metadatos**: Si el usuario pregunta por "Manuales 2024", filtrar por metadato `year: 2024` **antes** de buscar semánticamente.

#### Días 7-9: Capa 2 (Estrategia)

**System Prompt con Chain of Thought (CoT)**:
```
Instrucciones:
1. Primero, extrae los hechos del contexto recuperado
2. Segundo, identifica cuál de los 3 pilares estratégicos de FICEM aplica
3. Tercero, redacta la respuesta usando el tono institucional

Tono FICEM: Formal, técnico, propositivo (nunca defensivo o reactivo)
Siempre incluir citas verificables con documento y página
Si no hay información, decir "No tengo información oficial sobre esto"
```

**Detección de temas sensibles (Clasificación Previa)**:
- Paso intermedio con LLM rápido (GPT-4o mini)
- Pregunta: "¿Es este un tema de crisis o interpelación?"
- Si es sensible: agregar alerta visual: ⚠️ "Esta respuesta requiere validación del departamento de comunicación"

**Re-ranking con Cohere**:
- Recuperar 20-50 fragmentos usando vectores
- Pasarlos por Cohere Rerank v3 Multilingual
- Reordenar basándose en relevancia real respecto a la pregunta
- Esto sube la precisión del 60% al 90% inmediatamente

#### Días 10-12: Evaluación RAGAS

**Generación de Dataset Sintético (LLM-as-a-Judge)**:

No se necesita historial humano. El flujo es:
1. Tomar documentos reales
2. LLM potente (GPT-4o o Claude 3.5) analiza chunks y genera:
   - Una pregunta
   - Una respuesta ideal
   - El contexto de donde la sacó
3. RAGAS puede generar preguntas "difíciles" (razonamiento, multihop, con trampas)

**Tamaño del dataset**: 40-50 pares pregunta/respuesta (mínimo para ser estadísticamente relevante)

**Métricas RAGAS a monitorear**:

| Métrica | Qué mide |
|---------|----------|
| **Faithfulness** | ¿La respuesta se inventó algo o está 100% en los documentos? |
| **Answer Relevance** | ¿Responde realmente a lo que el usuario preguntó? |
| **Context Precision** | ¿Los fragmentos recuperados eran realmente útiles? |

**Automatización**: Integrar RAGAS para que corra ante cambios de parámetros (prompt, tamaño de chunk) y detecte regresiones.

#### Días 13-14: Demo UI

**Interfaz Streamlit**:
- Chat conversacional (familiar tipo ChatGPT)
- Mostrar fuentes citadas con links a documentos
- Indicar pilar estratégico aplicado
- Alertas visuales para temas sensibles
- Export a PDF/Word

### Entregables Fase 1

1. **Prototipo funcional** demostrable a directivos
2. **Base de conocimiento** con 94 documentos indexados en Markdown
3. **Reporte de evaluación** con métricas RAGAS (Faithfulness, Answer Relevance, Context Precision)
4. **Documentación técnica** del pipeline implementado

---

## FASE 2: Implementación Profesional (2-3 Meses)

### Objetivo

Sistema robusto, evaluado y listo para uso en producción con las dos capas completamente funcionales.

### Mes 1: Consolidación y Mejoras

| Semana | Actividad |
|--------|-----------|
| 1-2 | Refinamiento del parsing basado en feedback |
| 2-3 | Optimización de chunking y re-ranking |
| 3-4 | Integración de lineamientos comunicacionales formales |

**Lineamientos Comunicacionales**:
- Levantamiento formal con área de comunicaciones FICEM
- Documento estructurado: tono, mensajes clave, públicos, temas sensibles
- Validación por directivos antes de implementar

**Formato del documento de lineamientos**:
```
LINEAMIENTOS COMUNICACIONALES FICEM
===================================

1. TONO INSTITUCIONAL
   - Características: [lista]
   - Evitar: [lista]

2. MENSAJES CLAVE
   - Pilar 1: [descripción]
   - Pilar 2: [descripción]
   - Pilar 3: [descripción]

3. PÚBLICOS Y ADAPTACIÓN
   - Gobierno: [cómo adaptar]
   - Industria: [cómo adaptar]
   - Medios: [cómo adaptar]
   - Sociedad civil: [cómo adaptar]

4. TEMAS SENSIBLES (requieren validación humana)
   - [tema 1]: por qué es sensible
   - [tema 2]: por qué es sensible

5. EJEMPLOS DE REFERENCIA
   - Buen ejemplo: [link/cita]
   - Contraejemplo: [qué evitar]
```

### Mes 2: Escalamiento y Robustez

| Semana | Actividad |
|--------|-----------|
| 1-2 | GraphRAG para relaciones temporales entre posiciones |
| 2-3 | Multi-model LLM (Claude primary + GPT fallback) |
| 3-4 | Role-based access control (gobernanza de datos) |

**GraphRAG**:
- Extracción de entidades y relaciones de documentos
- Grafo de conocimiento para navegación semántica (Neo4j o FalkorDB)
- Permite preguntas como "¿Cómo evolucionó nuestra posición sobre X?"
- Entiende relaciones: si preguntas "¿Cómo afecta el cambio de política Y a los clientes de Europa?", navega por la relación legal entre esos nodos

**Gobernanza**:
- Metadatos de permisos en cada documento
- Filtrado por rol de usuario antes de generar respuesta
- Niveles: público, interno, confidencial

### Mes 3: Producción y Monitoreo

| Semana | Actividad |
|--------|-----------|
| 1-2 | Pipeline de actualización de documentos |
| 2-3 | Dashboard de monitoreo y métricas |
| 3-4 | Capacitación usuarios + go-live |

**Pipeline de ingesta**:
- Proceso definido para nuevos documentos
- Validación antes de indexar
- Versionamiento de base de conocimiento

**Preguntas críticas a definir**:
1. ¿Quién sube documentos nuevos?
2. ¿Qué formato estándar usarán? (PDF, Word, Excel)
3. ¿Cómo se etiquetan? (metadatos: tema, fecha, confidencialidad)
4. ¿Cada cuánto se actualizan?
5. ¿Quién valida que la información es correcta antes de ingestar?

### Stack Tecnológico Fase 2

| Componente | Fase 1 | Fase 2 (Mejora) |
|------------|--------|-----------------|
| Vector DB | Qdrant local | Qdrant Cloud (escalable) |
| Grafos | - | Neo4j / FalkorDB (GraphRAG) |
| LLM | Claude 3.5 | Claude + GPT fallback |
| Monitoreo | Manual | Dashboard automatizado |
| Auth | Básica | SSO + RBAC |
| Evaluación | RAGAS manual | RAGAS en CI/CD |

### Entregables Fase 2

1. **Sistema en producción** con SLA definido
2. **Lineamientos comunicacionales** formalizados e implementados
3. **GraphRAG** para consultas de evolución temporal
4. **Gobernanza de datos** con control de acceso por roles
5. **Pipeline de actualización** documentado
6. **Dashboard de métricas** operacionales
7. **Manual de usuario** y capacitación completada

---

## Riesgos y Mitigaciones

### Alto Impacto

| Riesgo | Mitigación |
|--------|------------|
| **Alucinaciones del LLM** | Citas obligatorias + validación humana para uso público + Faithfulness score |
| **Datos desactualizados** | Timestamp visible + alerta de antigüedad + source freshness score |
| **Desalineación comunicacional** | Lineamientos formalizados + feedback loop + revisión periódica |
| **Acceso no autorizado** | RBAC + logs de auditoría |
| **Extracción deficiente (PDFs)** | Invertir 60% del tiempo en parsing + validación con LLM auditor |

### Medio Impacto

| Riesgo | Mitigación |
|--------|------------|
| **Dependencia de LLM externo** | Multi-model con fallback |
| **Costo operativo** | Cache de respuestas + tier controlado |
| **Deriva de contexto** | Priorizar fechas + señalar cambios de postura explícitamente |
| **Cultural capture** (sesgo hacia organizaciones dominantes como GCCA) | Ponderación explícita de fuentes FICEM vs externas + audit trail |
| **Information overload** | Outputs en capas (resumen ejecutivo → detalles bajo demanda) |

---

## Diferenciadores de FICEM Watch

### Vs. Chatbots Genéricos (ChatGPT, etc.)

| Aspecto | Chatbot Genérico | FICEM Watch |
|---------|------------------|-------------|
| Conocimiento | General, puede inventar | Específico FICEM, con citas |
| Tono | Genérico | Institucional FICEM |
| Fuentes | Desconocidas | Documentos verificables |
| Sensibilidad | No detecta | Alerta temas críticos |

### Vs. RAG Básicos

| Aspecto | RAG Básico | FICEM Watch |
|---------|------------|-------------|
| Parsing | PyPDF (pierde tablas) | Docling (preserva estructura en Markdown) |
| Chunking | Por caracteres | Semántico por tema |
| Búsqueda | Solo vectorial | Híbrida + Re-ranking |
| Estrategia | Ninguna | Capa 2 comunicacional |
| Evaluación | Anecdótica | RAGAS automatizado |
| Precisión | ~60% | ~90% (con re-ranking) |

### Vs. Mercado Actual

| Característica | Mercado | FICEM Watch |
|----------------|---------|-------------|
| Enfoque | Corporaciones individuales | Asociaciones industriales |
| Región | USA/Europa | Latinoamérica |
| Idioma | Inglés | Español (ES/EN/PT) |
| Sector | Genérico | Cemento/Concreto |

---

## Recursos Disponibles

### Documentos (94 archivos)

| Categoría | Cantidad |
|-----------|----------|
| Coprocesamiento | 12 |
| Emisiones CO2/GEI | 15 |
| Institucional FICEM | 8 |
| Reportes Sostenibilidad | 30 |
| Buenas Prácticas | 41 |
| Congresos | 5 |
| Referencias externas | 14+ |

**Ubicación**: Indexados y disponibles para procesamiento

### Infraestructura

- Ambiente de desarrollo configurado
- APIs de LLM disponibles (Claude, OpenAI)
- Acceso a Cohere para Re-ranking

---

## Próximos Pasos Inmediatos

### Para iniciar Fase 1

1. **Aprobación** de este plan de implementación
2. **Acceso** a documentos FICEM para parsing
3. **Definición** de lineamientos comunicacionales preliminares
4. **Identificación** de 2-3 directivos para pruebas piloto

### Para preparar Fase 2

1. **Sesiones** con área de comunicaciones para levantamiento de lineamientos
2. **Definición** de roles y permisos de acceso
3. **Pipeline** de actualización de documentos

---

## Anexo: Referencias Técnicas

### Papers Fundamentales

- Barnett et al. (2024/2025): "Seven Failure Points When Engineering a Retrieval Augmented Generation System"
- Liu et al.: "Lost in the Middle" - comportamiento de LLMs con contexto largo
- "REPLUG: Retrieval-Augmented Black-Box Language Models"

### Herramientas Seleccionadas

| Herramienta | Uso | Documentación |
|-------------|-----|---------------|
| Docling (IBM) | Parsing PDF→Markdown | github.com/DS4SD/docling |
| Unstructured.io | Parsing alternativo con visión | unstructured.io |
| Marker | Parsing rápido | github.com/VikParuchuri/marker |
| Qdrant | Vector DB híbrida | qdrant.tech |
| Cohere Rerank v3 | Re-ranking multilingüe | cohere.com/rerank |
| Jina Reranker v2 | Re-ranking para chunks largos | jina.ai |
| BGE-M3 | Re-ranking open-source | huggingface.co/BAAI |
| LangChain | Orquestación | langchain.com |
| LlamaIndex | Orquestación alternativa | llamaindex.ai |
| RAGAS | Evaluación RAG | ragas.io |
| DeepEval | Evaluación alternativa | deepeval.com |
| Streamlit | UI rápida | streamlit.io |
| Neo4j | GraphRAG (Fase 2) | neo4j.com |
| FalkorDB | GraphRAG alternativo | falkordb.com |

### Frameworks Evaluados

| Framework | Recomendación |
|-----------|---------------|
| LangChain | Estándar industria, usar para prototipo |
| LlamaIndex | Excelente para manejo de datos |
| Haystack 2.x | Muy robusto para pipelines empresariales |

---

**Documento preparado por**: Equipo de Desarrollo
**Fecha**: Enero 2026
**Versión**: 1.1
