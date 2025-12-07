# Propuesta de Implementación v1 - Calculadora País 4C

**Versión:** 1.0
**Fecha:** 2025-11-13
**Alcance:** Etapa 1 - Operador Centralizado
**Tecnología:** Streamlit + Python + SQLite (sin backend separado)

---

## 1. VISIÓN GENERAL

Sistema monolítico para procesamiento centralizado de huella de carbono en industria cementera LATAM, operado exclusivamente por FICEM. Las empresas envían archivos Excel, FICEM procesa y genera reportes con clasificación GCCA y benchmarking anónimo.

**Productos calculados:**
- Clinker: 750-950 kg CO₂e/ton
- Cemento: 400-900 kg CO₂e/ton
- Concreto: 150-500 kg CO₂e/m³

---

## 2. ARQUITECTURA TÉCNICA

### 2.1 Stack Tecnológico
```
Frontend/Backend: Streamlit (app única monolítica)
Base de Datos: SQLite (archivo local)
Librerías: pandas, openpyxl, xlsxwriter, SQLAlchemy, plotly
Despliegue: Local en máquina operador FICEM
```

### 2.2 Estructura de Aplicación
```
v1/
├── app.py                    # App principal Streamlit
├── requirements.txt          # Dependencias
├── config/
│   ├── factores_emision.py   # FE SEIN, combustibles
│   └── bandas_gcca.py        # Clasificaciones GCCA
├── modules/
│   ├── excel_generator.py    # Generador templates
│   ├── excel_parser.py       # Parser datos ingresados
│   ├── validator.py          # Validaciones multinivel
│   ├── calculator.py         # Motor cálculos A1-A3
│   └── report_generator.py   # Generador reportes PDF
├── database/
│   ├── models.py             # Modelos SQLAlchemy
│   └── repository.py         # Acceso a datos
└── data/
    └── latam3c.db            # SQLite database
```

---

## 3. MÓDULOS FUNCIONALES

### 3.1 Generador de Templates Excel
**Entrada:**
- Perfil planta (integrada/molienda/concreto)
- País

**Salida:**
- Excel personalizado con:
  - Hojas según perfil
  - Validaciones integradas
  - Instrucciones contextuales
  - Dropdowns para datos maestros

**Lógica:**
- Plantillas base en código
- Generación dinámica con xlsxwriter
- Validaciones Excel (rangos, listas)

### 3.2 Parser y Validador
**Entrada:**
- Excel completado por empresa

**Proceso:**
1. Validación estructura (hojas, columnas requeridas)
2. Validación formato (tipos datos, rangos)
3. Validación coherencia:
   - Composiciones suman 100%
   - Balance masa clinker
   - Densidades vs volúmenes concreto
   - Rangos técnicos razonables

**Salida:**
- Datos validados → BD
- Lista errores específicos → corrección

### 3.3 Motor de Cálculo
**Entrada:**
- Datos validados desde BD
- Factores emisión por país (SEIN, combustibles)

**Cálculo por producto:**

**A1 - Materias Primas:**
```python
# Emisiones extracción y procesamiento upstream
emisiones_a1 = sum(materia_prima.cantidad * materia_prima.fe_upstream)
```

**A2 - Transporte:**
```python
# Emisiones transporte materias primas/combustibles
emisiones_a2 = sum(material.peso * material.distancia * fe_transporte)
```

**A3 - Producción:**
```python
# Clinker: Descarbonatación + combustibles + electricidad
emisiones_proceso = produccion_clinker * 0.525  # ~525 kg CO2/ton
emisiones_termicas = sum(combustible.consumo_tj * combustible.fe)
emisiones_electricas = consumo_mwh * factor_sein[pais][año]
emisiones_a3 = emisiones_proceso + emisiones_termicas + emisiones_electricas

# Cemento: Molienda + adiciones
emisiones_a3_cemento = emisiones_electricas_molienda + emisiones_adiciones

# Concreto: Mezclado + materiales
emisiones_a3_concreto = sum(componente.cantidad * componente.fe)
```

**Total:**
```python
emisiones_totales_a1a3 = emisiones_a1 + emisiones_a2 + emisiones_a3
```

### 3.4 Clasificador GCCA
**Entrada:**
- Emisiones kg CO₂e/unidad
- Resistencia (para concreto)
- Ratio clinker/cemento país (para cemento)

**Bandas Cemento:** A-G (según ratio país)
**Bandas Concreto:** AA-F (según resistencia MPa)

**Lógica:**
```python
def clasificar_cemento(emisiones, ratio_clinker_pais):
    bandas = calcular_bandas_equidistantes(ratio_clinker_pais)
    return banda_correspondiente(emisiones, bandas)

def clasificar_concreto(emisiones, resistencia_mpa):
    banda_aa, banda_f = BANDAS_GCCA_CONCRETO[resistencia_mpa]
    return interpolacion_lineal(emisiones, banda_aa, banda_f)
```

