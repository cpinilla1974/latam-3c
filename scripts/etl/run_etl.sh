#!/bin/bash
# ============================================================
# Script de ejecución completa del ETL
# Consolida datos de 5 bases SQLite a PostgreSQL
# ============================================================

set -e  # Detener en caso de error

echo "============================================================"
echo "ETL: Consolidación de Datos LATAM 3C"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"

# Directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Variables de entorno PostgreSQL (ajustar según configuración)
export PGHOST="${PGHOST:-localhost}"
export PGPORT="${PGPORT:-5432}"
export PGDATABASE="${PGDATABASE:-latam4c_db}"
export PGUSER="${PGUSER:-postgres}"
export PGPASSWORD="${PGPASSWORD:-postgres}"

echo ""
echo "Configuración PostgreSQL:"
echo "  Host: $PGHOST"
echo "  Port: $PGPORT"
echo "  Database: $PGDATABASE"
echo "  User: $PGUSER"
echo ""

# Verificar conexión PostgreSQL
echo "Verificando conexión PostgreSQL..."
if ! psql -c "SELECT 1" > /dev/null 2>&1; then
    echo "ERROR: No se puede conectar a PostgreSQL"
    echo "Verifique las credenciales y que el servidor esté activo"
    exit 1
fi
echo "✓ Conexión establecida"
echo ""

# Paso 1: Crear esquema
echo "============================================================"
echo "Paso 1: Creando esquema PostgreSQL..."
echo "============================================================"
psql -f 01_crear_esquema.sql
echo "✓ Esquema creado"
echo ""

# Paso 2: Migrar dimensiones
echo "============================================================"
echo "Paso 2: Migrando dimensiones..."
echo "============================================================"
python3 02_migrar_dimensiones.py
echo ""

# Paso 3: Migrar indicadores
echo "============================================================"
echo "Paso 3: Migrando indicadores..."
echo "============================================================"
python3 03_migrar_indicadores.py
echo ""

# Paso 4: Migrar distancias
echo "============================================================"
echo "Paso 4: Migrando distancias..."
echo "============================================================"
python3 04_migrar_distancias.py
echo ""

# Paso 5: Crear vistas materializadas
echo "============================================================"
echo "Paso 5: Creando vistas materializadas..."
echo "============================================================"
psql -f 05_crear_vistas.sql
echo "✓ Vistas creadas"
echo ""

# Paso 6: Validar datos
echo "============================================================"
echo "Paso 6: Validando datos..."
echo "============================================================"
python3 06_validar_datos.py
echo ""

echo "============================================================"
echo "ETL COMPLETADO EXITOSAMENTE"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""
echo "Archivos generados:"
echo "  - output/mapeos_dimension.json"
echo "  - output/validacion_resultado.json"
echo ""
echo "Para refrescar las vistas materializadas:"
echo "  psql -c \"SELECT refrescar_vistas_materializadas();\""
echo ""
