# Estrategias de Trading Disponibles

Este documento describe todas las estrategias de trading implementadas en el sistema.

## Estrategias Implementadas

### 1. RSI Strategy (Índice de Fuerza Relativa)

**Descripción:** Estrategia basada en el indicador RSI que identifica condiciones de sobrecompra y sobreventa.

**Señales:**
- 🟢 **Compra:** RSI < umbral inferior (default: 30) - Activo sobrevend ido
- 🔴 **Venta:** RSI > umbral superior (default: 70) - Activo sobrecomprado

**Parámetros:**
```python
RsiStrategy(
    period=14,        # Período de cálculo del RSI
    lower_threshold=30,  # Umbral de sobreventa
    upper_threshold=70   # Umbral de sobrecompra
)
```

**Ejemplo:**
```python
from strategies import RsiStrategy
from trading_engine import Backtester

strategy = RsiStrategy(period=14, lower_threshold=35, upper_threshold=65)
backtester = Backtester(strategy=strategy, initial_capital=100_000)
result = backtester.run(data)
```

**Uso recomendado:** Mercados con movimientos laterales o mean-reverting.

---

### 2. MACD Strategy (Moving Average Convergence Divergence)

**Descripción:** Estrategia basada en el cruce del MACD con su línea de señal.

**Señales:**
- 🟢 **Compra:** MACD cruza por encima de la línea de señal (histograma pasa de negativo a positivo)
- 🔴 **Venta:** MACD cruza por debajo de la línea de señal (histograma pasa de positivo a negativo)

**Parámetros:**
```python
MacdStrategy(
    fast_period=12,    # Período EMA rápida
    slow_period=26,    # Período EMA lenta
    signal_period=9    # Período línea de señal
)
```

**Ejemplo:**
```python
from strategies import MacdStrategy

strategy = MacdStrategy(fast_period=12, slow_period=26, signal_period=9)
```

**Uso recomendado:** Mercados con tendencias claras, seguimiento de momentum.

---

### 3. Bollinger Bands Strategy (Bandas de Bollinger)

**Descripción:** Estrategia basada en las Bandas de Bollinger que identifica extremos de precio.

**Señales:**
- 🟢 **Compra:** Precio toca o cruza la banda inferior (oversold)
- 🔴 **Venta:** Precio toca o cruza la banda superior (overbought)

**Parámetros:**
```python
BollingerBandsStrategy(
    period=20,      # Período para la media móvil
    num_std=2.0     # Número de desviaciones estándar
)
```

**Ejemplo:**
```python
from strategies import BollingerBandsStrategy

strategy = BollingerBandsStrategy(period=20, num_std=2.0)
```

**Uso recomendado:** Mercados volátiles con reversiones a la media.

---

### 4. Moving Average Cross Strategy (Cruce de Medias Móviles)

**Descripción:** Estrategia clásica de cruce de medias móviles (Golden Cross / Death Cross).

**Señales:**
- 🟢 **Compra:** MA rápida cruza por encima de MA lenta (Golden Cross)
- 🔴 **Venta:** MA rápida cruza por debajo de MA lenta (Death Cross)

**Parámetros:**
```python
MovingAverageCrossStrategy(
    fast_period=50,     # Período MA rápida
    slow_period=200,    # Período MA lenta
    ma_type="sma"       # Tipo: 'sma' o 'ema'
)
```

**Ejemplos:**
```python
from strategies import MovingAverageCrossStrategy

# Estrategia clásica 50/200 SMA
strategy = MovingAverageCrossStrategy(
    fast_period=50, 
    slow_period=200, 
    ma_type="sma"
)

# Estrategia rápida 12/26 EMA
strategy = MovingAverageCrossStrategy(
    fast_period=12, 
    slow_period=26, 
    ma_type="ema"
)
```

**Uso recomendado:** Mercados con tendencias fuertes y sostenidas.

---

### 5. Combined Strategy (Estrategia Combinada)

**Descripción:** Estrategia avanzada que combina RSI, MACD y Bandas de Bollinger para señales de consenso.

**Señales:**
- 🟢 **Compra:** Al menos N indicadores coinciden en señal alcista
- 🔴 **Venta:** Al menos N indicadores coinciden en señal bajista

**Parámetros:**
```python
CombinedStrategy(
    # RSI
    rsi_period=14,
    rsi_lower=30,
    rsi_upper=70,
    # MACD
    macd_fast=12,
    macd_slow=26,
    macd_signal=9,
    # Bollinger Bands
    bb_period=20,
    bb_std=2.0,
    # Consenso
    consensus_threshold=2  # Mínimo de indicadores que deben coincidir
)
```

**Ejemplo:**
```python
from strategies import CombinedStrategy

# Consenso de 2 de 3 indicadores
strategy = CombinedStrategy(consensus_threshold=2)

# Consenso estricto: todos los indicadores
strategy = CombinedStrategy(consensus_threshold=3)
```

**Uso recomendado:** Reducir falsos positivos, señales más robustas pero menos frecuentes.

---

## Comparación de Estrategias

