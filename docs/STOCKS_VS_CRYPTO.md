# 📊 Stocks vs Crypto Trading

Comparación rápida entre operar acciones y criptomonedas.

## 🎯 Comparación General

| Característica | Stocks (Acciones) | Crypto (Criptomonedas) |
|----------------|-------------------|------------------------|
| **Horario** | 9:30-16:00 ET (L-V) | 24/7 (Sin parar) |
| **Volatilidad** | Baja-Media (1-5% día) | ALTA (5-20% día) |
| **Liquidez** | Muy Alta | Alta (majors), Variable (alts) |
| **Regulación** | Muy Regulado (SEC) | Menos Regulado |
| **Comisiones** | $0 (Alpaca) | $0 (Alpaca) |
| **Capital Mínimo** | $100+ | $1+ (fraccional) |
| **Velocidad** | Moderada | Muy Rápida |

## ⚙️ Configuraciones Recomendadas

### Stocks (Acciones)

```python
# Configuración típica
SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
CAPITAL_PER_SYMBOL = 20_000  # $20k por acción
STOP_LOSS_PCT = 0.02         # 2% stop loss
TAKE_PROFIT_PCT = 0.05       # 5% take profit
UPDATE_INTERVAL = 300        # 5 minutos
LOOKBACK_DAYS = 60          # 60 días de historia

# Horario
TRADING_HOURS = "9:30-16:00 ET"  # Solo horario de mercado
WEEKEND_TRADING = False          # No opera fines de semana

# Estrategia
consensus_threshold = 2  # Conservador
```

### Crypto (Criptomonedas)

```python
# Configuración típica
SYMBOLS = ["BTC/USD", "ETH/USD", "SOL/USD"]
CAPITAL_PER_SYMBOL = 5_000   # $5k por cripto (menor)
STOP_LOSS_PCT = 0.05         # 5% stop loss (más amplio)
TAKE_PROFIT_PCT = 0.10       # 10% take profit (más ambicioso)
UPDATE_INTERVAL = 60         # 1 minuto (más frecuente)
LOOKBACK_DAYS = 30          # 30 días suficiente

# Horario
TRADING_HOURS = "24/7"      # Sin restricciones
WEEKEND_TRADING = True      # Opera siempre

# Estrategia
consensus_threshold = 2  # Igual de conservador
```

## 📈 Ejemplos de Movimientos

### Stocks - Movimiento Típico

```
AAPL - Un día normal
---------------------
Apertura:  $180.00
Máximo:    $182.00  (+1.1%)
Mínimo:    $179.00  (-0.6%)
Cierre:    $181.00  (+0.6%)

Volatilidad: BAJA
```

### Crypto - Movimiento Típico

```
BTC/USD - Un día normal
-----------------------
00:00:  $90,000
Máximo: $93,000  (+3.3%)
Mínimo: $87,000  (-3.3%)
23:59:  $91,500  (+1.7%)

Volatilidad: ALTA
```

## 💰 Gestión de Capital

### Para Stocks

```python
# Conservador
TOTAL_CAPITAL = 50_000
NUM_POSITIONS = 5
CAPITAL_PER_POSITION = 10_000  # 20% cada una

# Moderado (Recomendado)
TOTAL_CAPITAL = 100_000
NUM_POSITIONS = 5
CAPITAL_PER_POSITION = 20_000  # 20% cada una

# Agresivo
TOTAL_CAPITAL = 200_000
NUM_POSITIONS = 10
CAPITAL_PER_POSITION = 20_000  # 10% cada una
```

### Para Crypto

```python
# Conservador
TOTAL_CAPITAL = 10_000
NUM_POSITIONS = 2  # Solo BTC y ETH
CAPITAL_PER_POSITION = 5_000  # 50% cada una

# Moderado (Recomendado)
TOTAL_CAPITAL = 25_000
NUM_POSITIONS = 5
CAPITAL_PER_POSITION = 5_000  # 20% cada una

# Agresivo
TOTAL_CAPITAL = 50_000
NUM_POSITIONS = 10
CAPITAL_PER_POSITION = 5_000  # 10% cada una
```

## 🛡️ Gestión de Riesgo

### Stop Loss

| Capital | Stocks | Crypto |
|---------|--------|--------|
| $10k | 2% = $200 | 5% = $500 |
| $20k | 2% = $400 | 5% = $1,000 |
| $50k | 2% = $1,000 | 5% = $2,500 |

**Razón:** Crypto necesita más margen por volatilidad

### Take Profit

