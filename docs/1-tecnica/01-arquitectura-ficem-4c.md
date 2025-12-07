# Especificación Técnica: Arquitectura FICEM Core + 4C Perú

**Versión**: 1.0
**Fecha**: 2025-12-06
**Documento**: Vivo (se actualiza conforme se implementa)

> Este documento describe la arquitectura técnica detallada de las dos aplicaciones separadas.
> Está ligado al plan en `00-plan-etapa-1-dos-apps.md` y las decisiones registradas en `sesion_2025-12-06.md`.

---

## 1. PRINCIPIOS DE DISEÑO

- **Separación clara**: Backend (lógica) vs Frontend (presentación)
- **Reutilización**: Mismo código de cálculos para todos los países
- **Escalabilidad**: Agregar país = agregar solo frontend
- **Independencia**: Cada app puede funcionar en su propia máquina/contenedor
- **Comunicación clara**: APIs REST bien documentadas entre apps

---

## 2. FICEM CORE: ESPECIFICACIÓN TÉCNICA

### 2.1 Propósito

Backend centralizado que contiene:
- Todo cálculo de emisiones
- Toda validación de datos
- Base de datos unificada
- Gestión de factores de emisión

**Usuarios**: Operador FICEM, APIs (4C Perú y otros frontends)

### 2.2 Estructura de Módulos

```
ficem-core/
├── modules/
│   ├── __init__.py
│   ├── calculator.py              # Motor A1-A3
│   ├── validator.py               # Validaciones
│   ├── classifier.py              # GCCA
│   ├── excel_generator.py         # Generador templates
│   ├── excel_parser.py            # Parser datos
│   └── emissions_factor_manager.py # Gestor factores
│
├── database/
│   ├── __init__.py
│   ├── models.py                  # Modelos ORM
│   └── repository.py              # Acceso datos
│
├── api/
│   ├── __init__.py
│   ├── routes.py                  # Endpoints REST
│   ├── schemas.py                 # Validación requests
│   └── response_models.py         # Formatos respuestas
│
├── config/
│   ├── __init__.py
│   ├── factores_emision.py        # Datos factores
│   └── bandas_gcca.py             # Datos bandas
│
├── app.py                         # Streamlit (operador)
├── main.py                        # FastAPI (APIs)
└── requirements.txt
```

### 2.3 Módulo: Calculator.py

**Responsabilidad**: Ejecutar fórmulas de cálculo A1-A3

**Clase principal**:
```python
class CarbonFootprintCalculator:
    def calculate_clinker(self, data: dict) -> dict:
        """Calcula emisiones para clinker"""
        # A1: materias primas
        # A2: transporte
        # A3: proceso (descarbonatación + combustibles + electricidad)
        # Retorna: {a1, a2, a3, total}
        pass

    def calculate_cement(self, data: dict) -> dict:
        """Calcula emisiones para cemento"""
        pass

    def calculate_concrete(self, data: dict) -> dict:
        """Calcula emisiones para concreto"""
        pass
```

**Fórmulas por producto**:

```python
# CLINKER
A1 = sum(raw_material.cantidad * raw_material.fe_upstream)
A2 = sum(material.peso * material.distancia * fe_transporte)
A3_proceso = produccion_clinker * 0.525  # kg CO2/ton
A3_termico = sum(combustible.consumo_tj * combustible.fe)
A3_electrico = consumo_mwh * factor_sein[pais][año]
A3 = A3_proceso + A3_termico + A3_electrico
TOTAL = A1 + A2 + A3

# CEMENTO
A1_adiciones = sum(adicion.cantidad * adicion.fe)
A2 = (clinker_usado * fe_transporte_clinker) + (adiciones_transporte)
A3_molienda = consumo_electricidad_molienda * factor_sein[pais][año]
A3 = A3_molienda + A1_adiciones  # Las adiciones se cuentan en A3 para cemento
TOTAL = (clinker_emitidas / ratio_clinker_cemento) + A1_adiciones + A2 + A3_molienda

# CONCRETO
A1_totales = sum(componente.cantidad * componente.fe)  # Cemento, agregados, aditivos
A2 = sum(transporte_componentes)
A3_mezcla = consumo_electricidad * factor_sein[pais][año]
TOTAL = A1_totales + A2 + A3_mezcla
```

