# Análisis de Integración: ficem_bd → latam-3c v1

**Fecha**: 2025-01-12
**Objetivo**: Evaluar qué componentes de `ficem_bd` pueden integrarse a `latam-3c/v1`

---

## 📋 Resumen Ejecutivo

Después de revisar el código de `ficem_bd`, identifiqué **3 secciones principales** con funcionalidades valiosas:

1. **Explorar Data**: Sistema de consulta multidimensional con filtros avanzados
2. **Bandas GCCA**: Visualizaciones interactivas con clasificación automática
3. **Piloto IA**: Predictor ML + Generador de informes con LLM

### Recomendación General
**TRAER SELECTIVAMENTE** solo los componentes que agregan valor sin duplicar funcionalidad existente en v1.

---

## 🔍 Análisis por Sección

### 1. **Explorar Data** (`explora_data.py`)

#### Funcionalidades Clave:
- ✅ Sistema de filtrado avanzado con **diálogos modales**
- ✅ Filtros por: Fuente, Indicadores (jerarquía), Años, Entidades (región/subregión/país)
- ✅ Tabla pivotable dinámica
- ✅ Descarga Excel con nombre sugerido automático
- ✅ Session state para persistir filtros

#### Ventajas:
- **UX superior**: Diálogos modales vs multiselect largo
- **Filtros jerárquicos**: Supergrupo → Grupo → Subgrupo → Indicador
- **Reutilizable**: Funciones `select_entidades_dialog()` y `select_indicadores_dialog()`

#### Decisión: ✅ **TRAER ADAPTADO**
**Qué traer**:
- Lógica de diálogos modales para filtros
- Sistema de session_state para filtros persistentes
- Función `descargar_excel()` con nombre auto-generado

**Dónde integrarlo en v1**:
- Crear nueva página: `pages/analisis/05_explorar_data.py`
- Reutilizar en otras páginas que necesiten filtros complejos

---

### 2. **Bandas GCCA** (`bandas_cemento.py` y `bandas_concretos.py`)

#### Funcionalidades Clave Cemento:
- ✅ Slider para ajustar **relación clínker/cemento** (fórmula GCCA dinámica)
- ✅ Clasificación automática por GWP en bandas AA-G
- ✅ 4 visualizaciones diferentes:
  - Barras horizontales con límites de bandas
  - Scatter por tipo de cemento
  - Heatmap por origen y tipo
  - Donut de distribución por clase
- ✅ Filtrado interactivo con estadísticas en tiempo real

#### Funcionalidades Clave Concreto:
- ✅ **Modo Fantasma**: Anonimizar nombres de compañías
- ✅ 4 pestañas de análisis:
  - **Tab 1**: Gráfico líneas/burbujas/barras apiladas
  - **Tab 2**: Análisis integrado con manómetros (gauges) + 3 modos de filtrado:
    - Todas las resistencias
    - Solo resistencias exactas (20,25,30,35,40,45,50)
    - Rangos ±2 MPa
  - **Tab 3**: Bandas GCCA + datos superpuestos
  - **Tab 4**: Análisis comparativo por compañía (torta + barras agrupadas)
- ✅ Clasificación de remitos en bandas con bandas horizontales
- ✅ Descarga Excel multi-hoja con índice comparativo

#### Ventajas:
- **Visualizaciones profesionales**: Listas para reportes
- **Flexibilidad de análisis**: Múltiples formas de ver los mismos datos
- **Modo fantasma**: Esencial para demostraciones con datos sensibles
- **Export completo**: Excel con 4 hojas + comparativa

#### Decisión: ✅ **TRAER COMPLETO**
**Qué traer**:
- **TODO** el código de `bandas_cemento.py` → Adaptado para v1
- **TODO** el código de `bandas_concretos.py` → Adaptado para v1

**Dónde integrarlo en v1**:
- `pages/analisis/06_bandas_cemento.py` (NUEVO)
- `pages/analisis/07_bandas_concreto.py` (NUEVO)
- Reemplazar/mejorar páginas existentes si hay solapamiento con `03_analisis_bandas.py`

#### Dependencias a resolver:
```python
# ficem_bd usa:
from database.connection import get_connection  # ✅ Similar existe en v1
bandas_gcca.json  # ✅ Ya existe en storage
```

---

### 3. **Piloto IA** (páginas en `/ai/`)

#### Componentes principales:

