# 🎉 Trading Bot - Resumen de Capacidades

Sistema completo de trading algorítmico con soporte para **Stocks** y **Criptomonedas**.

---

## 🚀 Quick Overview

```
┌─────────────────────────────────────────────────────────┐
│                  TRADING AI BOT                         │
│                                                         │
│  📈 Stocks          💰 Crypto         📊 Backtest      │
│  9:30-16:00 ET      24/7              Histórico        │
│  AAPL, GOOGL...     BTC/USD, ETH...   Análisis         │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Modos de Operación

### 1️⃣ Trading de Acciones (Stocks)

```bash
python examples/live_trading_alpaca.py
```

**Características:**
- ✅ 5 acciones: AAPL, GOOGL, MSFT, TSLA, AMZN
- ✅ $20k por acción ($100k total)
- ✅ Horario: 9:30-16:00 ET
- ✅ Stop Loss: 2%
- ✅ Take Profit: 5%
- ✅ Actualización: Cada 5 minutos

**Ideal para:**
- Traders conservadores
- Operaciones durante horario laboral
- Capital $50k-$200k

---

### 2️⃣ Trading de Criptomonedas (Crypto)

```bash
python examples/live_trading_crypto.py
```

**Características:**
- ✅ 5 criptos: BTC, ETH, SOL, AVAX, DOGE
- ✅ $5k por cripto ($25k total)
- ✅ Horario: 24/7 sin parar
- ✅ Stop Loss: 5% (más amplio)
- ✅ Take Profit: 10% (más ambicioso)
- ✅ Actualización: Cada 60 segundos

**Ideal para:**
- Traders agresivos
- Alta tolerancia a volatilidad
- Capital $10k-$50k

---

### 3️⃣ Backtesting (Análisis Histórico)

```bash
python examples/run_rsi_advanced.py
```

**Características:**
- ✅ Analiza estrategias con datos históricos
- ✅ Métricas completas (Sharpe, Drawdown, Win Rate)
- ✅ Gráficos profesionales
- ✅ Optimización de parámetros
- ✅ Sin riesgo real

**Ideal para:**
- Desarrollo de estrategias
- Validación antes de live trading
- Análisis y optimización

---

## 🎯 Estrategias Disponibles

### Combined Strategy (Recomendada)

Combina 3 indicadores con sistema de consenso:

```python
strategy = CombinedStrategy(
    rsi_period=14,          # RSI
    macd_fast=12,           # MACD
    bb_period=20,           # Bollinger Bands
    consensus_threshold=2   # 2 de 3 deben coincidir
)
```

**Señal de Compra:** 2+ indicadores votan "comprar"  
**Señal de Venta:** 2+ indicadores votan "vender"

### Otras Estrategias

```python
# RSI (Momentum)
RsiStrategy(period=14, lower=30, upper=70)

# MACD (Tendencia)
MacdStrategy(fast=12, slow=26, signal=9)

# Bollinger Bands (Volatilidad)
BollingerStrategy(period=20, std=2.0)

# Moving Average Cross
MovingAverageCrossStrategy(fast=50, slow=200)
```

---

## 🛡️ Gestión de Riesgo

### Stop Loss & Take Profit

Toda posición tiene protección automática:

```
Compra AAPL @ $100
├─ Stop Loss  @ $98  (-2%)  ❌ Vende si baja
└─ Take Profit @ $105 (+5%)  ✅ Vende si sube
```

**Beneficios:**
- Pérdidas limitadas automáticamente
- Ganancias aseguradas sin intervención
- Opera 24/7 sin supervisión (crypto)

### Configuración por Tipo

| Mercado | Stop Loss | Take Profit | Razón |
|---------|-----------|-------------|-------|
| **Stocks** | 2% | 5% | Baja volatilidad |
| **Crypto** | 5% | 10% | Alta volatilidad |

---

## 📈 Flujo de Trabajo

### Desarrollo de Estrategia

```
1. Backtest → 2. Optimizar → 3. Paper Trading → 4. Live Trading
   ↓              ↓              ↓                  ↓
   Test con      Ajustar        Probar sin         ¡Real!
   históricos    parámetros     riesgo
