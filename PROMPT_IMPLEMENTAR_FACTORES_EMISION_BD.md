# PROMPT: Implementar Sistema de Gestión de Factores de Emisión en Base de Datos

## Contexto

Estás trabajando en el proyecto `latam-3c` (calculadora de CO2 para Perú). Actualmente los factores de emisión (GWP - Global Warming Potential) de materiales están **hardcodeados en diccionarios Python**. Necesitas migrar a un sistema dinámico de **base de datos** que permita:

1. **Múltiples fuentes** (GCCA, Ecoinvent, valores custom)
2. **Múltiples categorías de impacto** (GWP-total, GWP-fósil, GWP-biogénico, etc.)
3. **Gestión web** para agregar/editar/establecer factores por defecto
4. **Retrocompatibilidad** total con código existente
5. **Trazabilidad** completa de fuentes y versiones

Este sistema ya fue implementado exitosamente en el proyecto hermano `mzma-3c` (México) y debes replicarlo adaptándolo a Perú.

---

## Arquitectura del Sistema

### Modelo de Datos

```
tb_fuentes_factores
├─ id_fuente (PK)
├─ nombre_fuente (GCCA, Ecoinvent, CUSTOM_PERU, etc.)
├─ version
├─ metodologia (EN 15804, ISO 14040, etc.)
└─ año_publicacion

tb_categorias_impacto
├─ id_categoria (PK)
├─ codigo_categoria (GWP-tot, GWP-fos, GWP-bio, ODP, etc.)
├─ nombre_categoria
├─ unidad (kg CO2 eq., kg CFC-11 eq., etc.)
└─ orden_presentacion

tb_factores_emision
├─ id_factor (PK)
├─ id_subtipo_producto (FK → materiales: caliza, arcilla, yeso, etc.)
├─ id_fuente (FK → tb_fuentes_factores)
├─ id_categoria (FK → tb_categorias_impacto)
├─ valor_factor (NUMERIC)
├─ codigo_referencia (ID dentro de la fuente)
├─ nombre_proceso (descripción del proceso)
├─ ubicacion (GLOBAL, PE, CUSTOM)
├─ es_defecto (BOOLEAN) ← Solo uno TRUE por material+categoría
├─ notas (TEXT)
└─ auditoría (creado_por, fecha_creacion, actualizado_por, etc.)

tb_factores_defecto (VISTA)
└─ Vista de compatibilidad que emula estructura antigua
    Retorna solo factores donde es_defecto = TRUE
```

### Flujo de Datos

```
┌─────────────────────┐
│ Diccionario Python  │  ← Estado actual (hardcoded)
│ FACTORES_DEFECTO    │
└─────────────────────┘
          │
          │ MIGRACIÓN
          ↓
┌─────────────────────┐
│ tb_factores_emision │  ← Estado objetivo (BD)
│  + tb_fuentes       │
│  + tb_categorias    │
└─────────────────────┘
          │
          ↓
┌─────────────────────┐
│ v_factores_defecto  │  ← Vista de compatibilidad
│ (emula estructura   │     (código existente sigue funcionando)
│  del diccionario)   │
└─────────────────────┘
```

---

## Archivos a Crear

### 1. Schema SQL - Estructura de Tablas

**Ubicación**: `database/01_crear_modelo_factores_emision.sql`

**Referencia**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/database/schema_factores_emision.sql`

**Contenido** (adaptar a Perú):

```sql
-- Tabla de fuentes
CREATE TABLE tb_fuentes_factores (
    id_fuente SERIAL PRIMARY KEY,
    nombre_fuente VARCHAR(100) NOT NULL,
    version VARCHAR(50),
    metodologia VARCHAR(100),
    año_publicacion INTEGER,
    url_referencia TEXT,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creado_por VARCHAR(50) DEFAULT 'sistema'
);