##### 3.1 **Dashboard IA** (`piloto_ia_dashboard.py`)
- ⚠️ Dashboard informativo básico (fases, métricas)
- **Decisión**: ❌ **NO TRAER** - Demasiado específico de ficem_bd

##### 3.2 **Predictor ML** (`predictor_huella.py`)
- ✅ Interfaz completa para predicción con ML
- ✅ Modelo Gradient Boosting entrenado (R² = 0.9999)
- ✅ Visualización con intervalos de confianza
- ✅ Comparación automática con bandas GCCA
- ✅ Sidebar con parámetros configurables

**Dependencias**:
```python
from ai_modules.ml.predictor import HuellaPredictor  # Módulo externo
```

**Decisión**: ⚙️ **EVALUAR DESPUÉS**
- **Bloqueante**: Requiere módulo `ai_modules` completo
- **Valor**: Alto - predicciones en tiempo real
- **Complejidad**: Media-alta
- **Recomendación**: Traer en una segunda iteración cuando tengamos datos de múltiples plantas

##### 3.3 **Generador de Informes** (`generador_informes.py`)
- ✅ Interfaz para generar PDFs y Excel con análisis de IA
- ✅ Soporte para Ollama (local) y Claude (API)
- ✅ Selector de compañía/año/benchmark
- ✅ Vista previa antes de generar
- ✅ Descarga directa de archivos

**Dependencias**:
```python
from ai_modules.report_generator.pdf_generator import BenchmarkingReportPDF
from ai_modules.report_generator.excel_generator import BenchmarkingReportExcel
from ai_modules.rag.sql_tool import SQLTool
```

**Decisión**: ⚙️ **EVALUAR DESPUÉS**
- **Bloqueante**: Requiere módulos completos de IA
- **Valor**: Alto - reportes automáticos con análisis IA
- **Complejidad**: Alta
- **Recomendación**: Implementar cuando necesitemos reportes automatizados para empresas

---

## 📊 Plan de Integración Propuesto

### **FASE 1: Integración Inmediata** (Esta sesión)

#### 1.1 Traer Sistema de Filtros Avanzados
```bash
# Archivos a crear/modificar:
v1/modules/filters.py                    # NUEVO - Lógica de diálogos
v1/pages/analisis/05_explorar_data.py   # NUEVO - Página completa
```

**Tareas**:
- [ ] Extraer funciones de filtrado de `explora_data.py`
- [ ] Adaptar a la estructura de BD de v1
- [ ] Crear página nueva en sección Análisis
- [ ] Probar con datos de v1

**Tiempo estimado**: 1-2 horas

---

#### 1.2 Traer Visualizaciones de Bandas GCCA
```bash
# Archivos a crear:
v1/pages/analisis/06_bandas_cemento.py     # NUEVO
v1/pages/analisis/07_bandas_concreto.py    # NUEVO
v1/modules/bandas_utils.py                  # NUEVO - Funciones comunes
```

**Tareas**:
- [ ] Copiar `bandas_cemento.py` completo
- [ ] Adaptar imports y conexión a BD
- [ ] Copiar `bandas_concretos.py` completo
- [ ] Adaptar imports y conexión a BD
- [ ] Extraer funciones comunes a `bandas_utils.py`:
  - `calcular_rangos_gcca()`
  - `clasificar_cemento()`
  - `obtener_color_clase()`
  - `generar_excel_analisis()`
- [ ] Probar con datos de v1
- [ ] Integrar al menú de navegación en `app.py`

**Tiempo estimado**: 2-3 horas

---

### **FASE 2: Integración Futura** (Cuando se necesite)

#### 2.1 Módulo Predictor ML
**Cuándo**: Cuando tengamos datos históricos de múltiples plantas/años

**Requisitos previos**:
- Datos suficientes para entrenar modelo (>10k registros)
- Definir features exactos según estructura de v1
- Instalar scikit-learn, xgboost

#### 2.2 Generador de Informes IA
**Cuándo**: Cuando necesitemos reportes automáticos para empresas

**Requisitos previos**:
- Decisión: ¿Ollama local o Claude API?
- Templates de reportes definidos
- Módulos RAG implementados

---

## 🔧 Adaptaciones Necesarias

### Cambios en Conexión a BD
```python
# ficem_bd usa:
from database.connection import get_connection
ruta_db = st.session_state.get('ruta_db')
conn = get_connection(ruta_db)

# v1 usa:
from sqlalchemy.orm import Session
from database import get_db
# El engine está en st.session_state.db_engine
```

