#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera PDF profesional del análisis de emisiones de la cadena cemento-concreto.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from datetime import datetime
import os

# Configuración
OUTPUT_DIR = '/home/cpinilla/projects/latam-3c/docs/analisis'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'informe_emisiones_cadena_ia.pdf')

# Colores corporativos
COLOR_PRIMARY = colors.HexColor('#1a5f7a')
COLOR_SECONDARY = colors.HexColor('#57c5b6')
COLOR_ACCENT = colors.HexColor('#159895')
COLOR_WARNING = colors.HexColor('#e74c3c')
COLOR_SUCCESS = colors.HexColor('#27ae60')
COLOR_LIGHT = colors.HexColor('#f0f9ff')


def create_styles():
    """Crea estilos personalizados para el documento."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='TitleMain',
        parent=styles['Title'],
        fontSize=24,
        textColor=COLOR_PRIMARY,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.grey,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    ))

    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=COLOR_PRIMARY,
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=COLOR_PRIMARY,
        borderPadding=5
    ))

    styles.add(ParagraphStyle(
        name='SubsectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=COLOR_ACCENT,
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    ))

    # Modificar BodyText existente
    styles['BodyText'].fontSize = 10
    styles['BodyText'].textColor = colors.black
    styles['BodyText'].spaceAfter = 8
    styles['BodyText'].alignment = TA_JUSTIFY
    styles['BodyText'].leading = 14

    styles.add(ParagraphStyle(
        name='Highlight',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_PRIMARY,
        backColor=COLOR_LIGHT,
        borderPadding=8,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    ))

    return styles


def create_header(styles):
    """Crea el encabezado del documento."""
    elements = []

    # Título principal
    elements.append(Paragraph(
        "Análisis de Emisiones CO2",
        styles['TitleMain']
    ))
    elements.append(Paragraph(
        "Cadena Cemento-Concreto LATAM",
        styles['TitleMain']
    ))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "Estudio Potenciado con Inteligencia Artificial",
        styles['Subtitle']
    ))

    # Línea decorativa
    elements.append(HRFlowable(
        width="80%",
        thickness=2,
        color=COLOR_SECONDARY,
        spaceAfter=20,
        spaceBefore=10
    ))

    # Información del documento
    fecha = datetime.now().strftime("%d de %B de %Y")
    info_data = [
        ['Fecha de análisis:', '3 de diciembre de 2025'],
        ['Región:', 'Latinoamérica (Perú, México, Chile)'],
        ['Bases analizadas:', 'PACAS, MZMA, MELON, YURA, FICEM'],
        ['Registros procesados:', '~450,000+ despachos de concreto']
    ]

    info_table = Table(info_data, colWidths=[2.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), COLOR_PRIMARY),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_table)

    elements.append(Spacer(1, 30))

    return elements


def create_executive_summary(styles):
    """Crea la sección de resumen ejecutivo."""
    elements = []

    elements.append(Paragraph("1. Resumen Ejecutivo", styles['SectionTitle']))

    # KPIs principales
    elements.append(Paragraph("KPIs Principales de Emisiones", styles['SubsectionTitle']))

    kpi_data = [
        ['Métrica', 'Valor LATAM', 'Benchmark Global', 'Diferencia'],
        ['CO2 clínker', '875 kg/t', '793 kg/t', '+10.3%'],
        ['Factor clínker promedio', '0.72', '0.78', '-7.7%'],
        ['Consumo térmico', '~3,500 MJ/t', '3,644 MJ/t', '-4.0%'],
        ['CO2 concreto promedio', '189 kg/m³', '~180 kg/m³', '+5.0%']
    ]

    kpi_table = Table(kpi_data, colWidths=[2.2*inch, 1.5*inch, 1.5*inch, 1.3*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(kpi_table)

    elements.append(Spacer(1, 15))

    # Hallazgos críticos
    elements.append(Paragraph("Hallazgos Críticos", styles['SubsectionTitle']))

    hallazgos = [
        "<b>PACAS (Perú):</b> Emisiones de clínker elevadas (919 kg/t) - 16% sobre benchmark",
        "<b>MZMA (México):</b> Factor clínker bajo (0.65) indica uso de cementos compuestos",
        "<b>Mejor práctica identificada:</b> Austria con 639 kg CO2/t clínker"
    ]

    for h in hallazgos:
        elements.append(Paragraph(f"• {h}", styles['BodyText']))

    elements.append(Spacer(1, 15))

    # Score de sostenibilidad
    elements.append(Paragraph("Score de Sostenibilidad LATAM", styles['SubsectionTitle']))

    score_data = [
        ['Operación', 'Score', 'Estado'],
        ['PACAS (Perú)', '40/100', 'Requiere mejora'],
        ['MZMA (México)', '60/100', 'Moderado'],
        ['YURA (Perú)', '70/100', 'Bueno'],
        ['PROMEDIO LATAM', '57/100', 'En desarrollo']
    ]

    score_table = Table(score_data, colWidths=[2*inch, 1.5*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, -1), (-1, -1), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(score_table)

    return elements


def create_cement_analysis(styles):
    """Crea la sección de análisis de cementos."""
    elements = []

    elements.append(PageBreak())
    elements.append(Paragraph("2. Análisis de Cementos y Factor Clínker", styles['SectionTitle']))

    elements.append(Paragraph("Distribución de Tipos de Cemento", styles['SubsectionTitle']))

    cement_data = [
        ['Tipo Cemento', 'Registros', 'Factor Clínker', 'CO2 Bruto (kg/t)'],
        ['Tipo I (Ordinario)', '89', '0.89-0.95', '685-790'],
        ['Tipo IP (Puzolánico)', '93', '0.64-0.75', '478-550'],
        ['Tipo HE (Alta Resistencia)', '91', '0.84', '711'],
        ['Tipo V (Sulfatos)', '11', '0.94', '648-790'],
        ['CPC 30R (México)', '12', '~0.70', '669'],
        ['CPC 40 (México)', '12', '~0.85', '855']
    ]

    cement_table = Table(cement_data, colWidths=[2.2*inch, 1.2*inch, 1.3*inch, 1.5*inch])
    cement_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT]),
    ]))
    elements.append(cement_table)

    elements.append(Spacer(1, 15))

    # Correlación
    elements.append(Paragraph("Correlación Factor Clínker vs Emisiones", styles['SubsectionTitle']))

    elements.append(Paragraph(
        "<b>Correlación encontrada: r² = 0.87 (ALTA)</b><br/>"
        "Por cada 10% de reducción en factor clínker, se reducen aproximadamente 80 kg CO2/t cemento. "
        "Esta fuerte correlación confirma que la sustitución de clínker es la estrategia más efectiva "
        "para reducir emisiones en la producción de cemento.",
        styles['BodyText']
    ))

    elements.append(Spacer(1, 15))

    # Clasificación bandas GCCA
    elements.append(Paragraph("3. Clasificación Bandas GCCA", styles['SectionTitle']))

    bandas_data = [
        ['Banda', 'Rango kg CO2/t', 'Descripción', 'Cementos LATAM'],
        ['AA', '< 100', 'Near Zero', '0'],
        ['A', '100-300', 'Muy bajo', '2 (Mortero)'],
        ['B', '300-400', 'Bajo', '3 (Fortimax MS)'],
        ['C', '400-550', 'Moderado', '4 (Extraforte, IP)'],
        ['D', '550-700', 'Estándar', '5 (IL, CPC30R, HE)'],
        ['E', '700-900', 'Alto', '8 (Tipo I, CPC40, V)'],
        ['F', '> 900', 'Muy alto', '2 (casos extremos)']
    ]

    bandas_table = Table(bandas_data, colWidths=[1*inch, 1.3*inch, 1.3*inch, 2.5*inch])
    bandas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (0, 2), COLOR_SUCCESS),
        ('BACKGROUND', (0, 3), (0, 4), colors.HexColor('#f1c40f')),
        ('BACKGROUND', (0, 5), (0, 6), colors.HexColor('#e67e22')),
        ('BACKGROUND', (0, 7), (0, 7), COLOR_WARNING),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.white),
    ]))
    elements.append(bandas_table)

    return elements


def create_concrete_analysis(styles):
    """Crea la sección de análisis de concreto."""
    elements = []

    elements.append(PageBreak())
    elements.append(Paragraph("4. Concreto: Resistencia y Dosificación", styles['SectionTitle']))

    elements.append(Paragraph("Curva Resistencia vs Emisiones CO2", styles['SubsectionTitle']))

    concrete_data = [
        ['Resistencia', 'MPa', 'Despachos', 'CO2 (kg/m³)', 'Eficiencia'],
        ['70 kg/cm²', '6.9', '48,706', '95.9', 'Óptima'],
        ['100 kg/cm²', '9.8', '1,427,127', '149.3', 'Buena'],
        ['140 kg/cm²', '13.7', '323,392', '138.4', 'Muy buena'],
        ['175 kg/cm²', '17.2', '19,127,392', '144.4', 'Buena'],
        ['210 kg/cm²', '20.6', '46,262,115', '155.1', 'Buena'],
        ['245 kg/cm²', '24.0', '971,918', '180.5', 'Moderada'],
        ['280 kg/cm²', '27.4', '47,947,591', '213.8', 'Alta demanda'],
        ['315 kg/cm²', '30.9', '212,612', '273.2', 'Moderada'],
        ['350 kg/cm²', '34.3', '3,625,241', '324.0', 'Alta'],
        ['450 kg/cm²', '44.1', '1,146', '326.7', 'Muy alta']
    ]

    concrete_table = Table(concrete_data, colWidths=[1.3*inch, 0.8*inch, 1.3*inch, 1.2*inch, 1.2*inch])
    concrete_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT]),
    ]))
    elements.append(concrete_table)

    elements.append(Spacer(1, 15))

    # Distribución de resistencias
    elements.append(Paragraph("Distribución de Resistencias Demandadas", styles['SubsectionTitle']))

    elements.append(Paragraph(
        "El <b>79.6%</b> del concreto despachado corresponde a resistencias medias (210-280 kg/cm²), "
        "indicando un mercado dominado por construcción residencial y comercial estándar. "
        "Las resistencias altas (350+ kg/cm²) representan solo el <b>3.1%</b> del volumen total.",
        styles['BodyText']
    ))

    dist_data = [
        ['Resistencia', 'Volumen (millones)', 'Participación'],
        ['280 kg/cm²', '47.9M', '40.5%'],
        ['210 kg/cm²', '46.3M', '39.1%'],
        ['175 kg/cm²', '19.1M', '16.1%'],
        ['350 kg/cm²', '3.6M', '3.1%'],
        ['Otras', '1.5M', '1.2%']
    ]

    dist_table = Table(dist_data, colWidths=[1.8*inch, 1.8*inch, 1.5*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(dist_table)

    return elements


def create_chain_analysis(styles):
    """Crea la sección de análisis de cadena de emisiones."""
    elements = []

    elements.append(PageBreak())
    elements.append(Paragraph("5. Cadena de Emisiones Completa", styles['SectionTitle']))

    elements.append(Paragraph(
        "El flujo de emisiones CO2 a través de la cadena cemento-concreto sigue una secuencia "
        "multiplicativa donde cada etapa contribuye al impacto final.",
        styles['BodyText']
    ))

    elements.append(Paragraph("Factores de Conversión por Etapa", styles['SubsectionTitle']))

    chain_data = [
        ['Etapa', 'Factor', 'Unidad', 'Impacto'],
        ['Producción clínker', '875', 'kg CO2/t clínker', 'Base'],
        ['Factor clínker', '0.72', 't clínker/t cemento', 'x 0.72'],
        ['= Emisión cemento', '630', 'kg CO2/t cemento', 'Intermedio'],
        ['Dosificación', '320', 'kg cemento/m³', 'x 0.32'],
        ['+ Agregados', '10', 'kg CO2/m³', '+ 10'],
        ['+ Transporte', '19', 'kg CO2/m³', '+ 19'],
        ['= Emisión concreto', '189', 'kg CO2/m³', 'FINAL']
    ]

    chain_table = Table(chain_data, colWidths=[1.8*inch, 1*inch, 1.8*inch, 1.2*inch])
    chain_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, -1), (-1, -1), COLOR_ACCENT),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(chain_table)

    elements.append(Spacer(1, 15))

    # Desglose
    elements.append(Paragraph("Desglose de Emisiones por Componente", styles['SubsectionTitle']))

    desglose = [
        "• <b>Cemento (A1+A3):</b> 85% del total → 160 kg/m³",
        "• <b>Agregados (A1):</b> 5% del total → 10 kg/m³",
        "• <b>Transporte (A2):</b> 10% del total → 19 kg/m³"
    ]

    for d in desglose:
        elements.append(Paragraph(d, styles['BodyText']))

    elements.append(Spacer(1, 15))

    # Puntos de optimización
    elements.append(Paragraph("Puntos de Optimización Identificados", styles['SubsectionTitle']))

    opt_data = [
        ['Punto de Intervención', 'Potencial Reducción'],
        ['1. Reducir factor clínker (cementos IP/compuestos)', '30-40%'],
        ['2. Eficiencia térmica horno (combustibles alternativos)', '15-20%'],
        ['3. Optimizar dosificación (aditivos, diseño de mezcla)', '10-15%'],
        ['4. Logística de entrega (rutas, vehículos eficientes)', '5-8%']
    ]

    opt_table = Table(opt_data, colWidths=[4*inch, 1.8*inch])
    opt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_SUCCESS),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(opt_table)

    return elements


def create_benchmarking(styles):
    """Crea la sección de benchmarking internacional."""
    elements = []

    elements.append(PageBreak())
    elements.append(Paragraph("6. Benchmarking Internacional", styles['SectionTitle']))

    elements.append(Paragraph("Comparativa CO2 Clínker por País", styles['SubsectionTitle']))

    bench_data = [
        ['País', 'CO2 kg/t Clínker', 'vs Benchmark', 'Categoría'],
        ['Austria', '639', '-20%', 'Líder'],
        ['Alemania', '701', '-11%', 'Muy bueno'],
        ['Rep. Checa', '701', '-11%', 'Muy bueno'],
        ['Francia', '774', '-2%', 'Bueno'],
        ['Polonia', '759', '-4%', 'Bueno'],
        ['BENCHMARK GCCA', '793', '0%', 'Referencia'],
        ['España', '798', '+1%', 'Promedio'],
        ['Tailandia', '807', '+2%', 'Alto'],
        ['Brasil', '826', '+4%', 'Alto'],
        ['MZMA (México)', '831', '+5%', 'Alto'],
        ['Canadá', '840', '+6%', 'Muy alto'],
        ['PACAS (Perú)', '919', '+16%', 'Crítico']
    ]

    bench_table = Table(bench_data, colWidths=[1.8*inch, 1.3*inch, 1.2*inch, 1.2*inch])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, 3), colors.HexColor('#d5f5e3')),  # Verde claro
        ('BACKGROUND', (0, 6), (-1, 6), COLOR_LIGHT),  # Benchmark
        ('BACKGROUND', (0, 10), (-1, 10), colors.HexColor('#fadbd8')),  # México
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f5b7b1')),  # PACAS
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('FONTNAME', (0, 10), (-1, 10), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(bench_table)

    elements.append(Spacer(1, 15))

    # Tendencias
    elements.append(Paragraph("Tendencias Históricas GCCA (2010-2021)", styles['SubsectionTitle']))

    elements.append(Paragraph(
        "El benchmark global ha mostrado una reducción sostenida de <b>6.4%</b> en 11 años "
        "(de 792 a 749 kg CO2/t clínker), equivalente a una tasa de <b>-0.6% anual</b>. "
        "LATAM debe acelerar su ritmo de mejora para alcanzar la paridad.",
        styles['BodyText']
    ))

    trend_data = [
        ['Año', '2010', '2014', '2018', '2021', 'Variación'],
        ['CO2 clínker (kg/t)', '799', '776', '766', '749', '-6.4%'],
        ['Factor clínker', '0.78', '0.78', '0.78', '0.78', '0%'],
        ['Cons. térmico (MJ/t)', '3,572', '3,660', '3,651', '3,671', '+2.8%']
    ]

    trend_table = Table(trend_data, colWidths=[1.5*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 1*inch])
    trend_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(trend_table)

    elements.append(Spacer(1, 15))

    # Gap
    elements.append(Paragraph("Gap vs Mejores Prácticas", styles['SubsectionTitle']))

    gap_data = [
        ['Métrica', 'Austria (Mejor)', 'LATAM Promedio', 'Gap'],
        ['CO2 clínker', '639 kg/t', '875 kg/t', '+37%'],
        ['Factor clínker', '0.68', '0.72', '+6%'],
        ['Consumo térmico', '3,400 MJ/t', '3,500 MJ/t', '+3%']
    ]

    gap_table = Table(gap_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    gap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_WARNING),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(gap_table)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<b>Potencial de reducción absoluto:</b> 236 kg CO2/t clínker (-27%)",
        styles['Highlight']
    ))

    return elements


def create_conclusions(styles):
    """Crea la sección de conclusiones y recomendaciones."""
    elements = []

    elements.append(PageBreak())
    elements.append(Paragraph("7. Conclusiones y Recomendaciones IA", styles['SectionTitle']))

    # Diagnóstico
    elements.append(Paragraph("Diagnóstico General", styles['SubsectionTitle']))

    elements.append(Paragraph(
        "<b>Estado actual: MODERADO (57/100)</b>",
        styles['Highlight']
    ))

    elements.append(Paragraph("<b>Fortalezas:</b>", styles['BodyText']))
    fortalezas = [
        "Consumo térmico competitivo (-4% vs global)",
        "Uso de cementos compuestos en México (FC: 0.65)",
        "Alta eficiencia en concretos 210-245 kg/cm²"
    ]
    for f in fortalezas:
        elements.append(Paragraph(f"✓ {f}", styles['BodyText']))

    elements.append(Paragraph("<b>Debilidades:</b>", styles['BodyText']))
    debilidades = [
        "PACAS con CO2 clínker +16% sobre benchmark",
        "Predominio de cementos Tipo I (alto clínker)",
        "Falta de cementos Near Zero (Banda AA)"
    ]
    for d in debilidades:
        elements.append(Paragraph(f"✗ {d}", styles['BodyText']))

    elements.append(Spacer(1, 15))

    # Recomendaciones
    elements.append(Paragraph("Recomendaciones Priorizadas", styles['SubsectionTitle']))

    rec_data = [
        ['Acción', 'Reducción', 'Inversión', 'Plazo'],
        ['1. Aumentar uso de cementos IP/compuestos', '80-120 kg/t', 'Baja', 'Corto'],
        ['2. Optimizar hornos PACAS', '50-80 kg/t', 'Alta', 'Mediano'],
        ['3. Combustibles alternativos', '30-50 kg/t', 'Media', 'Mediano'],
        ['4. Captura de carbono (CCUS)', '200+ kg/t', 'Muy alta', 'Largo']
    ]

    rec_table = Table(rec_data, colWidths=[2.5*inch, 1.2*inch, 1*inch, 1*inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_SUCCESS),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(rec_table)

    elements.append(Spacer(1, 15))

    # Proyección
    elements.append(Paragraph("Proyección de Mejoras (10 años)", styles['SubsectionTitle']))

    elements.append(Paragraph(
        "Siguiendo las recomendaciones propuestas, se proyecta una reducción del <b>37%</b> "
        "en emisiones de concreto para 2035, pasando de 189 a 120 kg CO2/m³. Esta meta está "
        "alineada con los compromisos del Acuerdo de París y la ruta hacia Net Zero 2050.",
        styles['BodyText']
    ))

    proj_data = [
        ['Horizonte', 'CO2 kg/m³', 'Reducción'],
        ['Actual (2025)', '189', '-'],
        ['Año 3 (2028)', '172', '-9%'],
        ['Año 5 (2030)', '155', '-18%'],
        ['Año 7 (2032)', '140', '-26%'],
        ['Año 10 (2035)', '120', '-37%']
    ]

    proj_table = Table(proj_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch])
    proj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, -1), (-1, -1), COLOR_SUCCESS),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(proj_table)

    return elements


def create_footer(canvas, doc):
    """Añade pie de página a cada página."""
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)

    # Número de página
    page_num = canvas.getPageNumber()
    text = f"Página {page_num} | Análisis de Emisiones CO2 - LATAM 3C | Generado: {datetime.now().strftime('%Y-%m-%d')}"
    canvas.drawCentredString(letter[0]/2, 0.5*inch, text)

    canvas.restoreState()


def generate_pdf():
    """Genera el PDF completo."""
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = create_styles()
    elements = []

    # Construir documento
    elements.extend(create_header(styles))
    elements.extend(create_executive_summary(styles))
    elements.extend(create_cement_analysis(styles))
    elements.extend(create_concrete_analysis(styles))
    elements.extend(create_chain_analysis(styles))
    elements.extend(create_benchmarking(styles))
    elements.extend(create_conclusions(styles))

    # Nota final
    elements.append(Spacer(1, 30))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<i>Análisis generado mediante técnicas de minería de datos, correlación estadística y modelado predictivo. "
        "Los valores representan promedios ponderados de las bases de datos analizadas.</i>",
        styles['Footer']
    ))

    # Generar PDF
    doc.build(elements, onFirstPage=create_footer, onLaterPages=create_footer)

    return OUTPUT_FILE


if __name__ == '__main__':
    print("Generando PDF de análisis de emisiones...")
    output = generate_pdf()
    print(f"✅ PDF generado: {output}")

    # Mostrar tamaño
    import os
    size = os.path.getsize(output) / 1024
    print(f"   Tamaño: {size:.1f} KB")
