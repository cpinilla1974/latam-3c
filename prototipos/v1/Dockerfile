FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip
RUN pip install --upgrade pip

# Copiar requirements e instalar dependencias Python
COPY requirements-minimal.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación (excluyendo ai_modules)
COPY app.py .
COPY init_db.py .
COPY database/ ./database/
COPY modules/ ./modules/
COPY pages/ ./pages/
COPY services/ ./services/
COPY data/ ./data/
COPY sql/ ./sql/

# Crear directorio para reportes
RUN mkdir -p /app/reports

# Puerto de Streamlit
EXPOSE 8501

# Comando de inicio
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
