# Respuesta para Continuar Conversación con Gemini

## Contexto que Gemini necesita entender

Gracias por el análisis profundo. Antes de profundizar en la implementación técnica, necesito darte contexto completo sobre lo que estamos construyendo porque **FICEM Watch NO es solo un RAG**.

---

## FICEM Watch: Asistente Ejecutivo de Posicionamiento

### Qué es realmente

Es un sistema de **posicionamiento estratégico** para la Federación Interamericana del Cemento (FICEM). Los usuarios son directivos que necesitan:

1. **Respuestas alineadas con la estrategia comunicacional de FICEM** (no solo correctas, sino con el tono y enfoque institucional)
2. **Historial de posicionamiento** sobre temas específicos (qué hemos dicho antes sobre X)
3. **Datos duros con narrativa** para responder interpelaciones (de gobiernos, medios, sociedad civil)
4. **Alertas sobre temas sensibles** que requieren validación humana antes de responder

### Arquitectura de Dos Capas

| Capa | Función | Fuente |
|------|---------|--------|
| **Capa 1: Conocimiento** | Qué sabe FICEM (datos, posiciones históricas, documentos) | ~94 documentos, RAG |
| **Capa 2: Estrategia** | Cómo comunica FICEM (tono, mensajes clave, públicos, temas sensibles) | Lineamientos comunicacionales |

El RAG solo resuelve la Capa 1. La Capa 2 es igualmente crítica: una respuesta factualmente correcta pero con tono defensivo o que contradice los pilares comunicacionales es un **fracaso del sistema**.

---

## Recursos Disponibles

### Documentos (Capa 1)
- **94 documentos** en 10 categorías (coprocesamiento, emisiones CO2/GEI, institucional, etc.)
- Formatos: PDF (mayoritariamente), DOCX
- Incluyen: Reportes de sostenibilidad, buenas prácticas, actas de congresos, documentos internos
- Índice CSV con metadatos (categoría, subcategoría, descripción)
- Ruta: `/mnt/c/Users/cpini/OneDrive/RAG_DocumentosFICEM/`

### Lineamientos Comunicacionales (Capa 2)
- **Aún no existen formalizados** - hay una metodología definida para levantarlos con FICEM
- Para el prototipo: placeholder con lineamientos básicos inferidos de documentos existentes
- Para producción: documento formal validado por directivos FICEM

---

## Restricciones de Tiempo y Fases

### Fase 1: Prototipo Diferenciador (2 semanas)
**Objetivo**: Mostrar algo que funcione y que sea **claramente mejor** que los prototipos RAG básicos que fallan (como los que ya hemos intentado antes y no sirven).

**Expectativa**: No perfecto, pero que demuestre el potencial del enfoque avanzado.

### Fase 2: Implementación Profesional (2+ meses)
**Objetivo**: Sistema robusto, evaluado, con las dos capas funcionando completamente.

**Recursos**: Tiempo suficiente para hacer las cosas bien. Este es un proyecto corporativo serio.

---

## Preguntas Específicas

### Sobre Parsing (tu recomendación del 60% del tiempo)

1. **Docling vs Unstructured.io**: ¿Cuál recomiendas para PDFs con tablas técnicas (datos de emisiones, porcentajes, comparativas regionales)?

2. **Markdown como formato intermedio**: ¿Cómo manejas las tablas complejas que tienen celdas fusionadas o notas al pie?

3. **Verificación de calidad**: ¿Cómo valido que la extracción de un PDF fue correcta antes de indexarlo? ¿Hay métricas o checklists?

### Sobre Chunking

4. **Semantic Chunking**: Mencionas que se detectan cambios de tema. ¿Qué modelo/librería específica recomiendas para texto en español técnico?

5. **Small-to-Big Retrieval**: ¿Cómo implemento esto técnicamente? ¿Guardo dos versiones (chunk pequeño + contexto expandido) o se hace on-the-fly?

### Sobre Hybrid Search + Re-ranking

6. **Para 2 semanas**: ¿Cuál es el stack mínimo que debo implementar para tener Hybrid Search (vectores + BM25) con Re-ranking? ¿LangChain lo soporta out-of-the-box?

7. **Re-ranker en español**: Entre Cohere Rerank v3 y BGE-M3, ¿cuál tiene mejor rendimiento en español técnico? ¿Hay benchmarks?

### Sobre Evaluación (RAGAS)

8. **Dataset sintético**: ¿Cuántas preguntas/respuestas necesito generar como mínimo para que la evaluación sea significativa?

9. **Automatización**: ¿Puedo integrar RAGAS en un CI/CD para detectar regresiones cuando actualizo documentos o cambio parámetros?

### Sobre la Capa 2 (Estrategia Comunicacional)

10. **System Prompt estructurado**: ¿Cómo diseño el prompt para que respete los lineamientos sin ser rígido? ¿Hay patrones recomendados para "constitutional AI" aplicado a tono institucional?

11. **Detección de temas sensibles**: ¿Recomiendas clasificación previa de la pregunta o análisis post-generación para alertar sobre temas que requieren validación humana?

---

## Resumen de Mi Situación

- **Tengo**: 94 documentos, 2 semanas para prototipo, 2+ meses para producción
- **Necesito**: Sistema que demuestre valor real en Fase 1 y sea escalable para Fase 2
- **Diferenciador clave**: No es solo RAG - es posicionamiento estratégico con dos capas
- **Ya fallé antes**: Con prototipos RAG básicos que no sirven - necesito hacer esto bien

¿Puedes darme un **plan de implementación concreto para las 2 semanas** que priorice lo que más impacto tiene y deje preparado el terreno para la Fase 2?
