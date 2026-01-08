"""Ejemplo de uso de la nueva arquitectura de estrategias combinadas.

Este ejemplo muestra cómo combinar estrategias independientes para crear
sistemas de trading personalizados con votación por consenso.

Características:
- Cada estrategia es independiente y reutilizable
- Fácil agregar/quitar estrategias del mix
- Parámetros configurables por estrategia
- Sistema de votación flexible
- Incluye Elliott Waves para análisis de patrones
"""

from strategies import (
    RsiStrategy,
    MacdStrategy,
    BollingerBandsStrategy,
    ElliottWavesStrategy,
    Ma50Strategy,
    Ma100Strategy,
    Ma200Strategy,
    CombinedStrategy,
)
from trading_engine import DataLoader
import pandas as pd


def example_classic_indicators():
    """Ejemplo 1: Indicadores clásicos (RSI + MACD + BB)."""
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Indicadores Clásicos")
    print("=" * 70)
    
    # Crear estrategias individuales
    strategies = [
        RsiStrategy(period=14, lower=30, upper=70),
        MacdStrategy(fast_period=12, slow_period=26, signal_period=9),
        BollingerBandsStrategy(period=20, num_std=2.0),
    ]
    
    # Combinar con consenso 2 de 3 (66%)
    combined = CombinedStrategy(strategies, consensus_threshold=2)
    
    print(f"\nEstrategia: {combined}")
    print(f"Requiere: 2 de 3 estrategias en acuerdo (66%)")
    
    return combined


def example_with_moving_averages():
    """Ejemplo 2: Indicadores clásicos + Medias Móviles."""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Clásicos + Medias Móviles")
    print("=" * 70)
    
    strategies = [
        RsiStrategy(),
        MacdStrategy(),
        BollingerBandsStrategy(),
        Ma50Strategy(use_crossover=True),  # Señales en cruces
        Ma200Strategy(use_crossover=True),
    ]
    
    # Combinar con consenso 3 de 5 (60%)
    combined = CombinedStrategy(strategies, consensus_threshold=3)
    
    print(f"\nEstrategia: {combined}")
    print(f"Requiere: 3 de 5 estrategias en acuerdo (60%)")
    
    return combined


def example_triple_ma_system():
    """Ejemplo 3: Sistema Triple MA (MA50 + MA100 + MA200)."""
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Sistema Triple MA")
    print("=" * 70)
    
    strategies = [
        Ma50Strategy(use_crossover=True),
        Ma100Strategy(use_crossover=True),
        Ma200Strategy(use_crossover=True),
    ]
    
    # Combinar con consenso 2 de 3 (66%)
    combined = CombinedStrategy(strategies, consensus_threshold=2)
    
    print(f"\nEstrategia: {combined}")
    print(f"Requiere: 2 de 3 medias móviles en acuerdo (66%)")
    print("Este sistema es ideal para seguir tendencias fuertes")
    
    return combined


def example_aggressive_all_indicators():
    """Ejemplo 4: Todos los indicadores (agresivo)."""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Todos los Indicadores (Agresivo)")
    print("=" * 70)
    
    strategies = [
        RsiStrategy(),
        MacdStrategy(),
        BollingerBandsStrategy(),
        Ma50Strategy(use_crossover=True),
        Ma100Strategy(use_crossover=True),
        Ma200Strategy(use_crossover=True),
    ]
    
    # Consenso 3 de 6 (50%) - más agresivo
    combined = CombinedStrategy(strategies, consensus_threshold=3)
    
    print(f"\nEstrategia: {combined}")
    print(f"Requiere: 3 de 6 estrategias en acuerdo (50%)")
    print("Configuración agresiva - genera más señales")
    
    return combined


def example_conservative_all_indicators():
    """Ejemplo 5: Todos los indicadores (conservador)."""
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Todos los Indicadores (Conservador)")
    print("=" * 70)
    
    strategies = [
        RsiStrategy(),
        MacdStrategy(),
        BollingerBandsStrategy(),
        Ma50Strategy(use_crossover=True),
        Ma100Strategy(use_crossover=True),
        Ma200Strategy(use_crossover=True),
    ]
    
    # Consenso 5 de 6 (83%) - muy conservador
    combined = CombinedStrategy(strategies, consensus_threshold=5)
    
    print(f"\nEstrategia: {combined}")
    print(f"Requiere: 5 de 6 estrategias en acuerdo (83%)")
    print("Configuración conservadora - señales muy confiables")
    
    return combined


def example_custom_parameters():
    """Ejemplo 6: Parámetros personalizados por estrategia."""
    print("\n" + "=" * 70)
    print("EJEMPLO 6: Parámetros Personalizados")
    print("=" * 70)
    
    strategies = [
        # RSI más sensible
        RsiStrategy(period=10, lower=25, upper=75),
        
        # MACD más rápido
        MacdStrategy(fast_period=8, slow_period=21, signal_period=5),
        
        # Bandas más estrechas
        BollingerBandsStrategy(period=15, num_std=1.5),
        
        # MA50 con confirmación de volumen
        Ma50Strategy(use_crossover=True, volume_confirmation=True),
    ]
    
    combined = CombinedStrategy(strategies, consensus_threshold=3)
    
    print(f"\nEstrategia: {combined}")
    print(f"Cada estrategia con parámetros optimizados")
    
    return combined


