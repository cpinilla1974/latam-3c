# Analisis de Dificultad RAG - Informe Marcos Regulatorios 2025 FICEM

## Documento Analizado

| Campo | Valor |
|-------|-------|
| Nombre | Informe Marcos Regulatorios 2025 FICEM V edicion.pdf |
| Tamano | 32 MB |
| Paginas | 135 |
| Formato origen | PDF generado desde macOS Quartz (presentacion convertida a PDF) |
| Dimensiones pagina | 960 x 540 pts (formato presentacion/slides) |

## Diagnostico de Dificultad

### Nivel de Dificultad: **ALTO** (7/10)

### Problemas Identificados

#### 1. Formato de Presentacion (no documento)
- **Problema**: Es un PDF generado desde slides (960x540 pts = formato 16:9)
- **Impacto**: El texto NO fluye de forma lineal como un documento
- **Consecuencia RAG**: pdftotext extrae texto en orden de renderizado, no de lectura

#### 2. Tablas Complejas con Datos Multicolumna
```
                     1             2             3             4       5          6    ...
                             Ley Cambio     Compras      Normas de Cemento y
                   NDC       Climático     Públicas      Concreto Adiciones  ...

  Argentina          Si            Si                         Si       Si       ...
    Brasil           Si            Si                         Si       Si       ...
```
- **Problema**: Tablas con 13+ columnas que comparan paises
- **Impacto**: Si se fragmenta (chunking), se pierde la relacion fila-columna
- **Consecuencia RAG**: Respuestas incorrectas tipo "Argentina tiene Si" sin contexto

#### 3. Elementos Graficos con Texto
- **Problema**: Mapas, diagramas de flujo, graficos de barras con texto embebido
- **Impacto**: OCR basico no captura la relacion espacial
- **Ejemplo**: Figura 5 es un mapa de Latinoamerica con datos de cada pais superpuestos

#### 4. Multiples Bloques de Texto por Pagina
- **Problema**: Layout de presentacion con cuadros de texto independientes
- **Impacto**: pdftotext con `-layout` mezcla columnas de texto
- **Ejemplo**: Pagina de NDCs tiene texto izquierda + mapa derecha + leyenda abajo

#### 5. Mezcla de Idiomas y Acronimos Tecnicos
- **Problema**: NDCs, BURs, MRVs, REP, BAU, CCUS, GEI, etc.
- **Impacto**: Embeddings pueden no capturar bien acronimos en espanol tecnico
- **Mitigacion**: Glosario + expansion en preprocessing

## Comparacion de Extractores

### pdftotext (basico)
```bash
pdftotext archivo.pdf texto.txt
```
- **Resultado**: 6,911 lineas extraidas
- **Calidad**: Texto legible pero tablas destruidas
- **Usabilidad RAG**: 40% - pierde estructura

### pdftotext -layout
```bash
pdftotext -layout archivo.pdf texto.txt
```
- **Resultado**: Intenta mantener posiciones
- **Calidad**: Tablas parcialmente visibles pero columnas mezcladas
- **Usabilidad RAG**: 50% - mejor pero insuficiente

### Docling (recomendado en stack)
- **Esperado**: Detecta tablas como objetos estructurados
- **Output**: Markdown con tablas reales
- **Usabilidad RAG**: 85%+ esperado

## Recomendaciones Especificas

### 1. Preprocesamiento Obligatorio
```
PDF --> Docling --> Markdown --> Chunks semanticos --> Embeddings
```
NO usar extraccion directa con pdftotext.

### 2. Tratamiento de Tablas
- Extraer tablas como objetos JSON separados
- Crear chunks especificos por tabla completa
- Indexar con metadatos: "tabla_paises_normativas"

### 3. Chunks de Tamano Variable
| Tipo Contenido | Tamano Chunk |
|----------------|--------------|
| Texto narrativo | 512-1024 tokens |
| Tablas | Tabla completa (sin cortar) |
| Listas | Lista completa |
| Graficos | Caption + descripcion generada |

### 4. Metadatos Criticos por Chunk
```json
{
  "source": "Informe_Marcos_Regulatorios_2025",
  "page": 12,
  "section": "NDCs",
  "content_type": "table|text|figure",
  "countries_mentioned": ["Argentina", "Chile", ...],
  "topics": ["cambio_climatico", "coprocesamiento"]
}
```

### 5. Queries de Prueba Sugeridas
Para evaluacion RAGAS, crear preguntas que requieran:
1. **Dato puntual**: "Cual es la meta NDC 2030 de Colombia?"
2. **Comparacion**: "Que paises tienen ley de cambio climatico?"
3. **Relacion**: "Que relacion hay entre coprocesamiento y taxonomia verde?"
4. **Sintesis**: "Resume las diferencias en normativas de residuos entre Chile y Peru"

## Estimacion de Esfuerzo

| Actividad | Tiempo Estimado |
|-----------|-----------------|
| Parsing con Docling | 2-4 horas (incluye debugging) |
| Revision manual de tablas | 4-6 horas |
| Creacion de metadatos | 2-3 horas |
| **Total para 1 documento** | **8-13 horas** |

### Proyeccion 94 documentos
- Si todos son similares: 94 x 10h = 940 horas
- Con automatizacion: 94 x 2h = 188 horas
- **Conclusion**: Automatizacion con Docling es CRITICA

## Veredicto Final

Este documento es un **caso de prueba excelente** porque representa los peores escenarios:
1. PDF de presentacion (no documento)
2. Tablas complejas multicolumna
3. Elementos graficos con texto
4. Acronimos tecnicos en espanol

Si el pipeline de Docling + Qdrant + Cohere maneja bien este documento, manejara el resto del corpus FICEM.

---
*Analisis generado: 2026-01-22*
*Documento fuente: Dropbox /Espacio familiar/Archivos EGP/Patricio Flores Cierre/*
