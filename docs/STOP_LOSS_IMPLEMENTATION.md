# 🛡️ Stop Loss y Take Profit - Implementación Completa

## ✅ Implementado

Se ha añadido soporte completo para **Stop Loss** y **Take Profit** automáticos en el sistema de trading con Alpaca Markets.

## 📦 Componentes Modificados

### 1. AlpacaBroker ([alpaca_broker.py](../engine/src/trading_engine/brokers/alpaca_broker.py))

**Cambios:**
- ✅ Importación de `StopLossRequest` y `TakeProfitRequest` de Alpaca
- ✅ Modificación de `submit_order()` para aceptar `stop_loss_pct` y `take_profit_pct`
- ✅ Creación automática de bracket orders (orden + stop loss + take profit)
- ✅ Logging mejorado mostrando niveles de SL y TP

**Uso:**
```python
broker.submit_order(
    order,
    stop_loss_pct=0.02,  # 2% stop loss
    take_profit_pct=0.05  # 5% take profit
)
```

### 2. MultiSymbolLiveEngine ([live_engine.py](../engine/src/trading_engine/live_engine.py))

**Cambios:**
- ✅ Nuevos parámetros en `__init__()`: `stop_loss_pct` y `take_profit_pct`
- ✅ Valores por defecto: 2% SL, 5% TP
- ✅ `_execute_buy()` envía órdenes con stop loss y take profit
- ✅ Logging mejorado con emojis 🛡️ y 🎯
- ✅ Información de niveles en cada compra

**Configuración:**
```python
engine = MultiSymbolLiveEngine(
    symbols=["AAPL", "MSFT"],
    strategy=strategy,
    broker=broker,
    data_provider=data_provider,
    stop_loss_pct=0.02,  # 2% SL (configurable)
    take_profit_pct=0.05,  # 5% TP (configurable)
)
```

### 3. Ejemplo Actualizado ([live_trading_alpaca.py](../examples/live_trading_alpaca.py))

**Cambios:**
- ✅ Variables `STOP_LOSS_PCT` y `TAKE_PROFIT_PCT` configurables
- ✅ Motor inicializado con stop loss y take profit
- ✅ Información de gestión de riesgo en output

**Salida mejorada:**
```
🛡️ Gestión de Riesgo:
  Stop Loss: 2.0% (-$400 máx por posición)
  Take Profit: 5.0% (+$1,000 objetivo)

🟢 AAPL: COMPRA 111 @ $180.00 (Total: $19,980.00) 
   | 🛡️ SL: $176.40 | 🎯 TP: $189.00 | Order ID: xxx
```

## 📄 Documentación Creada

### 1. [RISK_MANAGEMENT.md](RISK_MANAGEMENT.md) (NUEVO)
Guía completa de gestión de riesgo:
- ✅ Explicación de stop loss y take profit
- ✅ Configuraciones recomendadas (conservador, moderado, agresivo)
- ✅ Ejemplos de cálculo de riesgo
- ✅ Mejores prácticas
- ✅ Troubleshooting
- ✅ ~500 líneas de documentación

### 2. [QUICKSTART_ALPACA.md](QUICKSTART_ALPACA.md)
Actualizado con información de stop loss

### 3. [ALPACA_LIVE_TRADING.md](ALPACA_LIVE_TRADING.md)
Actualizado con sección de bracket orders

### 4. [demo_stop_loss.py](../examples/demo_stop_loss.py) (NUEVO)
Script interactivo que muestra:
- ✅ Cómo funcionan las bracket orders
- ✅ Gestión de riesgo en portfolio
- ✅ Comparación de configuraciones
- ✅ Simulaciones de precios

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# Gestión de Riesgo
STOP_LOSS_PCT=0.02  # 2% stop loss automático
TAKE_PROFIT_PCT=0.05  # 5% take profit automático
```

### Configuraciones Recomendadas

| Perfil | Stop Loss | Take Profit | Ratio | Uso |
|--------|-----------|-------------|-------|-----|
| **Conservador** | 1% | 3% | 1:3 | Capital limitado |
| **Moderado** ⭐ | 2% | 5% | 1:2.5 | Recomendado |
| **Agresivo** | 5% | 15% | 1:3 | Alto riesgo |
| **Day Trading** | 0.5% | 1% | 1:2 | Intraday |
| **Swing Trading** | 3% | 10% | 1:3.3 | Varios días |

⭐ = Configuración por defecto

## 🔍 Funcionamiento

### Cuando compras una acción:

1. **Sistema detecta señal de compra** (RSI, MACD, etc.)
2. **Calcula cantidad** basada en capital asignado
3. **Envía bracket order a Alpaca:**
   - Orden principal: `BUY 111 AAPL @ Market`
   - Stop Loss: `SELL 111 AAPL @ $176.40 (stop)`
   - Take Profit: `SELL 111 AAPL @ $189.00 (limit)`

### Alpaca monitorea automáticamente:

- Si precio ≤ $176.40 → 🛡️ **STOP LOSS ejecutado** (pérdida: 2%)
- Si precio ≥ $189.00 → 🎯 **TAKE PROFIT ejecutado** (ganancia: 5%)
- Una vez ejecutado, la otra orden se cancela automáticamente

### Sin intervención manual:

- ✅ Funciona 24/7, incluso si apagas tu computadora
- ✅ Ejecución instantánea al alcanzar niveles
- ✅ Elimina decisiones emocionales
- ✅ Protege tu capital mientras duermes

## 📊 Ejemplo Práctico

### Compra con Stop Loss y Take Profit:

```python
# Configuración
Symbol: AAPL
Entry: $180.00
Quantity: 111
Capital: $19,980

