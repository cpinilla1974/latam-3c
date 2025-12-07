#!/usr/bin/env python3
"""
Script para convertir Markdown con diagramas Mermaid a PDF
Usa mermaid-cli para renderizar diagramas y markdown-pdf para generar el PDF
"""

import re
import subprocess
import tempfile
import os
import sys
from pathlib import Path

def extract_mermaid_blocks(content):
    """Extrae todos los bloques de código Mermaid del markdown"""
    pattern = r'```mermaid\n(.*?)```'
    matches = re.finditer(pattern, content, re.DOTALL)
    return [(m.group(0), m.group(1)) for m in matches]

def generate_mermaid_image(mermaid_code, output_path):
    """Genera una imagen PNG desde código Mermaid usando mermaid-cli"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(mermaid_code)
        mmd_file = f.name

    try:
        # Usar mmdc (mermaid-cli) para generar la imagen
        subprocess.run([
            'mmdc',
            '-i', mmd_file,
            '-o', output_path,
            '-b', 'transparent',
            '-t', 'default'
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generando imagen Mermaid: {e.stderr.decode()}")
        return False
    finally:
        os.unlink(mmd_file)

def replace_mermaid_with_images(content, output_dir):
    """Reemplaza bloques Mermaid con imágenes generadas"""
    mermaid_blocks = extract_mermaid_blocks(content)

    if not mermaid_blocks:
        return content

    os.makedirs(output_dir, exist_ok=True)
    modified_content = content

    for idx, (full_block, mermaid_code) in enumerate(mermaid_blocks):
        img_name = f"diagram_{idx + 1}.png"
        img_path = os.path.join(output_dir, img_name)

        if generate_mermaid_image(mermaid_code, img_path):
            # Reemplazar el bloque Mermaid con la imagen
            img_markdown = f"\n![Diagrama {idx + 1}]({img_path})\n"
            modified_content = modified_content.replace(full_block, img_markdown, 1)
        else:
            print(f"Advertencia: No se pudo generar diagrama {idx + 1}")

    return modified_content

def convert_to_pdf_pandoc(md_file, output_pdf):
    """Convierte Markdown a PDF usando pandoc"""
    try:
        subprocess.run([
            'pandoc',
            md_file,
            '-o', output_pdf,
            '--pdf-engine=weasyprint',
            '-V', 'geometry:margin=1in',
            '--toc',
            '--toc-depth=2'
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error con pandoc: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("pandoc no está instalado. Instalando...")
        return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python md2pdf.py <archivo.md> [output.pdf]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.md', '.pdf')

    if not os.path.exists(input_file):
        print(f"Error: Archivo {input_file} no encontrado")
        sys.exit(1)

    print(f"Procesando {input_file}...")

    # Leer contenido del archivo
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Crear directorio temporal para imágenes
    temp_dir = tempfile.mkdtemp(prefix='mermaid_images_')

    try:
        # Reemplazar bloques Mermaid con imágenes
        print("Generando diagramas Mermaid...")
        modified_content = replace_mermaid_with_images(content, temp_dir)

        # Crear archivo temporal con el contenido modificado
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(modified_content)
            temp_md = f.name

        print("Generando PDF...")
        # Intentar conversión con pandoc
        if convert_to_pdf_pandoc(temp_md, output_file):
            print(f"✓ PDF generado exitosamente: {output_file}")
        else:
            print("\nPandoc no disponible. Instalando dependencias...")
            print("Ejecuta: sudo apt-get install pandoc weasyprint")

    finally:
        # Limpiar archivos temporales
        if os.path.exists(temp_md):
            os.unlink(temp_md)
        # Mantener las imágenes por si se necesitan
        print(f"Imágenes de diagramas guardadas en: {temp_dir}")

if __name__ == '__main__':
    main()
