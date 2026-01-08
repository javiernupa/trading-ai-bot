# 💰 Inicio Rápido - Crypto Trading

Guía de **5 minutos** para empezar a operar criptomonedas con Alpaca.

## 🚀 Setup en 3 Pasos

### 1️⃣ Habilita Crypto en Alpaca

1. Ve a [Alpaca Dashboard](https://app.alpaca.markets/)
2. En **Paper Trading**, ve a **Settings**
3. Habilita **Crypto Trading**
4. ¡Listo! Las mismas API keys funcionan

### 2️⃣ Test de Conexión

```bash
# Verifica que todo funcione
python examples/test_crypto_connection.py
```

**Deberías ver:**
```
✅ BTC/USD: $90,000.00
✅ ETH/USD: $3,050.00
✅ SOL/USD: $127.00
```

### 3️⃣ Trading en Vivo

```bash
# Ejecuta el bot de crypto
python examples/live_trading_crypto.py
```

**¡Ya estás operando criptomonedas! 🎉**

---

## 💡 Diferencias Clave vs Stocks

| Aspecto | Stocks | Criptomonedas |
|---------|--------|---------------|
| **Horario** | 9:30-16:00 ET | **24/7** |
| **Volatilidad** | Baja-Media | **ALTA** |
| **Stop Loss** | 2% | **5-10%** |
| **Take Profit** | 5% | **10-20%** |
| **Capital** | $20k/símbolo | **$5k/símbolo** |
| **Actualización** | 5 min | **1 min** |

---

## ⚙️ Configuración Recomendada

### Conservador (Inicio)
```python
SYMBOLS = ["BTC/USD", "ETH/USD"]        # Solo majors
CAPITAL_PER_SYMBOL = 2_000              # $2k cada uno
STOP_LOSS_PCT = 0.10                    # 10% stop loss
TAKE_PROFIT_PCT = 0.20                  # 20% take profit
UPDATE_INTERVAL = 300                   # 5 minutos
TIMEFRAME = "1Hour"                     # Barras de 1 hora
LOOKBACK_DAYS = 5                       # 5 días = 120 horas
```

### Moderado (Recomendado)
```python
SYMBOLS = ["BTC/USD", "ETH/USD", "SOL/USD"]
CAPITAL_PER_SYMBOL = 5_000              # $5k cada uno
STOP_LOSS_PCT = 0.05                    # 5% stop loss
TAKE_PROFIT_PCT = 0.10                  # 10% take profit
UPDATE_INTERVAL = 60                    # 1 minuto
TIMEFRAME = "1Hour"                     # Barras de 1 hora
LOOKBACK_DAYS = 3                       # 3 días = 72 horas
```

### Agresivo (Experiencia)
```python
SYMBOLS = ["BTC/USD", "ETH/USD", "SOL/USD", "AVAX/USD", "DOGE/USD"]
CAPITAL_PER_SYMBOL = 10_000             # $10k cada uno
STOP_LOSS_PCT = 0.03                    # 3% stop loss
TAKE_PROFIT_PCT = 0.08                  # 8% take profit
UPDATE_INTERVAL = 30                    # 30 segundos
TIMEFRAME = "15Min"                     # Barras de 15 minutos (más rápido)
LOOKBACK_DAYS = 2                       # 2 días = 192 barras de 15min
```

---

## 🎯 Criptos Recomendadas

### Para Principiantes
```python
SYMBOLS = ["BTC/USD", "ETH/USD"]
```
- ✅ Muy líquidas
- ✅ Menos volátiles
- ✅ Fáciles de predecir

### Para Intermedios
```python
SYMBOLS = ["BTC/USD", "ETH/USD", "SOL/USD"]
```
- ✅ Diversificación
- ✅ Balance riesgo/retorno
- ✅ Buena liquidez

### Para Avanzados
```python
SYMBOLS = ["BTC/USD", "ETH/USD", "SOL/USD", "AVAX/USD", "LINK/USD"]
```
- ⚠️ Mayor volatilidad
- ⚠️ Altcoins más arriesgadas
- ✅ Mayor potencial de ganancia

---

## 🛡️ Reglas de Seguridad

### ❌ NO Hagas Esto
```python
# NO uses stop loss muy ajustado
STOP_LOSS_PCT = 0.01  # ❌ 1% es demasiado pequeño

# NO operes muchas criptos pequeñas
SYMBOLS = ["DOGE/USD", "SHIB/USD", "PEPE/USD"]  # ❌ Muy arriesgado

# NO uses todo tu capital
CAPITAL_PER_SYMBOL = 50_000  # ❌ Demasiado en una sola cripto
```

### ✅ Sí Haz Esto
```python
# SÍ usa stop loss amplio
STOP_LOSS_PCT = 0.05  # ✅ 5% da margen

# SÍ diversifica inteligentemente
SYMBOLS = ["BTC/USD", "ETH/USD", "SOL/USD"]  # ✅ Balance

# SÍ gestiona capital prudentemente
CAPITAL_PER_SYMBOL = 5_000  # ✅ Razonable
```

---

## 📊 Ejemplo Completo

```python
from strategies import CombinedStrategy
from trading_engine.brokers.alpaca_broker import AlpacaBroker
from trading_engine.data.crypto_provider import AlpacaCryptoProvider
from trading_engine.live_engine import MultiSymbolLiveEngine
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Configuración
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# 2. Broker (igual que stocks)
broker = AlpacaBroker(
    api_key=API_KEY,
    secret_key=SECRET_KEY,
    paper=True  # Paper trading primero!
)

# 3. Proveedor de datos CRYPTO
crypto_provider = AlpacaCryptoProvider(
    api_key=API_KEY,
    secret_key=SECRET_KEY
)

# 4. Estrategia
strategy = CombinedStrategy(consensus_threshold=2)

# 5. Motor de trading
engine = MultiSymbolLiveEngine(
    symbols=["BTC/USD", "ETH/USD"],
    strategy=strategy,
    broker=broker,
    data_provider=crypto_provider,  # <- Usar crypto provider
    capital_per_symbol=5000,
    stop_loss_pct=0.05,
    take_profit_pct=0.10,
    update_interval=60,
    timeframe="1Hour",              # <- Barras de 1 hora
    lookback_days=3                 # <- 3 días = 72 horas
)

# 6. ¡Iniciar!
engine.start()
```

---

## 🎓 Tips Importantes

### 1. Volatilidad
```
Las criptos se mueven 5-20% en un día

✅ NO te asustes por movimientos del 5%
✅ Usa stop loss más amplios (5-10%)
❌ NO uses stop loss de 1-2%
```

### 2. Horario 24/7
```
Las criptos operan día y noche

✅ Usa stop loss SIEMPRE
✅ Define horarios de monitoreo
❌ NO intentes monitorear 24/7
```

### 3. Liquidez
```
No todas las criptos son iguales

✅ BTC/USD, ETH/USD: Excelente liquidez
✅ SOL/USD, AVAX/USD: Buena liquidez
⚠️ Criptos pequeñas: Verifica spread
```

### 4. Gestión Emocional
```
Las criptos disparan emociones

✅ Define tu plan ANTES de operar
✅ Respeta tus stop loss
❌ NO cambies tu estrategia por pánico
```

---

## 🔧 Troubleshooting Rápido

### "Crypto trading not enabled"
```bash
1. Ve a Alpaca Dashboard
2. Settings → Enable Crypto Trading
3. Espera 5 minutos
4. Reinicia el script
```

### Stop Loss se ejecuta constantemente
```python
# Amplía stop loss
STOP_LOSS_PCT = 0.10  # 10% en lugar de 5%
```

### No se generan señales
```python
# Baja el threshold
strategy = CombinedStrategy(consensus_threshold=1)
```

### "Insufficient buying power"
```python
# Reduce capital
CAPITAL_PER_SYMBOL = 1_000  # $1k en lugar de $5k
```

---

## 📈 Próximos Pasos

1. **Lee la guía completa:** [CRYPTO_TRADING.md](CRYPTO_TRADING.md)
2. **Experimenta en paper:** Prueba diferentes configuraciones
3. **Analiza resultados:** Revisa qué funciona mejor
4. **Ajusta estrategia:** Usa [STRATEGY_TUNING.md](STRATEGY_TUNING.md)
5. **Opera con prudencia:** Empieza pequeño, crece gradualmente

---

**⚠️ IMPORTANTE:** Las criptomonedas son de **ALTO RIESGO**. Solo opera con capital que puedas permitirte perder. Este sistema es **educativo**.

💰 **¡Éxito en tu trading crypto!**
