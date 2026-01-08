# Trading AI Bot 🤖📈

Sistema modular de trading algorítmico con backtesting y soporte para múltiples estrategias.

## 🌟 Características

- **Motor de Backtesting**: Simula estrategias sobre datos históricos con métricas detalladas
- **Estrategias Modulares**: Biblioteca extensible de estrategias técnicas y ML
- **Configuración Centralizada**: Gestión de parámetros con Pydantic y variables de entorno
- **Testing Completo**: Suite de tests unitarios e integración con coverage
- **Containerización**: Docker y docker-compose para desarrollo y despliegue
- **CI/CD**: GitHub Actions para tests automáticos
- **Documentación**: Sphinx para documentación técnica

## 📁 Estructura del Proyecto

```
trading-ai-bot/
├── engine/              # Motor de backtesting y ejecución
├── strategies/          # Biblioteca de estrategias
├── config/              # Configuración centralizada
├── data/                # Datos históricos y ejemplos
├── docs/                # Documentación técnica
├── examples/            # Ejemplos de uso
├── logs/                # Archivos de log
├── reports/             # Reportes de backtesting
├── scripts/             # Scripts de utilidad
└── .github/             # GitHub Actions y templates
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Instalación Local

```bash
# Clonar el repositorio
git clone <repo-url>
cd trading-ai-bot

# Ejecutar script de instalación
bash scripts/bootstrap.sh

# Activar entorno virtual
source .venv/bin/activate

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores (opcional para empezar)
```

### Instalación Manual

```bash
# Crear entorno virtual con Python 3.10+
python3.10 -m venv .venv
source .venv/bin/activate

# Actualizar pip
pip install -U pip

# Instalar paquetes del proyecto
pip install -e ./engine -e ./strategies

# Instalar dependencias de desarrollo (opcional)
pip install -r requirements-dev.txt
```

### Uso con Docker

```bash
# Construir imagen
make docker-build

# Levantar servicios
make docker-up
```

## 📝 Uso Básico

```python
import pandas as pd
from trading_engine.backtest import Backtester
from strategies.rsi import RsiStrategy

# Cargar datos
df = pd.read_csv("data/examples/sample_data.csv")

# Crear estrategia
strategy = RsiStrategy(period=14, lower=30, upper=70)

# Ejecutar backtest
backtester = Backtester(strategy, df, cash=10000)
results = backtester.run()

print(f"PnL: ${results['pnl']:.2f}")
```

## 🧪 Testing

```bash
# Ejecutar tests
make test

# Ejecutar con cobertura
make coverage

# Linting
make lint

# Formatear código
make format
```

## 📊 Métricas Disponibles

### Performance Metrics
- ✅ **Total PnL** - Profit & Loss total en términos absolutos
- ✅ **Total Return %** - Retorno porcentual sobre capital inicial
- ✅ **Sharpe Ratio** - Ratio riesgo/retorno anualizado
- ✅ **Maximum Drawdown** - Pérdida máxima desde peak ($ y %)

### Trade Statistics
- ✅ **Total Trades** - Número total de operaciones
- ✅ **Winning/Losing Trades** - Trades ganadores y perdedores
- ✅ **Win Rate %** - Porcentaje de trades ganadores
- ✅ **Average Win/Loss** - Ganancia/pérdida promedio
- ✅ **Profit Factor** - Ratio de ganancias totales vs pérdidas totales

### Cost Analysis
- ✅ **Total Commission** - Comisión total pagada
- ✅ **Slippage Applied** - Slippage aplicado en cada operación

### Visualizations
- ✅ **Equity Curve** - Evolución del capital a lo largo del tiempo
- ✅ **Returns Distribution** - Histograma de PnL y retornos
- ✅ **Drawdown Chart** - Drawdown temporal
- ✅ **Monthly Returns** - PnL agregado por mes

## 🔧 Desarrollo

### Añadir Nueva Estrategia

1. Crear archivo en `strategies/src/strategies/`
2. Heredar de `BaseStrategy`
3. Implementar `generate_signals()`
4. Añadir tests en `strategies/tests/`

### Pre-commit Hooks

```bash
# Instalar hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

## 📚 Documentación

```bash
# Generar documentación
make docs

# Ver en navegador
open docs/_build/html/index.html
```

## 🤝 Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guías de contribución.

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 🛠️ Comandos Útiles

```bash
make help              # Ver todos los comandos disponibles
make install           # Instalar paquetes
make install-dev       # Instalar con deps de desarrollo
make test              # Ejecutar tests
make coverage          # Cobertura de tests
make lint              # Ejecutar linters
make format            # Formatear código
make clean             # Limpiar archivos temporales
make docker-build      # Construir imagen Docker
make docs              # Generar documentación
```
