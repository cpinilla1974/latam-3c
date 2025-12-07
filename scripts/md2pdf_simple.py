#!/usr/bin/env python3
"""
Script simple para convertir Markdown con Mermaid a PDF
"""

import re
import subprocess
import tempfile
import os
import sys
import markdown
from weasyprint import HTML, CSS

def extract_mermaid_blocks(content):
    """Extrae bloques Mermaid"""
    pattern = r'```mermaid\n(.*?)```'
    matches = re.finditer(pattern, content, re.DOTALL)
    return [(m.group(0), m.group(1)) for m in matches]

def generate_mermaid_image(mermaid_code, output_path):
    """Genera imagen desde Mermaid"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(mermaid_code)
        mmd_file = f.name

    try:
        subprocess.run(['mmdc', '-i', mmd_file, '-o', output_path, '-b', 'white'],
                      check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Error generando diagrama: {e}")
        return False
    finally:
        os.unlink(mmd_file)

def replace_mermaid_with_images(content, img_dir):
    """Reemplaza Mermaid con imágenes usando base64"""
    import base64
    blocks = extract_mermaid_blocks(content)
    if not blocks:
        return content

    os.makedirs(img_dir, exist_ok=True)
    modified = content

    for idx, (full_block, code) in enumerate(blocks):
        img_path = os.path.join(img_dir, f"diagram_{idx + 1}.png")
        if generate_mermaid_image(code, img_path):
            # Leer imagen y convertir a base64 para embeber en HTML
            with open(img_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                img_html = f'<div style="text-align: center; margin: 20px 0;"><img src="data:image/png;base64,{img_data}" style="max-width: 90%; height: auto;" /></div>'
                modified = modified.replace(full_block, img_html, 1)

    return modified

def resolve_image_paths(content, base_dir):
    """Resuelve rutas relativas de imágenes y las convierte a base64"""
    import base64
    from pathlib import Path

    # Buscar todas las imágenes markdown ![alt](path)
    pattern = r'!\[(.*?)\]\((.*?)\)'

    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)

        # Si es una ruta relativa, resolverla desde base_dir
        if not img_path.startswith(('http://', 'https://', 'data:')):
            full_path = Path(base_dir) / img_path
            if full_path.exists():
                with open(full_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()

                    # Gantt al 90%, diagramas de flujo al 70%
                    if 'gantt' in img_path.lower():
                        size_style = 'max-width: 90%; height: auto;'
                    else:
                        size_style = 'max-width: 70%; max-height: 600px; height: auto;'

                    return f'<div style="text-align: center; margin: 15px 0; page-break-inside: avoid;"><img src="data:image/png;base64,{img_data}" style="{size_style}" alt="{alt_text}" /></div>'

        return match.group(0)

    return re.sub(pattern, replace_image, content)

def main():
    if len(sys.argv) < 2:
        print("Uso: python md2pdf_simple.py <archivo.md> [output.pdf]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.md', '.pdf')

    print(f"Procesando {input_file}...")

    # Obtener directorio base del archivo de entrada
    from pathlib import Path
    base_dir = Path(input_file).parent

    # Leer markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generar imágenes de Mermaid
    temp_dir = tempfile.mkdtemp()
    print("Generando diagramas...")
    content = replace_mermaid_with_images(content, temp_dir)

    # Resolver rutas de imágenes relativas
    print("Resolviendo imágenes...")
    content = resolve_image_paths(content, base_dir)

    # Convertir markdown a HTML
    print("Convirtiendo a HTML...")
    html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])

    # CSS para PDF profesional
    css = CSS(string='''
        @page { size: Letter; margin: 2cm; }
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; border-bottom: 2px solid #bdc3c7; padding-bottom: 8px; margin-top: 30px; }
        h3 { color: #7f8c8d; margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #bdc3c7; padding: 12px; text-align: left; }
        th { background-color: #ecf0f1; font-weight: bold; }
        code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        img { max-width: 100%; height: auto; margin: 20px 0; }
        ul, ol { margin: 15px 0; }
        hr { border: none; border-top: 1px solid #bdc3c7; margin: 30px 0; }
    ''')

    # Generar PDF
    print("Generando PDF...")
    HTML(string=html_content).write_pdf(output_file, stylesheets=[css])

    print(f"✓ PDF generado: {output_file}")

if __name__ == '__main__':
    main()