def example_elliott_waves_combo():
    """Ejemplo 7: Elliott Waves + Indicadores Técnicos."""
    print("\n" + "=" * 70)
    print("EJEMPLO 7: Elliott Waves + Indicadores Técnicos")
    print("=" * 70)
    
    strategies = [
        # Elliott Waves para análisis de patrones
        ElliottWavesStrategy(
            pivot_window=5,
            min_wave_size=2.0,
            use_volume=True
        ),
        
        # RSI para confirmar sobreventa/sobrecompra
        RsiStrategy(period=14, lower=30, upper=70),
        
        # MACD para confirmar momentum
        MacdStrategy(fast_period=12, slow_period=26, signal_period=9),
        
        # MA200 para tendencia general
        Ma200Strategy(use_crossover=True),
    ]
    
    combined = CombinedStrategy(strategies, consensus_threshold=3)
    
    print(f"\nEstrategia: {combined}")
    print("Elliott Waves detecta patrones de ondas")
    print("Indicadores técnicos confirman las señales")
    print("Requiere: 3 de 4 estrategias en acuerdo (75%)")
    
    return combined


def run_backtest_example(strategy, symbol="AAPL", start="2023-01-01", end="2024-01-01"):
    """Ejecuta un backtest de ejemplo con la estrategia."""
    print(f"\n{'─' * 70}")
    print(f"Ejecutando backtest: {symbol} ({start} a {end})")
    print(f"{'─' * 70}")
    
    # Cargar datos históricos
    loader = DataLoader(provider="yahoo")
    data = loader.load(symbol, start_date=start, end_date=end)
    
    print(f"Datos cargados: {len(data)} barras")
    
    # Generar señales
    signals = strategy.generate_signals(data)
    
    # Contar señales
    buy_signals = (signals["signal"] == 1).sum()
    sell_signals = (signals["signal"] == -1).sum()
    hold_signals = (signals["signal"] == 0).sum()
    
    print(f"\nSeñales generadas:")
    print(f"  🟢 Compra: {buy_signals}")
    print(f"  🔴 Venta: {sell_signals}")
    print(f"  ⚪ Mantener: {hold_signals}")
    
    # Mostrar resumen de la estrategia
    if hasattr(strategy, 'get_strategy_summary'):
        summary = strategy.get_strategy_summary()
        print(f"\nResumen de la estrategia:")
        print(f"  Número de estrategias: {summary['num_strategies']}")
        print(f"  Consenso: {summary['consensus_threshold']}/{summary['num_strategies']} ({summary['consensus_percentage']:.1f}%)")
    
    return signals


if __name__ == "__main__":
    print("\n" + "🎯 " * 35)
    print("EJEMPLOS DE ESTRATEGIAS COMBINADAS")
    print("🎯 " * 35)
    
    # Ejemplo 1: Clásicos
    strategy1 = example_classic_indicators()
    
    # Ejemplo 2: Con MAs
    strategy2 = example_with_moving_averages()
    
    # Ejemplo 3: Triple MA
    strategy3 = example_triple_ma_system()
    
    # Ejemplo 4: Agresivo
    strategy4 = example_aggressive_all_indicators()
    
    # Ejemplo 5: Conservador
    strategy5 = example_conservative_all_indicators()
    
    # Ejemplo 6: Personalizado
    strategy6 = example_custom_parameters()
    
    # Ejemplo 7: Elliott Waves + Indicadores
    strategy7 = example_elliott_waves_combo()
    
    print("\n" + "=" * 70)
    print("BACKTEST DE EJEMPLO")
    print("=" * 70)
    print("\nEjecutando backtest con Ejemplo 7 (Elliott Waves + Indicadores)...")
    
    try:
        signals = run_backtest_example(strategy7, symbol="AAPL", start="2023-01-01", end="2024-01-01")
        print("\n✅ Backtest completado exitosamente!")
    except Exception as e:
        print(f"\n⚠️  Error en backtest: {e}")
        print("(Asegúrate de tener datos disponibles)")
    
    print("\n" + "💡 " * 35)
    print("VENTAJAS DE LA NUEVA ARQUITECTURA:")
    print("💡 " * 35)
    print("""
    ✓ Modular: Cada estrategia es independiente
    ✓ Flexible: Combina cualquier conjunto de estrategias
    ✓ Personalizable: Parámetros únicos por estrategia
    ✓ Escalable: Fácil agregar nuevas estrategias
    ✓ Testeable: Prueba estrategias individuales o combinadas
    ✓ Mantenible: Código más limpio y organizado
    """)
    
    print("\n" + "📚 " * 35)
    print("CÓMO CREAR TU PROPIA COMBINACIÓN:")
    print("📚 " * 35)
    print("""
    from strategies import (
        RsiStrategy, MacdStrategy, Ma200Strategy,
        CombinedStrategy
    )
    
    # 1. Selecciona tus estrategias
    my_strategies = [
        RsiStrategy(period=14),
        MacdStrategy(fast=12, slow=26),
        Ma200Strategy(use_crossover=True),
    ]
    
    # 2. Define el consenso (ej: 2 de 3)
    my_combined = CombinedStrategy(my_strategies, consensus_threshold=2)
    
    # 3. Genera señales
    signals = my_combined.generate_signals(data)
    """)
    
    print("\n" + "🚀 " * 35)
    print("¡Listo para empezar a tradear con tu estrategia personalizada!")
    print("🚀 " * 35 + "\n")
