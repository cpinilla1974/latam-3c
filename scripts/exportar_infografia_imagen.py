#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta la infografía HTML a imagen PNG de alta resolución
"""

from playwright.sync_api import sync_playwright
import os

HTML_FILE = '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_calidad_datos.html'
OUTPUT_DIR = '/home/cpinilla/projects/latam-3c/docs/analisis'

def exportar_a_imagen():
    """Exporta el HTML a imagen PNG."""

    with sync_playwright() as p:
        # Lanzar navegador headless
        browser = p.chromium.launch(headless=True)

        # Crear página con viewport grande para capturar todo
        page = browser.new_page(viewport={'width': 1400, 'height': 800})

        # Cargar el archivo HTML
        page.goto(f'file://{HTML_FILE}')

        # Esperar a que los gráficos de Chart.js se rendericen
        page.wait_for_timeout(3000)

        # Captura de página completa
        output_full = os.path.join(OUTPUT_DIR, 'infografia_calidad_datos_full.png')
        page.screenshot(path=output_full, full_page=True)
        print(f"✅ Imagen completa: {output_full}")

        # Captura solo la parte visible (primera pantalla)
        output_header = os.path.join(OUTPUT_DIR, 'infografia_calidad_datos_header.png')
        page.screenshot(path=output_header, full_page=False)
        print(f"✅ Imagen header: {output_header}")

        # Captura de alta resolución (2x)
        page_hd = browser.new_page(viewport={'width': 1400, 'height': 800}, device_scale_factor=2)
        page_hd.goto(f'file://{HTML_FILE}')
        page_hd.wait_for_timeout(3000)

        output_hd = os.path.join(OUTPUT_DIR, 'infografia_calidad_datos_hd.png')
        page_hd.screenshot(path=output_hd, full_page=True)
        print(f"✅ Imagen HD (2x): {output_hd}")

        browser.close()

    return output_full, output_hd


if __name__ == '__main__':
    print("Exportando infografía a imagen...")
    full, hd = exportar_a_imagen()

    # Mostrar tamaños
    for f in [full, hd]:
        size = os.path.getsize(f) / 1024
        print(f"   {os.path.basename(f)}: {size:.1f} KB")
