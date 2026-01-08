#!/bin/bash
# Script maestro para gestionar el bot de trading
# Uso: ./run.sh [comando]

# Cambiar al directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Función para mostrar el menú
show_menu() {
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║              🤖 TRADING BOT - MENÚ PRINCIPAL              ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Opciones disponibles:${NC}"
    echo ""
    echo -e "  ${GREEN}1. trading${NC}    - Ejecutar bot de trading (acciones)"
    echo -e "  ${GREEN}2. crypto${NC}     - Ejecutar bot de criptomonedas"
    echo -e "  ${GREEN}3. backtest${NC}   - Ejecutar backtesting"
    echo -e "  ${GREEN}4. test${NC}       - Probar conexión con Alpaca"
    echo -e "  ${GREEN}5. config${NC}     - Mostrar configuración actual"
    echo -e "  ${GREEN}6. setup${NC}      - Instalar/actualizar dependencias"
    echo ""
    echo -e "${YELLOW}Uso: ./run.sh [comando]${NC}"
    echo -e "${YELLOW}Ejemplo: ./run.sh trading${NC}"
    echo ""
}

# Función para verificar entorno
check_environment() {
    if [ ! -d ".venv" ]; then
        echo -e "${RED}❌ Entorno virtual no encontrado${NC}"
        echo -e "${YELLOW}💡 Ejecutando setup...${NC}"
        setup_environment
    fi
    
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ Archivo .env no encontrado${NC}"
        if [ -f ".env.example" ]; then
            echo -e "${YELLOW}💡 Copiando .env.example a .env...${NC}"
            cp .env.example .env
            echo -e "${GREEN}✅ Archivo .env creado${NC}"
            echo -e "${YELLOW}⚠️  IMPORTANTE: Edita .env y configura tus credenciales de Alpaca${NC}"
        else
            echo -e "${RED}❌ Tampoco existe .env.example${NC}"
            exit 1
        fi
    fi
}

# Función para instalar dependencias
setup_environment() {
    echo -e "${BLUE}🔧 Configurando entorno...${NC}"
    
    # Crear entorno virtual si no existe
    if [ ! -d ".venv" ]; then
        echo -e "${GREEN}📦 Creando entorno virtual...${NC}"
        python3 -m venv .venv
    fi
    
    # Activar entorno
    source .venv/bin/activate
    
    # Instalar dependencias
    echo -e "${GREEN}📥 Instalando dependencias...${NC}"
    pip install -q --upgrade pip
    pip install -q -r requirements-dev.txt
    pip install -q -e ./strategies
    
    echo -e "${GREEN}✅ Entorno configurado correctamente${NC}"
}

# Función para mostrar configuración
show_config() {
    check_environment
    source .venv/bin/activate
    
    echo -e "${BLUE}📋 Configuración actual:${NC}"
    echo ""
    
    python << EOF
import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar .env desde el directorio actual
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

configs = [
    ("Modo de Trading", os.getenv('TRADING_MODE', 'paper')),
    ("Símbolos (Acciones)", os.getenv('SYMBOLS', 'N/A')),
    ("Símbolos (Crypto)", os.getenv('CRYPTO_SYMBOLS', 'N/A')),
    ("Estrategias Activas", os.getenv('ACTIVE_STRATEGIES', 'N/A')),
    ("Consenso", os.getenv('CONSENSUS_THRESHOLD', 'N/A')),
    ("Capital por Símbolo", f"\${os.getenv('CAPITAL_PER_SYMBOL', 'N/A')}"),
    ("Stop Loss", f"{float(os.getenv('STOP_LOSS_PCT', '0.02')) * 100:.1f}%"),
    ("Take Profit", f"{float(os.getenv('TAKE_PROFIT_PCT', '0.05')) * 100:.1f}%"),
]

for label, value in configs:
    print(f"   {label:20} → {value}")

print()
print("Estrategias configuradas:")
for strategy in ['RSI', 'MACD', 'BOLLINGER', 'ELLIOTT', 'MA50', 'MA100', 'MA200']:
    config = os.getenv(f'STRATEGY_{strategy}')
    if config:
        print(f"   • {strategy:10} → {config}")
EOF
    echo ""
}

# Función para probar conexión
test_connection() {
    check_environment
    source .venv/bin/activate
    
    echo -e "${BLUE}🔌 Probando conexión con Alpaca...${NC}"
    python examples/test_alpaca_connection.py
}

# Procesar comando
COMMAND=${1:-menu}

case $COMMAND in
    trading)
        check_environment
        ./run_trading.sh
        ;;
    crypto)
        check_environment
        ./run_crypto.sh
        ;;
    backtest)
        check_environment
        STRATEGY=${2:-elliott}
        ./run_backtest.sh $STRATEGY
        ;;
    test)
        test_connection
        ;;
    config)
        show_config
        ;;
    setup)
        setup_environment
        ;;
    menu|help|--help|-h)
        show_menu
        ;;
    *)
        echo -e "${RED}❌ Comando desconocido: $COMMAND${NC}"
        show_menu
        exit 1
        ;;
esac