```

### Ejemplo Completo

```bash
# PASO 1: Backtest
python examples/run_rsi_advanced.py
# Analiza: ¿Funciona la estrategia?

# PASO 2: Paper Trading (Stocks)
python examples/test_alpaca_connection.py
python examples/live_trading_alpaca.py
# Prueba: ¿Funciona en tiempo real?

# PASO 3: Paper Trading (Crypto)
python examples/test_crypto_connection.py
python examples/live_trading_crypto.py
# Prueba: ¿Funciona con crypto?

# PASO 4: Live Trading
# Edita: PAPER_TRADING = False
# ⚠️ ¡DINERO REAL!
```

---

## 🎓 Guías Disponibles

### 🚀 Quick Starts (5 minutos)

- [QUICKSTART_ALPACA.md](QUICKSTART_ALPACA.md) - Stocks en 5 minutos
- [CRYPTO_QUICKSTART.md](CRYPTO_QUICKSTART.md) - Crypto en 5 minutos

### 📖 Guías Completas

- [ALPACA_LIVE_TRADING.md](ALPACA_LIVE_TRADING.md) - Todo sobre stocks
- [CRYPTO_TRADING.md](CRYPTO_TRADING.md) - Todo sobre crypto
- [STOCKS_VS_CRYPTO.md](STOCKS_VS_CRYPTO.md) - Comparación

### 🛡️ Gestión de Riesgo

- [RISK_MANAGEMENT.md](RISK_MANAGEMENT.md) - Stop loss y take profit
- [STRATEGY_TUNING.md](STRATEGY_TUNING.md) - Ajustar estrategias

### 📚 Documentación Técnica

- [GETTING_STARTED.md](GETTING_STARTED.md) - Inicio general
- [STRATEGIES.md](STRATEGIES.md) - Todas las estrategias
- [DATA_MANAGEMENT.md](DATA_MANAGEMENT.md) - Gestión de datos

---

## 💻 Arquitectura del Sistema

```
┌──────────────────────────────────────────────────┐
│                LIVE ENGINE                       │
│  (Motor de Trading en Tiempo Real)              │
└──────────────────────────────────────────────────┘
           ↓                    ↓
┌──────────────────┐  ┌──────────────────┐
│  DATA PROVIDER   │  │     BROKER       │
│                  │  │                  │
│  AlpacaData      │  │  AlpacaBroker    │
│  AlpacaCrypto ← NEW  │  (Paper/Live)    │
└──────────────────┘  └──────────────────┘
           ↓                    ↓
    ┌──────────┐          ┌──────────┐
    │  Yahoo   │          │ Alpaca   │
    │ Finance  │          │ Markets  │
    └──────────┘          └──────────┘
           ↓                    ↓
    Historical Data       Real Trading
```

---

## 🔧 Instalación

```bash
# 1. Clonar
git clone https://github.com/javiernupa/trading-ai-bot.git
cd trading-ai-bot

# 2. Entorno virtual
python -m venv .venv
source .venv/bin/activate

# 3. Instalar
pip install -e engine/
pip install -e strategies/
pip install alpaca-py python-dotenv

# 4. Configurar
cp .env.example .env
# Editar .env con tus API keys de Alpaca

# 5. Test
python examples/test_alpaca_connection.py

# 6. ¡Trading!
python examples/live_trading_alpaca.py
```

---

## 📊 Métricas y Análisis

### Durante Trading

```
AAPL @ $180.50
  RSI: 45.2 | Señal: 0
  MACD: 0.5 | Señal: 0
  BB: Señal: 0
  Consenso: Compra 0 | Venta 0 | MANTENER
