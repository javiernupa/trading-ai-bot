# Trading Engine

Motor completo de backtesting para estrategias de trading algorítmico.

## 🎯 Características

### ✅ **Backtesting Completo**
- Simulación realista con comisiones y slippage
- Gestión de órdenes (market, limit, stop)
- Tracking de posiciones long/short
- Cálculo automático de PnL

### 📊 **Métricas Avanzadas**
- Total PnL y retorno porcentual
- Sharpe Ratio
- Maximum Drawdown
- Win Rate y Profit Factor
- Average Win/Loss
- Equity curve detallada

### 📈 **Visualizaciones**
- Curva de equity
- Distribución de retornos
- Drawdown temporal
- Retornos mensuales

### 🔧 **Portfolio Management**
- Gestión automática de capital
- Control de posiciones
- Registro de trades
- Validación de órdenes

## 📦 Instalación

```bash
pip install -e .
```

## 🚀 Uso Básico

```python
from trading_engine import Backtester, MetricsCalculator
from strategies import RsiStrategy
import pandas as pd

# Cargar datos
df = pd.read_csv("data.csv")  # Debe tener columna 'close'

# Crear estrategia
strategy = RsiStrategy(period=14, lower=30, upper=70)

# Ejecutar backtest
backtester = Backtester(
    strategy=strategy,
    data=df,
    initial_cash=10000,
    commission=0.001,  # 0.1%
    slippage=0.0005    # 0.05%
)

result = backtester.run()

# Mostrar resultados
MetricsCalculator.print_summary(result)
```

## 📊 Visualizaciones

```python
from trading_engine import BacktestVisualizer

# Crear reporte completo con gráficas
BacktestVisualizer.create_full_report(result, output_dir="reports")

# O gráficas individuales
BacktestVisualizer.plot_equity_curve(result)
BacktestVisualizer.plot_returns_distribution(result)
BacktestVisualizer.plot_drawdown(result)
BacktestVisualizer.plot_monthly_returns(result)
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=trading_engine --cov-report=html
```

## 📚 Componentes Principales

### Backtester
Motor principal que ejecuta la simulación del backtest.

**Parámetros:**
- `strategy`: Instancia de Strategy a testear
- `data`: DataFrame con datos históricos (requiere columna 'close')
- `initial_cash`: Capital inicial (default: 10000)
- `commission`: Tasa de comisión (default: 0.001)
- `slippage`: Tasa de slippage (default: 0.0005)

### Portfolio
Gestiona el capital, posiciones y ejecución de órdenes.

**Métodos principales:**
- `execute_order()`: Ejecuta una orden
- `update_positions()`: Actualiza precios de posiciones
- `record_equity()`: Registra equity histórico

### MetricsCalculator
Calcula métricas de rendimiento del backtest.

**Métricas calculadas:**
- Performance: PnL, Return%, Sharpe, Max Drawdown
- Trade Statistics: Total trades, Win rate, Profit factor
- Additional: Equity curve, Commission tracking

### BacktestVisualizer
Genera visualizaciones de resultados.

**Métodos:**
- `plot_equity_curve()`: Gráfica de equity
- `plot_returns_distribution()`: Distribución de retornos
- `plot_drawdown()`: Drawdown temporal
- `plot_monthly_returns()`: PnL mensual
- `create_full_report()`: Reporte completo

## 🎓 Ejemplos

Ver carpeta `examples/`:
- `run_rsi.py`: Ejemplo básico
- `run_rsi_advanced.py`: Ejemplo avanzado con logs
- `run_with_charts.py`: Ejemplo con visualizaciones
- `backtest_analysis.ipynb`: Jupyter notebook interactivo

## 📖 Documentación API

### Order Types
```python
from trading_engine import OrderType, OrderSide

# Tipos de orden
OrderType.MARKET  # Orden de mercado
OrderType.LIMIT   # Orden limitada
OrderType.STOP    # Stop order

# Lado de la orden
OrderSide.BUY     # Compra
OrderSide.SELL    # Venta
```

### Trade Model
```python
from trading_engine import Trade

# Cada trade cerrado contiene:
trade.symbol           # Símbolo del activo
trade.entry_time       # Tiempo de entrada
trade.exit_time        # Tiempo de salida
trade.entry_price      # Precio de entrada
trade.exit_price       # Precio de salida
trade.quantity         # Cantidad
trade.side             # "long" o "short"
trade.pnl              # Profit & Loss
trade.pnl_percent      # PnL en porcentaje
trade.commission       # Comisión pagada
trade.duration_seconds # Duración del trade
trade.is_winner        # True si ganador
```

### BacktestResult
```python
# El resultado contiene todas las métricas
result.total_pnl              # PnL total
result.total_return_percent   # Retorno total %
result.sharpe_ratio           # Sharpe ratio
result.max_drawdown           # Max drawdown absoluto
result.max_drawdown_percent   # Max drawdown %
result.total_trades           # Total de trades
result.winning_trades         # Trades ganadores
result.losing_trades          # Trades perdedores
result.win_rate               # Win rate %
result.average_win            # Ganancia promedio
result.average_loss           # Pérdida promedio
result.profit_factor          # Profit factor
result.trades                 # Lista de trades
result.equity_curve           # DataFrame con equity
```

## 🔄 Flujo de Ejecución

```
1. Backtester inicializa Portfolio con capital inicial
2. Estrategia genera señales (-1, 0, 1) sobre datos
3. Para cada señal:
   - Se crea una Order
   - Portfolio valida fondos/posiciones
   - Se aplica slippage y comisión
   - Se ejecuta la orden
   - Se actualiza equity
4. Se cierran posiciones al final
5. MetricsCalculator calcula métricas
6. Retorna BacktestResult con todos los datos
```

## 🎯 Próximas Mejoras

- [ ] Multi-asset backtesting
- [ ] Event-driven mode para live trading
- [ ] Optimización de parámetros (grid search)
- [ ] Walk-forward analysis
- [ ] Risk management avanzado
- [ ] Integración con brokers (Alpaca, IB)
- [ ] Backtesting de opciones y futuros
- [ ] Machine learning strategies

## 📄 Licencia

MIT License
