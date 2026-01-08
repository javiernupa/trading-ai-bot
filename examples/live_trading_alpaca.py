"""Ejemplo de trading en vivo con Alpaca - Configuración desde .env"""

import os
from datetime import datetime

from dotenv import load_dotenv

from strategies import (
    CombinedStrategy,
    load_strategies_from_env,
    print_strategy_config,
)
from trading_engine.brokers.alpaca_broker import AlpacaBroker
from trading_engine.data.alpaca_provider import AlpacaDataProvider
from trading_engine.live_engine import MultiSymbolLiveEngine

# Cargar variables de entorno
load_dotenv()

# Configuración desde .env
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

# Trading mode
TRADING_MODE = os.getenv("TRADING_MODE", "paper").lower()
PAPER_TRADING = TRADING_MODE == "paper"

# Símbolos desde .env
SYMBOLS_STR = os.getenv("SYMBOLS", "ASTS,RKLB,IREN,TE,AMZN")
SYMBOLS = [s.strip() for s in SYMBOLS_STR.split(",")]

# Capital asignado por símbolo
INITIAL_CAPITAL = float(os.getenv("INITIAL_CAPITAL", "100000"))
CAPITAL_PER_SYMBOL = float(os.getenv("CAPITAL_PER_SYMBOL", "1000"))

# Intervalo de actualización (en segundos)
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "300"))

# Días de historial para indicadores
LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", "100"))

# Gestión de riesgo
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "0.02"))
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "0.05"))


