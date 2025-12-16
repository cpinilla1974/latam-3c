#!/usr/bin/env python3
"""
Calcula agregados nacionales según FORMULAS_AGREGACION.md (fuente de verdad).

Proceso:
1. Limpiar tabla agregados_nacionales
2. Insertar campos sumables desde datos_plantas
3. Calcular indicadores según fórmulas oficiales FICEM

Referencia: data_peru/docs/FORMULAS_AGREGACION.md
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "peru_consolidado.db"

# =============================================================================
# AÑOS VÁLIDOS PARA AGREGACIÓN NACIONAL
# Solo años con cobertura completa de plantas
# =============================================================================
# 2010, 2014: 5 plantas (Piura no existía)
# 2019, 2020, 2021, 2024: 6 plantas (completo)
# Años excluidos por datos incompletos: 2015, 2016, 2017, 2018, 2022, 2023
AÑOS_VALIDOS = [2010, 2014, 2019, 2020, 2021, 2024]

# =============================================================================
# CAMPOS SUMABLES (se agregan directamente desde datos_plantas)
# =============================================================================
CAMPOS_SUMABLES = [
    # Producción
    '8',      # Clínker producido
    '9',      # Clínker comprado
    '10',     # Clínker vendido
    '10a',    # Cambio en stock clínker
    '10b',    # Transferencia interna clínker
    '11',     # Clínker consumido
    '20',     # Cemento producido
    '21a',    # Producto cementitious
    '21b',    # Cemento equivalente (calculado por planta como [8]/[92a])
    # Energía
    '25',     # Consumo térmico total hornos
    '27',     # Energía fósiles alternativos
    '28',     # Energía biomasa
    '33',     # Consumo eléctrico total
    '33a',    # Consumo eléctrico autogenerado
    '33aa',   # Consumo eléctrico autogenerado usado
    '33c',    # Consumo eléctrico externo
    '33e',    # Consumo eléctrico hasta clínker
    # Emisiones absolutas
    '39',     # Emisiones CO₂ descarbonatación
    '40',     # Emisiones CO₂ fósiles convencionales
    '41',     # Emisiones CO₂ fósiles alternativos
    '43',     # Emisiones CO₂ combustibles fósiles hornos
    '44',     # Emisiones CO₂ equipos on-site
    '45a',    # Emisiones CO₂ vehículos on-site
    '45b',    # Emisiones CO₂ otros fuera horno
    '45c',    # Emisiones CO₂ generación eléctrica on-site
    '49a',    # Emisiones CO₂ electricidad externa
    '50',     # Emisiones CO₂ biomasa
    '59a',    # Emisiones netas materias primas
    '225',    # Emisiones CO₂ biomasa hornos
]


def limpiar_agregados(conn):
    """Paso 1: Limpiar tabla agregados_nacionales."""
    print("Paso 1: Limpiando tabla agregados_nacionales...")
    conn.execute("DELETE FROM agregados_nacionales")
    conn.commit()
    print("   Tabla limpiada.")


def insertar_sumables(conn):
    """Paso 2: Insertar campos sumables agrupados por año."""
    print("\nPaso 2: Insertando campos sumables...")
    print(f"   Años válidos para agregación: {AÑOS_VALIDOS}")

    # Solo usar años con cobertura completa de plantas
    años = AÑOS_VALIDOS

    registros = 0
    for campo in CAMPOS_SUMABLES:
        for año in años:
            # Sumar valores de todas las plantas para este campo y año
            result = conn.execute("""
                SELECT SUM(valor) as total, COUNT(DISTINCT id_planta) as num_plantas
                FROM datos_plantas
                WHERE codigo_indicador = ? AND año = ? AND valor IS NOT NULL
            """, (campo, año)).fetchone()

            total, num_plantas = result
            if total is not None and num_plantas > 0:
                conn.execute("""
                    INSERT INTO agregados_nacionales
                    (codigo_indicador, año, valor_nacional, tipo_agregacion, num_empresas)
                    VALUES (?, ?, ?, 'suma', ?)
                """, (campo, año, total, num_plantas))
                registros += 1

    conn.commit()
    print(f"   {registros} registros sumables insertados.")
    return registros


def obtener_suma(conn, campo, año):
    """Obtiene la suma de un campo para un año."""
    result = conn.execute("""
        SELECT valor_nacional FROM agregados_nacionales
        WHERE codigo_indicador = ? AND año = ?
    """, (campo, año)).fetchone()
    return result[0] if result else None


def obtener_datos_planta(conn, año):
    """Obtiene todos los datos de plantas para un año."""
    return pd.read_sql_query("""
        SELECT id_planta, codigo_indicador, valor
        FROM datos_plantas
        WHERE año = ? AND valor IS NOT NULL
    """, conn, params=(año,))


def calcular_indicadores(conn):
    """Paso 3: Calcular indicadores según FORMULAS_AGREGACION.md."""
    print("\nPaso 3: Calculando indicadores...")

    años = pd.read_sql_query(
        "SELECT DISTINCT año FROM agregados_nacionales ORDER BY año",
        conn
    )['año'].tolist()

    registros = 0

    for año in años:
        # Cargar sumas para este año
        s = {}
        for campo in CAMPOS_SUMABLES:
            s[campo] = obtener_suma(conn, campo, año)

        # Cargar datos por planta para cálculos complejos
        df_plantas = obtener_datos_planta(conn, año)

        indicadores = []

        # --- Eficiencia y Sustitución ---

        # 33d: Factor emisión red eléctrica = Σ[49a] / Σ[33c]
        if s.get('49a') and s.get('33c') and s['33c'] != 0:
            indicadores.append(('33d', s['49a'] / s['33c'], 'promedio_ponderado', '33c'))

        # 92a: Factor clínker = Σ[11] / Σ[20]
        if s.get('11') and s.get('20') and s['20'] != 0:
            indicadores.append(('92a', s['11'] / s['20'], 'ratio', '20'))

        # 93: Consumo térmico = (Σ[25] / Σ[8]) × 1000000
        if s.get('25') and s.get('8') and s['8'] != 0:
            indicadores.append(('93', (s['25'] / s['8']) * 1000000, 'promedio_ponderado', '8'))

        # 95: Fósiles alternativos % = (Σ[27] / Σ[25]) × 100
        if s.get('27') and s.get('25') and s['25'] != 0:
            indicadores.append(('95', (s['27'] / s['25']) * 100, 'ratio_porcentaje', '25'))

        # 96: Biomasa % = (Σ[28] / Σ[25]) × 100
        if s.get('28') and s.get('25') and s['25'] != 0:
            indicadores.append(('96', (s['28'] / s['25']) * 100, 'ratio_porcentaje', '25'))

        # 96a: Factor emisión combustibles = (Σ[43] / Σ[25]) × 1000
        if s.get('43') and s.get('25') and s['25'] != 0:
            indicadores.append(('96a', (s['43'] / s['25']) * 1000, 'promedio_ponderado', '25'))

        # 97: Consumo eléctrico específico = (Σ[33] / Σ[20]) × 1000
        if s.get('33') and s.get('20') and s['20'] != 0:
            indicadores.append(('97', (s['33'] / s['20']) * 1000, 'promedio_ponderado', '20'))

        # coprocesamiento = (Σ[27] + Σ[28]) / Σ[25]
        if s.get('27') is not None and s.get('28') is not None and s.get('25') and s['25'] != 0:
            indicadores.append(('coprocesamiento', (s['27'] + s['28']) / s['25'], 'ratio', '25'))

        # --- Emisiones Específicas - Clínker ---

        # 60a: Descarbonatación = (Σ[39] / Σ[8]) × 1000
        if s.get('39') and s.get('8') and s['8'] != 0:
            indicadores.append(('60a', (s['39'] / s['8']) * 1000, 'promedio_ponderado', '8'))

        # 1008: Fósiles convencionales = (Σ[40] / Σ[8]) × 1000
        if s.get('40') and s.get('8') and s['8'] != 0:
            indicadores.append(('1008', (s['40'] / s['8']) * 1000, 'promedio_ponderado', '8'))

        # 1009: Fósiles alternativos = (Σ[41] / Σ[8]) × 1000
        if s.get('41') and s.get('8') and s['8'] != 0:
            indicadores.append(('1009', (s['41'] / s['8']) * 1000, 'promedio_ponderado', '8'))

        # 1010: Fuera de horno = (Σ[44] + Σ[45a] + Σ[45b]) / Σ[8] × 1000
        if s.get('8') and s['8'] != 0:
            fuera_horno = (s.get('44') or 0) + (s.get('45a') or 0) + (s.get('45b') or 0)
            if fuera_horno > 0:
                indicadores.append(('1010', (fuera_horno / s['8']) * 1000, 'promedio_ponderado', '8'))

        # 1011: Biomasa = (Σ[225] / Σ[8]) × 1000
        if s.get('225') and s.get('8') and s['8'] != 0:
            indicadores.append(('1011', (s['225'] / s['8']) * 1000, 'promedio_ponderado', '8'))

        # 1012 y 1088: Requieren cálculos a nivel planta (más complejos)
        # Se implementan con datos por planta
        if len(df_plantas) > 0:
            val_1012 = calcular_1012(df_plantas, s)
            if val_1012 is not None:
                indicadores.append(('1012', val_1012, 'formula_compleja', '8'))

            val_1088 = calcular_1088(df_plantas, s)
            if val_1088 is not None:
                indicadores.append(('1088', val_1088, 'formula_compleja', '8'))

        # 60 y 73 se calculan después de tener los componentes (ver abajo)

        # --- Emisiones Específicas - Cementitious ---

        # 62a: Descarbonatación = (Σ[59a] / Σ[21a]) × 1000
        if s.get('59a') and s.get('21a') and s['21a'] != 0:
            indicadores.append(('62a', (s['59a'] / s['21a']) * 1000, 'promedio_ponderado', '21a'))

        # 82a: Electricidad externa = (Σ[49a] / Σ[21a]) × 1000
        if s.get('49a') and s.get('21a') and s['21a'] != 0:
            indicadores.append(('82a', (s['49a'] / s['21a']) * 1000, 'promedio_ponderado', '21a'))

        # 1020: Generación on-site (requiere datos planta)
        if len(df_plantas) > 0:
            val_1020 = calcular_1020(df_plantas, s, '21a')
            if val_1020 is not None:
                indicadores.append(('1020', val_1020, 'formula_compleja', '21a'))

        # 1021: Fuera de horno = (Σ[44] + Σ[45a] + Σ[45b]) / Σ[21a] × 1000
        if s.get('21a') and s['21a'] != 0:
            fuera_horno = (s.get('44') or 0) + (s.get('45a') or 0) + (s.get('45b') or 0)
            if fuera_horno > 0:
                indicadores.append(('1021', (fuera_horno / s['21a']) * 1000, 'promedio_ponderado', '21a'))

        # 1022: Fósiles convencionales = (Σ[40] / Σ[21a]) × 1000
        if s.get('40') and s.get('21a') and s['21a'] != 0:
            indicadores.append(('1022', (s['40'] / s['21a']) * 1000, 'promedio_ponderado', '21a'))

        # 1023: Fósiles alternativos = (Σ[41] / Σ[21a]) × 1000
        if s.get('41') and s.get('21a') and s['21a'] != 0:
            indicadores.append(('1023', (s['41'] / s['21a']) * 1000, 'promedio_ponderado', '21a'))

        # 1024: Biomasa = (Σ[50] / Σ[21a]) × 1000
        if s.get('50') and s.get('21a') and s['21a'] != 0:
            indicadores.append(('1024', (s['50'] / s['21a']) * 1000, 'promedio_ponderado', '21a'))

        # 62 y 74 se calculan después de tener los componentes (ver abajo)

        # --- Emisiones Específicas - Cemento ---
        # Nota: Fórmulas condicionales según [8] >= [11]

        # 1001: Descarbonatación cemento
        if s.get('39') and s.get('20') and s['20'] != 0:
            if s.get('8') and s.get('11') and s['8'] >= s['11']:
                # Usar proporción: Σ([39]×[11]/[8]) / Σ[20] × 1000
                val = calcular_proporcional(df_plantas, '39', '11', '8', s['20'])
            else:
                val = (s['39'] / s['20']) * 1000
            if val is not None:
                indicadores.append(('1001', val, 'formula_condicional', '20'))

        # 1002: Fuera de horno cemento = (Σ[44] + Σ[45a] + Σ[45b]) / Σ[20] × 1000
        if s.get('20') and s['20'] != 0:
            fuera_horno = (s.get('44') or 0) + (s.get('45a') or 0) + (s.get('45b') or 0)
            if fuera_horno > 0:
                indicadores.append(('1002', (fuera_horno / s['20']) * 1000, 'promedio_ponderado', '20'))

        # 1003: Fósiles convencionales cemento
        if s.get('40') and s.get('20') and s['20'] != 0:
            if s.get('8') and s.get('11') and s['8'] >= s['11']:
                val = calcular_proporcional(df_plantas, '40', '11', '8', s['20'])
            else:
                val = (s['40'] / s['20']) * 1000
            if val is not None:
                indicadores.append(('1003', val, 'formula_condicional', '20'))

        # 1004: Fósiles alternativos cemento
        if s.get('41') and s.get('20') and s['20'] != 0:
            if s.get('8') and s.get('11') and s['8'] >= s['11']:
                val = calcular_proporcional(df_plantas, '41', '11', '8', s['20'])
            else:
                val = (s['41'] / s['20']) * 1000
            if val is not None:
                indicadores.append(('1004', val, 'formula_condicional', '20'))

        # 1006: Clínker externo = 865 × Σ(([11]-[8])/[20])
        if s.get('11') and s.get('8') and s.get('20') and s['20'] != 0:
            val_1006 = 865 * ((s['11'] - s['8']) / s['20'])
            indicadores.append(('1006', val_1006, 'formula', '20'))

        # 1025: Generación on-site cemento
        if len(df_plantas) > 0:
            val_1025 = calcular_1020(df_plantas, s, '20')  # Misma fórmula, diferente denominador
            if val_1025 is not None:
                indicadores.append(('1025', val_1025, 'formula_compleja', '20'))

        # 1005: Electricidad externa cemento (fórmula compleja)
        if len(df_plantas) > 0:
            val_1005 = calcular_1005(df_plantas, s)
            if val_1005 is not None:
                indicadores.append(('1005', val_1005, 'formula_compleja', '20'))

        # 1043: Específica biomasa cemento
        # Fórmula similar a descarbonatación: ajustada por [11]/[8] si [8]>=[11]
        if s.get('50') and s.get('20') and s['20'] != 0:
            if s.get('8') and s.get('11') and s['8'] >= s['11']:
                val = calcular_proporcional(df_plantas, '50', '11', '8', s['20'])
            else:
                val = (s['50'] / s['20']) * 1000
            if val is not None:
                indicadores.append(('1043', val, 'formula_condicional', '20'))

        # 1044 y 1045 se calculan después de tener los componentes (ver abajo)

        # --- Emisiones Específicas - Cemento Equivalente ---
        # Códigos según BD común: 21b, 63a, 82c, 1410, 1411, 1412, 1416, 1417, 63, 75
        # Cemento equivalente [21b] = [8] / [92a] por planta, luego se suma
        # Fuente: Hoja 'Comments' del protocolo GNR (row 67)

        # 21b: Cemento equivalente - usar suma de plantas si existe (ya cargado en paso 2)
        cem_eq = s.get('21b')  # Suma de 21b por planta

        # Si no hay 21b por planta, calcular a nivel nacional
        if cem_eq is None or cem_eq == 0:
            if s.get('8') and s.get('11') and s.get('20') and s['11'] != 0:
                cem_eq = s['8'] * s['20'] / s['11']
                indicadores.append(('21b', cem_eq, 'formula', '8'))

        if cem_eq and cem_eq > 0:
            # 63a: Descarbonatación por cemento equivalente (Calcination)
            if s.get('59a'):
                indicadores.append(('63a', (s['59a'] / cem_eq) * 1000, 'promedio_ponderado', 'cem_eq'))

            # 63 y 75 se calculan después de tener los componentes (ver abajo)

            # 82c: Electricidad externa (cem. eq.) = (Σ[49a] / Σ[cem_eq]) × 1000
            if s.get('49a'):
                indicadores.append(('82c', (s['49a'] / cem_eq) * 1000, 'promedio_ponderado', 'cem_eq'))

            # 1410: Fósiles convencionales (cem. eq.) = (Σ[40] / Σ[cem_eq]) × 1000
            if s.get('40'):
                indicadores.append(('1410', (s['40'] / cem_eq) * 1000, 'promedio_ponderado', 'cem_eq'))

            # 1411: Fósiles alternativos (cem. eq.) = (Σ[41] / Σ[cem_eq]) × 1000
            if s.get('41'):
                indicadores.append(('1411', (s['41'] / cem_eq) * 1000, 'promedio_ponderado', 'cem_eq'))

            # 1412: Biomasa (cem. eq.) = (Σ[50] / Σ[cem_eq]) × 1000
            if s.get('50'):
                indicadores.append(('1412', (s['50'] / cem_eq) * 1000, 'promedio_ponderado', 'cem_eq'))

            # 1416: Fuera de horno (cem. eq.) = (Σ[44] + Σ[45a] + Σ[45b]) / Σ[cem_eq] × 1000
            fuera_horno_eq = (s.get('44') or 0) + (s.get('45a') or 0) + (s.get('45b') or 0)
            if fuera_horno_eq > 0:
                indicadores.append(('1416', (fuera_horno_eq / cem_eq) * 1000, 'promedio_ponderado', 'cem_eq'))

            # 1417: Generación on-site (cem. eq.)
            if len(df_plantas) > 0:
                val_1417 = calcular_1020(df_plantas, s, None, cem_eq)
                if val_1417 is not None:
                    indicadores.append(('1417', val_1417, 'formula_compleja', 'cem_eq'))

        # --- Calcular brutas y netas como suma de componentes ---
        # Crear diccionario para acceso rápido a indicadores calculados
        ind_dict = {codigo: valor for codigo, valor, _, _ in indicadores}

        # 60: Específica bruta clínker = 60a + 1010 + 1008 + 1009
        val_60a = ind_dict.get('60a', 0)
        val_1010 = ind_dict.get('1010', 0)
        val_1008 = ind_dict.get('1008', 0)
        val_1009 = ind_dict.get('1009', 0)
        if any([val_60a, val_1010, val_1008, val_1009]):
            indicadores.append(('60', val_60a + val_1010 + val_1008 + val_1009, 'suma_componentes', '8'))
            # 73: Específica neta clínker = 60a + 1010 + 1008
            indicadores.append(('73', val_60a + val_1010 + val_1008, 'suma_componentes', '8'))

        # 62: Específica bruta cementitious = 62a + 1021 + 1022 + 1023
        val_62a = ind_dict.get('62a', 0)
        val_1021 = ind_dict.get('1021', 0)
        val_1022 = ind_dict.get('1022', 0)
        val_1023 = ind_dict.get('1023', 0)
        if any([val_62a, val_1021, val_1022, val_1023]):
            indicadores.append(('62', val_62a + val_1021 + val_1022 + val_1023, 'suma_componentes', '21a'))
            # 74: Específica neta cementitious = 62a + 1021 + 1022
            indicadores.append(('74', val_62a + val_1021 + val_1022, 'suma_componentes', '21a'))

        # 1044: Intensidad bruta cemento = 1001 + 1002 + 1003 + 1004
        val_1001 = ind_dict.get('1001', 0)
        val_1002 = ind_dict.get('1002', 0)
        val_1003 = ind_dict.get('1003', 0)
        val_1004 = ind_dict.get('1004', 0)
        if any([val_1001, val_1002, val_1003, val_1004]):
            indicadores.append(('1044', val_1001 + val_1002 + val_1003 + val_1004, 'suma_componentes', '20'))
            # 1045: Intensidad neta cemento = 1001 + 1002 + 1003
            indicadores.append(('1045', val_1001 + val_1002 + val_1003, 'suma_componentes', '20'))

        # 63: Específica bruta cem. eq. = 63a + 1416 + 1410 + 1411
        val_63a = ind_dict.get('63a', 0)
        val_1416 = ind_dict.get('1416', 0)
        val_1410 = ind_dict.get('1410', 0)
        val_1411 = ind_dict.get('1411', 0)
        if any([val_63a, val_1416, val_1410, val_1411]):
            indicadores.append(('63', val_63a + val_1416 + val_1410 + val_1411, 'suma_componentes', 'cem_eq'))
            # 75: Específica neta cem. eq. = 63a + 1416 + 1410
            indicadores.append(('75', val_63a + val_1416 + val_1410, 'suma_componentes', 'cem_eq'))

        # Insertar indicadores calculados
        for codigo, valor, tipo, ponderador in indicadores:
            conn.execute("""
                INSERT OR REPLACE INTO agregados_nacionales
                (codigo_indicador, año, valor_nacional, tipo_agregacion, ponderador, num_empresas)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (codigo, año, valor, tipo, ponderador, 3))  # Asumimos 3 empresas
            registros += 1

    conn.commit()
    print(f"   {registros} indicadores calculados.")
    return registros


