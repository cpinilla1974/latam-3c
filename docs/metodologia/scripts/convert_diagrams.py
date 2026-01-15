#!/usr/bin/env python3
"""
Script para convertir diagramas Mermaid a PNG
Requiere: npm install -g @mermaid-js/mermaid-cli
"""

import os
import subprocess
import sys
from pathlib import Path

def extract_mermaid_code(md_file):
    """Extrae el código Mermaid de un archivo markdown"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar bloques de código mermaid
    lines = content.split('\n')
    mermaid_lines = []
    in_mermaid = False

    for line in lines:
        if line.strip() == '```mermaid':
            in_mermaid = True
            continue
        elif line.strip() == '```' and in_mermaid:
            break
        elif in_mermaid:
            mermaid_lines.append(line)

    return '\n'.join(mermaid_lines)

def convert_to_png(mermaid_file, output_file):
    """Convierte archivo .mmd a PNG usando mermaid-cli"""
    try:
        cmd = f"mmdc -i {mermaid_file} -o {output_file} -t neutral -b white --width 1200 --height 800"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ {output_file} generado exitosamente")
            return True
        else:
            print(f"❌ Error generando {output_file}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def main():
    # Rutas
    diagrams_dir = Path("docs/2-diagramas")
    output_dir = Path("docs/2-diagramas/images")

    # Crear directorio de salida
    output_dir.mkdir(exist_ok=True)

    # Archivos a procesar
    files_to_convert = [
        "flujo-general-etapa1.md",
        "secuencia-temporal-etapa1.md"
    ]

    print("🔄 Convirtiendo diagramas Mermaid a PNG...")

    for md_file in files_to_convert:
        md_path = diagrams_dir / md_file

        if not md_path.exists():
            print(f"⚠️  {md_file} no encontrado")
            continue

        # Extraer código mermaid
        mermaid_code = extract_mermaid_code(md_path)

        if not mermaid_code:
            print(f"⚠️  No se encontró código Mermaid en {md_file}")
            continue

        # Crear archivo temporal .mmd
        base_name = md_path.stem
        mmd_file = output_dir / f"{base_name}.mmd"
        png_file = output_dir / f"{base_name}.png"

        # Escribir código mermaid
        with open(mmd_file, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)

        # Convertir a PNG
        convert_to_png(mmd_file, png_file)

        # Limpiar archivo temporal
        mmd_file.unlink()

    print("\n📁 Archivos PNG generados en:", output_dir.absolute())

if __name__ == "__main__":
    print("🚀 Iniciando conversión de diagramas...")
    print("📋 Requisito: npm install -g @mermaid-js/mermaid-cli")
    print()

    main()