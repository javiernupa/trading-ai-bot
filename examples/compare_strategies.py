"""Ejemplo de uso de las nuevas estrategias."""

from datetime import datetime

from strategies import (
    BollingerBandsStrategy,
    CombinedStrategy,
    MacdStrategy,
    MovingAverageCrossStrategy,
)
from trading_engine.backtest import Backtester
from trading_engine.data import DataLoader
from trading_engine.metrics import MetricsCalculator
from trading_engine.visualization import BacktestVisualizer

# Configuración
SYMBOL = "AAPL"
START_DATE = "2023-01-01"
END_DATE = "2024-01-01"
INITIAL_CAPITAL = 100_000


def run_strategy(strategy, strategy_name: str):
    """Ejecuta una estrategia y muestra resultados."""
    print(f"\n{'=' * 60}")
    print(f"Ejecutando estrategia: {strategy_name}")
    print(f"{'=' * 60}")

    # Cargar datos
    loader = DataLoader(cache_dir="data/cache")
    data = loader.load_data(
        symbol=SYMBOL,
        start_date=START_DATE,
        end_date=END_DATE,
        provider="yahoo",
    )

    # Ejecutar backtest
    backtester = Backtester(
        strategy=strategy,
        initial_capital=INITIAL_CAPITAL,
        commission=0.001,
        slippage=0.0005,
    )

    result = backtester.run(data)

    # Calcular métricas
    calculator = MetricsCalculator()
    metrics = calculator.calculate_metrics(result)

    print(f"\nResultados para {strategy_name}:")
    calculator.print_summary(metrics)

    return result, metrics


def main():
    """Función principal."""

    # 1. Estrategia MACD
    macd_strategy = MacdStrategy(fast_period=12, slow_period=26, signal_period=9)
    macd_result, macd_metrics = run_strategy(macd_strategy, "MACD")

    # 2. Estrategia Bollinger Bands
    bb_strategy = BollingerBandsStrategy(period=20, num_std=2.0)
    bb_result, bb_metrics = run_strategy(bb_strategy, "Bollinger Bands")

    # 3. Estrategia Moving Average Cross
    ma_strategy = MovingAverageCrossStrategy(
        fast_period=50, slow_period=200, ma_type="sma"
    )
    ma_result, ma_metrics = run_strategy(ma_strategy, "MA Cross (50/200)")

    # 4. Estrategia Combinada
    combined_strategy = CombinedStrategy(
        rsi_period=14,
        rsi_lower=30,
        rsi_upper=70,
        consensus_threshold=2,
    )
    combined_result, combined_metrics = run_strategy(
        combined_strategy, "Combined (RSI+MACD+BB)"
    )

    # Comparar resultados
    print(f"\n{'=' * 60}")
    print("COMPARACIÓN DE ESTRATEGIAS")
    print(f"{'=' * 60}\n")

    comparison = {
        "MACD": macd_metrics,
        "Bollinger Bands": bb_metrics,
        "MA Cross": ma_metrics,
        "Combined": combined_metrics,
    }

    print(f"{'Estrategia':<20} {'Retorno Total':<15} {'Sharpe':<10} {'Max DD':<10}")
    print("-" * 60)

    for name, metrics in comparison.items():
        print(
            f"{name:<20} "
            f"{metrics['total_return']:<14.2%} "
            f"{metrics['sharpe_ratio']:<9.2f} "
            f"{metrics['max_drawdown']:<9.2%}"
        )

    # Generar visualización para la mejor estrategia
    best_strategy = max(
        comparison.items(),
        key=lambda x: x[1]["sharpe_ratio"],
    )

    print(f"\n🏆 Mejor estrategia: {best_strategy[0]}")
    print(f"   Sharpe Ratio: {best_strategy[1]['sharpe_ratio']:.2f}")

    # Crear visualizaciones
    visualizer = BacktestVisualizer()

    if best_strategy[0] == "MACD":
        result = macd_result
    elif best_strategy[0] == "Bollinger Bands":
        result = bb_result
    elif best_strategy[0] == "MA Cross":
        result = ma_result
    else:
        result = combined_result

    visualizer.create_full_report(result, f"results/best_strategy_{SYMBOL}.png")
    print(f"\n📊 Visualización guardada en: results/best_strategy_{SYMBOL}.png")


if __name__ == "__main__":
    main()
