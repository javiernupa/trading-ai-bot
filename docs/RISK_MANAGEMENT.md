# 🛡️ Gestión de Riesgo con Stop Loss y Take Profit

Sistema de protección automática de posiciones con Alpaca Markets.

## 🎯 ¿Qué son?

### Stop Loss
- **Orden automática** que cierra la posición si el precio cae un % determinado
- **Protege contra pérdidas** mayores
- **Se ejecuta automáticamente** sin intervención

**Ejemplo:**
```
Compra: 100 AAPL @ $180
Stop Loss: 2% → $176.40
Si el precio baja a $176.40, se vende automáticamente
Pérdida máxima: $360 (2%)
```

### Take Profit
- **Orden automática** que cierra la posición si el precio sube un % determinado
- **Asegura ganancias** al alcanzar objetivo
- **Se ejecuta automáticamente** sin intervención

**Ejemplo:**
```
Compra: 100 AAPL @ $180
Take Profit: 5% → $189
Si el precio sube a $189, se vende automáticamente
Ganancia asegurada: $900 (5%)
```

## ⚙️ Configuración

### En .env

```env
# Gestión de Riesgo
STOP_LOSS_PCT=0.02  # 2% stop loss
TAKE_PROFIT_PCT=0.05  # 5% take profit
```

### En el código

```python
from trading_engine.live_engine import MultiSymbolLiveEngine

engine = MultiSymbolLiveEngine(
    symbols=["AAPL", "MSFT", "GOOGL"],
    strategy=strategy,
    broker=broker,
    data_provider=data_provider,
    stop_loss_pct=0.02,  # 2% stop loss
    take_profit_pct=0.05,  # 5% take profit
)
```

### Desactivar

```python
# Sin stop loss ni take profit
engine = MultiSymbolLiveEngine(
    ...,
    stop_loss_pct=None,  # Desactivado
    take_profit_pct=None,  # Desactivado
)

# Solo stop loss
engine = MultiSymbolLiveEngine(
    ...,
    stop_loss_pct=0.02,  # 2%
    take_profit_pct=None,  # Desactivado
)
```

## 📊 Ejemplos de Configuración

### Conservador (Riesgo Bajo)
```python
stop_loss_pct=0.01  # 1% - pérdida máxima muy pequeña
take_profit_pct=0.03  # 3% - objetivo moderado
# Ratio 1:3 (riesgo:beneficio)
```

**Perfil:**
- Protección máxima
- Salidas frecuentes en pérdidas pequeñas
- Ideal para capital limitado

### Moderado (Recomendado)
```python
stop_loss_pct=0.02  # 2% - pérdida controlada
take_profit_pct=0.05  # 5% - objetivo razonable
# Ratio 1:2.5 (riesgo:beneficio)
```

**Perfil:**
- Balance entre protección y oportunidad
- **Configuración por defecto**
- Ideal para la mayoría de casos

### Agresivo (Riesgo Alto)
```python
stop_loss_pct=0.05  # 5% - pérdida mayor
take_profit_pct=0.15  # 15% - objetivo ambicioso
# Ratio 1:3 (riesgo:beneficio)
```

**Perfil:**
- Permite más volatilidad
- Busca ganancias mayores
- Requiere más capital

### Swing Trading
```python
stop_loss_pct=0.03  # 3%
take_profit_pct=0.10  # 10%
# Para posiciones de varios días
```

### Day Trading
```python
stop_loss_pct=0.005  # 0.5%
take_profit_pct=0.01  # 1%
# Para posiciones intraday
```

## 🔍 Cómo Funciona

### 1. Apertura de Posición

```python
# Usuario ejecuta:
engine.start()

# Sistema detecta señal de compra en AAPL @ $180
# Capital: $20,000 → Compra 111 acciones

# Alpaca crea automáticamente 3 órdenes:
# 1. Orden principal: BUY 111 AAPL @ Market
# 2. Stop Loss: SELL 111 AAPL @ $176.40 (stop)
# 3. Take Profit: SELL 111 AAPL @ $189.00 (limit)
```

### 2. Monitoreo Automático

Alpaca monitorea el precio continuamente:

```
Precio actual: $182 → Sin acción
Precio actual: $177 → Sin acción
Precio actual: $176.40 → ⚠️ STOP LOSS ejecutado
O
Precio actual: $189 → 🎯 TAKE PROFIT ejecutado
```

