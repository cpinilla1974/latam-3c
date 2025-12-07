#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta la infografía de emisiones HTML a imagen PNG de alta resolución
"""

from playwright.sync_api import sync_playwright
import os

HTML_FILE = '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_emisiones_cadena.html'
OUTPUT_DIR = '/home/cpinilla/projects/latam-3c/docs/analisis'

def exportar_a_imagen():
    """Exporta el HTML a imagen PNG."""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Captura de página completa
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        page.goto(f'file://{HTML_FILE}')
        page.wait_for_timeout(3000)  # Esperar renderizado de Chart.js

        output_full = os.path.join(OUTPUT_DIR, 'infografia_emisiones_cadena_full.png')
        page.screenshot(path=output_full, full_page=True)
        print(f"✅ Imagen completa: {output_full}")

        # Captura HD (2x resolución)
        page_hd = browser.new_page(viewport={'width': 1400, 'height': 900}, device_scale_factor=2)
        page_hd.goto(f'file://{HTML_FILE}')
        page_hd.wait_for_timeout(3000)

        output_hd = os.path.join(OUTPUT_DIR, 'infografia_emisiones_cadena_hd.png')
        page_hd.screenshot(path=output_hd, full_page=True)
        print(f"✅ Imagen HD (2x): {output_hd}")

        browser.close()

    return output_full, output_hd


if __name__ == '__main__':
    print("Exportando infografía de emisiones a imagen...")
    full, hd = exportar_a_imagen()

    for f in [full, hd]:
        size = os.path.getsize(f) / 1024
        print(f"   {os.path.basename(f)}: {size:.1f} KB")