```

### Post-Backtest

```
Total Return:     +15.2%
Sharpe Ratio:     1.85
Max Drawdown:     -8.5%
Win Rate:         58%
Profit Factor:    1.92
Avg Trade:        +0.8%
```

---

## ⚠️ Advertencias Importantes

### ❌ NO Hagas Esto

```python
# NO uses stop loss muy ajustado en crypto
STOP_LOSS_PCT = 0.01  # ❌ Demasiado pequeño

# NO operes sin entender la estrategia
python examples/live_trading_crypto.py  # ❌ Sin leer docs

# NO uses todo tu capital
CAPITAL_PER_SYMBOL = 100_000  # ❌ Muy arriesgado

# NO ignores las señales del sistema
# Si stop loss se activa → ¡Déjalo funcionar!
```

### ✅ SÍ Haz Esto

```python
# SÍ empieza con paper trading
PAPER_TRADING = True  # ✅ Sin riesgo

# SÍ lee la documentación
docs/CRYPTO_QUICKSTART.md  # ✅ Entiende primero

# SÍ gestiona capital prudentemente
CAPITAL_PER_SYMBOL = 5_000  # ✅ Razonable

# SÍ respeta tus stop loss
# Si pierdes 5% → Acepta la pérdida
```

---

## 🎯 Ejemplos de Uso

### Trader Conservador

```python
# Stocks con poco capital
SYMBOLS = ["AAPL", "MSFT"]
CAPITAL_PER_SYMBOL = 10_000
STOP_LOSS_PCT = 0.02
TAKE_PROFIT_PCT = 0.05
strategy = CombinedStrategy(consensus_threshold=3)  # Muy conservador
```

### Trader Moderado

```python
# Mix de stocks y crypto
# 70% Stocks ($70k)
stocks = ["AAPL", "GOOGL", "MSFT"]
stock_capital = 23_333

# 30% Crypto ($30k)
cryptos = ["BTC/USD", "ETH/USD"]
crypto_capital = 15_000
```

### Trader Agresivo

```python
# Solo crypto con alta frecuencia
SYMBOLS = ["BTC/USD", "ETH/USD", "SOL/USD", "AVAX/USD"]
CAPITAL_PER_SYMBOL = 10_000
STOP_LOSS_PCT = 0.03
TAKE_PROFIT_PCT = 0.08
UPDATE_INTERVAL = 30  # 30 segundos
strategy = CombinedStrategy(consensus_threshold=1)  # Muy agresivo
```

---

## 🚀 Próximos Pasos

### Principiante

1. ✅ Leer [CRYPTO_QUICKSTART.md](CRYPTO_QUICKSTART.md)
2. ✅ Ejecutar `test_crypto_connection.py`
3. ✅ Probar con **2 criptos** y **$2k cada una**
4. ✅ Observar durante **1 semana**

### Intermedio

1. ✅ Leer [STRATEGY_TUNING.md](STRATEGY_TUNING.md)
2. ✅ Experimentar con **consensus_threshold**
3. ✅ Operar **3-5 símbolos**
4. ✅ Ajustar según resultados

### Avanzado

1. ✅ Desarrollar estrategias propias
2. ✅ Combinar stocks + crypto
3. ✅ Optimizar con backtesting
4. ✅ Automatizar completamente

---

## 📞 Soporte

- **Documentación:** [docs/](docs/)
- **Ejemplos:** [examples/](examples/)
- **Issues:** GitHub Issues
- **Discord:** (Próximamente)

---

**⚠️ DISCLAIMER:** Este sistema es para **propósitos educativos**. El trading conlleva riesgos. Solo opera con capital que puedas permitirte perder.

💰 **¡Opera con inteligencia. Trade with AI!**

---

```
█████╗ ██╗    ████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
██╔══██╗██║    ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
███████║██║       ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗
██╔══██║██║       ██║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║
██║  ██║██║       ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝
╚═╝  ╚═╝╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                        
            🤖 AI-Powered Trading Bot 📈                               
```