### 3.5 Base de Datos Benchmarking
**Almacenamiento anónimo:**
```sql
CREATE TABLE productos_anonimos (
    id INTEGER PRIMARY KEY,
    pais VARCHAR(50),
    año INTEGER,
    tipo_producto VARCHAR(20),  -- clinker/cemento/concreto
    emisiones_kgco2e FLOAT,
    resistencia_mpa FLOAT NULL, -- solo concreto
    banda_gcca VARCHAR(2),
    timestamp DATETIME
);
```

**Agregaciones:**
- Percentiles por país/región (P10, P25, P50, P75, P90)
- Curvas CO₂ vs resistencia (concreto)
- Distribución por bandas

---

## 4. SERVICIOS DE BACKEND (LÓGICA INTERNA)

### Servicio de Empresas
- CRUD empresas
- Gestión perfiles planta
- Historial submissions

### Servicio de Cálculo
- Orquestación pipeline validación → cálculo → clasificación
- Gestión factores emisión por país/año
- Actualización factores SEIN

### Servicio de Reportes
- Generación PDFs individuales (empresa)
- Dashboards consolidados (operador FICEM)
- Exportación datos CSV

### Servicio de Benchmarking
- Agregación anónima
- Cálculo percentiles
- Generación curvas comparativas

---

## 5. ESTRUCTURA DE NAVEGACIÓN

### 📊 DASHBOARD
- **Resumen Consolidado**: Métricas país, total empresas, submissions procesadas
- **Distribución Bandas GCCA**: Gráficos por producto (clinker/cemento/concreto)
- **Histórico Timeline**: Evolución temporal de emisiones

### 🏭 EMPRESAS
- **Listado Empresas**: Tabla con búsqueda/filtros
- **Registro Nueva Empresa**: Formulario (nombre, país, perfil planta, contacto)
- **Detalle Empresa**: Historial submissions, resultados históricos

### 🔧 CALCULADORAS 3C (Prioridad Fase 1)
- **Importar desde 3C**: Upload formato exportado desde calculadora corporativa
- **Validar Importación**: Verificación automática datos 3C
- **Calcular**: Ejecución motor cálculos A1-A3
- **Resultados 3C**: Visualización emisiones + banda GCCA

### 📋 EXCEL TRADICIONAL
- **Generar Templates**: Selector perfil → descarga Excel personalizado
- **Cargar Excel Manual**: Upload + validación estructura/formato/coherencia
- **Corregir Errores**: Feedback específico para re-envío
- **Procesar**: Cálculo tras validación exitosa

### 📈 ANÁLISIS Y VISUALIZACIONES
- **Curvas CO₂ vs Resistencia**: Benchmarking concretos
- **Comparativa por País**: Percentiles P10-P90
- **Análisis por Bandas**: Distribución empresas en clasificación GCCA
- **Tendencias Temporales**: Evolución emisiones multi-año

### 📄 REPORTES
- **Generar Reporte Individual**: PDF por empresa con clasificación + benchmarking
- **Reporte Consolidado País**: Agregación anónima para autoridad
- **Exportar Datos**: CSV/Excel con resultados seleccionados

### 🛣️ HOJA DE RUTA
- **Estado Implementación**: Fase actual (1-4) + progreso %
- **Checklist Entregables**: Tareas por fase con estado (pendiente/en proceso/completado)
- **Empresas Piloto**: Tracking validación 2 empresas con 3C + 1 Excel manual

**Total:** 7 secciones menú, 23 páginas

---

## 6. MODELO DE DATOS (SIMPLIFICADO)

```python
class Empresa:
    id, nombre, pais, perfil_planta, contacto

class Submission:
    id, empresa_id, año, archivo_excel, estado, timestamp

class ResultadoClikerCemento:
    id, submission_id, tipo_producto, emisiones_a1, a2, a3, total, banda_gcca

class ResultadoConcreto:
    id, submission_id, diseño, resistencia_mpa, emisiones_a1a3, banda_gcca

class FactorEmision:
    id, pais, año, tipo, valor, unidad, fuente
```

---

## 7. CRITERIOS DE ÉXITO

- Generación templates en <5 segundos
- Validación archivo Excel en <10 segundos
- Cálculo completo planta en <30 segundos
- Generación reporte PDF en <15 segundos
- Interfaz responsive sin recargas innecesarias

---

## 8. LIMITACIONES CONSCIENTES (PARA ETAPA 2)

- Sin autenticación multi-usuario
- Sin API REST
- Sin gestión multi-año automática
- Sin formularios web (solo Excel)
- Sin hosting cloud
- Sin backups automáticos

---

**Fin del Documento**
