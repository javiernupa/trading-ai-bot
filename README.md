# Trading AI Bot 🤖📈

Sistema profesional de backtesting **y trading en vivo** con Alpaca Markets.

## 🌟 Características

### 🎯 Trading en Vivo (NUEVO)
- ✅ **Alpaca Markets Integration** - Paper y Live Trading
- ✅ **Multi-Symbol Trading** - Opera múltiples acciones simultáneamente
- ✅ **💰 Crypto Trading** - Bitcoin, Ethereum, Solana y más 24/7
- ✅ **Real-Time Data** - Cotizaciones y barras en tiempo real
- ✅ **Automatic Execution** - Ejecución automática de señales
- ✅ **Position Management** - Gestión completa de posiciones
- ✅ **Paper Trading** - Prueba con dinero simulado primero
- ✅ **🛡️ Stop Loss & Take Profit** - Protección automática de posiciones

### Motor de Backtesting
- ✅ Motor de backtesting completo con gestión de órdenes y posiciones
- ✅ Cálculo de comisiones y slippage
- ✅ Métricas detalladas (Sharpe Ratio, drawdown, win rate, profit factor, etc.)
- ✅ Visualizaciones profesionales (equity curve, distribuciones, drawdowns)
- ✅ Arquitectura event-driven extensible

### Estrategias de Trading
- ✅ **RSI Strategy** - Índice de Fuerza Relativa
- ✅ **MACD Strategy** - Moving Average Convergence Divergence
- ✅ **Bollinger Bands Strategy** - Bandas de Bollinger
- ✅ **Moving Average Cross** - Cruce de medias móviles (Golden/Death Cross)
- ✅ **Combined Strategy** - Estrategia multi-indicador con consenso

### Gestión de Datos
- ✅ **Yahoo Finance Provider** - Descarga automática de datos de mercado
- ✅ **CSV Provider** - Carga de datos desde archivos CSV
- ✅ **Alpaca Data Provider** - Datos en tiempo real de Alpaca Markets
- ✅ **Data Loader** - Sistema unificado con caché automático
- ✅ **Data Validator** - Validación y limpieza automática de datos
- ✅ Gestión de caché para optimizar descargas

### Infraestructura
- ✅ Testing completo (62 tests, 70%+ coverage)
- ✅ Docker y docker-compose
- ✅ CI/CD con GitHub Actions
- ✅ Pre-commit hooks (black, ruff, mypy)
- ✅ Makefile para comandos comunes
- ✅ Documentación completa

## 📦 Instalación

### Requisitos
- Python 3.10+
- pip o poetry

### Instalación rápida

```bash
# Clonar repositorio
git clone https://github.com/javiernupa/trading-ai-bot.git
cd trading-ai-bot

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows

# Instalar dependencias
make install
# o
pip install -e engine/
pip install -e strategies/

# Para trading en vivo, también instalar:
pip install alpaca-py python-dotenv
```

## 🚀 Inicio Rápido

### Opción A: Trading en Vivo con Alpaca 🔴 NUEVO

#### 1. Crear cuenta en Alpaca Markets