### 3. Ejecución

- **Solo una** de las órdenes se ejecuta
- La otra se **cancela automáticamente**
- **Sin intervención manual** necesaria

## 📈 Ventajas

### ✅ Protección 24/7
- Funciona incluso si apagas el sistema
- No necesitas estar monitoreando constantemente
- Protege contra gaps y movimientos bruscos

### ✅ Disciplina
- Elimina decisiones emocionales
- Sigue el plan de trading estrictamente
- Evita "esperar que se recupere"

### ✅ Automatización
- Sin intervención manual
- Velocidad de ejecución instantánea
- Reduce errores humanos

### ✅ Gestión de Riesgo
- Pérdida máxima conocida de antemano
- Capital protegido
- Permite dormir tranquilo

## ⚠️ Consideraciones

### 1. Slippage
- En mercados volátiles, el precio de ejecución puede variar ligeramente
- Stop loss garantiza que **no perderás más** del porcentaje, pero puede ejecutarse a un precio ligeramente peor

### 2. Gaps
- Si el mercado abre con gap (salto de precio), el stop loss se ejecuta al primer precio disponible
- Puede resultar en pérdida ligeramente mayor al esperado

### 3. Volatilidad
- Stop loss muy ajustado → Salidas frecuentes en movimientos normales
- Stop loss muy amplio → Mayor riesgo, pero menos salidas prematuras

### 4. Comisiones
- Cada ejecución (stop loss o take profit) cuenta como trade
- Considera las comisiones en tu cálculo de rentabilidad

## 📊 Cálculo de Riesgo

### Por Posición

```python
capital_per_symbol = 20000  # $20k
stop_loss_pct = 0.02  # 2%

# Pérdida máxima por posición
max_loss = capital_per_symbol * stop_loss_pct
# = $20,000 * 0.02 = $400

# Ganancia objetivo
take_profit_value = capital_per_symbol * take_profit_pct
# = $20,000 * 0.05 = $1,000
```

### Portfolio Completo

```python
# 5 símbolos con $20k cada uno
total_capital = 100000  # $100k
stop_loss_pct = 0.02  # 2%
num_symbols = 5

# Pérdida máxima si todos los stop loss se ejecutan
max_total_loss = total_capital * stop_loss_pct
# = $100,000 * 0.02 = $2,000 (2% del total)

# Por símbolo
max_loss_per_symbol = max_total_loss / num_symbols
# = $2,000 / 5 = $400 por símbolo
```

## 🔧 Ajuste Dinámico

### Trailing Stop Loss (Próximamente)
```python
# Stop loss que se ajusta automáticamente si el precio sube
trailing_stop_pct = 0.02  # 2% trailing

# Compra: $180
# Stop Loss inicial: $176.40
# Precio sube a $190
# Stop Loss ajustado: $186.20 (conserva 2% de $190)
```

### Stop Loss Basado en ATR (Próximamente)
```python
# Stop loss dinámico basado en volatilidad del símbolo
atr_multiplier = 2.0  # 2x ATR

# Símbolo volátil → Stop loss más amplio
# Símbolo estable → Stop loss más ajustado
```

## 📝 Mejores Prácticas

### 1. Define tu Riesgo Máximo
```python
# Regla general: No más del 1-2% del capital por trade
account_equity = 100000  # $100k
max_risk_per_trade = 0.01  # 1%
max_loss = account_equity * max_risk_per_trade  # $1,000

# Con 5 posiciones
capital_per_position = 20000  # $20k
stop_loss_pct = max_loss / capital_per_position  # 5% stop loss
```

### 2. Ratio Riesgo:Beneficio
```python
# Recomendado: Al menos 1:2 (arriesgas $1 para ganar $2)
stop_loss_pct = 0.02  # 2%
take_profit_pct = stop_loss_pct * 2  # 4% (ratio 1:2)

# Ideal: 1:3
take_profit_pct = stop_loss_pct * 3  # 6% (ratio 1:3)
```

### 3. Backtesting
```python
# Prueba diferentes configuraciones con datos históricos
from trading_engine import Backtester

# Test 1: Conservador
result_1 = backtest_with_stops(stop_loss=0.01, take_profit=0.03)

# Test 2: Moderado
result_2 = backtest_with_stops(stop_loss=0.02, take_profit=0.05)

# Test 3: Agresivo
result_3 = backtest_with_stops(stop_loss=0.05, take_profit=0.15)

# Comparar resultados
```

