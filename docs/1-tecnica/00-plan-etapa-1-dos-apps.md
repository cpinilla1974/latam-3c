# Plan Etapa 1 - Arquitectura dos aplicaciones separadas

**Versión:** 2.0 (actualizado 2025-12-06)
**Fecha:** 2025-12-06
**Alcance:** Etapa 1 - Arquitectura FICEM Core + 4C Perú
**Tecnología:** Streamlit + Python + SQLite + APIs REST

> **Nota histórica**: Esta es la versión 2 del plan. La versión 1 (monolito) fue archivada en `docs/4-historico/v1/13-plan-etapa-1-HASTA_2025-12-06.md`

---

## 1. VISIÓN GENERAL

Sistema de huella de carbono con **arquitectura de dos aplicaciones separadas**:

1. **FICEM CORE**: Backend centralizado con motor de cálculos, validaciones y base de datos
2. **4C PERÚ**: Frontend específico de Perú con dashboards, resultados y empresas peruanas

Esta arquitectura permite reutilizar toda la lógica de cálculos para múltiples países (Colombia, Ecuador, etc.) en Etapa 2+.

**Productos calculados:**
- Clinker: 750-950 kg CO₂e/ton
- Cemento: 400-900 kg CO₂e/ton
- Concreto: 150-500 kg CO₂e/m³

---

## 2. ARQUITECTURA

### 2.1 Diagrama General

```
┌─────────────────────────────────────────────────────────┐
│          FICEM CORE (Backend Centralizado)              │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Servicios/Módulos:                               │  │
│  │  • Motor cálculos A1-A3                          │  │
│  │  • Validador de datos                            │  │
│  │  • Clasificador GCCA                             │  │
│  │  • Generador Excel (API REST)                    │  │
│  │  • Gestor factores de emisión                    │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Base de Datos Centralizada (SQLite → PostgreSQL) │ │
│  │  • Empresas, plantas, materiales, producción     │  │
│  │  • Resultados cálculos                           │  │
│  │  • Benchmarking anónimo global                   │  │
│  │  • Factores de emisión por país/año              │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↑                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Interfaz Operador FICEM (Streamlit):             │  │
│  │  • Carga de archivos Excel                       │  │
│  │  • Monitoreo de procesamiento                    │  │
│  │  • Gestión de empresas                           │  │
│  │  • Vista de resultados consolidados              │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
              ↓               ↓               ↓
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │ 4C PERÚ     │ │ 4C COLOMBIA │ │ 4C ECUADOR  │
        │ (v1.0)      │ │ (Futuro)    │ │ (Futuro)    │
        │             │ │             │ │             │
        │ Frontend    │ │ Frontend    │ │ Frontend    │
        │ específico  │ │ específico  │ │ específico  │
        └─────────────┘ └─────────────┘ └─────────────┘
```

### 2.2 Stack Tecnológico

**FICEM Core:**
```
Frontend/Operador: Streamlit (puede evolucionar a React/Vue)
Backend APIs: FastAPI o Flask (futuro)
Base de Datos: SQLite (desarrollo) → PostgreSQL (producción)
Librerías: pandas, openpyxl, xlsxwriter, SQLAlchemy, plotly
```

**4C Perú:**
```
Frontend: Streamlit (inicial) → Next.js/React (futuro)
Cliente API: requests, httpx
Base de Datos: ninguna (consume de FICEM Core vía API)
Librerías: pandas, plotly, requests
```

### 2.3 Estructura de Carpetas