**Solución**: Crear función adaptadora en `v1/modules/db_helpers.py`

---

### Cambios en Paths de Datos
```python
# ficem_bd usa:
json_path = os.path.join(os.getenv("COMUN_FILES_PATH"), "bandas_gcca.json")

# v1 debería usar:
json_path = "data/bandas_gcca.json"  # Ruta relativa
```

**Solución**: Copiar `bandas_gcca.json` a `v1/data/`

---

### Cambios en Nombres de Tablas
```python
# ficem_bd usa:
pd.read_sql_query("SELECT * FROM cementos", conn)
pd.read_sql_query("SELECT * FROM huella_concretos", conn)
pd.read_sql_query("SELECT * FROM tb_cubo", conn)

# v1 usa nombres diferentes - VERIFICAR schema actual
```

**Solución**: Revisar schema de v1 y mapear nombres correctos

---

## 📦 Archivos a Copiar/Adaptar

### Copiar directamente:
```
data/bandas_gcca.json  →  v1/data/bandas_gcca.json
```

### Adaptar código:
```
ficem_bd/pages/explora_data/explora_data.py
  → v1/modules/filters.py (funciones)
  → v1/pages/analisis/05_explorar_data.py (página)

ficem_bd/pages/explora_data/bandas_cemento.py
  → v1/pages/analisis/06_bandas_cemento.py
  → v1/modules/bandas_utils.py (funciones comunes)

ficem_bd/pages/explora_data/bandas_concretos.py
  → v1/pages/analisis/07_bandas_concreto.py
  → v1/modules/bandas_utils.py (funciones comunes)
```

---

## ✅ Checklist de Integración

### Pre-requisitos
- [ ] Backup del código actual de v1
- [ ] Verificar estructura de BD de v1
- [ ] Copiar `bandas_gcca.json` a `v1/data/`
- [ ] Crear rama git para integración

### Fase 1 - Sistema de Filtros
- [ ] Crear `v1/modules/filters.py`
- [ ] Implementar `select_entidades_dialog()`
- [ ] Implementar `select_indicadores_dialog()`
- [ ] Crear página `05_explorar_data.py`
- [ ] Probar filtros con datos reales
- [ ] Actualizar navegación en `app.py`

### Fase 1 - Bandas GCCA
- [ ] Crear `v1/modules/bandas_utils.py`
- [ ] Migrar funciones comunes
- [ ] Crear `06_bandas_cemento.py`
- [ ] Adaptar conexiones a BD
- [ ] Probar visualizaciones
- [ ] Crear `07_bandas_concreto.py`
- [ ] Implementar modo fantasma
- [ ] Probar las 4 pestañas
- [ ] Actualizar navegación en `app.py`

---

## 🎯 Resultado Esperado

Después de la **Fase 1**, `latam-3c/v1` tendrá:

1. ✅ **3 páginas nuevas** en sección Análisis:
   - Explorar Data (filtros avanzados)
   - Bandas Cemento (clasificación GCCA)
   - Bandas Concreto (análisis multi-pestaña)

2. ✅ **1 módulo nuevo** de utilidades:
   - `modules/bandas_utils.py`
   - `modules/filters.py`

3. ✅ **Funcionalidades mejoradas**:
   - Filtrado más intuitivo con diálogos
   - Visualizaciones profesionales listas para reportes
   - Modo fantasma para demos
   - Exports multi-hoja con análisis comparativo

---

## 💰 Estimación de Esfuerzo

| Tarea | Complejidad | Tiempo Estimado |
|-------|-------------|-----------------|
| Sistema de Filtros | Media | 1-2 horas |
| Bandas Cemento | Media | 1-1.5 horas |
| Bandas Concreto | Alta | 1.5-2 horas |
| Testing & Ajustes | Media | 1 hora |
| **TOTAL FASE 1** | - | **4.5-6.5 horas** |

---

## 🚀 Próximos Pasos Propuestos

**AHORA** (en esta sesión):
1. Revisar este análisis contigo
2. Confirmar plan de integración
3. Comenzar con Fase 1 si estás de acuerdo

**DESPUÉS** (siguientes sesiones):
- Fase 2: Evaluar integración de módulos IA cuando tengamos más datos

---

**Documentado por**: Claude Code
**Fecha**: 2025-01-12
**Basado en**: Revisión completa de ficem_bd (explora_data, bandas, piloto IA)
