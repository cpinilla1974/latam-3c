# Deploy Calculadora 4C Peru - Demo FICEM

## Archivos

- `requirements-minimal.txt` - Dependencias mínimas (sin IA)
- `deploy.sh` - Script de deploy automático

## Uso Rápido

```bash
# Desde este directorio
./deploy.sh [usuario] [host] [puerto]

# Ejemplo
./deploy.sh root vps.omniscien.cl 8510
```

## Requisitos del VPS

- Ubuntu 20.04+ o Debian 11+
- Python 3.10+
- Puerto abierto (8510 por defecto)
- rsync instalado

## Deploy Manual (alternativa)

Si prefieres hacerlo paso a paso:

```bash
# 1. En el VPS, crear directorio
mkdir -p /opt/calculadora-4c-peru
cd /opt/calculadora-4c-peru

# 2. Copiar archivos (desde tu máquina local)
rsync -avz --exclude 'venv*' --exclude '__pycache__' --exclude 'ai_modules' \
    /path/to/prototipos/v1/ root@tu-vps:/opt/calculadora-4c-peru/

# 3. En el VPS, crear entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Inicializar BD (si es necesario)
python init_db.py

# 5. Ejecutar
streamlit run app.py --server.port=8510 --server.address=0.0.0.0
```

## Servicio Systemd

El script crea automáticamente un servicio systemd. Comandos útiles:

```bash
# Ver estado
systemctl status calculadora-4c-peru

# Ver logs en tiempo real
journalctl -u calculadora-4c-peru -f

# Reiniciar
systemctl restart calculadora-4c-peru

# Detener
systemctl stop calculadora-4c-peru
```

## URL Final

Una vez deployado, la app estará disponible en:

```
http://[tu-vps]:8510
```

## Notas

- Este deploy es para DEMO solamente
- No incluye módulos de IA (ai_modules/) para reducir dependencias
- La BD SQLite se copia con datos de prueba
