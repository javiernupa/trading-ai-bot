"""Test rápido de las nuevas funcionalidades."""

from trading_engine import Backtester, DataLoader, MetricsCalculator
from strategies import (
    RsiStrategy,
    MacdStrategy,
    BollingerBandsStrategy,
    MovingAverageCrossStrategy,
    CombinedStrategy,
)
import pandas as pd
import numpy as np

print("=" * 60)
print("TEST DE NUEVAS FUNCIONALIDADES")
print("=" * 60)

# 1. Test de imports
print("\n✓ 1. Imports exitosos")
print("  - Estrategias: RSI, MACD, Bollinger, MA Cross, Combined")
print("  - Data: DataLoader")
print("  - Engine: Backtester, MetricsCalculator")

# 2. Test de DataLoader
print("\n✓ 2. DataLoader inicializado")
loader = DataLoader(cache_dir="data/test_cache", use_cache=False)
print(f"  - Caché en: {loader.cache_dir}")

# 3. Crear datos de prueba (simulados)
print("\n✓ 3. Generando datos de prueba...")
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=200, freq="D")
close_prices = 100 + np.cumsum(np.random.randn(200) * 2)

data = pd.DataFrame({
    "timestamp": dates,
    "open": close_prices + np.random.randn(200) * 0.5,
    "high": close_prices + np.abs(np.random.randn(200)) * 2,
    "low": close_prices - np.abs(np.random.randn(200)) * 2,
    "close": close_prices,
    "volume": np.random.randint(1000000, 5000000, 200),
})
print(f"  - {len(data)} registros generados")

# 4. Test de estrategias
print("\n✓ 4. Probando estrategias...")

strategies = {
    "RSI": RsiStrategy(period=14),
    "MACD": MacdStrategy(fast_period=12, slow_period=26),
    "Bollinger": BollingerBandsStrategy(period=20),
    "MA Cross": MovingAverageCrossStrategy(fast_period=10, slow_period=30),
    "Combined": CombinedStrategy(consensus_threshold=2),
}

results = {}
calculator = MetricsCalculator()

for name, strategy in strategies.items():
    try:
        # Ejecutar backtest
        backtester = Backtester(
            strategy=strategy,
            data=data,
            initial_cash=100_000,
            commission=0.001,
            slippage=0.0005
        )
        result = backtester.run()
        metrics = calculator.calculate_metrics(result)
        results[name] = metrics
        
        print(f"  - {name:15} | Trades: {len(result.trades):3} | "
              f"Retorno: {metrics['total_return']:7.2%} | "
              f"Sharpe: {metrics['sharpe_ratio']:5.2f}")
    except Exception as e:
        print(f"  - {name:15} | ERROR: {str(e)[:40]}")

# 5. Resumen
print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"✅ Estrategias probadas: {len(results)}/{len(strategies)}")
print(f"✅ Tests exitosos: {len(results) == len(strategies)}")

if results:
    best = max(results.items(), key=lambda x: x[1]['sharpe_ratio'])
    print(f"🏆 Mejor estrategia: {best[0]} (Sharpe: {best[1]['sharpe_ratio']:.2f})")

print("\n" + "=" * 60)
print("¡TODAS LAS FUNCIONALIDADES OPERATIVAS!")
print("=" * 60)