-- Tabla de categorías de impacto
CREATE TABLE tb_categorias_impacto (
    id_categoria SERIAL PRIMARY KEY,
    codigo_categoria VARCHAR(20) NOT NULL UNIQUE,
    nombre_categoria VARCHAR(200) NOT NULL,
    nombre_corto VARCHAR(50),
    unidad VARCHAR(50),
    descripcion TEXT,
    orden_presentacion INTEGER,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de factores de emisión
CREATE TABLE tb_factores_emision (
    id_factor SERIAL PRIMARY KEY,
    id_subtipo_producto INTEGER NOT NULL,
    id_fuente INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    valor_factor NUMERIC(20, 12) NOT NULL,
    codigo_referencia VARCHAR(100),
    nombre_proceso VARCHAR(200),
    ubicacion VARCHAR(10),
    es_defecto BOOLEAN DEFAULT FALSE,
    notas TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_vigencia_inicio DATE,
    fecha_vigencia_fin DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creado_por VARCHAR(50),
    fecha_actualizacion TIMESTAMP,
    actualizado_por VARCHAR(50),

    FOREIGN KEY (id_subtipo_producto) REFERENCES tb_subtipo_producto(id_subtipo_producto),
    FOREIGN KEY (id_fuente) REFERENCES tb_fuentes_factores(id_fuente),
    FOREIGN KEY (id_categoria) REFERENCES tb_categorias_impacto(id_categoria),

    -- Solo un factor por defecto por material y categoría
    UNIQUE (id_subtipo_producto, id_categoria, es_defecto)
           WHERE es_defecto = TRUE
);

-- Vista de compatibilidad (emula tb_factores_defecto antigua)
CREATE OR REPLACE VIEW v_factores_defecto AS
SELECT
    fe.id_subtipo_producto,
    fe.valor_factor,
    ff.nombre_fuente as fuente,
    fe.codigo_referencia as referencia_fuente,
    fe.notas as comentarios,
    sp.codigo_material,
    sp.nombre_display
FROM tb_factores_emision fe
JOIN tb_fuentes_factores ff ON fe.id_fuente = ff.id_fuente
JOIN tb_subtipo_producto sp ON fe.id_subtipo_producto = sp.id_subtipo_producto
JOIN tb_categorias_impacto ci ON fe.id_categoria = ci.id_categoria
WHERE fe.es_defecto = TRUE
  AND fe.activo = TRUE
  AND ci.codigo_categoria = 'GWP-tot';

-- Crear alias para compatibilidad total
CREATE OR REPLACE VIEW tb_factores_defecto AS
SELECT * FROM v_factores_defecto;
```

**Datos iniciales**:

```sql
-- Fuentes de factores para Perú
INSERT INTO tb_fuentes_factores (nombre_fuente, version, metodologia, año_publicacion, descripcion) VALUES
('GCCA', 'EPD_5_1', 'EN 15804:2012+A2:2019', 2024, 'Global Cement and Concrete Association - Environmental Product Declaration v5.1'),
('CUSTOM_PERU', '1.0', 'Interno', 2025, 'Factores personalizados basados en datos locales de Perú'),
('Ecoinvent', '3.9.1', 'ISO 14040/14044', 2023, 'Base de datos Ecoinvent v3.9.1'),
('FICEM_ASOCEM', '2025', 'Protocolo MRV FICEM', 2025, 'Protocolo MRV para industria cementera Perú');

-- Categorías de impacto (según EN 15804)
INSERT INTO tb_categorias_impacto (codigo_categoria, nombre_categoria, nombre_corto, unidad, orden_presentacion) VALUES
('GWP-tot', 'Potencial de Calentamiento Global - Total', 'GWP Total', 'kg CO2 eq.', 1),
('GWP-fos', 'Potencial de Calentamiento Global - Fósil', 'GWP Fósil', 'kg CO2 eq.', 2),
('GWP-bio', 'Potencial de Calentamiento Global - Biogénico', 'GWP Biogénico', 'kg CO2 eq.', 3),
('GWP-luc', 'Potencial de Calentamiento Global - Cambio Uso Suelo', 'GWP Uso Suelo', 'kg CO2 eq.', 4),
('ODP', 'Potencial de Agotamiento de Ozono', 'ODP', 'kg CFC-11 eq.', 5),
('AP', 'Potencial de Acidificación', 'AP', 'kg SO2 eq.', 6),
('EP-fw', 'Potencial de Eutrofización - Agua dulce', 'EP Agua dulce', 'kg P eq.', 7),
('EP-mar', 'Potencial de Eutrofización - Marina', 'EP Marina', 'kg N eq.', 8),
('EP-ter', 'Potencial de Eutrofización - Terrestre', 'EP Terrestre', 'mol N eq.', 9),
('POCP', 'Potencial de Formación de Ozono Fotoquímico', 'POCP', 'kg NMVOC eq.', 10);
```

### 2. Script de Migración - Migrar Datos Existentes

**Ubicación**: `database/02_migrar_factores_existentes.sql`

**Referencia**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/database/02_migrar_datos_existentes.sql`

**Función**: Migrar factores desde diccionarios Python actuales a tablas de BD

**Proceso**:

1. Identificar diccionario actual de factores en el código (probablemente en `config/project_types.py` o similar)
2. Extraer valores actuales
3. Insertar en `tb_factores_emision` con:
   - `id_fuente` → CUSTOM_PERU (por defecto)
   - `id_categoria` → GWP-tot
   - `es_defecto` → TRUE (todos inicialmente)
   - `ubicacion` → 'PE' o 'GLOBAL'

**Ejemplo**:

```sql
-- Migrar factores existentes
INSERT INTO tb_factores_emision (
    id_subtipo_producto,
    id_fuente,
    id_categoria,
    valor_factor,
    codigo_referencia,
    es_defecto,
    ubicacion,
    notas,
    creado_por
)
VALUES
-- Caliza (ejemplo - usar valores reales del diccionario actual)
(
    (SELECT id_subtipo_producto FROM tb_subtipo_producto WHERE codigo_material = 'caliza'),
    (SELECT id_fuente FROM tb_fuentes_factores WHERE nombre_fuente = 'CUSTOM_PERU'),
    (SELECT id_categoria FROM tb_categorias_impacto WHERE codigo_categoria = 'GWP-tot'),
    0.003029,  -- Valor actual del diccionario
    NULL,
    TRUE,
    'PE',
    'Factor migrado desde diccionario Python',
    'migracion'
),
-- Arcilla
(
    (SELECT id_subtipo_producto FROM tb_subtipo_producto WHERE codigo_material = 'arcilla'),
    (SELECT id_fuente FROM tb_fuentes_factores WHERE nombre_fuente = 'CUSTOM_PERU'),
    (SELECT id_categoria FROM tb_categorias_impacto WHERE codigo_categoria = 'GWP-tot'),
    0.003300,  -- Valor actual del diccionario
    NULL,
    TRUE,
    'PE',
    'Factor migrado desde diccionario Python',
    'migracion'
)
-- ... continuar con todos los materiales del diccionario
;
```

**IMPORTANTE**: Necesitas identificar el diccionario actual en tu código base de Perú y extraer todos los valores.

### 3. Página Streamlit - Gestión de Factores

**Ubicación**: `paginas/gestion_factores_emision.py`

**Referencia completa**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/paginas/gestion_factores_emision.py`

**Características**:

- **Layout 3 columnas**:
  - Columna 1: Selector de tipo de producto (Clinker, Cemento, Concreto, Agregados)
  - Columna 2: Selector de material (caliza, arcilla, yeso, etc.)
  - Columna 3: Tabla de factores del material seleccionado

- **Funcionalidades**:
  - Ver todos los factores de un material (múltiples fuentes)
  - Identificar visualmente el factor por defecto (resaltado en verde)
  - Cambiar factor por defecto (selector + botón)
  - Agregar nuevo factor (formulario con fuente, categoría, valor, notas)
  - Editar factor existente (botón ✏️ por factor)

- **Estructura visual**:

```python
MATERIALES_POR_PRODUCTO = {
    'Clinker': {
        41: 'Caliza',
        45: 'Arcilla',
        59: 'Óxido de Hierro',
        55: 'Sílice',
        # ... adaptados a Perú
    },
    'Cemento': {
        42: 'Clinker',
        48: 'Yeso',
        47: 'Puzolana',
        # ... adaptados a Perú
    },
    'Concreto': {
        1: 'Cemento',
        4: 'Grava',
        9: 'Arena Natural',
        # ... adaptados a Perú
    }
}
```

**Funciones principales**:

```python
def cargar_factores_material(engine, schema, id_material):
    """Carga todos los factores para un material específico"""
    # Query que JOIN tb_factores_emision + tb_fuentes_factores + tb_categorias_impacto

def agregar_factor(engine, schema, datos_factor):
    """INSERT nuevo factor"""

def establecer_factor_defecto(engine, schema, id_factor, id_material):
    """
    1. UPDATE es_defecto=FALSE para material actual
    2. UPDATE es_defecto=TRUE para factor seleccionado
    """

def actualizar_factor(engine, schema, id_factor, datos_actualizacion):
    """UPDATE valores de un factor existente"""
```

### 4. Configuración de Navegación

**Archivo**: `pages.toml` o equivalente

```toml
[[pages]]
section = "HERRAMIENTAS"
path = "paginas/gestion_factores_emision.py"
name = "Factores de Emisión"
icon = "🏭"
```

---

## Impacto en Código Existente

### Compatibilidad Total Garantizada

Gracias a la vista `tb_factores_defecto`, el código existente que consulta factores **NO requiere modificación**:

**Código existente** (sigue funcionando igual):

```python
# En calculadores actuales
query = """
SELECT id_subtipo_producto, valor_factor
FROM tb_factores_defecto
WHERE codigo_material = 'caliza'
"""
```

**Ventaja**: La vista `tb_factores_defecto` internamente consulta `tb_factores_emision` filtrando por `es_defecto = TRUE`.

### Evolución Opcional (Futuro)

Una vez validado el sistema, puedes evolucionar a consultas más explícitas:

```python
# Versión mejorada (opcional, para futuro)
query = """
SELECT
    fe.valor_factor,
    ff.nombre_fuente,
    ci.codigo_categoria
FROM tb_factores_emision fe
JOIN tb_fuentes_factores ff ON fe.id_fuente = ff.id_fuente
JOIN tb_categorias_impacto ci ON fe.id_categoria = ci.id_categoria
WHERE fe.id_subtipo_producto = :id_material
  AND fe.es_defecto = TRUE
  AND ci.codigo_categoria = 'GWP-tot'
"""
```

---

## Orden de Implementación

### Fase 1: Preparación (30 min)

1. **Identificar diccionario actual**:
   ```bash
   cd /home/cpinilla/projects/latam-3c
   grep -r "FACTORES.*EMISION\|FACTORES.*DEFECTO" . --include="*.py"
   ```

2. **Extraer valores actuales**:
   - Documentar todos los materiales y sus factores
   - Identificar unidades (kg CO2/kg, kg CO2/ton, etc.)
   - Normalizar a kg CO2/kg si es necesario

3. **Verificar estructura de `tb_subtipo_producto`**:
   ```sql
   SELECT id_subtipo_producto, codigo_material, nombre_display
   FROM tb_subtipo_producto
   ORDER BY id_subtipo_producto;
   ```

### Fase 2: Creación de Estructura (15 min)

1. **Ejecutar script de creación**:
   ```bash
   psql -U <usuario> -d <database> -f database/01_crear_modelo_factores_emision.sql
   ```

2. **Verificar tablas creadas**:
   ```sql
   \d tb_factores_emision
   \d tb_fuentes_factores
   \d tb_categorias_impacto
   \dv tb_factores_defecto
   ```

3. **Verificar datos iniciales**:
   ```sql
   SELECT * FROM tb_fuentes_factores;
   SELECT * FROM tb_categorias_impacto;
   ```

### Fase 3: Migración de Datos (30 min)

1. **Adaptar script de migración**:
   - Editar `02_migrar_factores_existentes.sql`
   - Completar con todos los materiales del diccionario actual

2. **Ejecutar migración**:
   ```bash
   psql -U <usuario> -d <database> -f database/02_migrar_factores_existentes.sql
   ```

3. **Validar migración**:
   ```sql
   -- Verificar que se migraron todos los factores
   SELECT
       sp.codigo_material,
       sp.nombre_display,
       fe.valor_factor,
       ff.nombre_fuente,
       fe.es_defecto
   FROM tb_factores_emision fe
   JOIN tb_subtipo_producto sp ON fe.id_subtipo_producto = sp.id_subtipo_producto
   JOIN tb_fuentes_factores ff ON fe.id_fuente = ff.id_fuente
   WHERE fe.creado_por = 'migracion'
   ORDER BY sp.codigo_material;

   -- Verificar vista de compatibilidad
   SELECT * FROM tb_factores_defecto
   ORDER BY codigo_material;
   ```

### Fase 4: Implementación de Interfaz (45 min)

1. **Copiar y adaptar página**:
   ```bash
   cp /home/cpinilla/projects/mzma-3c/streamlit_v3/paginas/gestion_factores_emision.py \
      /home/cpinilla/projects/latam-3c/paginas/gestion_factores_emision.py
   ```

2. **Adaptar diccionario de materiales**:
   - Editar `MATERIALES_POR_PRODUCTO`
   - Usar IDs y nombres de `tb_subtipo_producto` de Perú

3. **Verificar conexión a BD**:
   - Adaptar `get_database_connection()` si es necesario
   - Probar con material de prueba

4. **Agregar a navegación** (pages.toml)

### Fase 5: Validación y Pruebas (30 min)

1. **Prueba de lectura**:
   - Abrir página "Factores de Emisión"
   - Seleccionar producto y material
   - Verificar que aparecen factores migrados
   - Verificar que hay uno marcado como "Por defecto ✓"

2. **Prueba de cambio de defecto**:
   - Agregar un segundo factor (fuente Ecoinvent, valor diferente)
   - Cambiar cuál es el factor por defecto
   - Verificar que UI actualiza correctamente
   - Verificar en BD:
     ```sql
     SELECT id_factor, valor_factor, es_defecto
     FROM tb_factores_emision
     WHERE id_subtipo_producto = <id_material_prueba>;
     ```

3. **Prueba de compatibilidad**:
   - Ejecutar calculador existente
   - Verificar que sigue obteniendo factores correctos
   - Verificar que usa el factor marcado como defecto

4. **Prueba de edición**:
   - Editar un factor existente (cambiar valor, notas)
   - Verificar UPDATE en BD
   - Verificar que UI refleja cambios

---

## Diferencias Perú vs México

| Aspecto | México (MZMA) | Perú (LATAM) |
|---------|---------------|--------------|
| Fuente custom | MZMA_CUSTOM | CUSTOM_PERU |
| Fuente local | GCCA | FICEM_ASOCEM |
| Regulación | SEMARNAT | MINEM (opcional) |
| Materiales | Específicos MX | Específicos PE |
| Unidades | kg CO2 eq. | kg CO2 eq. (mantener) |

---

## Validación Final

### SQL de Verificación

```sql
-- 1. Contar factores por material
SELECT
    sp.codigo_material,
    COUNT(*) as num_factores,
    SUM(CASE WHEN fe.es_defecto THEN 1 ELSE 0 END) as num_defectos
FROM tb_factores_emision fe
JOIN tb_subtipo_producto sp ON fe.id_subtipo_producto = sp.id_subtipo_producto
WHERE fe.activo = TRUE
GROUP BY sp.codigo_material
ORDER BY sp.codigo_material;

-- Resultado esperado: num_defectos = 1 para cada material

-- 2. Verificar que vista de compatibilidad funciona
SELECT COUNT(*) as total_factores_defecto
FROM tb_factores_defecto;

-- Resultado esperado: Igual al número de materiales migrados

-- 3. Comparar diccionario original vs BD
-- (Ejecutar manualmente comparando valores)
SELECT
    codigo_material,
    valor_factor
FROM tb_factores_defecto
ORDER BY codigo_material;
```

### Checklist de Completitud

- [ ] Tablas creadas: `tb_fuentes_factores`, `tb_categorias_impacto`, `tb_factores_emision`
- [ ] Vista creada: `tb_factores_defecto` (alias de compatibilidad)
- [ ] Fuentes insertadas: GCCA, CUSTOM_PERU, Ecoinvent, FICEM_ASOCEM
- [ ] Categorías insertadas: GWP-tot, GWP-fos, GWP-bio, etc.
- [ ] Factores migrados: Todos los materiales del diccionario original
- [ ] Cada material tiene exactamente 1 factor con `es_defecto = TRUE`
- [ ] Página Streamlit funciona correctamente
- [ ] Se puede cambiar factor por defecto
- [ ] Se puede agregar nuevo factor
- [ ] Se puede editar factor existente
- [ ] Código calculador existente sigue funcionando sin modificación
- [ ] Navegación actualizada (pages.toml)

---

## Documentación de Referencia

### Archivos del Proyecto México (para copiar/adaptar):

1. **Schema SQL**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/database/schema_factores_emision.sql`
2. **Migración SQL**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/database/02_migrar_datos_existentes.sql`
3. **Página Streamlit**: `/home/cpinilla/projects/mzma-3c/streamlit_v3/paginas/gestion_factores_emision.py`
4. **Sesión documentada**: `/home/cpinilla/projects/mzma-3c/sesion_2025-10-04.md` (sección de factores)

### Consultas de Debugging

```sql
-- Ver todos los factores de un material
SELECT
    sp.nombre_display as material,
    ff.nombre_fuente as fuente,
    ci.codigo_categoria as categoria,
    fe.valor_factor,
    fe.es_defecto,
    fe.ubicacion
FROM tb_factores_emision fe
JOIN tb_subtipo_producto sp ON fe.id_subtipo_producto = sp.id_subtipo_producto
JOIN tb_fuentes_factores ff ON fe.id_fuente = ff.id_fuente
JOIN tb_categorias_impacto ci ON fe.id_categoria = ci.id_categoria
WHERE sp.codigo_material = 'caliza';

-- Ver resumen por fuente
SELECT
    ff.nombre_fuente,
    COUNT(*) as total_factores
FROM tb_factores_emision fe
JOIN tb_fuentes_factores ff ON fe.id_fuente = ff.id_fuente
GROUP BY ff.nombre_fuente;
```

---

## Beneficios del Sistema

1. **Flexibilidad**: Múltiples fuentes sin cambiar código
2. **Trazabilidad**: Conocer origen de cada factor
3. **Versionamiento**: Histórico de cambios con auditoría
4. **Multiusuario**: Varios usuarios pueden gestionar factores
5. **Validación**: Interfaz web previene errores de formato
6. **Escalabilidad**: Agregar nuevas categorías de impacto (ODP, AP, EP, etc.)
7. **Comparabilidad**: Comparar factores de diferentes fuentes lado a lado

---

## Resultado Final Esperado

Al completar esta implementación, el sistema tendrá:

✅ **Base de datos normalizada** con factores multi-fuente y multi-categoría
✅ **Interfaz web** para gestión completa de factores
✅ **Compatibilidad total** con código existente (vista de retrocompatibilidad)
✅ **Trazabilidad** completa de fuentes y versiones
✅ **Auditoría** de cambios (quién, cuándo, qué)
✅ **Escalabilidad** para agregar nuevas fuentes/categorías
✅ **Gestión visual** del factor "por defecto" por material

---

## Comandos Rápidos

```bash
# Navegar al proyecto
cd /home/cpinilla/projects/latam-3c

# Crear directorios si no existen
mkdir -p database

# Ejecutar schemas
psql -U <user> -d <database> -f database/01_crear_modelo_factores_emision.sql
psql -U <user> -d <database> -f database/02_migrar_factores_existentes.sql

# Verificar
psql -U <user> -d <database> -c "SELECT * FROM tb_fuentes_factores;"
psql -U <user> -d <database> -c "SELECT COUNT(*) FROM tb_factores_defecto;"

# Iniciar aplicación
streamlit run app.py
```

---

## Fin del Prompt

¿Dudas? Consulta directamente los archivos de referencia en el proyecto México listados arriba. El sistema está **probado y funcionando** en producción.
