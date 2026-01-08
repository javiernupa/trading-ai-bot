# 💰 Trading de Criptomonedas con Alpaca

Guía completa para operar criptomonedas en Alpaca Markets.

## 🚀 Características

- ✅ **Trading 24/7** - Las criptomonedas operan sin parar
- ✅ **Sin comisiones** - Alpaca no cobra comisiones en crypto
- ✅ **Fragmentación** - Compra fracciones de Bitcoin (0.001 BTC, etc.)
- ✅ **Mismo sistema** - Usa las mismas estrategias que stocks
- ✅ **Paper Trading** - Prueba con dinero simulado primero

## 📊 Criptomonedas Disponibles

Alpaca soporta las principales criptomonedas:

| Símbolo | Nombre | Típico Capital |
|---------|--------|----------------|
| BTC/USD | Bitcoin | $5,000+ |
| ETH/USD | Ethereum | $2,000+ |
| SOL/USD | Solana | $500+ |
| AVAX/USD | Avalanche | $300+ |
| DOGE/USD | Dogecoin | $100+ |
| LTC/USD | Litecoin | $500+ |
| BCH/USD | Bitcoin Cash | $500+ |
| LINK/USD | Chainlink | $300+ |
| UNI/USD | Uniswap | $300+ |

## ⚙️ Configuración

### 1. Habilitar Crypto Trading en Alpaca