def main():
    """Función principal."""
    print("=" * 70)
    print("SISTEMA DE TRADING EN VIVO - ALPACA MARKETS")
    print("=" * 70)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Modo: {'PAPER TRADING' if PAPER_TRADING else '⚠️  LIVE TRADING ⚠️ '}")
    print(f"\nSímbolos: {', '.join(SYMBOLS)}")
    print(f"Capital por símbolo: ${CAPITAL_PER_SYMBOL:,}")
    print(f"Capital total: ${CAPITAL_PER_SYMBOL * len(SYMBOLS):,}")
    print(f"Intervalo de actualización: {UPDATE_INTERVAL}s")
    print(f"\n🛡️ Gestión de Riesgo:")
    print(f"  Stop Loss: {STOP_LOSS_PCT:.1%} (-${CAPITAL_PER_SYMBOL * STOP_LOSS_PCT:,.0f} máx por posición)")
    print(f"  Take Profit: {TAKE_PROFIT_PCT:.1%} (+${CAPITAL_PER_SYMBOL * TAKE_PROFIT_PCT:,.0f} objetivo)")

    # Validar credenciales
    if not API_KEY or not SECRET_KEY:
        print("\n❌ ERROR: Faltan credenciales de Alpaca")
        print("   Configura ALPACA_API_KEY y ALPACA_SECRET_KEY en .env")
        return

    # Advertencia para live trading
    if not PAPER_TRADING:
        print("\n" + "!" * 70)
        print("⚠️  ¡ADVERTENCIA! ESTÁS USANDO LIVE TRADING CON DINERO REAL")
        print("!" * 70)
        response = input("\n¿Estás SEGURO de continuar? (escribe 'SI ESTOY SEGURO'): ")
        if response != "SI ESTOY SEGURO":
            print("Operación cancelada.")
            return

    # Cargar estrategias desde .env
    print("\n📊 Cargando configuración de estrategias desde .env...")
    print("-" * 70)
    
    try:
        strategies, consensus = load_strategies_from_env()
        strategy = CombinedStrategy(strategies, consensus)
        
        print(f"\n✅ Estrategia cargada: {strategy}")
        print(f"   • {len(strategies)} estrategias activas")
        print(f"   • Consenso: {consensus}/{len(strategies)}")
        
        # Mostrar detalle de estrategias con parámetros
        print(f"\n📋 Detalle de estrategias configuradas:")
        print("-" * 70)
        for i, strat in enumerate(strategies, 1):
            strat_name = strat.__class__.__name__
            
            # Obtener parámetros específicos de cada estrategia
            params = []
            if hasattr(strat, 'period'):
                params.append(f"period={strat.period}")
            if hasattr(strat, 'rsi_period'):
                params.append(f"period={strat.rsi_period}")
            if hasattr(strat, 'lower'):
                params.append(f"lower={strat.lower}")
            if hasattr(strat, 'upper'):
                params.append(f"upper={strat.upper}")
            if hasattr(strat, 'fast_period'):
                params.append(f"fast={strat.fast_period}")
            if hasattr(strat, 'slow_period'):
                params.append(f"slow={strat.slow_period}")
            if hasattr(strat, 'signal_period'):
                params.append(f"signal={strat.signal_period}")
            if hasattr(strat, 'num_std'):
                params.append(f"std={strat.num_std}")
            if hasattr(strat, 'use_crossover'):
                params.append(f"crossover={strat.use_crossover}")
            if hasattr(strat, 'pivot_window'):
                params.append(f"pivot_window={strat.pivot_window}")
            if hasattr(strat, 'min_wave_size'):
                params.append(f"min_wave={strat.min_wave_size}")
            if hasattr(strat, 'use_volume'):
                params.append(f"volume={strat.use_volume}")
            
            params_str = f"({', '.join(params)})" if params else ""
            print(f"   {i}. {strat_name} {params_str}")
        
        print(f"\n💡 Sistema de consenso:")
        print(f"   • Se requieren al menos {consensus} estrategias de acuerdo para operar")
        print(f"   • Porcentaje de consenso: {consensus/len(strategies)*100:.1f}%")
        print(f"   • Cada estrategia vota: COMPRA (+1), NEUTRAL (0), o VENTA (-1)")
        
    except Exception as e:
        print(f"\n❌ Error cargando estrategias desde .env: {e}")
        print("\n💡 Consejo: Verifica tu archivo .env")
        print("   Ejemplo de configuración:")
        print("   ACTIVE_STRATEGIES=RSI,MACD,MA50,MA200")
        print("   CONSENSUS_THRESHOLD=3")
        return

    # Crear broker
    print("\nConectando a Alpaca...")
    broker = AlpacaBroker(
        api_key=API_KEY,
        secret_key=SECRET_KEY,
        paper=PAPER_TRADING,
    )

    # Crear proveedor de datos
    data_provider = AlpacaDataProvider(
        api_key=API_KEY,
        secret_key=SECRET_KEY,
    )

    # Crear motor de trading
    engine = MultiSymbolLiveEngine(
        symbols=SYMBOLS,
        strategy=strategy,
        broker=broker,
        data_provider=data_provider,        initial_capital=INITIAL_CAPITAL,        capital_per_symbol=CAPITAL_PER_SYMBOL,
        update_interval=UPDATE_INTERVAL,
        lookback_days=LOOKBACK_DAYS,
        stop_loss_pct=STOP_LOSS_PCT,
        take_profit_pct=TAKE_PROFIT_PCT,
    )

    # Mostrar información importante
    print("\n" + "=" * 70)
    print("INFORMACIÓN IMPORTANTE")
    print("=" * 70)
    print("• El sistema actualizará las señales cada", UPDATE_INTERVAL, "segundos")
    print("• Se ejecutarán órdenes de mercado cuando haya señales")
    print("• Presiona Ctrl+C para detener el sistema de forma segura")
    print("• Las posiciones abiertas NO se cerrarán automáticamente al detener")
    print("=" * 70)

    input("\nPresiona ENTER para iniciar el trading en vivo...")

    try:
        # Iniciar motor
        engine.start()

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupción detectada")

    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()

    finally:
        print("\n" + "=" * 70)
        print("Sistema detenido")
        print("=" * 70)


if __name__ == "__main__":
    main()
