import pandas as pd
import numpy as np
from strategies import load_strategies_from_env, CombinedStrategy

# Cargar estrategias
print("Cargando estrategias...")
strategies, consensus = load_strategies_from_env()
strategy = CombinedStrategy(strategies, consensus)

# Crear datos simulados
print("\nGenerando datos simulados...")
dates = pd.date_range(start='2024-01-01', periods=300, freq='H')
data = pd.DataFrame({
    'timestamp': dates,
    'open': np.random.uniform(80, 85, 300),
    'high': np.random.uniform(85, 90, 300),
    'low': np.random.uniform(75, 80, 300),
    'close': np.random.uniform(80, 85, 300),
    'volume': np.random.randint(100000, 200000, 300)
})

# Generar señales
print("Generando señales...")
result = strategy.generate_signals(data)

# Mostrar todas las columnas que terminan en _signal
print("\n" + "="*70)
print("TODAS las columnas que terminan en '_signal':")
print("="*70)
signal_cols = [col for col in result.columns if col.endswith("_signal")]
for col in sorted(signal_cols):
    print(f"  {col}")
    
print("\n" + "="*70)
print("Columnas con 'strategy_' y terminan en '_signal':")
print("="*70)
strategy_signal_cols = [col for col in result.columns if col.endswith("_signal") and "strategy_" in col]
for col in sorted(strategy_signal_cols):
    parts = col.split("_")
    is_valid = len(parts) >= 3 and parts[-1] == "signal" and parts[-2].isdigit()
    print(f"  {col}")
    print(f"    -> parts={parts}")
    print(f"    -> last={parts[-1]}, second_last={parts[-2] if len(parts) >= 2 else 'N/A'}")
    print(f"    -> válido={is_valid}")
