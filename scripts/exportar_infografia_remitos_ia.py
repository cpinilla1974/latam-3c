"""
Exportar infografía de remitos a PNG usando Playwright
"""
import asyncio
from playwright.async_api import async_playwright
import os

async def exportar_infografia():
    """Exporta la infografía HTML a PNG"""

    input_html = '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_remitos_ia.html'
    output_png = '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_remitos_ia_full.png'
    output_png_hd = '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_remitos_ia_hd.png'

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Cargar HTML local
        file_url = f'file://{os.path.abspath(input_html)}'
        await page.goto(file_url, wait_until='networkidle')

        # Esperar a que Plotly renderize
        await page.wait_for_load_state('networkidle')
        await page.evaluate('() => new Promise(resolve => setTimeout(resolve, 2000))')

        # Obtener altura de la página
        height = await page.evaluate('() => document.documentElement.scrollHeight')

        # Screenshot full page
        print(f"📸 Capturando página completa (altura: {height}px)...")
        await page.screenshot(
            path=output_png,
            full_page=True
        )
        print(f"   ✅ Guardado: {output_png}")

        # Screenshot HD (crear nueva pestaña con viewport 2x)
        print(f"📸 Capturando en HD (2x resolución)...")
        page_hd = await browser.new_page(viewport={'width': 2000, 'height': int(height*2)})
        await page_hd.goto(file_url, wait_until='networkidle')
        await page_hd.wait_for_load_state('networkidle')
        await page_hd.screenshot(
            path=output_png_hd,
            full_page=True
        )
        print(f"   ✅ Guardado: {output_png_hd}")
        await page_hd.close()

        # Información de archivos
        size_full = os.path.getsize(output_png) / (1024*1024)
        size_hd = os.path.getsize(output_png_hd) / (1024*1024)

        print(f"\n📊 Archivos generados:")
        print(f"   • Estándar: {size_full:.1f} MB")
        print(f"   • HD: {size_hd:.1f} MB")

        await browser.close()

if __name__ == '__main__':
    print("🚀 Exportando infografía a PNG usando Playwright...\n")
    asyncio.run(exportar_infografia())
    print("\n✅ Exportación completada!")