def calcular_1012(df_plantas, sumas):
    """Calcula 1012: Electricidad externa clínker.
    Fórmula: Σ([33d] × [33c] × [33e]/[33]) / Σ[8]
    """
    if not sumas.get('8') or sumas['8'] == 0:
        return None

    # Pivotar para tener campos por planta
    pivot = df_plantas.pivot(index='id_planta', columns='codigo_indicador', values='valor')

    campos_req = ['33d', '33c', '33e', '33']
    if not all(c in pivot.columns for c in campos_req):
        return None

    # Calcular numerador por planta
    pivot = pivot.dropna(subset=campos_req)
    if len(pivot) == 0:
        return None

    pivot['numerador'] = pivot['33d'] * pivot['33c'] * (pivot['33e'] / pivot['33'])
    numerador_total = pivot['numerador'].sum()

    return numerador_total / sumas['8']


def calcular_1088(df_plantas, sumas):
    """Calcula 1088: Generación eléctrica on-site clínker.
    Fórmula: Σ([45c] × [33aa]/[33a] × [33e]/[33]) / Σ[8] × 1000
    """
    if not sumas.get('8') or sumas['8'] == 0:
        return None

    pivot = df_plantas.pivot(index='id_planta', columns='codigo_indicador', values='valor')

    campos_req = ['45c', '33aa', '33a', '33e', '33']
    if not all(c in pivot.columns for c in campos_req):
        return None

    pivot = pivot.dropna(subset=campos_req)
    if len(pivot) == 0:
        return None

    # Evitar división por cero
    pivot = pivot[(pivot['33a'] != 0) & (pivot['33'] != 0)]
    if len(pivot) == 0:
        return None

    pivot['numerador'] = pivot['45c'] * (pivot['33aa'] / pivot['33a']) * (pivot['33e'] / pivot['33'])
    numerador_total = pivot['numerador'].sum()

    return (numerador_total / sumas['8']) * 1000


