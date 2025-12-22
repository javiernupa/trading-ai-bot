"""Ejemplo mejorado de uso del backtester con RSI."""

import pandas as pd
from loguru import logger

from trading_engine.backtest import Backtester
from trading_engine.metrics import MetricsCalculator
from strategies.rsi import RsiStrategy

# Configurar logging
logger.add("logs/backtest.log", rotation="10 MB")


def load_sample_data() -> pd.DataFrame:
    """Carga datos de ejemplo."""
    # Opción 1: Cargar desde CSV
    try:
        df = pd.read_csv("data/examples/sample_data.csv")
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        return df
    except FileNotFoundError:
        # Opción 2: Generar datos sintéticos
        logger.warning("No sample data found, generating synthetic data...")
        dates = pd.date_range(start="2023-01-01", periods=200, freq="D")
        
        # Generar precio con tendencia y ruido
        import numpy as np
        np.random.seed(42)
        trend = np.linspace(100, 120, 200)
        noise = np.random.normal(0, 2, 200)
        close_prices = trend + noise
        
        return pd.DataFrame({
            "date": dates,
            "close": close_prices,
            "high": close_prices + abs(np.random.normal(0, 1, 200)),
            "low": close_prices - abs(np.random.normal(0, 1, 200)),
            "open": close_prices + np.random.normal(0, 0.5, 200),
            "volume": np.random.randint(1000000, 2000000, 200),
        })


def main() -> None:
    """Ejecuta el backtest de la estrategia RSI."""
    logger.info("=" * 60)
    logger.info("Starting RSI Strategy Backtest")
    logger.info("=" * 60)

    # Cargar datos
    df = load_sample_data()
    logger.info(f"Loaded {len(df)} data points from {df.iloc[0]['date']} to {df.iloc[-1]['date']}")

    # Configurar estrategia
    strategy = RsiStrategy(
        period=14,
        lower=30,  # Sobrevendido
        upper=70,  # Sobrecomprado
    )
    logger.info("Strategy: RSI(14) - Long when RSI < 30, Exit when RSI > 70")

    # Configurar y ejecutar backtest
    backtester = Backtester(
        strategy=strategy,
        data=df,
        initial_cash=10000,
        commission=0.001,  # 0.1%
        slippage=0.0005,   # 0.05%
    )

    # Ejecutar
    result = backtester.run()

    # Mostrar resultados
    MetricsCalculator.print_summary(result)

    # Detalles de trades individuales
    if result.trades:
        logger.info(f"\n{'='*60}")
        logger.info("INDIVIDUAL TRADES")
        logger.info(f"{'='*60}")
        
        for i, trade in enumerate(result.trades[:10], 1):  # Mostrar primeros 10
            logger.info(
                f"{i}. {trade.side.upper()}: "
                f"Entry ${trade.entry_price:.2f} → Exit ${trade.exit_price:.2f} | "
                f"PnL: ${trade.pnl:+,.2f} ({trade.pnl_percent:+.2f}%) | "
                f"Duration: {trade.duration_seconds/3600:.1f}h"
            )
        
        if len(result.trades) > 10:
            logger.info(f"... and {len(result.trades) - 10} more trades")

    # Guardar resultados
    if result.equity_curve is not None:
        result.equity_curve.to_csv("reports/equity_curve.csv")
        logger.success("Equity curve saved to reports/equity_curve.csv")


if __name__ == "__main__":
    main()
