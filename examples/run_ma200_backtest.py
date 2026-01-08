"""Ejemplo de backtesting con estrategia MA200."""

from datetime import datetime

from strategies import Ma200Strategy
from trading_engine.backtest import Backtester
from trading_engine.data.loader import DataLoader
from trading_engine.visualization import BacktestVisualizer

# Configuración
SYMBOL = "AAPL"
START_DATE = "2020-01-01"
END_DATE = "2024-12-20"
INITIAL_CAPITAL = 100_000


def run_ma200_backtest():
    """Ejecuta backtest con estrategia MA200."""
    print("=" * 70)
    print("BACKTEST - ESTRATEGIA MA200")
    print("=" * 70)
    print(f"\nSímbolo: {SYMBOL}")
    print(f"Período: {START_DATE} a {END_DATE}")
    print(f"Capital inicial: ${INITIAL_CAPITAL:,.0f}")

    # Cargar datos
    print("\n1. Cargando datos históricos...")
    loader = DataLoader()
    data = loader.load_data(
        symbol=SYMBOL, start_date=START_DATE, end_date=END_DATE, provider="yahoo"
    )
    print(f"   ✓ {len(data)} barras cargadas")

    # Crear estrategia MA200
    print("\n2. Configurando estrategia MA200...")
    strategy = Ma200Strategy(
        period=200,
        use_crossover=True,  # Solo señales en cruces (conservador)
        volume_confirmation=False,  # Sin confirmación de volumen
    )
    print(f"   ✓ {strategy}")

    # Ejecutar backtest
    print("\n3. Ejecutando backtest...")
    backtester = Backtester(
        strategy=strategy,
        data=data,
        initial_cash=INITIAL_CAPITAL,
        commission=0.001,  # 0.1% comisión
        slippage=0.001,  # 0.1% slippage
    )

    result = backtester.run()

    # Mostrar resultados
    print("\n" + "=" * 70)
    print("RESULTADOS DEL BACKTEST")
    print("=" * 70)

    print(f"\n📊 Rendimiento:")
    print(f"  Total Return:     {result.total_return_percent:.2%}")
    print(f"  Sharpe Ratio:     {result.sharpe_ratio:.2f}")

    print(f"\n💰 Capital:")
    print(f"  Inicial:          ${result.initial_capital:,.0f}")
    print(f"  Final:            ${result.final_capital:,.0f}")

    print(f"\n📉 Riesgo:")
    print(f"  Max Drawdown:     {result.max_drawdown_percent:.2%}")

    print(f"\n🎯 Operaciones:")
    print(f"  Total:            {result.total_trades}")
    print(f"  Ganadoras:        {result.winning_trades} ({result.win_rate:.1%})")
    print(f"  Perdedoras:       {result.losing_trades}")
    print(f"  Win Rate:         {result.win_rate:.1%}")
    print(f"  Profit Factor:    {result.profit_factor:.2f}")

    print(f"\n💵 Trade Promedio:")
    print(f"  Ganancia:         ${result.average_win:,.2f}")
    print(f"  Pérdida:          ${result.average_loss:,.2f}")

    # Generar visualización
    print("\n4. Generando gráficos...")
    output_dir = f"reports/ma200_{SYMBOL}_{datetime.now().strftime('%Y%m%d')}"
    viz = BacktestVisualizer()
    viz.create_full_report(result, output_dir=output_dir)
    print(f"   ✓ Gráficos guardados en: {output_dir}/")

    print("\n" + "=" * 70)
    print("✅ Backtest completado")
    print("=" * 70)

    return result


def compare_ma200_modes():
    """Compara MA200 en modo crossover vs position."""
    print("\n" + "=" * 70)
    print("COMPARACIÓN: CROSSOVER vs POSITION")
    print("=" * 70)

    loader = DataLoader()
    data = loader.load_data(
        symbol=SYMBOL, start_date=START_DATE, end_date=END_DATE, provider="yahoo"
    )

    results_comparison = {}

    # Modo 1: Crossover (conservador)
    print("\n1. Probando modo CROSSOVER (solo cruces)...")
    strategy_cross = Ma200Strategy(period=200, use_crossover=True)
    backtester_cross = Backtester(
        strategy=strategy_cross,
        data=data,
        initial_cash=INITIAL_CAPITAL,
        commission=0.001,
    )
    results_cross = backtester_cross.run()
    results_comparison["Crossover"] = results_cross.metrics

    # Modo 2: Position (agresivo)
    print("2. Probando modo POSITION (continuo)...")
    strategy_pos = Ma200Strategy(period=200, use_crossover=False)
    backtester_pos = Backtester(
        strategy=strategy_pos,
        data=data,
        initial_cash=INITIAL_CAPITAL,
        commission=0.001,
    )
    results_pos = backtester_pos.run()
    results_comparison["Position"] = results_pos.metrics

    # Comparar resultados
    print("\n" + "=" * 70)
    print("COMPARACIÓN DE RESULTADOS")
    print("=" * 70)

    print(f"\n{'Métrica':<25} {'Crossover':>15} {'Position':>15} {'Mejor':>10}")
    print("-" * 70)

    comparisons = [
        ("Total Return", "total_return", "%"),
        ("Sharpe Ratio", "sharpe_ratio", ""),
        ("Max Drawdown", "max_drawdown", "%"),
        ("Win Rate", "win_rate", "%"),
        ("Total Trades", "total_trades", ""),
        ("Profit Factor", "profit_factor", ""),
    ]

    for name, key, fmt in comparisons:
        cross_val = results_comparison["Crossover"].get(key, 0)
        pos_val = results_comparison["Position"].get(key, 0)

        # Determinar cuál es mejor (excepto drawdown, donde menor es mejor)
        if key == "max_drawdown":
            better = "Crossover" if abs(cross_val) < abs(pos_val) else "Position"
        else:
            better = "Crossover" if cross_val > pos_val else "Position"

        if fmt == "%":
            print(
                f"{name:<25} {cross_val:>14.2%} {pos_val:>14.2%} {better:>10}"
            )
        else:
            print(
                f"{name:<25} {cross_val:>15.2f} {pos_val:>15.2f} {better:>10}"
            )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Ejecutar backtest básico
    results = run_ma200_backtest()

    # Comparar modos (opcional)
    response = input("\n¿Quieres comparar Crossover vs Position? (s/n): ")
    if response.lower() == "s":
        compare_ma200_modes()

    print("\n💡 Recomendación:")
    print("  - Use 'crossover=True' para trading más conservador (menos trades)")
    print("  - Use 'crossover=False' para seguir tendencia continuamente")
    print("  - MA200 funciona mejor en mercados con tendencia clara")
    print("  - Evite usar MA200 en mercados laterales (muchas señales falsas)")