### 2.4 Módulo: Validator.py

**Responsabilidad**: Validar datos Excel antes de cálculos

**Niveles de validación**:

```python
class ExcelValidator:
    def validate_structure(self, excel_file) -> ValidationReport:
        """Verifica que existan hojas requeridas, columnas correctas"""
        # Valida: hojas presentes, columnas esperadas, tipos datos
        pass

    def validate_format(self, excel_file) -> ValidationReport:
        """Verifica tipos de datos, formatos, rangos"""
        # Valida: números vs texto, fechas, decimales
        pass

    def validate_coherence(self, excel_file) -> ValidationReport:
        """Verifica lógica entre datos"""
        # Validaciones específicas:
        # - Composiciones suman 100%
        # - Balance masa clinker
        # - Densidades vs volúmenes (concreto)
        # - Rangos técnicos razonables
        pass

    def validate_completeness(self, excel_file) -> ValidationReport:
        """Verifica que no falten datos críticos"""
        pass
```

**Salida**: `ValidationReport` con errores específicos por campo

### 2.5 Módulo: Classifier.py

**Responsabilidad**: Asignar bandas GCCA según emisiones

```python
class GCCAClassifier:
    def classify_cement(self, emisiones_kg_co2_ton: float,
                       ratio_clinker_pais: float) -> dict:
        """Clasifica cemento en bandas A-G"""
        # Bandas dinámicas según ratio país
        # Retorna: {banda: "A", posicion: 15%, percentil: "top 15%"}
        pass

    def classify_concrete(self, emisiones_kg_co2_m3: float,
                         resistencia_mpa: float) -> dict:
        """Clasifica concreto en bandas AA-F"""
        # Bandas según resistencia
        # Retorna: {banda: "AA", posicion: 5%, percentil: "top 5%"}
        pass
```

### 2.6 Base de Datos - Modelo Conceptual

```
EMPRESAS
├── id (PK)
├── nombre
├── pais
├── perfil_planta (integrada/molienda/concreto)
└── contacto

PLANTAS
├── id (PK)
├── empresa_id (FK)
├── nombre
├── ubicacion
└── tipo_equipamiento

SUBMISSIONS (cargas de datos)
├── id (PK)
├── empresa_id (FK)
├── archivo_nombre
├── estado (pendiente/validando/calculando/completado/error)
├── timestamp
└── datos_json (datos raw)

RESULTADOS_CLINKER
├── id (PK)
├── submission_id (FK)
├── planta_id (FK)
├── emisiones_a1
├── emisiones_a2
├── emisiones_a3
├── emisiones_total
├── banda_gcca
└── timestamp

RESULTADOS_CEMENTO
└── [similar a clinker]

RESULTADOS_CONCRETO
├── id (PK)
├── submission_id (FK)
├── resistencia_mpa
├── emisiones_a1a3
├── banda_gcca
├── volumen_m3
└── timestamp

FACTORES_EMISION
├── id (PK)
├── pais
├── año
├── tipo (SEIN/combustible/transporte/materia_prima)
├── valor
├── unidad
└── fuente

RESULTADOS_ANONIMOS (benchmarking)
├── id (PK)
├── pais
├── año
├── tipo_producto (clinker/cemento/concreto)
├── emisiones_kg_co2_unit
├── banda_gcca
└── timestamp
```

### 2.7 API REST (Futuro)

**Base URL**: `http://ficem-core:8000` (desarrollo local)

**Endpoints**:

```
# Generador Excel
GET /api/v1/excel-generator/generate
  params: perfil, pais, empresa_nombre (opt)
  return: archivo .xlsx

# Validación
POST /api/v1/validator/validate
  body: FormData (archivo Excel)
  return: {valid: bool, errors: []}

# Cálculos
POST /api/v1/calculator/calculate
  body: {datos_validados}
  return: {clinker: {...}, cemento: {...}, concreto: {...}}

# Clasificación
POST /api/v1/classifier/classify
  body: {producto, emisiones, parametros_opcionales}
  return: {banda, posicion, percentil}

# Empresas
GET /api/v1/empresas
  params: pais, nombre (opt)
  return: [{id, nombre, pais, perfil}]

GET /api/v1/empresas/{id}
  return: {id, nombre, pais, perfil, plantas: []}

# Resultados
GET /api/v1/resultados/{submission_id}
  return: {clinker, cemento, concreto}
```

---

## 3. 4C PERÚ: ESPECIFICACIÓN TÉCNICA

### 3.1 Propósito

Frontend específico para Perú que:
- Muestra resultados de empresas peruanas
- Permite generar Excel (consumiendo API de FICEM Core)
- Genera reportes específicos país
- Provee dashboards y análisis para Perú

**Usuarios**: Stakeholders, empresas, público interesado

### 3.2 Estructura

```
4c-peru/
├── pages/
│   ├── 01_dashboard.py            # Dashboard Perú
│   ├── 02_empresas.py             # Listado empresas PE
│   ├── 03_generador_excel.py      # Genera Excel (API)
│   ├── 04_resultados.py           # Vista resultados
│   ├── 05_benchmarking.py         # Benchmarking PE
│   └── 06_reportes.py             # Reportes PE
│
├── config/
│   ├── __init__.py
│   └── api_config.py              # URL de FICEM Core
│
├── utils/
│   ├── __init__.py
│   ├── api_client.py              # Cliente REST
│   └── formatters.py              # Formatos PE
│
├── app.py                         # Main Streamlit
└── requirements.txt
```

### 3.3 Cliente REST (api_client.py)

```python
class FiemCoreClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def generar_excel(self, perfil: str) -> bytes:
        """Descarga archivo Excel personalizado"""
        response = self.session.get(
            f"{self.base_url}/api/v1/excel-generator/generate",
            params={"perfil": perfil, "pais": "PE"}
        )
        return response.content

    def obtener_empresas_peru(self) -> list:
        """Obtiene listado de empresas peruanas"""
        response = self.session.get(
            f"{self.base_url}/api/v1/empresas",
            params={"pais": "PE"}
        )
        return response.json()

    def obtener_resultados(self, empresa_id: int) -> dict:
        """Obtiene resultados de una empresa"""
        response = self.session.get(
            f"{self.base_url}/api/v1/resultados/{empresa_id}"
        )
        return response.json()
```

### 3.4 Páginas Streamlit

**01_dashboard.py**: Métricas consolidadas de Perú
- Total de empresas procesadas
- Total de remitos/muestras
- Promedio de emisiones por producto
- Gráficos de distribución por bandas GCCA

**02_empresas.py**: Directorio de empresas peruanas
- Tabla con búsqueda y filtros
- Información de contacto
- Último envío procesado
- Link a detalle

**03_generador_excel.py**: Generador integrado
- Selector de perfil de planta
- Botón "Descargar Excel"
- Consume GET /api/v1/excel-generator/generate
- Instruye sobre llenado

**04_resultados.py**: Vista de cálculos
- Tabla de resultados procesados
- Búsqueda por empresa
- Exportación a Excel

**05_benchmarking.py**: Análisis comparativo de Perú
- Gráficos CO₂ vs Resistencia
- Distribución por bandas
- Percentiles de desempeño

**06_reportes.py**: Generación de reportes
- Reporte individual empresa (PDF)
- Reporte consolidado país
- Exportación datos CSV

---

## 4. FLUJO DE DATOS

### 4.1 Flujo de Cálculo (Usuario FICEM)