### 4. Monitoreo
- Revisa qué porcentaje de trades alcanzan stop loss vs take profit
- Si >60% alcanzan stop loss → Stop muy ajustado o estrategia deficiente
- Si >70% alcanzan take profit → Excelente, pero verifica que no estés dejando ganancias sobre la mesa

## 📚 Ejemplo Completo

```python
"""Trading con stop loss y take profit."""

import os
from dotenv import load_dotenv

from strategies import CombinedStrategy
from trading_engine.brokers.alpaca_broker import AlpacaBroker
from trading_engine.data.alpaca_provider import AlpacaDataProvider
from trading_engine.live_engine import MultiSymbolLiveEngine

load_dotenv()

# Configuración
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Portfolio
SYMBOLS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
CAPITAL_PER_SYMBOL = 20000  # $20k por símbolo

# Gestión de Riesgo
STOP_LOSS_PCT = 0.02  # 2% pérdida máxima
TAKE_PROFIT_PCT = 0.05  # 5% ganancia objetivo

# Broker y Data
broker = AlpacaBroker(api_key=API_KEY, secret_key=SECRET_KEY, paper=True)
data_provider = AlpacaDataProvider(api_key=API_KEY, secret_key=SECRET_KEY)
strategy = CombinedStrategy(consensus_threshold=2)

# Motor con stop loss y take profit
engine = MultiSymbolLiveEngine(
    symbols=SYMBOLS,
    strategy=strategy,
    broker=broker,
    data_provider=data_provider,
    capital_per_symbol=CAPITAL_PER_SYMBOL,
    stop_loss_pct=STOP_LOSS_PCT,
    take_profit_pct=TAKE_PROFIT_PCT,
)

# Iniciar
print(f"Stop Loss: {STOP_LOSS_PCT:.1%} → Pérdida máxima: ${CAPITAL_PER_SYMBOL * STOP_LOSS_PCT:,.0f} por posición")
print(f"Take Profit: {TAKE_PROFIT_PCT:.1%} → Ganancia objetivo: ${CAPITAL_PER_SYMBOL * TAKE_PROFIT_PCT:,.0f} por posición")
print(f"Pérdida máxima total: ${len(SYMBOLS) * CAPITAL_PER_SYMBOL * STOP_LOSS_PCT:,.0f}")

engine.start()
```

**Salida:**
```
🟢 AAPL: COMPRA 111 @ $180.00 (Total: $19,980.00) | 🛡️ SL: $176.40 | 🎯 TP: $189.00

Riesgo: $400 (-2%)
Objetivo: $1,000 (+5%)
Ratio: 1:2.5
```

## 🚨 Troubleshooting

### Stop Loss no se ejecuta

1. **Verifica que la orden se creó:**
   ```python
   # Revisa en Alpaca Dashboard → Orders
   # Debe haber 3 órdenes: Market, Stop, Limit
   ```

2. **Verifica el tipo de cuenta:**
   - Paper trading simula todo correctamente
   - Cuenta live debe tener fondos suficientes

3. **Horario de mercado:**
   - Stop loss solo se ejecuta durante horario de mercado
   - Si el precio cae fuera de horario, se ejecuta en la apertura

### Take Profit muy ajustado

- Si nunca alcanza take profit → Incrementa el porcentaje
- Si siempre alcanza stop loss primero → Revisa tu estrategia

### Muchas salidas prematuras

- Stop loss muy ajustado para la volatilidad del símbolo
- Considera usar ATR o ampliar el stop loss

## 📈 Métricas Importantes

Analiza en Alpaca Dashboard:

- **Win Rate con Stops:** % de trades que alcanzan TP vs SL
- **Average Win:** Ganancia promedio en TPs
- **Average Loss:** Pérdida promedio en SLs
- **Profit Factor:** (Total TP) / (Total SL) → Debe ser >1.5

---

**⚠️ IMPORTANTE:** Stop loss y take profit son herramientas de gestión de riesgo, no garantizan ganancias. Úsalos junto con una estrategia sólida y backtesting exhaustivo.

🛡️ **Protege tu capital. Opera con disciplina.**
