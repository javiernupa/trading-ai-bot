#!/usr/bin/env bash
set -e

echo "=================================================="
echo "  Trading AI Bot - Setup Script"
echo "=================================================="
echo ""

# Verificar versión de Python
echo "Verificando versión de Python..."
PYTHON_CMD=""

# Intentar encontrar Python 3.10+
for cmd in python3.13 python3.12 python3.11 python3.10 python3 python; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)
        
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON_CMD=$cmd
            echo "✓ Encontrado $cmd (versión $VERSION)"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "✗ Error: Se requiere Python 3.10 o superior"
    echo ""
    echo "Por favor, instala Python 3.10+ desde:"
    echo "  - https://www.python.org/downloads/"
    echo "  - O usa pyenv: pyenv install 3.11"
    exit 1
fi

echo ""
echo "Creando entorno virtual..."
$PYTHON_CMD -m venv .venv

echo "Activando entorno virtual..."
source .venv/bin/activate

echo "Actualizando pip..."
pip install -U pip setuptools wheel

echo ""
echo "Instalando paquetes del proyecto..."
pip install -e ./engine -e ./strategies

echo ""
echo "Instalando dependencias de desarrollo..."
pip install -r requirements-dev.txt || echo "⚠ requirements-dev.txt no encontrado, continuando..."

echo ""
echo "=================================================="
echo "  ✓ Instalación completada"
echo "=================================================="
echo ""
echo "Para activar el entorno virtual, ejecuta:"
echo "  source .venv/bin/activate"
echo ""
echo "Para ejecutar tests:"
echo "  make test"
echo ""
echo "Para ejecutar un ejemplo:"
echo "  python examples/run_rsi.py"
echo ""