| Estrategia          | Complejidad | Frecuencia Señales | Mejor en          | Riesgo      |
|---------------------|-------------|-------------------|-------------------|-------------|
| RSI                 | Baja        | Alta              | Laterales         | Medio       |
| MACD                | Media       | Media             | Tendencias        | Medio-Alto  |
| Bollinger Bands     | Baja        | Media-Alta        | Volátil           | Alto        |
| MA Cross            | Baja        | Baja              | Tendencias largas | Bajo-Medio  |
| Combined            | Alta        | Baja              | Todos             | Bajo        |

## Ejemplo: Comparar Todas las Estrategias

```python
from strategies import (
    RsiStrategy,
    MacdStrategy,
    BollingerBandsStrategy,
    MovingAverageCrossStrategy,
    CombinedStrategy,
)
from trading_engine import Backtester, DataLoader, MetricsCalculator

# Cargar datos
loader = DataLoader()
data = loader.load_data("AAPL", "2023-01-01", "2024-01-01", provider="yahoo")

# Definir estrategias
strategies = {
    "RSI": RsiStrategy(),
    "MACD": MacdStrategy(),
    "Bollinger": BollingerBandsStrategy(),
    "MA Cross": MovingAverageCrossStrategy(fast_period=50, slow_period=200),
    "Combined": CombinedStrategy(consensus_threshold=2),
}

# Ejecutar backtests
results = {}
calculator = MetricsCalculator()

for name, strategy in strategies.items():
    backtester = Backtester(strategy=strategy, initial_capital=100_000)
    result = backtester.run(data)
    metrics = calculator.calculate_metrics(result)
    results[name] = metrics
    
    print(f"\n{name}:")
    print(f"  Retorno: {metrics['total_return']:.2%}")
    print(f"  Sharpe: {metrics['sharpe_ratio']:.2f}")
    print(f"  Max DD: {metrics['max_drawdown']:.2%}")

# Mejor estrategia
best = max(results.items(), key=lambda x: x[1]['sharpe_ratio'])
print(f"\n🏆 Mejor estrategia: {best[0]} (Sharpe: {best[1]['sharpe_ratio']:.2f})")
```

Usa el script proporcionado:
```bash
python examples/compare_strategies.py
```

## Crear Estrategias Personalizadas

### Plantilla Básica

```python
from strategies import BaseStrategy
import pandas as pd

class MyCustomStrategy(BaseStrategy):
    """Mi estrategia personalizada."""
    
    def __init__(self, param1: int = 10, param2: float = 0.5):
        """Inicializa la estrategia."""
        self.param1 = param1
        self.param2 = param2
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading.
        
        Args:
            data: DataFrame con columnas: timestamp, open, high, low, close, volume
            
        Returns:
            DataFrame con columna 'signal' añadida:
            - 1: Señal de compra
            - 0: Sin señal (mantener)
            - -1: Señal de venta
        """
        df = data.copy()
        
        # Tu lógica aquí
        # ...
        
        # Inicializar señales en 0
        df['signal'] = 0
        
        # Generar señales de compra
        df.loc[condicion_compra, 'signal'] = 1
        
        # Generar señales de venta
        df.loc[condicion_venta, 'signal'] = -1
        
        return df
```

### Ejemplo: Estrategia de Volatilidad

```python
from strategies import BaseStrategy
import pandas as pd

class VolatilityStrategy(BaseStrategy):
    """Compra en baja volatilidad, vende en alta volatilidad."""
    
    def __init__(self, window: int = 20, threshold: float = 1.5):
        self.window = window
        self.threshold = threshold
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # Calcular volatilidad (desviación estándar de retornos)
        returns = df['close'].pct_change()
        volatility = returns.rolling(window=self.window).std()
        
        # Volatilidad relativa
        vol_mean = volatility.rolling(window=50).mean()
        vol_ratio = volatility / vol_mean
        
        df['signal'] = 0
        df.loc[vol_ratio < 1 / self.threshold, 'signal'] = 1  # Baja vol
        df.loc[vol_ratio > self.threshold, 'signal'] = -1     # Alta vol
        
        return df
```

## Optimización de Parámetros

```python
from strategies import RsiStrategy
from trading_engine import Backtester, DataLoader, MetricsCalculator

loader = DataLoader()
data = loader.load_data("AAPL", "2023-01-01", "2024-01-01")

# Grid search
best_sharpe = -999
best_params = None

for period in [10, 12, 14, 16, 18, 20]:
    for lower in [20, 25, 30, 35]:
        for upper in [65, 70, 75, 80]:
            strategy = RsiStrategy(
                period=period,
                lower_threshold=lower,
                upper_threshold=upper
            )
            
            backtester = Backtester(strategy=strategy, initial_capital=100_000)
            result = backtester.run(data)
            
            calculator = MetricsCalculator()
            metrics = calculator.calculate_metrics(result)
            
            if metrics['sharpe_ratio'] > best_sharpe:
                best_sharpe = metrics['sharpe_ratio']
                best_params = (period, lower, upper)

print(f"Mejores parámetros: period={best_params[0]}, "
      f"lower={best_params[1]}, upper={best_params[2]}")
print(f"Sharpe Ratio: {best_sharpe:.2f}")
```

## Próximas Estrategias

En desarrollo:
- 🔜 Mean Reversion Strategy
- 🔜 Momentum Strategy
- 🔜 Pairs Trading
- 🔜 Machine Learning Strategy
- 🔜 Sentiment Analysis Strategy