1. Regístrate en [Alpaca Markets](https://alpaca.markets/) (gratis)
2. Activa **Paper Trading** (trading simulado)
3. Obtén tus API keys en el [Dashboard](https://app.alpaca.markets/)

#### 2. Configurar credenciales

```bash
# Copiar plantilla
cp .env.example .env

# Editar .env y añadir tus credenciales:
# ALPACA_API_KEY=PK...
# ALPACA_SECRET_KEY=...
# ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

#### 3. Test de conexión

```bash
python examples/test_alpaca_connection.py
```

#### 4. Iniciar trading en vivo

```bash
# Trading con 5 acciones (AAPL, GOOGL, MSFT, TSLA, AMZN)
python examples/live_trading_alpaca.py
```

**¿Qué hace?**
- Opera 5 acciones con $20k cada una ($100k total)
- Usa estrategia combinada (RSI + MACD + Bollinger)
- Actualiza señales cada 5 minutos
- Ejecuta órdenes automáticamente
- 🛡️ **Stop Loss 2%** - Protección automática
- 🎯 **Take Profit 5%** - Asegura ganancias
- Presiona Ctrl+C para detener

**📖 Guía completa:** [Alpaca Live Trading](docs/ALPACA_LIVE_TRADING.md)  
**🚀 Quick Start:** [Guía de 5 minutos](docs/QUICKSTART_ALPACA.md)  

---

### Opción A2: Trading de Criptomonedas 💰 NUEVO

#### 1. Habilitar Crypto en Alpaca

1. Ve a [Alpaca Dashboard](https://app.alpaca.markets/)
2. En **Paper Trading**, Settings
3. Habilita **Crypto Trading**
4. ¡Mismas API keys!

#### 2. Test de conexión crypto

```bash
python examples/test_crypto_connection.py
```

#### 3. Iniciar trading de crypto

```bash
# Trading con 5 criptos (BTC, ETH, SOL, AVAX, DOGE)
python examples/live_trading_crypto.py
```

**¿Qué hace?**
- Opera 5 criptomonedas 24/7
- $5k por cripto ($25k total)
- Actualiza cada 60 segundos
- 🛡️ **Stop Loss 5%** - Más amplio por volatilidad
- 🎯 **Take Profit 10%** - Más ambicioso
- ⚡ **24/7** - Sin horario de mercado

**💰 Guía completa:** [Crypto Trading](docs/CRYPTO_TRADING.md)  
**🚀 Quick Start:** [Crypto en 5 minutos](docs/CRYPTO_QUICKSTART.md)  

---

### Opción B: Backtesting (Análisis Histórico)
**🛡️ Gestión de Riesgo:** [Stop Loss & Take Profit](docs/RISK_MANAGEMENT.md)

---

### Opción B: Backtesting (análisis histórico)

#### 1. Backtest Simple con RSI

```python
from trading_engine import Backtester, DataLoader, MetricsCalculator
from strategies import RsiStrategy

# Cargar datos desde Yahoo Finance
loader = DataLoader()
data = loader.load_data(
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    provider="yahoo"
)

# Crear estrategia
strategy = RsiStrategy(period=14, lower_threshold=30, upper_threshold=70)

# Ejecutar backtest
backtester = Backtester(
    strategy=strategy,
    initial_capital=100_000,
    commission=0.001,
    slippage=0.0005
)

result = backtester.run(data)

# Mostrar resultados
calculator = MetricsCalculator()
metrics = calculator.calculate_metrics(result)
calculator.print_summary(metrics)
```

#### 2. Comparar Múltiples Estrategias

```python
from strategies import (
    RsiStrategy,
    MacdStrategy,
    BollingerBandsStrategy,
    MovingAverageCrossStrategy,
    CombinedStrategy,
)

strategies = {
    "RSI": RsiStrategy(),
    "MACD": MacdStrategy(),
    "Bollinger": BollingerBandsStrategy(),
    "MA Cross": MovingAverageCrossStrategy(fast_period=50, slow_period=200),
    "Combined": CombinedStrategy(consensus_threshold=2),
}

for name, strategy in strategies.items():
    backtester = Backtester(strategy=strategy, initial_capital=100_000)
    result = backtester.run(data)
    metrics = calculator.calculate_metrics(result)
    
    print(f"{name}: Retorno {metrics['total_return']:.2%}, "
          f"Sharpe {metrics['sharpe_ratio']:.2f}")
```

#### 3. Descargar Datos Históricos

```python
from trading_engine.data import DataLoader

loader = DataLoader()

# Descargar y guardar
symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "BTC-USD"]
for symbol in symbols:
    filepath = loader.download_and_save(
        symbol=symbol,
        start_date="2022-01-01",
        end_date="2024-01-01",
        output_file=f"data/{symbol}.csv"
    )
    print(f"✓ {symbol} guardado en {filepath}")
```

O usar el script proporcionado:

```bash
python scripts/download_data.py
```

## 📊 Ejemplos

### Ejecutar Ejemplo Completo

```bash
# Comparar todas las estrategias
python examples/compare_strategies.py

# Backtest avanzado con RSI
python examples/run_rsi_advanced.py

# Backtest con visualizaciones
python examples/run_with_charts.py
```

### Notebook Interactivo

```bash
jupyter notebook examples/backtest_analysis.ipynb
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
make test

# Tests con cobertura
make coverage

# Informe HTML de cobertura
make coverage
open htmlcov/index.html
```

## 📚 Documentación

- [🚀 Quick Start - Alpaca](docs/QUICKSTART_ALPACA.md) - Guía de 5 minutos para trading en vivo
- [📖 Alpaca Live Trading](docs/ALPACA_LIVE_TRADING.md) - Guía completa de Alpaca
- [� Crypto Trading](docs/CRYPTO_TRADING.md) - **NUEVO** Trading de criptomonedas 24/7- [🚀 Crypto Quick Start](docs/CRYPTO_QUICKSTART.md) - **NUEVO** Crypto en 5 minutos
- [📊 Stocks vs Crypto](docs/STOCKS_VS_CRYPTO.md) - **NUEVO** Comparación completa- [�🛡️ Risk Management](docs/RISK_MANAGEMENT.md) - Stop Loss y Take Profit
- [🎯 Strategy Tuning](docs/STRATEGY_TUNING.md) - Ajustar estrategias y señales
- [Getting Started Guide](docs/GETTING_STARTED.md) - Guía de inicio detallada
- [Strategies Documentation](docs/STRATEGIES.md) - Todas las estrategias disponibles
- [Data Management](docs/DATA_MANAGEMENT.md) - Sistema de gestión de datos
- [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md) - Resumen técnico

## 🏗️ Estructura del Proyecto

```
trading-ai-bot/
├── engine/                      # Motor de backtesting
│   ├── src/trading_engine/
│   │   ├── backtest.py         # Motor principal
│   │   ├── portfolio.py        # Gestión de portafolio
│   │   ├── models.py           # Modelos de datos
│   │   ├── metrics.py          # Calculador de métricas
│   │   ├── visualization.py    # Gráficos y reportes
│   │   └── data/               # Sistema de gestión de datos
│   │       ├── providers.py    # Yahoo Finance, CSV
│   │       ├── loader.py       # DataLoader con caché
│   │       └── validator.py    # Validación de datos
│   └── tests/                  # 29 tests (engine)
│
├── strategies/                  # Biblioteca de estrategias
│   ├── src/strategies/
│   │   ├── base.py             # Clase base
│   │   ├── rsi.py              # RSI Strategy
│   │   ├── macd.py             # MACD Strategy
│   │   ├── bollinger.py        # Bollinger Bands
│   │   ├── moving_average.py   # MA Cross
│   │   └── combined.py         # Combined Strategy
│   └── tests/                  # 19 tests (strategies)
│
├── examples/                    # Ejemplos de uso
│   ├── compare_strategies.py   # Comparar estrategias
│   ├── run_rsi_advanced.py     # Backtest avanzado
│   ├── live_trading_alpaca.py  # Trading en vivo (stocks)
│   ├── live_trading_crypto.py  # Trading de criptos 24/7
│   ├── test_alpaca_connection.py # Test de conexión
│   ├── test_crypto_connection.py # Test crypto
│   └── backtest_analysis.ipynb # Notebook interactivo
│
├── scripts/                     # Scripts útiles
│   └── download_data.py        # Descargar datos históricos
│
├── docs/                        # Documentación completa
├── .github/workflows/           # CI/CD
├── Makefile                     # Comandos comunes
└── docker-compose.yml          # Docker setup
```

## 🎯 Métricas Calculadas

- **Total Return** - Retorno total del período
- **Annualized Return** - Retorno anualizado
- **Sharpe Ratio** - Ratio de Sharpe (ajustado por riesgo)
- **Max Drawdown** - Máxima caída desde pico
- **Win Rate** - Porcentaje de trades ganadores
- **Profit Factor** - Ratio ganancias/pérdidas
- **Average Win/Loss** - Promedio de ganancias y pérdidas
- **Total Trades** - Número total de operaciones
- **Total Commission** - Comisiones totales pagadas

## 📈 Visualizaciones

El sistema genera automáticamente:

- **Equity Curve** - Evolución del capital
- **Returns Distribution** - Distribución de retornos
- **Drawdown Chart** - Gráfico de drawdowns
- **Monthly Returns Heatmap** - Heatmap de retornos mensuales
- **Full Report** - Reporte completo en una imagen

## 🔧 Desarrollo

### Configuración del Entorno

```bash
# Instalar dependencias de desarrollo
make dev-install

# Instalar pre-commit hooks
pre-commit install

# Formatear código
make format

# Linter
make lint

# Type checking
make typecheck
```

### Crear Nueva Estrategia

```python
from strategies import BaseStrategy
import pandas as pd

class MyStrategy(BaseStrategy):
    def __init__(self, param1: int = 10):
        self.param1 = param1
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df['signal'] = 0
        
        # Tu lógica aquí
        # df.loc[condicion_compra, 'signal'] = 1
        # df.loc[condicion_venta, 'signal'] = -1
        
        return df
```

## 🐳 Docker

```bash
# Construir imagen
docker-compose build

# Ejecutar tests
docker-compose run --rm tests

# Jupyter notebook
docker-compose up jupyter
# Abre http://localhost:8888
```

## 📊 Resultados de Tests

```
================================ 62 passed in 1.26s =================================
- Engine tests: 29 passed
- Strategy tests: 19 passed  
- Data tests: 18 passed
- Import tests: 9 passed

Coverage: 70%+ (core modules 90%+)
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🔮 Roadmap

### En Progreso
- [ ] Optimización de parámetros (grid search, genetic algorithms)
- [ ] Paper trading con Alpaca API
- [ ] WebSocket para datos en tiempo real
- [ ] Dashboard web interactivo

### Futuro
- [ ] Más estrategias (momentum, mean reversion, pairs trading)
- [ ] Machine Learning strategies
- [ ] Sentiment analysis integration
- [ ] Multi-asset portfolio optimization
- [ ] Walk-forward analysis
- [ ] Monte Carlo simulations

## 📞 Contacto

- **Issues**: [GitHub Issues](https://github.com/javiernupa/trading-ai-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/javiernupa/trading-ai-bot/discussions)

## ⭐ Star History

Si este proyecto te resulta útil, ¡dale una estrella! ⭐

---

**Nota**: Este sistema es solo para fines educativos y de investigación. No es un consejo de inversión. Siempre realiza tu propia investigación antes de invertir.

**Disclaimer**: Trading involves substantial risk. Past performance does not guarantee future results.
