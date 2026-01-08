# Configuración de Estrategias desde .env

Este sistema permite configurar todas tus estrategias de trading desde el archivo `.env` sin necesidad de modificar código.

## 📋 Tabla de Contenidos

- [Configuración Básica](#configuración-básica)
- [Estrategias Disponibles](#estrategias-disponibles)
- [Parámetros por Estrategia](#parámetros-por-estrategia)
- [Ejemplos de Configuración](#ejemplos-de-configuración)
- [Uso en Código](#uso-en-código)

## Configuración Básica

### 1. Archivo .env

Agrega estas líneas a tu archivo `.env`:

```env
# ========================================
# STRATEGY CONFIGURATION
# ========================================

# Estrategias activas (separadas por coma)
ACTIVE_STRATEGIES=RSI,MACD,BOLLINGER,MA50,MA200

# Consenso mínimo (número de estrategias que deben coincidir)
CONSENSUS_THRESHOLD=3

# Configuración de cada estrategia
STRATEGY_RSI=period:14,lower:30,upper:70
STRATEGY_MACD=fast_period:12,slow_period:26,signal_period:9
STRATEGY_BOLLINGER=period:20,num_std:2.0
STRATEGY_MA50=period:50,use_crossover:true
STRATEGY_MA100=period:100,use_crossover:true
STRATEGY_MA200=period:200,use_crossover:true
```

### 2. Variables Principales

- **ACTIVE_STRATEGIES**: Lista de estrategias a usar (separadas por coma)
- **CONSENSUS_THRESHOLD**: Número mínimo de estrategias que deben coincidir para generar señal
- **STRATEGY_<NOMBRE>**: Parámetros específicos de cada estrategia

## Estrategias Disponibles

| Nombre | Descripción | Parámetros |
|--------|-------------|------------|
| `RSI` | Relative Strength Index | `period`, `lower`, `upper` |
| `MACD` | Moving Average Convergence Divergence | `fast_period`, `slow_period`, `signal_period` |
| `BOLLINGER` | Bandas de Bollinger | `period`, `num_std` |
| `ELLIOTT` | Elliott Waves | `pivot_window`, `min_wave_size`, `use_volume`, `wave_count` |
| `MA50` | Media Móvil 50 períodos | `period`, `use_crossover`, `volume_confirmation` |
| `MA100` | Media Móvil 100 períodos | `period`, `use_crossover`, `volume_confirmation` |
| `MA200` | Media Móvil 200 períodos | `period`, `use_crossover`, `volume_confirmation` |

## Parámetros por Estrategia

### RSI (Relative Strength Index)

```env
STRATEGY_RSI=period:14,lower:30,upper:70
```

- **period**: Período de cálculo (default: 14)
- **lower**: Umbral inferior - sobreventa (default: 30)
- **upper**: Umbral superior - sobrecompra (default: 70)

### MACD

```env
STRATEGY_MACD=fast_period:12,slow_period:26,signal_period:9
```

- **fast_period**: Período EMA rápida (default: 12)
- **slow_period**: Período EMA lenta (default: 26)
- **signal_period**: Período línea de señal (default: 9)

### Bollinger Bands

```env
STRATEGY_BOLLINGER=period:20,num_std:2.0
```

- **period**: Período media móvil (default: 20)
- **num_std**: Desviaciones estándar (default: 2.0)

### Elliott Waves

```env
STRATEGY_ELLIOTT=pivot_window:5,min_wave_size:2.0,use_volume:true,wave_count:5
```

- **pivot_window**: Ventana para identificar pivotes/máximos/mínimos locales (default: 5)
- **min_wave_size**: Tamaño mínimo de onda en porcentaje (default: 2.0)
- **use_volume**: Confirmar señales con análisis de volumen (default: true)
- **wave_count**: Número de ondas para análisis (default: 5)

**Funcionamiento:**
- Detecta patrones de ondas de Elliott (impulsivas y correctivas)
- Genera señales de COMPRA en inicio de ondas 3 o 5 (las más fuertes)
- Genera señales de VENTA al final de onda 5 o inicio de corrección
- Requiere volumen alto en ondas impulsivas para confirmar señales

### MA50, MA100, MA200 (Medias Móviles)

```env
STRATEGY_MA50=period:50,use_crossover:true,volume_confirmation:false
STRATEGY_MA100=period:100,use_crossover:true,volume_confirmation:false
STRATEGY_MA200=period:200,use_crossover:true,volume_confirmation:false
```

- **period**: Período de la media (default: 50/100/200)
- **use_crossover**: Si true, señales solo en cruces. Si false, señales continuas (default: true)
- **volume_confirmation**: Requiere volumen alto para señal (default: false)

## Ejemplos de Configuración

### Configuración Conservadora

Usa 5 estrategias con consenso alto (4 de 5):

```env
ACTIVE_STRATEGIES=RSI,MACD,BOLLINGER,MA100,MA200
CONSENSUS_THRESHOLD=4

STRATEGY_RSI=period:14,lower:25,upper:75
STRATEGY_MACD=fast_period:12,slow_period:26,signal_period:9
STRATEGY_BOLLINGER=period:20,num_std:2.5
STRATEGY_MA100=period:100,use_crossover:true
STRATEGY_MA200=period:200,use_crossover:true
```

**Características:**
- Señales muy confiables pero poco frecuentes
- Ideal para inversores conservadores
- Menor riesgo, menor frecuencia de trading

### Configuración Moderada

Usa 4 estrategias con consenso medio (2 de 4):

```env
ACTIVE_STRATEGIES=RSI,MACD,MA50,MA200
CONSENSUS_THRESHOLD=2

STRATEGY_RSI=period:14,lower:30,upper:70
STRATEGY_MACD=fast_period:12,slow_period:26,signal_period:9
STRATEGY_MA50=period:50,use_crossover:true
STRATEGY_MA200=period:200,use_crossover:true
```

**Características:**
- Balance entre frecuencia y confiabilidad
- Ideal para traders moderados
- Riesgo medio, frecuencia media

### Configuración Agresiva

Usa 3 estrategias rápidas con consenso bajo (2 de 3):

```env
ACTIVE_STRATEGIES=RSI,MACD,MA50
CONSENSUS_THRESHOLD=2

STRATEGY_RSI=period:10,lower:35,upper:65
STRATEGY_MACD=fast_period:8,slow_period:21,signal_period:5
STRATEGY_MA50=period:50,use_crossover:true,volume_confirmation:true
```

**Características:**
- Señales frecuentes
- Ideal para day traders
- Mayor riesgo, mayor frecuencia de trading

### Solo Medias Móviles (Triple MA System)

```env
ACTIVE_STRATEGIES=MA50,MA100,MA200
CONSENSUS_THRESHOLD=2

STRATEGY_MA50=period:50,use_crossover:true
STRATEGY_MA100=period:100,use_crossover:true
STRATEGY_MA200=period:200,use_crossover:true
```

**Características:**
- Sistema clásico de tendencias

### Elliott Waves + Indicadores Técnicos

```env
ACTIVE_STRATEGIES=ELLIOTT,RSI,MACD,BOLLINGER
CONSENSUS_THRESHOLD=3

STRATEGY_ELLIOTT=pivot_window:5,min_wave_size:2.0,use_volume:true
STRATEGY_RSI=period:14,lower:30,upper:70
STRATEGY_MACD=fast_period:12,slow_period:26,signal_period:9
STRATEGY_BOLLINGER=period:20,num_std:2.0
```

**Características:**
- Combina análisis de patrones de ondas con indicadores técnicos
- Elliott Waves detecta estructura del mercado
- RSI, MACD y Bollinger confirman las señales
- Ideal para trading de medio plazo
- Señales claras y definidas
- Ideal para seguir tendencias fuertes

## Uso en Código

### Opción 1: Usar directamente en tus scripts

```python
from dotenv import load_dotenv
from strategies import load_strategies_from_env, CombinedStrategy

# Cargar .env
load_dotenv()

# Cargar estrategias automáticamente
strategies, consensus = load_strategies_from_env()

# Crear estrategia combinada
combined = CombinedStrategy(strategies, consensus)

# Usar en trading
signals = combined.generate_signals(data)
```

### Opción 2: Ver configuración actual

```python
from dotenv import load_dotenv
from strategies import print_strategy_config

load_dotenv()

# Mostrar configuración legible
print_strategy_config()
```

### Opción 3: Usar el ejemplo incluido

```bash
# Trading en vivo con estrategias desde .env
python examples/live_trading_from_env.py
```

## Tipos de Datos

El sistema reconoce automáticamente los tipos:

- **Números enteros**: `period:14` → `14` (int)
- **Números decimales**: `num_std:2.5` → `2.5` (float)
- **Booleanos**: `use_crossover:true` → `True` (bool)
- **Strings**: Cualquier otro valor se trata como string

## Validación

El sistema valida automáticamente:

✅ Nombres de estrategias válidos
✅ Consenso no mayor que número de estrategias
✅ Parámetros requeridos por cada estrategia
✅ Tipos de datos correctos

## Ventajas

- 🔧 **Sin código**: Cambia estrategias sin tocar Python
- 🚀 **Rápido**: Modifica y prueba configuraciones al instante
- 📊 **Flexible**: Combina cualquier conjunto de estrategias
- 🧪 **Testeable**: Prueba diferentes configuraciones fácilmente
- 📝 **Documentado**: Configuración clara y legible
- ✅ **Validado**: Errores detectados automáticamente

## Ejemplos Prácticos

### Cambiar solo el consenso

```env
# Más conservador (3 de 4)
ACTIVE_STRATEGIES=RSI,MACD,MA50,MA200
CONSENSUS_THRESHOLD=3

# Más agresivo (2 de 4)
ACTIVE_STRATEGIES=RSI,MACD,MA50,MA200
CONSENSUS_THRESHOLD=2
```

### Agregar/quitar estrategias

```env
# Antes: 3 estrategias
ACTIVE_STRATEGIES=RSI,MACD,BOLLINGER

# Después: Añadir MA200
ACTIVE_STRATEGIES=RSI,MACD,BOLLINGER,MA200
CONSENSUS_THRESHOLD=3
```

### Ajustar parámetros

```env
# RSI más sensible
STRATEGY_RSI=period:10,lower:35,upper:65

# RSI más conservador
STRATEGY_RSI=period:21,lower:25,upper:75
```

## Solución de Problemas

### Error: "Estrategia no válida"

Verifica que el nombre esté en mayúsculas y sea uno de: RSI, MACD, BOLLINGER, MA50, MA100, MA200

### Error: "Consenso mayor que estrategias"

El `CONSENSUS_THRESHOLD` no puede ser mayor que el número de estrategias activas.

### No se cargan estrategias

1. Verifica que el archivo `.env` esté en la raíz del proyecto
2. Asegúrate de llamar `load_dotenv()` antes de cargar estrategias
3. Revisa que los nombres de variables sean correctos (MAYÚSCULAS)

## Recursos

- 📖 [Documentación completa](../docs/OVERVIEW.md)
- 🎯 [Ejemplos](../examples/)
- 📊 [Estrategias individuales](../strategies/src/strategies/)

---

¡Ahora puedes configurar todo desde `.env` sin tocar código! 🚀