```
Operador FICEM
    ↓
Carga Excel en FICEM CORE (app.py)
    ↓
Validador (validator.py) valida estructura/formato/coherencia
    ↓ (si hay errores)
Genera reporte con problemas → Operador corrige
    ↓ (si válido)
Calculador (calculator.py) calcula A1-A3
    ↓
Clasificador (classifier.py) asigna bandas GCCA
    ↓
Almacena resultados en BD
    ↓
Operador ve resultados en FICEM CORE Dashboard
    ↓
Datos disponibles para 4C Perú vía API
```

### 4.2 Flujo de Generación Excel (Usuario 4C Perú)

```
Usuario en 4C Perú accede a "Generador Excel"
    ↓
Selecciona perfil de planta
    ↓
Clickea "Descargar Excel"
    ↓
4C Perú llama API FICEM CORE
    GET /api/v1/excel-generator/generate?perfil=X&pais=PE
    ↓
FICEM CORE genera archivo dinámicamente
    ↓
Retorna .xlsx al usuario
    ↓
Usuario descarga y completa
    ↓
Usuario carga en FICEM CORE (enviada por operador o empresa)
```

---

## 5. CONFIGURACIÓN

### 5.1 Variables de Entorno

**FICEM CORE** (`.env.ficem`):
```
DATABASE_URL=sqlite:///latam4c.db
FACTORES_EMISION_PATH=config/factores_emision.py
BANDAS_GCCA_PATH=config/bandas_gcca.py
STREAMLIT_PORT=8501
API_PORT=8000
```

**4C PERÚ** (`.env.4c-peru`):
```
FICEM_CORE_URL=http://localhost:8000
STREAMLIT_PORT=8502
PAIS_CODIGO=PE
```

### 5.2 Dependencias

**FICEM CORE**:
```
streamlit
fastapi
uvicorn
sqlalchemy
pandas
openpyxl
xlsxwriter
plotly
python-dotenv
```

**4C PERÚ**:
```
streamlit
requests
pandas
plotly
python-dotenv
```

---

## 6. TESTING

### 6.1 Unit Tests (FICEM Core)

```python
# test_calculator.py
def test_calculate_clinker():
    calc = CarbonFootprintCalculator()
    result = calc.calculate_clinker({...})
    assert result['total'] > 0
    assert result['a1'] + result['a2'] + result['a3'] == result['total']

def test_validate_coherence():
    validator = ExcelValidator()
    errors = validator.validate_coherence({...})
    assert len(errors) == 0

def test_classify_cement():
    classifier = GCCAClassifier()
    result = classifier.classify_cement(550, 0.65)
    assert result['banda'] in ['A', 'B', 'C', 'D', 'E', 'F', 'G']
```

### 6.2 Integration Tests

```python
# test_full_flow.py
def test_excel_to_results():
    # 1. Generar Excel
    # 2. Llenar datos
    # 3. Validar
    # 4. Calcular
    # 5. Clasificar
    # 6. Verificar resultado
    pass
```

### 6.3 API Tests

```python
def test_excel_generator_endpoint():
    response = client.get("/api/v1/excel-generator/generate?perfil=concreto&pais=PE")
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/vnd.openxmlformats'
```

---

## 7. DEPLOYMENT

### 7.1 Desarrollo Local

```bash
# Terminal 1: FICEM Core
cd ficem-core
python -m streamlit run app.py --server.port 8501

# Terminal 2: APIs (futuro)
uvicorn main:app --port 8000

# Terminal 3: 4C Perú
cd ../4c-peru
python -m streamlit run app.py --server.port 8502
```

### 7.2 Producción (Futuro)

- FICEM Core: servidor privado + PostgreSQL
- 4C Perú: servidor público + CDN
- APIs: FastAPI en contenedor Docker
- Reverse proxy (nginx) para enrutamiento

---

## 8. EVOLUCIÓN FUTURA

**Etapa 2**: Agregar nuevo país (Colombia)
```
4c-colombia/ ← Nuevo frontend (mismo código, otro pais)
    ↓
Consume APIs de FICEM Core (sin cambios)
    ↓
Mismos cálculos, presentación diferente
```

---

**Documento en evolución**: Se actualiza conforme se implementa
**Última actualización**: 2025-12-06
**Estado**: Especificación técnica inicial
