#!/bin/bash
# Script para ejecutar el bot de trading con configuración desde .env
# Uso: ./run_trading.sh

# Cambiar al directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              TRADING BOT - ALPACA MARKETS                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar que existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Error: No se encontró el entorno virtual .venv${NC}"
    echo -e "${YELLOW}💡 Ejecuta primero: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt${NC}"
    exit 1
fi

# Verificar que existe el archivo .env
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: No se encontró el archivo .env${NC}"
    echo -e "${YELLOW}💡 Copia .env.example a .env y configura tus credenciales${NC}"
    exit 1
fi

# Activar entorno virtual
echo -e "${GREEN}🔧 Activando entorno virtual...${NC}"
source .venv/bin/activate

# Verificar instalación de dependencias
echo -e "${GREEN}📦 Verificando dependencias...${NC}"
python -c "import pandas; import numpy; from strategies import *; from trading_engine import *" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Instalando dependencias faltantes...${NC}"
    pip install -q -r requirements-dev.txt
    pip install -q -e ./strategies
    pip install -q -e ./engine
fi

# Mostrar configuración
echo -e "${BLUE}📋 Configuración actual:${NC}"
python << EOF
import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar .env desde el directorio actual
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

mode = os.getenv('TRADING_MODE', 'paper')
symbols = os.getenv('SYMBOLS', 'N/A')
strategies = os.getenv('ACTIVE_STRATEGIES', 'N/A')
consensus = os.getenv('CONSENSUS_THRESHOLD', 'N/A')

print(f"   Modo: {mode.upper()}")
print(f"   Símbolos: {symbols}")
print(f"   Estrategias: {strategies}")
print(f"   Consenso: {consensus}")
EOF

echo ""
echo -e "${GREEN}🚀 Iniciando bot de trading...${NC}"
echo -e "${YELLOW}💡 Presiona Ctrl+C para detener${NC}"
echo ""

# Ejecutar el bot
python examples/live_trading_alpaca.py

# Capturar código de salida
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ El bot se detuvo con errores (código: $EXIT_CODE)${NC}"
else
    echo ""
    echo -e "${GREEN}✅ Bot detenido correctamente${NC}"
fi

exit $EXIT_CODE
