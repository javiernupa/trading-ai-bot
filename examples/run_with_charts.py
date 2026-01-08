"""Ejemplo completo con visualizaciones."""

import pandas as pd
from loguru import logger

from trading_engine.backtest import Backtester
from trading_engine.metrics import MetricsCalculator
from trading_engine.visualization import BacktestVisualizer
from strategies.rsi import RsiStrategy


def main() -> None:
    """Ejecuta backtest completo con visualizaciones."""
    logger.info("Iniciando backtest con visualizaciones...")

    # Generar datos sintéticos
    import numpy as np

    np.random.seed(42)
    n_days = 252  # Un año

    dates = pd.date_range(start="2023-01-01", periods=n_days, freq="D")
    trend = np.linspace(100, 150, n_days)
    seasonality = 10 * np.sin(np.linspace(0, 4 * np.pi, n_days))
    noise = np.random.normal(0, 2, n_days)

    df = pd.DataFrame({
        "date": dates,
        "close": trend + seasonality + noise,
    })

    logger.info(f"Datos generados: {len(df)} días")

    # Estrategia y backtest
    strategy = RsiStrategy(period=14, lower=30, upper=70)
    backtester = Backtester(strategy, df, initial_cash=10000)
    result = backtester.run()

    # Mostrar resultados
    MetricsCalculator.print_summary(result)

    # Generar visualizaciones
    logger.info("\nGenerando visualizaciones...")
    BacktestVisualizer.create_full_report(result, output_dir="reports")

    logger.success("✓ Proceso completado")


if __name__ == "__main__":
    main()
