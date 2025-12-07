"""
Exportar infografía a PNG con fondo negro en máxima resolución
Usa screenshot de Playwright con resolución ultra HD
"""
import asyncio
from playwright.async_api import async_playwright
import os
import sys

async def exportar_con_fondo_negro():
    """Exporta la infografía con fondo negro en máxima resolución"""

    input_html = '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_remitos_ia.html'

    # Diferentes resoluciones para exportar
    exports = [
        {
            'name': '4K Ultra HD',
            'width': 3840,
            'height': 2160,
            'scale': 2,
            'output': '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_remitos_4k.png'
        },
        {
            'name': '2K High Definition',
            'width': 2560,
            'height': 1440,
            'scale': 2,
            'output': '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_remitos_2k.png'
        },
        {
            'name': 'Full Page 4K',
            'width': 3840,
            'height': None,  # Full height
            'scale': 2,
            'output': '/home/cpinilla/projects/latam-3c/docs/analisis/infografia_remitos_fullpage_4k.png'
        }
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for export_config in exports:
            print(f"\n📸 Exportando: {export_config['name']}")
            print(f"   Resolución: {export_config['width']}x{export_config['height'] or 'FULL'}")

            # Crear página con viewport específico
            page = await browser.new_page(
                viewport={'width': export_config['width'], 'height': export_config['height'] or 2160}
            )

            # Cargar HTML local
            file_url = f'file://{os.path.abspath(input_html)}'
            await page.goto(file_url, wait_until='networkidle')

            # Esperar a que Plotly renderice completamente
            await page.wait_for_load_state('networkidle')
            await page.evaluate('() => new Promise(resolve => setTimeout(resolve, 3000))')

            # Inyectar CSS para fondo negro
            await page.add_style_tag(content="""
                body {
                    background-color: #000000 !important;
                    color: #ffffff !important;
                }
                html {
                    background-color: #000000 !important;
                }
                .plotly-graph-div {
                    background-color: #000000 !important;
                }
            """)

            # Esperar a que el CSS se aplique
            await page.evaluate('() => new Promise(resolve => setTimeout(resolve, 500))')

            # Screenshot
            if export_config['height']:
                # Viewport fijo
                await page.screenshot(
                    path=export_config['output'],
                    full_page=False
                )
                print(f"   ✅ Guardado: {export_config['output']}")
            else:
                # Full page height
                height = await page.evaluate('() => document.documentElement.scrollHeight')
                print(f"   Altura de página: {height}px")
                await page.screenshot(
                    path=export_config['output'],
                    full_page=True
                )
                print(f"   ✅ Guardado: {export_config['output']}")

            # Información del archivo
            if os.path.exists(export_config['output']):
                size = os.path.getsize(export_config['output']) / (1024*1024)
                print(f"   Tamaño: {size:.1f} MB")

            await page.close()

        await browser.close()

    # Resumen final
    print("\n" + "="*80)
    print("✨ EXPORTACIÓN COMPLETADA")
    print("="*80)
    print("\n📊 Archivos generados (fondo negro, máxima resolución):")
    for export_config in exports:
        if os.path.exists(export_config['output']):
            size = os.path.getsize(export_config['output']) / (1024*1024)
            print(f"\n  {export_config['name']}")
            print(f"    📍 {export_config['output']}")
            print(f"    📐 {export_config['width']}x{export_config['height'] or 'VARIABLE'}")
            print(f"    💾 {size:.1f} MB")

if __name__ == '__main__':
    print("🚀 Exportando infografía a PNG con fondo negro en máxima resolución...")
    print("   Esto puede tardar unos minutos...\n")
    asyncio.run(exportar_con_fondo_negro())
    print("\n🎉 Completado!")
