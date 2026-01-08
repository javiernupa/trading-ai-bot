"""Ejemplo básico de uso del backtester con RSI."""

import pandas as pd
from trading_engine.backtest import Backtester
from trading_engine.metrics import MetricsCalculator
from strategies.rsi import RsiStrategy

# Datos de ejemplo
df = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", periods=15, freq="D"),
    "close": [100, 101, 102, 101, 99, 98, 100, 102, 105, 104, 103, 105, 106, 108, 107],
})

# Crear estrategia
strategy = RsiStrategy(period=5, lower=30, upper=70)

# Ejecutar backtest
backtester = Backtester(strategy, df, initial_cash=10000)
result = backtester.run()

# Mostrar resultados
MetricsCalculator.print_summary(result)

print("\nTrades realizados:")
for i, trade in enumerate(result.trades, 1):
    print(f"{i}. PnL: ${trade.pnl:+,.2f} ({trade.pnl_percent:+.2f}%)")
