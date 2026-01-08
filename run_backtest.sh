#!/bin/bash
# Script para ejecutar backtesting con diferentes estrategias
# Uso: ./run_backtest.sh [estrategia]
# Ejemplo: ./run_backtest.sh elliott  (para Elliott Waves)
#          ./run_backtest.sh ma200    (para MA200)

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
echo -e "${BLUE}║                 BACKTEST - ANÁLISIS HISTÓRICO              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar que existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Error: No se encontró el entorno virtual .venv${NC}"
    exit 1
fi

# Activar entorno virtual
source .venv/bin/activate

# Determinar qué backtest ejecutar
STRATEGY=${1:-elliott}

case $STRATEGY in
    elliott|ELLIOTT)
        echo -e "${GREEN}🌊 Ejecutando backtest de Elliott Waves...${NC}"
        python examples/run_elliott_backtest.py
        ;;
    ma200|MA200)
        echo -e "${GREEN}📈 Ejecutando backtest de MA200...${NC}"
        python examples/run_ma200_backtest.py
        ;;
    *)
        echo -e "${YELLOW}Estrategias disponibles:${NC}"
        echo "  • elliott  - Elliott Waves"
        echo "  • ma200    - Media Móvil 200"
        echo ""
        echo -e "${YELLOW}Uso: ./run_backtest.sh [estrategia]${NC}"
        echo ""
        echo -e "${GREEN}🌊 Ejecutando Elliott Waves por defecto...${NC}"
        python examples/run_elliott_backtest.py
        ;;
esac

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Backtest completado${NC}"
    echo -e "${BLUE}📊 Los reportes se guardaron en backtest_results/${NC}"
else
    echo ""
    echo -e "${RED}❌ Error en backtest (código: $EXIT_CODE)${NC}"
fi

exit $EXIT_CODE
