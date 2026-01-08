# Arquitectura del Sistema

## Visión General

El sistema de trading está diseñado como un monorepo modular con dos paquetes principales:

### 1. Engine (`trading_engine`)

Motor de backtesting y ejecución que proporciona:
- Framework de backtesting
- Gestión de órdenes y posiciones
- Cálculo de métricas de rendimiento
- Sistema de eventos para live trading

### 2. Strategies (`strategies`)

Biblioteca de estrategias de trading que incluye:
- Interface abstracta `Strategy`
- Estrategias técnicas (RSI, MACD, etc.)
- Estrategias basadas en ML (próximamente)

## Flujo de Datos

```
Data Provider → Engine → Strategy → Signals → Portfolio → Trades → Metrics
```

## Componentes Principales

### Backtester
- Simula ejecución de estrategias sobre datos históricos
- Gestiona capital, comisiones y slippage
- Genera métricas de rendimiento

### Strategy Interface
- Define el contrato que deben cumplir todas las estrategias
- Método `generate_signals()` retorna señales de compra/venta

### Portfolio Manager
- Gestión de posiciones abiertas
- Cálculo de PnL
- Risk management

## Tecnologías

- **Python 3.10+**: Lenguaje principal
- **Pandas/Numpy**: Procesamiento de datos
- **Pydantic**: Validación y configuración
- **Loguru**: Logging estructurado
- **Pytest**: Testing

## Próximas Mejoras

- [ ] Live trading con brokers reales
- [ ] ML strategies con sklearn/tensorflow
- [ ] Dashboard web con Streamlit
- [ ] Sistema de notificaciones