# Niveles automáticos
Stop Loss: $176.40 (-2%) → Pérdida máxima: $400
Take Profit: $189.00 (+5%) → Ganancia objetivo: $1,000

# Ratio riesgo:beneficio: 1:2.5
# Arriesgas $400 para ganar $1,000
```

### Portfolio completo (5 acciones):

```
Total Capital: $100,000
Capital por símbolo: $20,000

Stop Loss: 2% por posición
- Pérdida máxima por símbolo: $400
- Pérdida máxima total: $2,000 (2% del portfolio)

Take Profit: 5% por posición
- Ganancia objetivo por símbolo: $1,000
- Ganancia objetivo total: $5,000 (5% del portfolio)
```

## 🚀 Cómo Usar

### 1. Ejecutar Demo
```bash
python examples/demo_stop_loss.py
```

### 2. Trading en Vivo con Stop Loss
```bash
# Usar valores por defecto (2% SL, 5% TP)
python examples/live_trading_alpaca.py
```

### 3. Personalizar en el código:

```python
from trading_engine.live_engine import MultiSymbolLiveEngine

# Sin stop loss ni take profit
engine = MultiSymbolLiveEngine(
    ...,
    stop_loss_pct=None,  # Desactivado
    take_profit_pct=None  # Desactivado
)

# Solo stop loss
engine = MultiSymbolLiveEngine(
    ...,
    stop_loss_pct=0.03,  # 3%
    take_profit_pct=None  # Desactivado
)

# Agresivo
engine = MultiSymbolLiveEngine(
    ...,
    stop_loss_pct=0.05,  # 5%
    take_profit_pct=0.15  # 15%
)
```

## 📈 Ventajas

1. **Protección Automática** - No necesitas monitorear constantemente
2. **Gestión de Riesgo** - Pérdida máxima conocida de antemano
3. **Disciplina** - Elimina decisiones emocionales
4. **Sin Intervención** - Funciona 24/7 automáticamente
5. **Velocidad** - Ejecución instantánea al alcanzar niveles

## ⚠️ Consideraciones

1. **Slippage** - En mercados volátiles, el precio puede variar ligeramente
2. **Gaps** - Si el mercado abre con gap, se ejecuta al primer precio disponible
3. **Volatilidad** - Stop loss muy ajustado → salidas frecuentes
4. **Comisiones** - Cada ejecución cuenta como trade
5. **Horario** - Solo se ejecuta durante horario de mercado

## 🧪 Testing

```bash
# 1. Ejecutar demo
python examples/demo_stop_loss.py

# 2. Test de conexión a Alpaca
python examples/test_alpaca_connection.py

# 3. Paper trading con stop loss
python examples/live_trading_alpaca.py
```

## 📚 Recursos

- [RISK_MANAGEMENT.md](RISK_MANAGEMENT.md) - Guía completa de gestión de riesgo
- [ALPACA_LIVE_TRADING.md](ALPACA_LIVE_TRADING.md) - Documentación de Alpaca
- [Alpaca Bracket Orders](https://docs.alpaca.markets/docs/orders#bracket-orders) - Documentación oficial

## 🎯 Próximos Pasos

Funcionalidades futuras:

- [ ] Trailing Stop Loss (ajuste automático si precio sube)
- [ ] Stop Loss basado en ATR (volatilidad)
- [ ] Partial Take Profit (cerrar posición en etapas)
- [ ] Time-based stops (cerrar después de X tiempo)
- [ ] Backtesting con stop loss y take profit

## 📊 Métricas

Analiza en Alpaca Dashboard:

- **Win Rate con Stops:** % trades que alcanzan TP vs SL
- **Average Win:** Ganancia promedio en TPs
- **Average Loss:** Pérdida promedio en SLs  
- **Profit Factor:** (Total TP) / (Total SL) → >1.5 es bueno

---

✅ **Implementación completa de Stop Loss y Take Profit**

🛡️ **Protege tu capital. Opera con disciplina.**

---

**Fecha de implementación:** 22 de diciembre de 2024  
**Versión:** 1.0.0  
**Status:** ✅ PRODUCTION READY