def calcular_1020(df_plantas, sumas, denominador_campo=None, denominador_valor=None):
    """Calcula 1020/1025/1020_eq: Generación eléctrica on-site.
    Fórmula: Σ([33aa]/[33a] × [45c]) / Σ[denominador] × 1000
    """
    if denominador_valor is None:
        if not denominador_campo or not sumas.get(denominador_campo):
            return None
        denominador_valor = sumas[denominador_campo]

    if denominador_valor == 0:
        return None

    pivot = df_plantas.pivot(index='id_planta', columns='codigo_indicador', values='valor')

    campos_req = ['33aa', '33a', '45c']
    if not all(c in pivot.columns for c in campos_req):
        return None

    pivot = pivot.dropna(subset=campos_req)
    if len(pivot) == 0:
        return None

    pivot = pivot[pivot['33a'] != 0]
    if len(pivot) == 0:
        return None

    pivot['numerador'] = (pivot['33aa'] / pivot['33a']) * pivot['45c']
    numerador_total = pivot['numerador'].sum()

    return (numerador_total / denominador_valor) * 1000


def calcular_1005(df_plantas, sumas):
    """Calcula 1005: Electricidad externa cemento.
    Fórmula compleja según Anexo V1.4 FICEM:
    - Plantas integradas: Aᵢ = [33d]ᵢ × [33c]ᵢ/[33]ᵢ × ([33e]ᵢ × [11]ᵢ/[8]ᵢ + [33]ᵢ - [33e]ᵢ)
    - Moliendas: Aᵢ = [33d]ᵢ × [33c]ᵢ
    Resultado: Σ(Aᵢ) / Σ[20]ᵢ
    """
    if not sumas.get('20') or sumas['20'] == 0:
        return None

    pivot = df_plantas.pivot(index='id_planta', columns='codigo_indicador', values='valor')

    # Campos mínimos necesarios
    if '33d' not in pivot.columns or '33c' not in pivot.columns:
        return None

    numerador_total = 0

    for planta in pivot.index:
        row = pivot.loc[planta]
        val_33d = row.get('33d')
        val_33c = row.get('33c')

        if pd.isna(val_33d) or pd.isna(val_33c):
            continue

        # Determinar si es planta integrada (tiene [8] clínker producido)
        val_8 = row.get('8')
        val_11 = row.get('11')
        val_33 = row.get('33')
        val_33e = row.get('33e')

        if pd.notna(val_8) and val_8 > 0 and pd.notna(val_33) and val_33 > 0:
            # Planta integrada
            if pd.notna(val_33e) and pd.notna(val_11):
                # Fórmula completa para integrada
                A_i = val_33d * (val_33c / val_33) * (val_33e * val_11 / val_8 + val_33 - val_33e)
            else:
                # Si faltan datos, usar aproximación
                A_i = val_33d * val_33c
        else:
            # Molienda
            A_i = val_33d * val_33c

        numerador_total += A_i

    if numerador_total == 0:
        return None

    return numerador_total / sumas['20']


