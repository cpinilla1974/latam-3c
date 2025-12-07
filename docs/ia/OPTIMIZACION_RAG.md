# Optimización del Sistema RAG

## 📊 Análisis de Rendimiento Actual

**Tiempo total por consulta: ~107 segundos**

### Desglose:
- ✅ Búsqueda vectorial: 2.09s (1.9%) - Excelente
- ❌ Generación LLM: 105s (98.1%) - **CUELLO DE BOTELLA**

### Diagnóstico:
El modelo `qwen2.5:7b` (7.6B parámetros, 4.7 GB) es demasiado lento para interacción en tiempo real.

---

## 🚀 Soluciones Recomendadas

### 1. **Cambiar a Modelo Más Rápido** (Reducción estimada: 70-80%)

#### Opción A: Modelos pequeños cuantizados
```bash
# Descargar modelo de 1.5B parámetros (mucho más rápido)
ollama pull qwen2.5:1.5b

# O usar versión 3B (balance calidad/velocidad)
ollama pull qwen2.5:3b
```

**Impacto esperado:**
- `qwen2.5:1.5b`: ~15-25s por consulta (70-75% más rápido)
- `qwen2.5:3b`: ~35-50s por consulta (50-60% más rápido)

#### Opción B: Modelos especializados en español
```bash
# Modelo ligero optimizado para español
ollama pull gemma2:2b
```

**Cambio en el código:**
```python
# En pages/ai/chat_benchmarking.py, línea 22
rag = RAGChain(
    llm_model="qwen2.5:1.5b",  # Cambiar aquí
    temperature=0.1,
    top_k=5
)
```

---

### 2. **Limitar Longitud de Respuestas** (Reducción: 20-30%)

Modificar el prompt para generar respuestas más concisas.

**Cambio en el código:**
```python
# En ai_modules/rag/rag_chain.py, línea 66
system_prompt = """Eres un asistente experto en descarbonización de la industria del cemento y concreto.

Usa el siguiente contexto para responder la pregunta de forma CONCISA (máximo 3-4 oraciones).
Si no sabes la respuesta, di que no lo sabes.

Contexto:
{context}"""
```

**Impacto esperado:**
- Respuestas más cortas = menos tokens generados = 20-30% más rápido

---

### 3. **Reducir Número de Documentos Recuperados** (Reducción: 5-10%)

Actualmente recupera 5 documentos (`top_k=5`). Reducir a 3 acelera ligeramente.

**Cambio en el código:**
```python
# En pages/ai/chat_benchmarking.py, línea 22
rag = RAGChain(
    llm_model="qwen2.5:7b",
    temperature=0.1,
    top_k=3  # Reducir de 5 a 3
)
```

**Impacto esperado:**
- Menos contexto = respuesta más rápida
- Puede reducir precisión en preguntas complejas

---

### 4. **Usar Streaming de Respuestas** (Mejora percepción, no velocidad)

Mostrar la respuesta mientras se genera (como ChatGPT).

**Ventaja:**
- El usuario ve progreso inmediato
- Percepción de mayor rapidez
- No reduce tiempo total, pero mejora UX

**Implementación:**
```python
# En pages/ai/chat_benchmarking.py
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    # Streaming del LLM
    for chunk in rag.llm.stream(prompt_with_context):
        full_response += chunk
        message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)
```

---

### 5. **Cachear Respuestas Comunes** (Reducción: 100% en hits)

Guardar respuestas a preguntas frecuentes.

**Implementación:**
```python
# Agregar cache en session_state
if "response_cache" not in st.session_state:
    st.session_state.response_cache = {}

# Antes de consultar RAG
cache_key = hash(prompt)
if cache_key in st.session_state.response_cache:
    result = st.session_state.response_cache[cache_key]
else:
    result = rag.query(prompt)
    st.session_state.response_cache[cache_key] = result
```

**Impacto:**
- Primera vez: mismo tiempo
- Consultas repetidas: instantáneo

---

### 6. **Optimizar Configuración de Ollama** (Reducción: 10-15%)

Ajustar parámetros de inferencia:

```bash
# Aumentar hilos de CPU para Ollama
export OLLAMA_NUM_THREADS=8

# Usar GPU si está disponible (automático en Ollama)
# Verificar: ollama ps
```

**Configuración en código:**
```python
# En ai_modules/rag/rag_chain.py
self.llm = OllamaLLM(
    model=llm_model,
    base_url="http://localhost:11434",
    temperature=temperature,
    num_ctx=2048,  # Reducir contexto (default 4096)
    num_predict=256  # Limitar tokens generados
)
```

---

## 📝 Recomendación Final

### Implementación por Fases:

**FASE 1 - Impacto Inmediato (70-80% mejora):**
1. Descargar `qwen2.5:1.5b`
2. Cambiar modelo en `chat_benchmarking.py`
3. Limitar longitud de respuestas en prompt

**Resultado esperado: 15-25 segundos por consulta**

**FASE 2 - Refinamiento (mejora adicional):**
1. Implementar streaming
2. Reducir `top_k` a 3
3. Agregar caché de respuestas

**Resultado esperado: 10-20 segundos + mejor UX**

**FASE 3 - Optimización Avanzada:**
1. Optimizar configuración Ollama
2. Considerar usar GPU (CUDA/ROCm)
3. Implementar sistema de pre-carga de respuestas comunes

---

## 🎯 Tabla Comparativa

| Configuración | Tiempo/Consulta | Calidad | Implementación |
|---------------|-----------------|---------|----------------|
| **Actual** (qwen2.5:7b) | ~107s | ★★★★★ | ✅ Actual |
| **qwen2.5:3b** + prompts cortos | ~35-40s | ★★★★☆ | ⚡ Fácil |
| **qwen2.5:1.5b** + optimizaciones | ~15-20s | ★★★☆☆ | ⚡ Fácil |
| **1.5b** + streaming + caché | ~15s (percepción <5s) | ★★★☆☆ | 🔧 Media |

---

## 💡 Próximo Paso Sugerido

```bash
# 1. Descargar modelo más rápido
ollama pull qwen2.5:3b

# 2. Modificar una línea de código
# En pages/ai/chat_benchmarking.py, línea 22:
# llm_model="qwen2.5:3b"

# 3. Reiniciar Streamlit
# La app ya estará 60% más rápida
```

**Nota:** Puedes probar diferentes modelos sin cambiar nada más. Solo cambia el parámetro `llm_model`.
