# LATAM-3C Sistema de Huella de Carbono

Sistema para el cálculo y gestión de huella de carbono en la industria cementera de América Latina.

## Estructura del Proyecto

```
latam-3c/
├── docs/                   # Documentación del sistema
│   ├── 01-estructura-datos-entrada.md
│   ├── 02-sistema-perfiles-proceso.md
│   ├── 03-calculos-salidas.md
│   ├── 04-modelo-datos.md
│   └── 05-dilemas-decisiones.md
├── data/                   # Archivos de datos de ejemplo
│   ├── ejemplo_acme_excel_clinker_cemento.json
│   ├── ejemplo_acme_excel_concreto.json
│   └── ejemplo_cementosandinos_colombia_*.json
└── v1/                     # Aplicación Streamlit v1
    ├── app.py              # Aplicación principal
    ├── requirements.txt    # Dependencias Python
    ├── modules/            # Módulos reutilizables
    │   └── excel_generator.py
    ├── pages/              # Páginas de la aplicación
    │   ├── admin/
    │   │   └── generar_excel.py
    │   ├── empresas/
    │   └── reportes/
    └── database/           # Módulos de base de datos
        └── __init__.py

```

## Instalación

1. Clonar el repositorio:
```bash
git clone [url-repositorio]
cd latam-3c
```

2. Configurar entorno virtual para v0:
```bash
cd v0
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Para recrear el entorno virtual (si es necesario):
```bash
cd v0
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

### Para v0 (versión actual):
1. Activar el entorno virtual:
```bash
cd v0
source venv/bin/activate
```

2. Ejecutar la aplicación:
```bash
streamlit run app.py
```

### Para v1 (versión futura):
1. Activar el entorno virtual:
```bash
source venv/bin/activate
```

2. Ejecutar la aplicación:
```bash
cd v1
streamlit run app.py
```

3. Abrir navegador en http://localhost:8501

## Características

- **Gestión de Empresas**: Registro y administración de empresas cementeras
- **Generación de Excel**: Creación de plantillas Excel para captura de datos
- **Cálculo de Huella**: Procesamiento según protocolo GCCA
- **Reportes**: Visualización de indicadores y comparativas

## Tecnologías

- Python 3.8+
- Streamlit
- SQLite
- Pandas
- XlsxWriter

## Licencia

[Por definir]