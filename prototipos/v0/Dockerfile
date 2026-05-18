FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    streamlit==1.32.0 \
    pandas==2.2.0 \
    openpyxl==3.1.2 \
    xlsxwriter==3.1.9 \
    matplotlib>=3.5.0 \
    numpy>=1.21.0

COPY . .

# Crear ruta hardcodeada para bandas_gcca.json
RUN mkdir -p /home/cpinilla/storage/files && \
    cp /app/data/bandas_gcca.json /home/cpinilla/storage/files/

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
