# 🎯 Guía de Ajuste de Estrategia

## ¿Por qué no veo señales de trading?

La estrategia **SÍ está funcionando**, pero con configuración conservadora genera pocas señales. Esto es **intencional** para evitar operaciones innecesarias.

## Entendiendo el Consenso

La estrategia `CombinedStrategy` usa **3 indicadores**:

1. **RSI** (Relative Strength Index)
2. **MACD** (Moving Average Convergence Divergence)
3. **Bollinger Bands**

Cada indicador vota independientemente:
- **+1** = Señal de compra
- **-1** = Señal de venta
- **0** = Sin señal

### Parámetro `consensus_threshold`

Define cuántos indicadores deben coincidir para generar señal:

| Threshold | Requisito | Frecuencia | Riesgo | Uso |
|-----------|-----------|------------|--------|-----|
| **1** | 1 de 3 indicadores | Alta | Alto | Agresivo |
| **2** | 2 de 3 indicadores | Media | Medio | **Recomendado** |
| **3** | 3 de 3 indicadores | Baja | Bajo | Ultra conservador |

**Configuración actual:** `consensus_threshold=2` (moderado)

## Ejemplo de Análisis

```
📅 2025-12-19 - Cierre: $273.87
   RSI: 47.85 (Señal: 0)          ← Neutral (entre 30-70)
   MACD: -1.17 (Señal: 0)          ← Neutral (sin cruce)
   BB: Price dentro (Señal: 0)     ← Neutral (no toca bandas)
   
   Consenso: Compra 0 | Venta 0   ← Nadie vota
   ➡️  SEÑAL FINAL: ⚪ MANTENER    ← Sin acción
```

**¿Por qué no hay señal?**
- RSI está en zona neutral (30-70)
- MACD no cruza línea de señal
- Precio no toca bandas de Bollinger
- **Resultado:** 0 votos → sin señal (correcto!)

## Cómo Ajustar la Estrategia

### Opción 1: Reducir Threshold (Más Señales)

```python
# En live_trading_alpaca.py
strategy = CombinedStrategy(
    consensus_threshold=1,  # ← Cambiar de 2 a 1
    # ... resto de parámetros
)
```

**Efecto:**
- ✅ Más señales de trading
- ✅ Captura más oportunidades
- ⚠️ Más operaciones (más comisiones)
- ⚠️ Mayor riesgo de falsas señales

### Opción 2: Ajustar Umbrales de RSI

```python
strategy = CombinedStrategy(
    rsi_period=14,
    rsi_lower=40,  # ← Cambiar de 30 a 40 (menos estricto)
    rsi_upper=60,  # ← Cambiar de 70 a 60 (menos estricto)
    consensus_threshold=2,
)
```

**Efecto:**
- RSI genera señales más frecuentemente
- Detecta sobrecompra/sobreventa antes

### Opción 3: Estrategia Simple (Una Sola Señal)

```python
from strategies import RsiStrategy

# Solo RSI (más señales)
strategy = RsiStrategy(
    period=14,
    lower_threshold=30,
    upper_threshold=70
)
```

**O MACD:**
```python
from strategies import MacdStrategy

strategy = MacdStrategy(
    fast_period=12,
    slow_period=26,
    signal_period=9
)
```

## Verificar Señales Antes de Operar

```bash
# Test rápido
python examples/test_strategy_signals.py
```

Esto muestra:
- ✅ Últimos 10 días de análisis detallado
- ✅ Señales generadas por cada indicador
- ✅ Consenso final
- ✅ Frecuencia de señales

## Configuraciones Recomendadas

### Conservador (Pocas pero buenas señales)
```python
strategy = CombinedStrategy(
    rsi_lower=25,  # Muy sobrevendido
    rsi_upper=75,  # Muy sobrecomprado
    consensus_threshold=3,  # Los 3 indicadores deben coincidir
)
```
**Resultado:** ~1-2% de días con señal

### Moderado (Balance) ⭐ Recomendado
```python
strategy = CombinedStrategy(
    rsi_lower=30,
    rsi_upper=70,
    consensus_threshold=2,  # 2 de 3 indicadores
)
```
**Resultado:** ~5-10% de días con señal