```
latam-3c/
│
├── ficem-core/                          # Backend centralizado
│   ├── app.py                           # Interfaz operador FICEM
│   ├── requirements.txt
│   │
│   ├── modules/                         # Lógica de negocio
│   │   ├── calculator.py                # Motor cálculos A1-A3
│   │   ├── validator.py                 # Validaciones multinivel
│   │   ├── classifier.py                # Clasificación GCCA
│   │   ├── excel_generator.py           # Generador templates
│   │   └── excel_parser.py              # Parser datos Excel
│   │
│   ├── api/                             # APIs REST (futuro)
│   │   ├── generator_api.py             # API generador Excel
│   │   ├── calculator_api.py            # API cálculos
│   │   ├── validator_api.py             # API validación
│   │   └── classifier_api.py            # API clasificación
│   │
│   ├── database/
│   │   ├── models.py                    # Modelos SQLAlchemy
│   │   ├── repository.py                # Acceso a datos
│   │   └── latam4c.db                   # SQLite (dev)
│   │
│   └── config/
│       ├── factores_emision.py          # FE SEIN, combustibles
│       └── bandas_gcca.py               # Clasificaciones GCCA
│
├── 4c-peru/                             # Frontend específico Perú
│   ├── app.py                           # App principal
│   ├── requirements.txt
│   │
│   ├── pages/
│   │   ├── 01_dashboard.py              # Dashboard Perú
│   │   ├── 02_empresas.py               # Listado empresas Perú
│   │   ├── 03_generador_excel.py        # Generador (consume API)
│   │   ├── 04_resultados.py             # Resultados cálculos
│   │   ├── 05_benchmarking.py           # Benchmarking Perú
│   │   └── 06_reportes.py               # Reportes Perú
│   │
│   ├── config/
│   │   └── api_config.py                # URLs APIs FICEM Core
│   │
│   └── utils/
│       ├── api_client.py                # Cliente REST
│       └── formatters.py                # Formatos específicos Perú
│
├── docs/
│   ├── 1-tecnica/
│   │   ├── 00-plan-etapa-1-dos-apps.md (este archivo)
│   │   └── 01-arquitectura-ficem-4c.md
│   │
│   ├── 3-sesiones/
│   │   └── sesion_2025-12-06.md
│   │
│   └── 4-historico/v1/
│       └── 13-plan-etapa-1-HASTA_2025-12-06.md (versión anterior)
│
└── [archivos raíz: README, requirements, etc.]
```

---

## 3. APLICACIÓN 1: FICEM CORE (Backend)

### 3.1 Responsabilidades

- Validación de datos Excel (estructura, formato, coherencia)
- Cálculos de emisiones A1-A3 (Clinker, Cemento, Concreto)
- Clasificación GCCA (bandas A-G, AA-F)
- Gestión de factores de emisión por país/año
- Generación de plantillas Excel personalizadas
- Almacenamiento centralizado de resultados
- APIs REST para consumo por frontends

### 3.2 Módulos Funcionales

**Módulo 1: Generador de Templates Excel**
- Entrada: Perfil planta (integrada/molienda/concreto), país
- Salida: Excel con hojas dinámicas según perfil
- Responsabilidad: Generar plantillas consistentes

**Módulo 2: Validador Excel**
- Entrada: Excel completado por empresa
- Proceso: Validaciones estructura → formato → coherencia
- Salida: Datos validados o lista de errores

**Módulo 3: Motor de Cálculos**
- Entrada: Datos validados
- Proceso: Cálculos A1-A3 por producto
- Salida: Emisiones por alcance, totales, factores

**Módulo 4: Clasificador GCCA**
- Entrada: Emisiones + resistencia (si aplica)
- Proceso: Clasificación según bandas GCCA
- Salida: Banda asignada + posición en benchmarking

**Módulo 5: Gestor Factores Emisión**
- Entrada: País, año, tipo (SEIN, combustible, transporte)
- Proceso: Actualización y gestión de factores
- Salida: Factores vigentes para cálculos

### 3.3 Base de Datos

**Tablas principales:**
```sql
-- Datos maestros
CREATE TABLE empresas (id, nombre, pais, perfil_planta, contacto);
CREATE TABLE plantas (id, empresa_id, nombre, ubicacion, tipo);
CREATE TABLE factores_emision (id, pais, año, tipo, valor, unidad);

-- Procesamiento
CREATE TABLE submissions (id, empresa_id, archivo, estado, timestamp);
CREATE TABLE datos_validados (id, submission_id, datos_json);

-- Resultados
CREATE TABLE resultados_clinker (id, submission_id, emisiones_a1, a2, a3, total, banda_gcca);
CREATE TABLE resultados_cemento (id, submission_id, emisiones_a1, a2, a3, total, banda_gcca);
CREATE TABLE resultados_concreto (id, submission_id, resistencia_mpa, emisiones_a1a3, banda_gcca);

-- Benchmarking anónimo
CREATE TABLE resultados_anonimos (id, pais, año, tipo_producto, emisiones, banda_gcca, timestamp);
```

---