1. Ve a [Alpaca Dashboard](https://app.alpaca.markets/)
2. En **Paper Trading**, ve a Settings
3. Habilita **Crypto Trading**
4. Las mismas API keys funcionan para stocks y crypto

### 2. Variables de Entorno

Usa las mismas credenciales que para stocks:

```env
ALPACA_API_KEY=your_key_here
ALPACA_SECRET_KEY=your_secret_here
```

## 🎯 Uso

### Test de Conexión

```bash
python examples/test_crypto_connection.py
```

Verifica:
- ✅ Conexión a Alpaca Crypto API
- ✅ Descarga de datos históricos
- ✅ Cotizaciones en tiempo real
- ✅ Últimas barras OHLCV

### Trading en Vivo

```bash
python examples/live_trading_crypto.py
```

**Configuración por defecto:**
- 5 criptos: BTC/USD, ETH/USD, SOL/USD, AVAX/USD, DOGE/USD
- $5,000 por cripto ($25k total)
- Actualización cada 60 segundos
- Stop Loss: 5% (más amplio por volatilidad)
- Take Profit: 10% (más ambicioso)

## 🛡️ Gestión de Riesgo para Crypto

### Diferencias vs Acciones

| Aspecto | Acciones | Criptomonedas |
|---------|----------|---------------|
| **Volatilidad** | Baja-Media | ALTA |
| **Horario** | 9:30-16:00 ET | 24/7 |
| **Stop Loss** | 2% | 5-10% |
| **Take Profit** | 5% | 10-20% |
| **Capital** | $20k/símbolo | $5k/símbolo |
| **Update** | 5 min | 1 min |

### Configuración Recomendada

```python
# Conservador (menos riesgo)
CAPITAL_PER_SYMBOL = 2_000  # $2k por crypto
STOP_LOSS_PCT = 0.10  # 10% stop loss
TAKE_PROFIT_PCT = 0.20  # 20% take profit
UPDATE_INTERVAL = 300  # 5 minutos
TIMEFRAME = "1Hour"  # Barras de 1 hora
LOOKBACK_DAYS = 5  # 5 días = 120 horas

# Moderado (recomendado)
CAPITAL_PER_SYMBOL = 5_000  # $5k por crypto
STOP_LOSS_PCT = 0.05  # 5% stop loss
TAKE_PROFIT_PCT = 0.10  # 10% take profit
UPDATE_INTERVAL = 60  # 1 minuto
TIMEFRAME = "1Hour"  # Barras de 1 hora
LOOKBACK_DAYS = 3  # 3 días = 72 horas

# Agresivo (alta frecuencia)
CAPITAL_PER_SYMBOL = 10_000  # $10k por crypto
STOP_LOSS_PCT = 0.03  # 3% stop loss
TAKE_PROFIT_PCT = 0.08  # 8% take profit
UPDATE_INTERVAL = 30  # 30 segundos
TIMEFRAME = "15Min"  # Barras de 15 minutos
LOOKBACK_DAYS = 2  # 2 días = 192 barras
```

## 📈 Ejemplo de Uso

```python
from strategies import CombinedStrategy
from trading_engine.brokers.alpaca_broker import AlpacaBroker
from trading_engine.data.crypto_provider import AlpacaCryptoProvider
from trading_engine.live_engine import MultiSymbolLiveEngine

# Configuración
API_KEY = "tu_api_key"
SECRET_KEY = "tu_secret_key"

# Broker (mismo para stocks y crypto)
broker = AlpacaBroker(
    api_key=API_KEY,
    secret_key=SECRET_KEY,
    paper=True
)

# Proveedor de datos CRYPTO
crypto_provider = AlpacaCryptoProvider(
    api_key=API_KEY,
    secret_key=SECRET_KEY
)

# Estrategia (igual que stocks)
strategy = CombinedStrategy(consensus_threshold=2)

# Motor de trading
engine = MultiSymbolLiveEngine(
    symbols=["BTC/USD", "ETH/USD", "SOL/USD"],
    strategy=strategy,
    broker=broker,
    data_provider=crypto_provider,  # <- Usar crypto provider
    capital_per_symbol=5000,
    stop_loss_pct=0.05,  # 5%
    take_profit_pct=0.10,  # 10%
    update_interval=60
)

engine.start()
```

## 💡 Consejos para Crypto Trading

### 1. Volatilidad

```
Las criptos pueden moverse 5-20% en un día

✅ Usa stop loss más amplios (5-10%)
✅ No te asustes por movimientos del 3-5%
✅ Ajusta posiciones según volatilidad
❌ No uses stop loss de 1-2% (salidas constantes)
```

### 2. Horario 24/7

```
Las criptos nunca duermen

✅ Define horarios de monitoreo
✅ Usa stop loss SIEMPRE
✅ Ten alertas configuradas
❌ No intentes monitorear 24/7 manualmente
```

### 3. Liquidez

```
Bitcoin y Ethereum son muy líquidas
Otras criptos pueden tener spreads mayores

✅ BTC/USD y ETH/USD: Excelente liquidez
✅ SOL/USD, AVAX/USD: Buena liquidez
⚠️ Criptos pequeñas: Verifica spread
```

### 4. Correlación

```
Las criptos tienden a moverse juntas

✅ Diversifica con 3-5 criptos diferentes
✅ No pongas todo en "memecoins"
✅ Combina majors (BTC, ETH) con alts
```

### 5. Noticias

```
Las criptos reaccionan violentamente a noticias

✅ Monitorea Twitter crypto
✅ Sigue @cz_binance, @VitalikButerin
✅ Revisa CoinDesk, CoinTelegraph
⚠️ No operes durante noticias importantes
```

## 🎯 Estrategias Específicas para Crypto

### Estrategia 1: Bitcoin Seguidor

```python
# Solo BTC/USD con mucho capital
SYMBOLS = ["BTC/USD"]
CAPITAL_PER_SYMBOL = 25_000
STOP_LOSS_PCT = 0.08  # 8%
TAKE_PROFIT_PCT = 0.15  # 15%

# RSI más sensible
strategy = RsiStrategy(
    period=14,
    lower_threshold=35,
    upper_threshold=65
)
```

### Estrategia 2: Altcoins Volátiles

```python
# Criptos pequeñas con alto potencial
SYMBOLS = ["SOL/USD", "AVAX/USD", "DOGE/USD"]
CAPITAL_PER_SYMBOL = 3_000
STOP_LOSS_PCT = 0.10  # 10%
TAKE_PROFIT_PCT = 0.25  # 25%

# Más agresivo
strategy = CombinedStrategy(consensus_threshold=1)
```

### Estrategia 3: Portfolio Diversificado

```python
# Mix de majors y alts
SYMBOLS = ["BTC/USD", "ETH/USD", "SOL/USD", "LINK/USD"]
CAPITAL_PER_SYMBOL = 5_000
STOP_LOSS_PCT = 0.05  # 5%
TAKE_PROFIT_PCT = 0.12  # 12%

strategy = CombinedStrategy(consensus_threshold=2)
```

## 📊 Análisis de Mercado Crypto

### Indicadores Importantes

```python
# RSI: Más extremo en crypto
rsi_lower = 25  # En lugar de 30
rsi_upper = 75  # En lugar de 70

# Bollinger Bands: Más anchas
bb_std = 3.0  # En lugar de 2.0

# MACD: Periodos más cortos
macd_fast = 8   # En lugar de 12
macd_slow = 21  # En lugar de 26
```

### Timeframes

```python
# Scalping (muy rápido)
timeframe = "1Min"
update_interval = 15  # 15 segundos

# Day Trading
timeframe = "5Min"
update_interval = 60  # 1 minuto

# Swing Trading
timeframe = "1Hour"
update_interval = 300  # 5 minutos

# Position Trading
timeframe = "1Day"
update_interval = 3600  # 1 hora
```

## ⚠️ Consideraciones Importantes

### 1. Impuestos

En muchos países, cada operación crypto es un evento imponible:

```
✅ Mantén registro de todas las operaciones
✅ Usa software de tracking fiscal
✅ Consulta con contador especializado en crypto
```

### 2. Custodia

Alpaca custodia tus criptos:

```
✅ No necesitas wallet personal
✅ Alpaca es custodio regulado
⚠️ No puedes retirar crypto (solo USD)
```

### 3. Fragmentación

Puedes comprar fracciones:

```python
# Ejemplo: $5,000 en BTC @ $100,000
quantity = 5000 / 100000  # 0.05 BTC

# Alpaca permite comprar 0.0001 BTC (mínimo)
```

### 4. Fees

```
Alpaca NO cobra comisiones en crypto

✅ 0% comisión
✅ Solo spread (diferencia bid/ask)
✅ Típico spread: 0.1-0.5% en majors
```

## 🔧 Troubleshooting

### Error: "Crypto trading not enabled"

1. Ve a Alpaca Dashboard
2. Settings → Enable Crypto Trading
3. Espera 5 minutos
4. Reinicia el script

### Error: "Insufficient buying power"

```python
# Reduce capital por símbolo
CAPITAL_PER_SYMBOL = 1_000  # En lugar de 5_000
```

### Stop Loss ejecutado constantemente

```python
# Amplía stop loss para crypto
STOP_LOSS_PCT = 0.10  # 10% en lugar de 5%
```

### No se generan señales

```python
# Usa consensus más permisivo
strategy = CombinedStrategy(consensus_threshold=1)

# O RSI más sensible
strategy = RsiStrategy(lower_threshold=40, upper_threshold=60)
```

## 📚 Recursos

- [Alpaca Crypto](https://docs.alpaca.markets/docs/crypto-trading) - Documentación oficial
- [CoinMarketCap](https://coinmarketcap.com/) - Precios y datos
- [CoinGecko](https://www.coingecko.com/) - Análisis de mercado
- [TradingView](https://www.tradingview.com/markets/cryptocurrencies/) - Gráficos crypto

## 🎓 Mejores Prácticas

1. **Empieza pequeño:**
   - $1,000-$2,000 por cripto
   - Solo 2-3 criptos inicialmente
   - Paper trading primero

2. **Gestión de riesgo estricta:**
   - SIEMPRE usa stop loss
   - No más del 5-10% del portfolio en una cripto
   - Stop loss de 5-10% (no 2%)

3. **Monitoreo:**
   - Revisa al menos 2 veces al día
   - Configura alertas
   - Ten plan de salida claro

4. **Educación continua:**
   - Lee sobre las criptos que operas
   - Entiende la tecnología subyacente
   - Sigue desarrolladores y comunidad

---

**⚠️ DISCLAIMER:** Las criptomonedas son extremadamente volátiles y de alto riesgo. Solo opera con capital que puedas permitirte perder. Este sistema es para propósitos educativos.

💰 **Opera con responsabilidad. Las criptos no son para todos.**
