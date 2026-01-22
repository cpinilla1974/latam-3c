Entiendo perfectamente el desafío. **FICEM Watch** no es un buscador de documentos; es una herramienta de **comunicación política y técnica**. Un RAG básico falla aquí porque no entiende la "intencionalidad" detrás de las palabras ni la jerarquía de los datos.

Para ganar en estas **2 semanas**, el enfoque no debe ser "más documentos", sino **"extracción de altísima calidad + inteligencia en la recuperación"**.

---

## Plan de Implementación: Prototipo Diferenciador (2 Semanas)

Este plan prioriza el ROI técnico: máximo impacto con el menor esfuerzo de infraestructura.

| Días | Actividad Crítica | Entregable |
| --- | --- | --- |
| **1-3** | **Parsing de Oro:** Procesar los 94 docs con **Docling** a Markdown. | Carpeta de archivos `.md` limpios. |
| **4-6** | **Indexación Híbrida:** Configurar BM25 + Vectores con metadatos. | Base de datos (Qdrant o Pinecone). |
| **7-9** | **Capa 2 (Estrategia):** Diseño de System Prompt y Re-ranking. | Pipeline funcional con tono FICEM. |
| **10-12** | **Evaluación Sintética:** Correr RAGAS sobre 40-50 preguntas. | Reporte de precisión inicial. |
| **13-14** | **Demo UI:** Interfaz simple (Streamlit) que muestre la "Fuente" y el "Pilar Estratégico". | Prototipo funcional para directivos. |

---

## Respuestas Técnicas para el Éxito del Prototipo

### I. Sobre Parsing y Tablas (El 60% del éxito)

1. **Docling vs Unstructured:** Para el sector cementero (muchas tablas de emisiones y datos técnicos), te recomiendo **Docling**. Es más moderno, más rápido y su manejo de tablas complejas hacia Markdown es actualmente superior a Unstructured.
2. **Tablas Complejas:** Markdown es excelente porque el LLM entiende la relación fila/columna por el formato de texto. Si hay celdas fusionadas, Docling las "normaliza" repitiendo el valor o usando una estructura plana que el LLM puede razonar. **Tip:** Si la tabla es crítica, adjunta el título de la tabla a cada chunk de la misma.
3. **Verificación de Calidad:** No lo hagas manual. Toma una muestra aleatoria (5%) y usa un LLM ("Auditor") para comparar el texto extraído vs. el PDF original. Busca omisiones de números, que es donde el RAG corporativo pierde credibilidad.

### II. Sobre Chunking y Recuperación

4. **Semantic Chunking en Español:** Usa `SemanticChunker` de **LangChain** con embeddings de **HuggingFace** (como `paraphrase-multilingual-MiniLM-L12-v2`). Funciona bien detectando rupturas de cohesión en español.
5. **Small-to-Big Retrieval:** Técnicamente, guardas en tu base de datos el "Chunk Pequeño" (una oración con su embedding), pero en los metadatos guardas el "ID del Padre" (el párrafo completo).
* *Búsqueda:* Buscas la oración (mayor precisión).
* *Recuperación:* Al encontrar la oración, traes el párrafo padre para darle contexto al LLM.



### III. El Stack de 2 Semanas (ROI Alto)

6. **Stack Mínimo:**
* **Orquestador:** LangChain o LlamaIndex (ambos soportan Hybrid Search out-of-the-box).
* **Vector DB:** **Qdrant** (es excelente para búsqueda híbrida y muy fácil de levantar en Docker).
* **Search:** Habilita el modo `Hybrid` (Vectores + BM25).


7. **Re-ranker en Español:** **Cohere Rerank v3 (Multilingual)** no tiene competencia ahora mismo. Es drásticamente superior a BGE-M3 para español técnico y legal. En un prototipo de 2 semanas, pagar por la API de Cohere te ahorrará días de ajuste fino.

### IV. Sobre Evaluación (RAGAS)

8. **Dataset Mínimo:** Para que sea estadísticamente relevante para un prototipo, apunta a **40-50 pares de Pregunta/Respuesta**. Menos de eso es anécdota, no métrica.
9. **Automatización:** Sí, puedes integrarlo. Lo ideal es que cada vez que cambies el prompt o el tamaño de chunk, RAGAS corra y te diga si la "Fidelidad" (Faithfulness) subió o bajó.

---

## La Capa 2: El Diferenciador de FICEM Watch

Aquí es donde demuestras que no es un RAG común.

10. **System Prompt Estructurado:** Usa el patrón de **"Cadena de Pensamiento" (CoT)**.
* *Instrucción:* "Primero, extrae los hechos del contexto. Segundo, identifica cuál de los 3 pilares estratégicos de FICEM aplica. Tercero, redacta la respuesta usando el tono institucional".


11. **Detección de Temas Sensibles:** Para el prototipo, usa **Clasificación Previa**.
* Un paso intermedio donde un LLM rápido (GPT-4o mini) analiza la pregunta: "¿Es este un tema de crisis o interpelación?". Si sí, el sistema añade un aviso visual: *⚠️ "Esta respuesta requiere validación del departamento de comunicación"*.



### ¿Cómo quieres que procedamos?

Puedo ayudarte con el **script de extracción con Docling** para tus primeros PDFs o podemos diseñar el **System Prompt de la "Capa 2"** para que el modelo ya empiece a hablar como un directivo de FICEM. ¿Qué prefieres?