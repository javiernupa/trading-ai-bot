# Trading en Vivo con Alpaca Markets

Guía completa para configurar y ejecutar trading en vivo con Alpaca.

## 🔏 Características

- ✅ **Paper Trading** - Dinero simulado para pruebas seguras
- ✅ **Multi-Symbol** - Opera hasta 5 acciones simultáneamente
- ✅ **Bracket Orders** - Stop Loss y Take Profit automáticos
- ✅ **Real-Time Data** - Cotizaciones y datos actualizados
- ✅ **Risk Management** - Gestión de riesgo integrada
- ✅ **Auto Execution** - Ejecución automática de señales

## 🔐 Configuración Inicial

### 1. Crear Cuenta en Alpaca

1. Ve a [Alpaca Markets](https://alpaca.markets/)
2. Crea una cuenta (es gratis)
3. Verifica tu identidad (requerido)
4. Activa **Paper Trading** (trading simulado)

### 2. Obtener Credenciales API

1. Inicia sesión en [Alpaca Dashboard](https://app.alpaca.markets/)
2. Ve a "Paper Trading" (esquina superior derecha)
3. Navega a "API Keys"
4. Genera nuevas keys:
   - **API Key ID**
   - **Secret Key**
5. ⚠️ **Guarda el Secret Key** - solo se muestra una vez

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

Edita `.env` y añade tus credenciales:

```env
# Alpaca API Configuration
ALPACA_API_KEY=PK...  # Tu API Key
ALPACA_SECRET_KEY=...  # Tu Secret Key
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading

# Trading Configuration
TRADING_MODE=paper
SYMBOLS=AAPL,GOOGL,MSFT,TSLA,AMZN
CAPITAL_PER_SYMBOL=20000

# Risk Management
STOP_LOSS_PCT=0.02  # 2% stop loss
TAKE_PROFIT_PCT=0.05  # 5% take profit
```

### 4. Instalar Dependencias

```bash
# Instalar alpaca-py
pip install alpaca-py python-dotenv

# O reinstalar el paquete completo
pip install -e engine/
```

## 🧪 Test de Conexión

Antes de empezar, verifica que todo funcione:

```bash
python examples/test_alpaca_connection.py
```

Esto verificará:
- ✅ Conexión al broker
- ✅ Información de cuenta
- ✅ Descarga de datos históricos
- ✅ Cotizaciones en tiempo real

## 🚀 Uso

### Opción 1: Trading en Vivo con 5 Acciones

```bash
python examples/live_trading_alpaca.py
```

**¿Qué hace?**
- Opera con 5 acciones: AAPL, GOOGL, MSFT, TSLA, AMZN
- Asigna $20,000 de capital por acción ($100k total)
- Usa estrategia combinada (RSI + MACD + Bollinger Bands)
- Actualiza señales cada 5 minutos
- Ejecuta órdenes automáticamente cuando hay señales
- 🛡️ **Stop Loss 2%** - Protege contra pérdidas mayores
- 🎯 **Take Profit 5%** - Asegura ganancias al objetivo

**Flujo de Ejecución:**
1. Conecta a Alpaca (paper trading)
2. Carga datos históricos (100 días)
3. Verifica posiciones actuales
4. Entra en loop de trading:
   - Actualiza datos de cada símbolo
   - Genera señales con la estrategia
   - Ejecuta órdenes (compra/venta) con stop loss y take profit
   - Verifica órdenes pendientes
   - Muestra estado actual
   - Espera 5 minutos
5. Repite hasta Ctrl+C

### Opción 2: Personalizado

```python
from strategies import RsiStrategy
from trading_engine.brokers.alpaca_broker import AlpacaBroker
from trading_engine.data.alpaca_provider import AlpacaDataProvider
from trading_engine.live_engine import MultiSymbolLiveEngine

# Tus credenciales
API_KEY = "tu_api_key"
SECRET_KEY = "tu_secret_key"

# Broker
broker = AlpacaBroker(
    api_key=API_KEY,
    secret_key=SECRET_KEY,
    paper=True  # Paper trading
)

# Proveedor de datos
data_provider = AlpacaDataProvider(
    api_key=API_KEY,
    secret_key=SECRET_KEY
)

# Estrategia
strategy = RsiStrategy(period=14, lower_threshold=30, upper_threshold=70)

# Motor de trading
engine = MultiSymbolLiveEngine(
    symbols=["AAPL", "MSFT", "GOOGL"],  # Tus símbolos
    strategy=strategy,
    broker=broker,
    data_provider=data_provider,
    capital_per_symbol=10000,  # $10k por símbolo
    update_interval=60,  # Actualizar cada 60s
    lookback_days=100,  # 100 días de historial
    stop_loss_pct=0.02,  # 2% stop loss
    take_profit_pct=0.05,  # 5% take profit
)

# Iniciar
engine.start()
```

## 📊 Monitoreo

### Dashboard de Alpaca

Monitorea tu cuenta en: https://app.alpaca.markets/paper/dashboard

Verás:
- Capital actual
- Posiciones abiertas
- Órdenes ejecutadas
- Historial de trades
- Gráficos de performance

### Logs del Sistema

El sistema imprime información detallada:

```
============================================================
ITERACIÓN 1 - 2024-12-22 10:30:00
============================================================
AAPL: Actualizando datos...
🟢 AAPL: COMPRA 50 @ $180.50 (Total: $9,025.00)

MSFT: Actualizando datos...
Sin acción (Signal: 0, Position: False)

📊 ESTADO ACTUAL:
  Capital: $100,000.00
  Cash: $90,975.00
  Posiciones: 1
    AAPL: 50.00 @ $180.50 → $181.20 | PnL: $35.00 (+0.39%)
```

## ⚙️ Configuración Avanzada

### Cambiar Estrategia

```python
# RSI
from strategies import RsiStrategy
strategy = RsiStrategy(period=14, lower_threshold=30, upper_threshold=70)

# MACD
from strategies import MacdStrategy
strategy = MacdStrategy(fast_period=12, slow_period=26, signal_period=9)

# Moving Average Cross
from strategies import MovingAverageCrossStrategy
strategy = MovingAverageCrossStrategy(fast_period=50, slow_period=200)

# Combined (recomendado)
from strategies import CombinedStrategy
strategy = CombinedStrategy(consensus_threshold=2)
```

### Ajustar Símbolos

```python
# Tech stocks
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]

# Blue chips
symbols = ["JPM", "JNJ", "WMT", "PG", "V"]

# ETFs
symbols = ["SPY", "QQQ", "IWM", "DIA", "VTI"]

# Crypto (con Alpaca crypto API)
symbols = ["BTCUSD", "ETHUSD", "SOLUSD"]
```

### Intervalos de Actualización

```python
# Alta frecuencia (1 minuto) - requiere más recursos
update_interval = 60

# Media frecuencia (5 minutos) - recomendado
update_interval = 300

# Baja frecuencia (15 minutos)
update_interval = 900

# Daily (1 día) - para swing trading
update_interval = 86400
```

## 🛡️ Seguridad

### Paper Trading (Recomendado)

**SIEMPRE** empieza con paper trading:

```python
broker = AlpacaBroker(
    api_key=API_KEY,
    secret_key=SECRET_KEY,
    paper=True  # ✅ Seguro - usa dinero simulado
)
```

**Ventajas:**
- ✅ Dinero simulado
- ✅ Sin riesgo real
- ✅ Misma API que live
- ✅ Datos de mercado reales
- ✅ Perfecto para testing

### Live Trading (⚠️ Cuidado)

**Solo** después de probar extensivamente en paper:

```python
broker = AlpacaBroker(
    api_key=API_KEY,
    secret_key=SECRET_KEY,
    paper=False  # ⚠️ DINERO REAL
)
```

**Protecciones:**
1. Empieza con capital pequeño
2. Limita el capital por símbolo
3. Usa stop losses
4. Monitorea constantemente
5. Ten un plan de salida

### Manejo de Credenciales

❌ **NUNCA** hagas esto:
```python
API_KEY = "PK123456..."  # Hardcoded
```

✅ **SIEMPRE** usa variables de entorno:
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPACA_API_KEY")
```

✅ Añade `.env` a `.gitignore`:
```
.env
.env.local
*.key
```

## 🔧 Troubleshooting

### Error: "alpaca-py not available"

```bash
pip install alpaca-py
```

### Error: "Invalid API credentials"

1. Verifica que las keys sean correctas
2. Verifica que estés en el modo correcto (paper/live)
3. Regenera las keys en Alpaca Dashboard

### Error: "Insufficient buying power"

- Reduce `capital_per_symbol`
- Reduce el número de símbolos
- Verifica tu saldo en Alpaca Dashboard

### Las órdenes no se ejecutan

- Verifica que sea horario de mercado (9:30-16:00 ET, lunes-viernes)
- Verifica que haya señales de trading
- Revisa los logs para errores
- Comprueba las posiciones existentes

### Datos no se actualizan

- Verifica conexión a internet
- Verifica que las API keys tengan permisos de datos
- Prueba con otro símbolo

## 📈 Mejores Prácticas

### 1. Testing Exhaustivo

```bash
# 1. Test de conexión
python examples/test_alpaca_connection.py

# 2. Backtest con datos históricos
python examples/run_rsi_advanced.py

# 3. Paper trading por al menos 1-2 semanas
python examples/live_trading_alpaca.py

# 4. Solo entonces considera live trading
```

### 2. Gestión de Riesgo

- 📉 Nunca arriesgues más del 2% por trade
- 🎯 Define stop losses claros
- 💰 Limita el capital por símbolo
- 📊 Diversifica entre varios símbolos
- ⏰ No operes fuera de horario de mercado

### 3. Monitoreo

- 👀 Revisa el sistema regularmente
- 📧 Configura alertas por email
- 📊 Revisa métricas diarias
- 🔍 Analiza trades fallidos
- 📝 Mantén un journal de trading

### 4. Mantenimiento

- 🔄 Actualiza datos históricos regularmente
- 🧪 Re-testea estrategias periódicamente
- 📊 Ajusta parámetros según performance
- 🔧 Actualiza dependencias
- 💾 Haz backups de configuración

## 🚨 Limitaciones

### Alpaca Paper Trading

- ✅ Datos de mercado reales
- ✅ Misma API que live
- ❌ Sin slippage real
- ❌ Sin impact en el mercado
- ❌ Fills instantáneos (no realista)

### Sistema Actual

- ✅ Multi-símbolo
- ✅ Múltiples estrategias
- ✅ Paper & Live trading
- ❌ Sin stop losses automáticos (próximamente)
- ❌ Sin trailing stops (próximamente)
- ❌ Solo órdenes de mercado (próximamente limit/stop)

## 📚 Recursos

- [Alpaca Docs](https://docs.alpaca.markets/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-py)
- [Paper Trading Dashboard](https://app.alpaca.markets/paper/dashboard)
- [Market Data](https://docs.alpaca.markets/docs/market-data)
- [Trading API](https://docs.alpaca.markets/docs/trading-api)

## 🆘 Soporte

**Problemas con Alpaca:**
- Support: support@alpaca.markets
- Slack: alpaca-community.slack.com

**Problemas con el código:**
- GitHub Issues
- Revisa logs en `logs/trading.log`
- Ejecuta tests de diagnóstico

---

**⚠️ DISCLAIMER:** Trading involves substantial risk of loss. Este software es para fines educativos. No es asesoramiento financiero. Opera bajo tu propia responsabilidad.
