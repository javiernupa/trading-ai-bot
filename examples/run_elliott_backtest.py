"""
Ejemplo de backtest con la estrategia Elliott Waves

Este script demuestra cómo usar la estrategia Elliott Waves
para detectar patrones de ondas y generar señales de trading.

Elliott Waves identifica:
- Ondas impulsivas (1, 3, 5) en dirección de la tendencia
- Ondas correctivas (2, 4) contra la tendencia
- Patrones ABC correctivos

Señales:
- COMPRA: Inicio de onda 3 o onda 5 (las más fuertes)
- VENTA: Final de onda 5 o inicio de corrección
"""

import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from backtester.backtester import Backtester
from backtester.visualizer import BacktestVisualizer
from data_providers.yahoo_finance import YahooFinanceProvider
from strategies import ElliottWavesStrategy

# Cargar variables de entorno
load_dotenv()


def main():
    """Ejecuta backtest con estrategia Elliott Waves."""
    
    print("=" * 70)
    print("BACKTEST - ESTRATEGIA ELLIOTT WAVES")
    print("=" * 70)
    print()
    
    # Configuración
    symbol = "AAPL"
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 1)
    initial_capital = 10000.0
    
    print(f"📊 Símbolo: {symbol}")
    print(f"📅 Período: {start_date.date()} - {end_date.date()}")
    print(f"💰 Capital inicial: ${initial_capital:,.2f}")
    print()
    
    # Configuración de la estrategia Elliott Waves
    print("🌊 CONFIGURACIÓN ELLIOTT WAVES:")
    print("-" * 70)
    
    # Crear estrategia con parámetros personalizados
    strategy = ElliottWavesStrategy(
        pivot_window=5,      # Ventana para detectar pivotes
        min_wave_size=2.0,   # Mínimo 2% de movimiento para considerar onda
        use_volume=True,     # Confirmar con volumen
        wave_count=5         # Analizar ciclo completo de 5 ondas
    )
    
    print(f"   Ventana de pivotes: {strategy.pivot_window}")
    print(f"   Tamaño mínimo onda: {strategy.min_wave_size * 100:.1f}%")
    print(f"   Confirmación volumen: {strategy.use_volume}")
    print(f"   Ondas analizadas: {strategy.wave_count}")
    print()
    
    print("📈 Teoría Elliott Waves:")
    print("   • Onda 1: Primera onda impulsiva (inicio tendencia)")
    print("   • Onda 2: Corrección de onda 1")
    print("   • Onda 3: Onda más fuerte (señal COMPRA) ⭐")
    print("   • Onda 4: Corrección de onda 3")
    print("   • Onda 5: Última onda impulsiva (señal COMPRA)")
    print("   • Ondas ABC: Corrección completa (señal VENTA)")
    print()
    
    # Inicializar proveedor de datos
    print("📡 Descargando datos históricos...")
    data_provider = YahooFinanceProvider()
    
    # Crear y ejecutar backtester
    backtester = Backtester(
        strategy=strategy,
        data_provider=data_provider,
        initial_capital=initial_capital,
        commission=0.001,  # 0.1% comisión
        stop_loss_pct=0.02,  # Stop loss 2%
        take_profit_pct=0.05  # Take profit 5%
    )
    
    print("⚙️  Ejecutando backtest...")
    results = backtester.run(symbol, start_date, end_date)
    
    # Mostrar resultados
    print()
    print("=" * 70)
    print("📊 RESULTADOS DEL BACKTEST")
    print("=" * 70)
    print()
    
    print(f"📈 Rendimiento:")
    print(f"   Capital final: ${results['final_capital']:,.2f}")
    print(f"   Retorno total: {results['total_return']:.2f}%")
    print(f"   Retorno anualizado: {results['annualized_return']:.2f}%")
    print()
    
    print(f"📊 Estadísticas de Trading:")
    print(f"   Total operaciones: {results['total_trades']}")
    print(f"   Operaciones ganadoras: {results['winning_trades']}")
    print(f"   Operaciones perdedoras: {results['losing_trades']}")
    print(f"   Win rate: {results['win_rate']:.2f}%")
    print()
    
    print(f"💰 Rentabilidad:")
    print(f"   Ganancia promedio: {results['avg_win']:.2f}%")
    print(f"   Pérdida promedio: {results['avg_loss']:.2f}%")
    print(f"   Profit factor: {results['profit_factor']:.2f}")
    print()
    
    print(f"📉 Riesgo:")
    print(f"   Máxima caída: {results['max_drawdown']:.2f}%")
    print(f"   Sharpe ratio: {results['sharpe_ratio']:.2f}")
    print()
    
    # Análisis específico de Elliott Waves
    print("=" * 70)
    print("🌊 ANÁLISIS ELLIOTT WAVES")
    print("=" * 70)
    print()
    
    # Analizar el último período con la estrategia
    data = backtester.data_with_signals
    
    # Contar señales por tipo de onda
    wave_3_signals = len(data[(data['signal'] == 1) & (data['wave_number'] == 3)])
    wave_5_signals = len(data[(data['signal'] == 1) & (data['wave_number'] == 5)])
    correction_signals = len(data[(data['signal'] == -1) & (data['wave_type'] == 'corrective')])
    
    print(f"📊 Señales detectadas:")
    print(f"   Ondas 3 (más fuertes): {wave_3_signals} señales COMPRA")
    print(f"   Ondas 5 (finales): {wave_5_signals} señales COMPRA")
    print(f"   Correcciones: {correction_signals} señales VENTA")
    print()
    
    # Pivotes detectados
    total_pivots = data['pivot_high'].sum() + data['pivot_low'].sum()
    print(f"📍 Pivotes detectados: {int(total_pivots)}")
    print(f"   Máximos locales: {int(data['pivot_high'].sum())}")
    print(f"   Mínimos locales: {int(data['pivot_low'].sum())}")
    print()
    
    print("💡 Interpretación:")
    if results['total_return'] > 0:
        print("   ✅ La estrategia generó retornos positivos")
        if results['win_rate'] > 55:
            print("   ✅ Alto win rate - Patrones de ondas bien identificados")
        if results['profit_factor'] > 2.0:
            print("   ✅ Excelente profit factor - Buena gestión de riesgo")
    else:
        print("   ⚠️  La estrategia no fue rentable en este período")
        print("   💡 Considera ajustar:")
        print("      - pivot_window (probar 3 o 7)")
        print("      - min_wave_size (probar 1.5% o 3.0%)")
        print("      - use_volume (probar false si el volumen es irregular)")
    print()
    
    # Generar visualización
    print("=" * 70)
    print("📊 GENERANDO REPORTE VISUAL")
    print("=" * 70)
    print()
    
    output_dir = "backtest_results"
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer = BacktestVisualizer(results, backtester.data_with_signals)
    report_path = visualizer.generate_report(
        symbol=symbol,
        output_dir=output_dir,
        filename=f"elliott_waves_{symbol.lower()}_{datetime.now().strftime('%Y%m%d')}.html"
    )
    
    print(f"✅ Reporte generado: {report_path}")
    print()
    print("💡 Abre el reporte en tu navegador para ver:")
    print("   • Gráficos de equity y drawdown")
    print("   • Pivotes y ondas detectadas")
    print("   • Señales de compra/venta marcadas")
    print("   • Estadísticas detalladas")
    print()
    
    print("=" * 70)
    print("✅ BACKTEST COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
