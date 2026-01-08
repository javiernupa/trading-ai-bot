# Sistema de Gestión de Datos

El motor de backtesting incluye un sistema completo de gestión de datos con las siguientes características:

## Características

### 1. Proveedores de Datos

#### Yahoo Finance Provider
```python
from trading_engine.data import YahooFinanceProvider

provider = YahooFinanceProvider()
data = provider.fetch_data(
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    interval="1d"  # 1d, 1h, 5m, etc.
)
```

#### CSV Provider
```python
from trading_engine.data import CsvDataProvider

provider = CsvDataProvider(data_dir="data/historical")

# Cargar datos
data = provider.fetch_data(
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    filename="AAPL.csv"
)

# Guardar datos
provider.save_data(data, symbol="AAPL")
```

### 2. Data Loader con Caché

El `DataLoader` proporciona una interfaz unificada con caché automático:

```python
from trading_engine.data import DataLoader

loader = DataLoader(
    cache_dir="data/cache",
    use_cache=True,
    validate_data=True
)

# Descarga y caché automático
data = loader.load_data(
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    provider="yahoo",
    force_download=False  # Usa caché si existe
)
```

**Ventajas:**
- Caché local para evitar descargas repetidas
- Validación automática de datos
- Limpieza automática de datos
- Gestión de errores mejorada

### 3. Validación de Datos

El `DataValidator` asegura la calidad de los datos:

```python
from trading_engine.data import DataValidator

validator = DataValidator()

# Validar datos
is_valid, warnings = validator.validate(data, strict=False)

if not is_valid:
    print("Warnings encontrados:")
    for warning in warnings:
        print(f"  - {warning}")

# Limpiar datos
clean_data = validator.clean(data)
```

**Validaciones realizadas:**
- ✅ DataFrame no vacío
- ✅ Columnas requeridas presentes
- ✅ Tipos de datos correctos
- ✅ Valores nulos detectados
- ✅ Precios negativos detectados
- ✅ Relación high >= low
- ✅ Close entre low y high
- ✅ Datos ordenados por timestamp
- ✅ Sin duplicados en timestamp

**Limpieza automática:**
- 🔧 Elimina duplicados
- 🔧 Rellena valores nulos (forward/backward fill)
- 🔧 Elimina precios negativos
- 🔧 Corrige relaciones high/low
- 🔧 Ordena por timestamp

## Ejemplos de Uso

### Ejemplo 1: Descarga Simple

```python
from trading_engine.data import DataLoader

loader = DataLoader()
data = loader.load_data(
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    provider="yahoo"
)

print(f"Descargados {len(data)} registros")
print(data.head())
```

### Ejemplo 2: Gestión de Caché

```python
from trading_engine.data import DataLoader

loader = DataLoader(cache_dir="data/cache")

# Primera llamada: descarga y guarda en caché
data = loader.load_data("AAPL", "2023-01-01", "2024-01-01")

# Segunda llamada: usa caché (rápido)
data = loader.load_data("AAPL", "2023-01-01", "2024-01-01")

# Forzar descarga
data = loader.load_data(
    "AAPL", 
    "2023-01-01", 
    "2024-01-01",
    force_download=True
)

# Limpiar caché
loader.clear_cache()  # Todo
loader.clear_cache(symbol="AAPL")  # Solo AAPL
```

### Ejemplo 3: Validación Manual

```python
from trading_engine.data import DataValidator
import pandas as pd

# Cargar datos de cualquier fuente
data = pd.read_csv("mi_datos.csv")

# Validar
validator = DataValidator()
is_valid, warnings = validator.validate(data, strict=False)

if not is_valid:
    print("Datos con problemas, limpiando...")
    data = validator.clean(data)
    
# Ahora los datos están listos para backtesting
```

### Ejemplo 4: Descarga Masiva

```python
from trading_engine.data import DataLoader

symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
loader = DataLoader()

for symbol in symbols:
    try:
        filepath = loader.download_and_save(
            symbol=symbol,
            start_date="2023-01-01",
            end_date="2024-01-01",
            output_file=f"data/{symbol}.csv"
        )
        print(f"✓ {symbol} guardado")
    except Exception as e:
        print(f"✗ Error con {symbol}: {e}")
```

### Ejemplo 5: Integración con Backtesting

```python
from trading_engine.data import DataLoader
from trading_engine import Backtester
from strategies import RsiStrategy

# Cargar datos
loader = DataLoader()
data = loader.load_data(
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    provider="yahoo",
    clean_data=True
)

# Ejecutar backtest
strategy = RsiStrategy()
backtester = Backtester(strategy=strategy, initial_capital=100_000)
result = backtester.run(data)

print(f"Retorno total: {result.total_return:.2%}")
```

## Scripts Útiles

### Script de Descarga

```bash
python scripts/download_data.py
```

Este script descarga datos históricos para múltiples símbolos y los guarda en `data/historical/`.

### Formato de Datos Esperado

Los datos deben tener las siguientes columnas:

| Columna   | Tipo      | Descripción                    |
|-----------|-----------|--------------------------------|
| timestamp | datetime  | Fecha y hora                   |
| open      | float     | Precio de apertura             |
| high      | float     | Precio máximo                  |
| low       | float     | Precio mínimo                  |
| close     | float     | Precio de cierre               |
| volume    | int/float | Volumen de operaciones         |

## Proveedores Futuros

En desarrollo:
- 🔜 Alpaca Markets API
- 🔜 Binance API
- 🔜 Polygon.io
- 🔜 Alpha Vantage
- 🔜 IEX Cloud

## Configuración Avanzada

### Personalizar Proveedor

```python
from trading_engine.data import DataProvider
import pandas as pd

class CustomProvider(DataProvider):
    def fetch_data(self, symbol, start_date, end_date, **kwargs):
        # Tu lógica personalizada
        data = mi_funcion_descarga(symbol, start_date, end_date)
        return data

# Usar con DataLoader
loader = DataLoader()
data = loader.load_data(
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    provider=CustomProvider()
)
```

## Troubleshooting

### Error: yfinance no disponible

```bash
pip install yfinance
```

### Error: Datos vacíos

- Verifica que el símbolo sea correcto (ej: "AAPL" no "Apple")
- Verifica las fechas (formato: "YYYY-MM-DD")
- Para criptomonedas usa: "BTC-USD", "ETH-USD"

### Error: Valores nulos

```python
# El DataLoader limpia automáticamente
loader = DataLoader(validate_data=True)
data = loader.load_data(..., clean_data=True)
```

### Caché corrupto

```python
loader = DataLoader()
loader.clear_cache()  # Limpia todo el caché
```
