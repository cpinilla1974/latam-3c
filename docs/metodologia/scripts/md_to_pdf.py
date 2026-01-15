#!/usr/bin/env python3
"""
Script para convertir archivos Markdown a PDF usando markdown2 y reportlab.
Uso: python md_to_pdf.py <archivo.md>
"""

import sys
import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from bs4 import BeautifulSoup
import re

def md_to_pdf(md_file, output_pdf=None):
    """Convierte archivo Markdown a PDF."""

    if output_pdf is None:
        output_pdf = md_file.replace('.md', '.pdf')

    # Leer archivo markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convertir markdown a HTML
    html = markdown.markdown(md_content, extensions=['extra', 'nl2br'])

    # Parsear HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Crear PDF
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=2.5*inch/2.54*10,  # 2.5cm
        leftMargin=2.5*inch/2.54*10,
        topMargin=2.5*inch/2.54*10,
        bottomMargin=2.5*inch/2.54*10
    )

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo personalizado para título principal
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor='#1a1a1a',
        spaceAfter=30,
        alignment=TA_CENTER,
        leading=24
    ))

    # Estilos para headers
    styles.add(ParagraphStyle(
        name='CustomH2',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#2a2a2a',
        spaceAfter=12,
        spaceBefore=20,
        leading=20
    ))

    styles.add(ParagraphStyle(
        name='CustomH3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor='#3a3a3a',
        spaceAfter=10,
        spaceBefore=15,
        leading=18
    ))

    # Construir story (contenido del PDF)
    story = []

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'hr']):
        if element.name == 'h1':
            story.append(Paragraph(element.get_text(), styles['CustomTitle']))
            story.append(Spacer(1, 12))
        elif element.name == 'h2':
            story.append(Paragraph(element.get_text(), styles['CustomH2']))
            story.append(Spacer(1, 6))
        elif element.name == 'h3':
            story.append(Paragraph(element.get_text(), styles['CustomH3']))
            story.append(Spacer(1, 6))
        elif element.name == 'h4':
            story.append(Paragraph(element.get_text(), styles['Heading4']))
            story.append(Spacer(1, 6))
        elif element.name == 'hr':
            story.append(Spacer(1, 12))
            story.append(PageBreak())
        elif element.name == 'p':
            text = element.get_text()
            if text.strip():
                story.append(Paragraph(text, styles['Normal']))
                story.append(Spacer(1, 6))

    # Generar PDF
    doc.build(story)
    print(f"✅ PDF generado: {output_pdf}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python md_to_pdf.py <archivo.md> [salida.pdf]")
        sys.exit(1)

    md_file = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        md_to_pdf(md_file, output_pdf)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
