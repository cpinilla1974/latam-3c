#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración centralizada para el proceso ETL
Todas las rutas y parámetros de conexión en un solo lugar
"""

import os

# ============================================================
# RUTAS BASE
# ============================================================

# Directorio raíz de bases de datos
DATABASES_ROOT = '/home/cpinilla/databases'
PROJECTS_ROOT = '/home/cpinilla/projects'

# ============================================================
# BASES DE DATOS SQLite ORIGEN
# ============================================================

SQLITE_DATABASES = {
    # Base de PACAS (México - Cementos y Concretos del Pacífico)
    'pacas': {
        'path': '/home/cpinilla/pacas-3c/data/main.db',
        'descripcion': 'PACAS - México - 363MB',
        'tipo': 'operativa',
        'pais_default': 'MEX',
        'empresa': 'Cementos y Concretos del Pacífico',
        'tablas_principales': ['tb_planta', 'tb_producto', 'tb_dataset', 'tb_data',
                               'tb_remitos', 'tb_distancias_plantas']
    },

    # Base de MZMA (México - Moctezuma)
    # NOTA: La base correcta está en mzma-3c/data/main.db, NO en mzma_main.db (vacía)
    'mzma': {
        'path': '/home/cpinilla/databases/mzma-3c/data/main.db',
        'descripcion': 'MZMA - México - 2GB',
        'tipo': 'operativa',
        'pais_default': 'MEX',
        'empresa': 'Cementos Moctezuma',
        'tablas_principales': ['tb_planta', 'tb_dataset', 'tb_data',
                               'tb_remitos', 'tb_distancias_rutas']
    },

    # Base de Melón (Chile)
    'melon': {
        'path': '/home/cpinilla/databases/melon-3c/data/old/Melon_2.db',
        'descripcion': 'Melón - Chile - 296MB',
        'tipo': 'operativa',
        'pais_default': 'CHL',
        'empresa': 'Cementos Melón',
        'tablas_principales': ['tb_planta', 'tb_producto', 'tb_dataset', 'tb_data',
                               'tb_remitos', 'tb_distancias_rutas']
    },

    # Base de Yura (Perú)
    'yura': {
        'path': '/home/cpinilla/databases/yura-2c/data/main.db',
        'descripcion': 'Yura - Perú - 28MB',
        'tipo': 'operativa',
        'pais_default': 'PER',
        'empresa': 'Yura S.A.',
        'tablas_principales': ['tb_planta', 'tb_producto', 'tb_dataset', 'tb_data',
                               'cementos_bruto'],
        'distancias_hardcodeadas': True  # Están en código Python, no en BD
    },

    # Base FICEM (benchmark y referencia)
    'ficem': {
        'path': '/home/cpinilla/databases/ficem_bd/data/ficem_bd.db',
        'descripcion': 'FICEM - Benchmark - 170MB',
        'tipo': 'referencia',
        'tablas_principales': ['plantas_latam', 'combustibles', 'gnr_data',
                               'data_global', 'indicadores', 'cementos']
    },

    # Base de Indicadores (catálogo común)
    'indicadores': {
        'path': '/home/cpinilla/databases/comun/indicadores.db',
        'descripcion': 'Indicadores - Catálogo común',
        'tipo': 'catalogo',
        'tablas_principales': ['indicadores', 'traza_cemento']
    }
}

# ============================================================
# CONFIGURACIÓN POSTGRESQL DESTINO
# ============================================================

PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'latam4c_db',
    'user': 'postgres',
    'password': 'postgres'  # Cambiar según configuración local
}

# Alternativa: usar variable de entorno
# PG_CONFIG = {
#     'host': os.environ.get('PG_HOST', 'localhost'),
#     'port': int(os.environ.get('PG_PORT', 5432)),
#     'database': os.environ.get('PG_DATABASE', 'latam4c_db'),
#     'user': os.environ.get('PG_USER', 'postgres'),
#     'password': os.environ.get('PG_PASSWORD', 'postgres')
# }

# ============================================================
# MAPEO DE TIPOS DE PLANTA
# ============================================================

TIPOS_PLANTA = {
    1: 'cemento',
    2: 'concreto',
    3: 'agregados',
    4: 'molienda'
}

TIPOS_PRODUCTO = {
    1: 'clinker',
    2: 'cemento',
    3: 'concreto',
    4: 'agregado'
}

# ============================================================
# MAPEO DE TEMPORALIDADES
# ============================================================

TEMPORALIDADES = {
    1: 'anual',
    2: 'mensual',
    3: 'evento'
}

# ============================================================
# INDICADORES CLAVE GCCA
# ============================================================

# Indicadores de energía
INDICADORES_ENERGIA = {
    'electrico_cemento': ['33', '33a', '33b', '33c'],  # MWh
    'electrico_concreto': ['1090', '1134'],  # kWh/m3
    'termico_clinker': ['30', '32', '93'],  # MJ/t clinker
}

# Indicadores de emisiones
INDICADORES_EMISIONES = {
    'co2_bruto_clinker': '60',
    'co2_neto_clinker': '63',
    'co2_especifico_clinker': '73',
    'co2_bruto_cemento': '82',
    'co2_neto_cemento': '85'
}

# Indicadores de producción
INDICADORES_PRODUCCION = {
    'clinker_producido': '8',
    'cemento_producido': '20',
    'factor_clinker': '92a'
}

# ============================================================
# DISTANCIAS DEFAULT YURA (hardcodeadas)
# Copiadas de /home/cpinilla/projects/yura-2c/streamlit/services/const.py
# ============================================================

DISTANCIAS_DEFAULT_YURA = {
    'caliza': {
        'Peru': {'camion': 5}
    },
    'arcilla': {
        'Peru': {'camion': 5}
    },
    'oxido_hierro': {
        'Peru': {'camion': 350},
        'Turquia': {'barco': 12000, 'camion': 1000}
    },
    'silice': {
        'Peru': {'camion': 350}
    },
    'yeso': {
        'Peru': {'camion': 100}
    },
    'puzolana': {
        'Peru': {'camion': 50}
    },
    'caliza_extra': {
        'Peru': {'camion': 100}
    },
    'petcoke': {
        'Colombia': {'barco': 2800},
        'USA': {'barco': 7000}
    },
    'carbon': {
        'Colombia': {'barco': 2800}
    },
    'gas_natural': {
        'Peru': {'gasoducto': 0}
    },
    'diesel': {
        'Peru': {'camion': 100}
    },
    'aceite_residual': {
        'Peru': {'camion': 100}
    },
    'llantas': {
        'Peru': {'camion': 50}
    },
    'residuos_solidos': {
        'Peru': {'camion': 50}
    },
    'biomasa': {
        'Peru': {'camion': 100}
    },
    'clinker_importado': {
        'Korea': {'barco': 15000, 'camion': 1000},
        'Japan': {'barco': 14000, 'camion': 1000},
        'Vietnam': {'barco': 12000, 'camion': 1000}
    },
    'cemento_despachado': {
        'Peru': {'camion': 200}
    }
}

# ============================================================
# FACTORES DE EMISIÓN TRANSPORTE (kg CO2 / t.km)
# ============================================================

FACTORES_EMISION_TRANSPORTE = {
    'camion': 0.062,      # Camión pesado diesel
    'barco': 0.016,       # Transporte marítimo
    'tren': 0.022,        # Ferrocarril diesel
    'gasoducto': 0.0      # Gas natural por tubería
}

# ============================================================
# RUTAS DE ARCHIVOS DE SALIDA
# ============================================================

ETL_OUTPUT_DIR = os.path.join(
    PROJECTS_ROOT,
    'latam-3c/scripts/etl/output'
)

MAPEOS_FILE = os.path.join(ETL_OUTPUT_DIR, 'mapeos_dimension.json')
LOG_FILE = os.path.join(ETL_OUTPUT_DIR, 'etl_log.txt')

# Crear directorio si no existe
os.makedirs(ETL_OUTPUT_DIR, exist_ok=True)

# ============================================================
# VALIDACIÓN DE CONFIGURACIÓN
# ============================================================

def validar_configuracion():
    """Valida que todas las rutas de bases de datos existan."""
    errores = []

    for key, config in SQLITE_DATABASES.items():
        path = config['path']
        if not os.path.exists(path):
            errores.append(f"Base {key} no encontrada: {path}")

    if errores:
        print("ERRORES DE CONFIGURACIÓN:")
        for error in errores:
            print(f"  - {error}")
        return False

    print("Configuración validada correctamente")
    return True


if __name__ == '__main__':
    validar_configuracion()