## 4. APLICACIÓN 2: 4C PERÚ (Frontend)

### 4.1 Responsabilidades

- Mostrar resultados específicos de Perú
- Información de empresas peruanas
- Dashboards y visualizaciones para Perú
- Generación de Excel (consumiendo API de FICEM Core)
- Reportes específicos país
- Interfaz para stakeholders de Perú

### 4.2 Páginas/Secciones

1. **Dashboard Perú**: Métricas consolidadas del país
2. **Empresas**: Listado y detalle de empresas peruanas
3. **Generador Excel**: Interfaz que consume API del generador
4. **Resultados**: Vista de cálculos y clasificaciones
5. **Benchmarking**: Análisis comparativo nacional
6. **Reportes**: Exportación de datos y reportes

### 4.3 Comunicación con FICEM Core

**Cliente HTTP:**
```python
# En utils/api_client.py
class FiemCoreClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def generar_excel(self, perfil, pais):
        # GET /api/excel-generator/generate
        pass

    def obtener_empresas_peru(self):
        # GET /api/empresas?pais=PE
        pass

    def obtener_resultados(self, empresa_id):
        # GET /api/resultados?empresa_id=X
        pass
```

---

## 5. MICROSERVICIO: GENERADOR EXCEL

### 5.1 Ubicación e Implementación

- **Ubicación**: Dentro de FICEM Core (`ficem-core/api/generator_api.py`)
- **Tipo**: API REST (FastAPI/Flask)
- **Consumidor**: 4C Perú y otros frontends

### 5.2 Endpoint

```
GET /api/excel-generator/generate
Parameters:
  - perfil: "integrada" | "molienda" | "concreto"
  - pais: "PE" | "CO" | "EC"
  - empresa_nombre: string (opcional)

Response:
  - 200: archivo Excel descargable
  - 400: error en parámetros
```

---

## 6. FASES DE IMPLEMENTACIÓN

### Fase 1: Separación y Estructura (Semana 1-2)

1. Crear estructura carpetas `ficem-core/` y `4c-peru/`
2. Copiar código v1 a carpetas correspondientes
3. Refactorizar imports para evitar referencias cruzadas
4. Crear `__init__.py` y modularizar código

**Entregable**: Código organizado, sin cambio funcional

### Fase 2: Validador y Cálculos (Semana 3-4)

1. Implementar módulo `modules/validator.py` completo
2. Implementar módulo `modules/calculator.py` (A1-A3)
3. Implementar módulo `modules/classifier.py` (GCCA)
4. Testing con datos reales

**Entregable**: Motor de cálculos funcional en FICEM Core

### Fase 3: APIs REST (Semana 5)

1. Crear API REST para generador Excel
2. Crear API REST para validador
3. Crear API REST para calculador
4. Documentación OpenAPI/Swagger

**Entregable**: APIs funcionales y documentadas

### Fase 4: Integración 4C Perú (Semana 6)

1. Crear cliente REST en `4c-peru/utils/api_client.py`
2. Actualizar páginas para consumir APIs
3. Testing de comunicación entre apps
4. Deploy de ambas apps

**Entregable**: Dos apps funcionando juntas

### Fase 5: Validación Final (Semana 7+)

1. Testing end-to-end con datos reales
2. Ajustes según feedback
3. Documentación de operación
4. Deploy a producción

---

## 7. CRITERIOS DE ÉXITO

- ✅ Dos aplicaciones separadas y funcionando
- ✅ Motor de cálculos A1-A3 preciso y validado
- ✅ APIs REST documentadas y estables
- ✅ 4C Perú consume exitosamente datos de FICEM Core
- ✅ Generador Excel funciona como microservicio
- ✅ Base de datos centralizada con datos de múltiples empresas

---

## 8. PRÓXIMA ETAPA (Etapa 2)

Con esta arquitectura, Etapa 2 puede:
- Agregar nuevo país (Colombia, Ecuador) como nuevo frontend
- Mantener FICEM Core sin cambios (reutilización de APIs)
- Agregar portal web para empresas (formularios dinámicos)
- Escalar base de datos a PostgreSQL

---

**Versión**: 2.0
**Última actualización**: 2025-12-06
**Estado**: Plan vigente
**Documento anterior**: `docs/4-historico/v1/13-plan-etapa-1-HASTA_2025-12-06.md`