def calcular_proporcional(df_plantas, campo_emision, campo_11, campo_8, denominador):
    """Calcula emisión proporcional según FICEM V1.4:
    - Si [8] >= [11] en planta: usar [emision] × [11]/[8]
    - Si [8] < [11] en planta: usar [emision] directamente (sin factor)
    """
    if denominador == 0:
        return None

    pivot = df_plantas.pivot(index='id_planta', columns='codigo_indicador', values='valor')

    if not all(c in pivot.columns for c in [campo_emision, campo_11, campo_8]):
        return None

    pivot = pivot.dropna(subset=[campo_emision, campo_11, campo_8])
    if len(pivot) == 0:
        return None

    pivot = pivot[pivot[campo_8] != 0]
    if len(pivot) == 0:
        return None

    # Aplicar condición FICEM por planta
    numerador_total = 0
    for idx, row in pivot.iterrows():
        v8 = row[campo_8]
        v11 = row[campo_11]
        v_emision = row[campo_emision]

        if v8 >= v11:
            # Planta produce más clínker del que consume: aplicar factor
            numerador_total += v_emision * (v11 / v8)
        else:
            # Planta consume más clínker del que produce: usar emisión directa
            numerador_total += v_emision

    return (numerador_total / denominador) * 1000


def generar_reporte(conn):
    """Genera reporte de los agregados calculados."""
    print("\n" + "=" * 60)
    print("REPORTE DE AGREGADOS NACIONALES")
    print("=" * 60)

    # Contar por tipo
    result = conn.execute("""
        SELECT tipo_agregacion, COUNT(*) as n
        FROM agregados_nacionales
        GROUP BY tipo_agregacion
    """).fetchall()

    print("\nPor tipo de agregación:")
    for tipo, n in result:
        print(f"   {tipo}: {n}")

    # Contar por año
    result = conn.execute("""
        SELECT año, COUNT(*) as n
        FROM agregados_nacionales
        GROUP BY año
        ORDER BY año
    """).fetchall()

    print("\nPor año:")
    for año, n in result:
        print(f"   {año}: {n} indicadores")

    # Total
    total = conn.execute("SELECT COUNT(*) FROM agregados_nacionales").fetchone()[0]
    print(f"\nTotal: {total} registros")


def exportar_csv(conn):
    """Exporta agregados a CSV."""
    output_path = Path(__file__).parent.parent / "datos_procesados" / "agregados_nacionales.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_sql_query("SELECT * FROM agregados_nacionales ORDER BY año, codigo_indicador", conn)
    df.to_csv(output_path, index=False)
    print(f"\nExportado a: {output_path}")


def main():
    print("=" * 60)
    print("CÁLCULO DE AGREGADOS NACIONALES")
    print("Fuente: FORMULAS_AGREGACION.md")
    print("=" * 60)

    if not DB_PATH.exists():
        print(f"Error: Base de datos no encontrada: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)

    try:
        limpiar_agregados(conn)
        insertar_sumables(conn)
        calcular_indicadores(conn)
        generar_reporte(conn)
        exportar_csv(conn)
        print("\nProceso completado.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


if __name__ == "__main__":
    main()