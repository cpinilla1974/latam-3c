#!/bin/bash
# =====================================================
# Deploy Calculadora 4C Peru - Demo FICEM
# =====================================================
# Uso: ./deploy.sh [usuario] [host] [puerto]
# Ejemplo: ./deploy.sh root vps.ejemplo.com 8510
# =====================================================

set -e

# Configuración por defecto
VPS_USER="${1:-root}"
VPS_HOST="${2:-tu-vps.com}"
APP_PORT="${3:-8510}"
APP_NAME="calculadora-4c-peru"
REMOTE_DIR="/opt/$APP_NAME"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deploy Calculadora 4C Peru - FICEM   ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "VPS: ${YELLOW}$VPS_USER@$VPS_HOST${NC}"
echo -e "Puerto: ${YELLOW}$APP_PORT${NC}"
echo -e "Directorio remoto: ${YELLOW}$REMOTE_DIR${NC}"
echo ""

# Confirmar
read -p "¿Continuar? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Cancelado."
    exit 1
fi

# Directorio base (donde está este script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
V1_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo -e "${YELLOW}[1/5] Creando estructura en VPS...${NC}"
ssh $VPS_USER@$VPS_HOST "mkdir -p $REMOTE_DIR"

echo -e "${YELLOW}[2/5] Copiando archivos...${NC}"
# Copiar todo excepto venv, __pycache__, .git
rsync -avz --progress \
    --exclude 'venv*' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.git' \
    --exclude 'deploy' \
    --exclude 'ai_modules' \
    "$V1_DIR/" "$VPS_USER@$VPS_HOST:$REMOTE_DIR/"

# Copiar requirements minimal
scp "$SCRIPT_DIR/requirements-minimal.txt" "$VPS_USER@$VPS_HOST:$REMOTE_DIR/requirements.txt"

echo -e "${YELLOW}[3/5] Configurando entorno virtual...${NC}"
ssh $VPS_USER@$VPS_HOST << EOF
cd $REMOTE_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
EOF

echo -e "${YELLOW}[4/5] Creando servicio systemd...${NC}"
ssh $VPS_USER@$VPS_HOST << EOF
cat > /etc/systemd/system/$APP_NAME.service << 'SYSTEMD'
[Unit]
Description=Calculadora 4C Peru - Demo FICEM
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$REMOTE_DIR
Environment="PATH=$REMOTE_DIR/venv/bin"
ExecStart=$REMOTE_DIR/venv/bin/streamlit run app.py --server.port=$APP_PORT --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SYSTEMD

systemctl daemon-reload
systemctl enable $APP_NAME
systemctl restart $APP_NAME
EOF

echo -e "${YELLOW}[5/5] Verificando...${NC}"
sleep 3
ssh $VPS_USER@$VPS_HOST "systemctl status $APP_NAME --no-pager"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deploy completado!                   ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "URL: ${YELLOW}http://$VPS_HOST:$APP_PORT${NC}"
echo ""
echo "Comandos útiles:"
echo "  Ver logs:    ssh $VPS_USER@$VPS_HOST 'journalctl -u $APP_NAME -f'"
echo "  Reiniciar:   ssh $VPS_USER@$VPS_HOST 'systemctl restart $APP_NAME'"
echo "  Detener:     ssh $VPS_USER@$VPS_HOST 'systemctl stop $APP_NAME'"