### Agresivo (Muchas señales)
```python
strategy = CombinedStrategy(
    rsi_lower=40,
    rsi_upper=60,
    consensus_threshold=1,  # Solo 1 indicador necesario
)
```
**Resultado:** ~20-30% de días con señal

## Backtesting de Configuraciones

```python
from trading_engine import Backtester
from strategies import CombinedStrategy

# Test 1: Conservador
strategy_conservative = CombinedStrategy(consensus_threshold=3)
result_1 = backtester.run(data)

# Test 2: Moderado
strategy_moderate = CombinedStrategy(consensus_threshold=2)
result_2 = backtester.run(data)

# Test 3: Agresivo
strategy_aggressive = CombinedStrategy(consensus_threshold=1)
result_3 = backtester.run(data)

# Comparar resultados
print(f"Conservador: {result_1.total_return:.2%}")
print(f"Moderado: {result_2.total_return:.2%}")
print(f"Agresivo: {result_3.total_return:.2%}")
```

## Interpretación de Indicadores

### RSI (Relative Strength Index)
```
0-30:   Sobrevendido → Señal de COMPRA
30-70:  Neutral      → Sin señal
70-100: Sobrecomprado → Señal de VENTA
```

### MACD
```
Histogram > 0 y cruzando desde abajo → COMPRA (momentum alcista)
Histogram < 0 y cruzando desde arriba → VENTA (momentum bajista)
```

### Bollinger Bands
```
Precio toca banda inferior → COMPRA (sobreventa)
Precio toca banda superior → VENTA (sobrecompra)
Precio entre bandas       → Sin señal
```

## Ejemplo Real con Ajustes

**Situación:** AAPL últimos 40 días, solo 2 señales de venta

```python
# Configuración original (muy conservadora)
strategy = CombinedStrategy(consensus_threshold=2)
# Resultado: 5% frecuencia (2/40 días)

# Ajuste 1: Más permisivo
strategy = CombinedStrategy(consensus_threshold=1)
# Resultado esperado: ~15-20% frecuencia

# Ajuste 2: RSI más sensible
strategy = CombinedStrategy(
    rsi_lower=40,  # Detecta sobreventa antes
    rsi_upper=60,  # Detecta sobrecompra antes
    consensus_threshold=1
)
# Resultado esperado: ~25-30% frecuencia
```

## Monitoreo en Vivo

El sistema ahora muestra información detallada:

```
AAPL: Analizando @ $273.87
  RSI: 47.85 | Señal: 0
  MACD: 0.5022 | Signal: 1.6717 | Señal: 0
  BB: Upper $285.45 | Lower $269.60 | Señal: 0
  Consenso: Compra 0 | Venta 0 | Señal Final: 0
```

**Interpretación:**
- Todos los indicadores están neutros
- Sin consenso para operar
- Sistema esperando condiciones más claras

## Consejos

1. **No te preocupes si no hay señales inmediatas**
   - Es mejor esperar buenas oportunidades
   - Evita operar por operar

2. **Backtest primero**
   - Prueba diferentes configuraciones con datos históricos
   - Encuentra el balance entre frecuencia y rentabilidad

3. **Considera el contexto del mercado**
   - Mercado lateral → pocas señales (normal)
   - Mercado tendencial → más señales

4. **Ajusta según tu estilo**
   - Day trading → `consensus_threshold=1`, RSI sensible
   - Swing trading → `consensus_threshold=2` (default)
   - Position trading → `consensus_threshold=3`, RSI estricto

## Verificación Rápida

```bash
# 1. Ver si la estrategia funciona
python examples/test_strategy_signals.py

# 2. Si quieres más señales, edita live_trading_alpaca.py:
# consensus_threshold=1  # en lugar de 2

# 3. Reinicia el trading
python examples/live_trading_alpaca.py
```

---

**📊 Resumen:**

✅ La estrategia **está funcionando correctamente**  
✅ Configuración conservadora = pocas señales (por diseño)  
✅ Ajusta `consensus_threshold` para más señales  
✅ Usa `test_strategy_signals.py` para verificar

🎯 **Recomendación:** Empieza con `consensus_threshold=2`, observa unos días, ajusta según necesites.