| Capital | Stocks | Crypto |
|---------|--------|--------|
| $10k | 5% = $500 | 10% = $1,000 |
| $20k | 5% = $1,000 | 10% = $2,000 |
| $50k | 5% = $2,500 | 10% = $5,000 |

**Razón:** Crypto ofrece mayores retornos potenciales

## 🎯 ¿Cuál Elegir?

### Elige Stocks Si:

✅ Prefieres menor volatilidad  
✅ Quieres operar solo en horario laboral  
✅ Buscas inversiones más "seguras"  
✅ Tienes más capital ($50k+)  
✅ Prefieres empresas con fundamentales  

### Elige Crypto Si:

✅ Toleras alta volatilidad  
✅ Quieres operar 24/7  
✅ Buscas mayores retornos (y riesgos)  
✅ Tienes menos capital ($5k-$25k)  
✅ Te interesa la tecnología blockchain  

### ¿Por Qué No Ambos? 🤷

```python
# Portfolio Mixto (70% Stocks, 30% Crypto)
STOCKS_CAPITAL = 70_000
CRYPTO_CAPITAL = 30_000
TOTAL = 100_000

# Stocks (más conservador)
STOCK_SYMBOLS = ["AAPL", "GOOGL", "MSFT"]
STOCK_CAPITAL_EACH = 23_333

# Crypto (más agresivo)
CRYPTO_SYMBOLS = ["BTC/USD", "ETH/USD"]
CRYPTO_CAPITAL_EACH = 15_000
```

**Ventajas:**
- Diversificación entre mercados
- Balance riesgo/retorno
- Aprovechar ambas oportunidades

## 📊 Performance Esperado

### Stocks (Histórico)

```
Retorno Anual Promedio:  8-12%
Mejor Día:               +3-5%
Peor Día:                -3-5%
Drawdown Máximo:         -20-30%
Win Rate:                ~55%

Perfil: CONSERVADOR
```

### Crypto (Histórico)

```
Retorno Anual Promedio:  50-200% (volátil)
Mejor Día:               +10-30%
Peor Día:                -10-30%
Drawdown Máximo:         -50-80%
Win Rate:                ~45%

Perfil: AGRESIVO
```

## 🚀 Empezar

### Con Stocks

```bash
# 1. Test
python examples/test_alpaca_connection.py

# 2. Trading
python examples/live_trading_alpaca.py

# Documentación
docs/QUICKSTART_ALPACA.md
```

### Con Crypto

```bash
# 1. Habilitar en Alpaca Dashboard
# Settings → Enable Crypto Trading

# 2. Test
python examples/test_crypto_connection.py

# 3. Trading
python examples/live_trading_crypto.py

# Documentación
docs/CRYPTO_QUICKSTART.md
```

### Con Ambos

```python
# Crear dos engines separados

# Engine 1: Stocks
stocks_engine = MultiSymbolLiveEngine(
    symbols=["AAPL", "GOOGL", "MSFT"],
    data_provider=AlpacaDataProvider(...),  # Stock provider
    capital_per_symbol=20_000,
    stop_loss_pct=0.02,
    take_profit_pct=0.05
)

# Engine 2: Crypto
crypto_engine = MultiSymbolLiveEngine(
    symbols=["BTC/USD", "ETH/USD"],
    data_provider=AlpacaCryptoProvider(...),  # Crypto provider
    capital_per_symbol=10_000,
    stop_loss_pct=0.05,
    take_profit_pct=0.10
)

# Ejecutar ambos en threads separados
```

## 💡 Consejos Finales

### Para Stocks

1. **Opera en horario de mercado** (9:30-16:00 ET)
2. **Evita pre/post market** (más volátil)
3. **Sigue earnings reports** (mueven precios)
4. **Respeta días festivos** (mercado cerrado)
5. **Analiza fundamentales** (P/E, ventas, etc.)

### Para Crypto

1. **Usa stop loss SIEMPRE** (opera 24/7)
2. **Evita fines de semana** (menos liquidez)
3. **Sigue noticias crypto** (impacto instantáneo)
4. **No operes dormido** (configura alertas)
5. **Enfócate en tecnología** (no solo precio)

### Para Ambos

1. **Empieza en paper trading** (sin riesgo)
2. **Define tu estrategia ANTES** (no improvises)
3. **Respeta tus stop loss** (disciplina)
4. **Registra todo** (aprende de errores)
5. **No inviertas lo que no puedes perder** (regla #1)

---

**🎯 Elige según tu perfil de riesgo y disponibilidad de tiempo.**

**💡 La mejor opción es la que se ajusta a TU estilo de trading.**
