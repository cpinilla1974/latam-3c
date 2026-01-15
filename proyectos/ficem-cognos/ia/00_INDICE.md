# Documentación Piloto IA - LATAM-3C

Documentación completa del sistema de Inteligencia Artificial para análisis de benchmarking y predicción de huella de carbono.

**Origen:** Migrado desde ficem_bd
**Fecha de migración:** 2025-12-01

---

## 📚 Índice de Documentos

### 1. [README_ai_modules.md](README_ai_modules.md)
**Descripción general del sistema de módulos de IA**

Contenido:
- Estructura de carpetas (`rag/`, `ml/`, `report_generator/`)
- Casos de uso principales
- Configuración de entorno (.env)
- Instalación de Ollama
- Datos utilizados
- Métricas de desempeño
- Workflow de desarrollo

**Usa este documento para:** Entender la arquitectura general del sistema de IA

---

### 2. [PILOTO_IA_CASOS_USO.md](PILOTO_IA_CASOS_USO.md)
**Especificación detallada de casos de uso del piloto**

Contenido:
- **Caso de Uso 1:** Benchmarking Comparativo
- **Caso de Uso 2:** Análisis de Portafolio
- **Caso de Uso 3:** Predicción de Huella CO₂
- **Caso de Uso 4:** Detección de Anomalías
- **Caso de Uso 5:** Roadmap de Descarbonización
- **Caso de Uso 6:** Comparación Temporal

Cada caso incluye:
- Descripción del problema
- Usuario tipo
- Inputs esperados (queries de ejemplo)
- Outputs esperados (texto, visualizaciones, tablas)
- Datos necesarios (tablas SQL, modelos ML)
- Criterios de éxito

**Usa este documento para:** Entender qué debe hacer el sistema y cómo validarlo

---

### 3. [OPTIMIZACION_RAG.md](OPTIMIZACION_RAG.md)
**Guía de optimización del sistema RAG**

Contenido:
- Análisis de rendimiento actual (107s por consulta)
- Diagnóstico: LLM `qwen2.5:7b` es el cuello de botella
- **6 Soluciones de optimización:**
  1. Cambiar a modelo más rápido (reducción 70-80%)
  2. Limitar longitud de respuestas (reducción 20-30%)
  3. Reducir documentos recuperados (reducción 5-10%)
  4. Implementar streaming (mejora UX)
  5. Cachear respuestas comunes (100% en hits)
  6. Optimizar configuración Ollama (reducción 10-15%)
- Recomendación final por fases
- Tabla comparativa de configuraciones

**Usa este documento para:** Acelerar el sistema RAG cuando esté lento

---

### 4. [PILOTO_IA_PROGRESO.json](PILOTO_IA_PROGRESO.json)
**Estado del proyecto y roadmap técnico**

Contenido estructurado en JSON:
- Stack tecnológico
- **5 Fases del proyecto:**
  - FASE 1: Preparación de Datos
  - FASE 2: Módulo Predictor ML
  - FASE 3: Módulo RAG
  - FASE 4: Interfaz de Usuario
  - FASE 5: Testing y Refinamiento
- Tareas y subtareas detalladas
- Métricas de éxito (objetivos vs actuales)
- Decisiones pendientes
- Riesgos identificados
- Log de sesiones

**Usa este documento para:** Tracking del progreso y planificación de tareas

---

### 5. [requirements_ia_piloto.txt](requirements_ia_piloto.txt)
**Dependencias Python para el piloto IA**

Categorías:
- **RAG y LLM:** langchain, chromadb, sentence-transformers
- **Machine Learning:** scikit-learn, xgboost, prophet
- **Análisis de datos:** pandas, numpy, scipy
- **Visualización:** matplotlib, seaborn, plotly
- **Reportes:** reportlab, python-docx
- **Utilidades:** pydantic, python-dotenv

**Usa este documento para:** Instalar dependencias del módulo IA

---

## 🔄 Estado del Piloto IA

Según [PILOTO_IA_PROGRESO.json](PILOTO_IA_PROGRESO.json):

- ✅ **FASE 1:** Preparación de Datos - **Completada**
- ✅ **FASE 2:** Módulo Predictor ML - **Completada**
  - Random Forest: R² = 0.9999, RMSE = 0.43 (mejor modelo)
  - XGBoost: R² = 0.9999, RMSE = 0.61
  - Linear Regression: R² = 0.9978, RMSE = 3.80
- ⏸️ **FASE 3:** Módulo RAG - **Pendiente**
- ⏸️ **FASE 4:** Interfaz de Usuario - **Pendiente**
- ⏸️ **FASE 5:** Testing y Refinamiento - **Pendiente**

---

## 🎯 Priorización de Casos de Uso (MVP)

Según [PILOTO_IA_CASOS_USO.md](PILOTO_IA_CASOS_USO.md):

**Fase 1 (MVP):**
1. Benchmarking Comparativo ⭐⭐⭐⭐⭐
2. Análisis de Portafolio ⭐⭐⭐⭐⭐
3. Predicción de Huella CO₂ ⭐⭐⭐⭐

**Fase 2 (Extensión):**
4. Detección de Anomalías ⭐⭐⭐
5. Comparación Temporal ⭐⭐⭐

**Fase 3 (Avanzado):**
6. Roadmap de Descarbonización ⭐⭐⭐⭐

---

## 📖 Guía Rápida de Uso

### Para desarrolladores:

1. **Entender la arquitectura:** Lee [README_ai_modules.md](README_ai_modules.md)
2. **Ver qué debe hacer:** Consulta [PILOTO_IA_CASOS_USO.md](PILOTO_IA_CASOS_USO.md)
3. **Trackear progreso:** Revisa [PILOTO_IA_PROGRESO.json](PILOTO_IA_PROGRESO.json)
4. **Instalar dependencias:**
   ```bash
   pip install -r requirements_ia_piloto.txt
   ```
5. **Si RAG es lento:** Sigue [OPTIMIZACION_RAG.md](OPTIMIZACION_RAG.md)

### Para analistas/usuarios:

1. **Ver qué puede hacer el sistema:** Lee [PILOTO_IA_CASOS_USO.md](PILOTO_IA_CASOS_USO.md)
2. **Ejemplos de preguntas:** Cada caso de uso incluye queries de ejemplo

---

## 🔗 Referencias Adicionales

- **Instalación de Ollama:** https://ollama.com/
- **Modelos recomendados:**
  - `qwen2.5:1.5b` (rápido)
  - `qwen2.5:3b` (balance)
  - `llama3.1:8b` (calidad)

---

**Última actualización:** 2025-12-01
**Fuente original:** /home/cpinilla/projects/ficem_bd
