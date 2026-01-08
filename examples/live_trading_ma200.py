"""Ejemplo de trading en vivo con estrategia MA200.

Este ejemplo usa configuración desde .env para todos los parámetros.
Puedes cambiar la estrategia y parámetros editando el archivo .env.
"""

import os
from datetime import datetime

from dotenv import load_dotenv

from strategies import load_strategy_from_env
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

# Símbolos para trading de tendencia con MA200
SYMBOLS_STR = os.getenv("SYMBOLS", "AAPL,MSFT,GOOGL,NVDA,TSLA")
SYMBOLS = [s.strip() for s in SYMBOLS_STR.split(",")]

# Parámetros de trading
CAPITAL_PER_SYMBOL = float(os.getenv("CAPITAL_PER_SYMBOL", "20000"))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "300"))
LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", "250"))

# Gestión de riesgo
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "0.05"))
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "0.15"))


def main():
    """Función principal."""
    print("=" * 70)
    print("SISTEMA DE TRADING EN VIVO - ESTRATEGIA MA200")
    print("=" * 70)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Modo: {'PAPER TRADING' if PAPER_TRADING else '⚠️  LIVE TRADING ⚠️ '}")

    print(f"\n📈 Acciones: {', '.join(SYMBOLS)}")
    print(f"Capital por acción: ${CAPITAL_PER_SYMBOL:,}")
    print(f"Capital total: ${CAPITAL_PER_SYMBOL * len(SYMBOLS):,}")
    print(f"Intervalo de actualización: {UPDATE_INTERVAL}s")

    print(f"\n🛡️ Gestión de Riesgo:")
    print(
        f"  Stop Loss: {STOP_LOSS_PCT:.1%} "
        f"(-${CAPITAL_PER_SYMBOL * STOP_LOSS_PCT:,.0f} máx por posición)"
    )
    print(
        f"  Take Profit: {TAKE_PROFIT_PCT:.1%} "
        f"(+${CAPITAL_PER_SYMBOL * TAKE_PROFIT_PCT:,.0f} objetivo)"
    )

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
        response = input(
            "\n¿Estás SEGURO de continuar? (escribe 'SI ESTOY SEGURO'): "
        )
        if response != "SI ESTOY SEGURO":
            print("Operación cancelada.")
            return

    # Cargar estrategia MA200 desde .env
    print("\n📊 Cargando estrategia desde .env...")
    try:
        strategy = load_strategy_from_env("MA200")
        print(f"  ✓ Estrategia cargada: {strategy}")
    except Exception as e:
        print(f"  ❌ Error cargando estrategia: {e}")
        print("\n💡 Asegúrate de tener en .env:")
        print("   STRATEGY_MA200=period:200,use_crossover:true,volume_confirmation:false")
        return
    
    print("  ✓ Trading de tendencia a largo plazo")
    print(f"  ✓ Parámetros: {strategy.get_parameters()}")

    # Crear broker
    print("\n🔗 Conectando a Alpaca...")
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
        data_provider=data_provider,
        capital_per_symbol=CAPITAL_PER_SYMBOL,
        update_interval=UPDATE_INTERVAL,
        lookback_days=LOOKBACK_DAYS,
        timeframe="1Day",  # Datos diarios para MA200
        stop_loss_pct=STOP_LOSS_PCT,
        take_profit_pct=TAKE_PROFIT_PCT,
    )

    # Mostrar información importante
    print("\n" + "=" * 70)
    print("⚠️  CONSIDERACIONES PARA MA200")
    print("=" * 70)
    print("• Estrategia de LARGO PLAZO (tendencias de semanas/meses)")
    print("• Genera pocas señales pero de alta calidad")
    print("• Solo opera cuando hay cruce de MA200 (conservador)")
    print("• Mejor en mercados con tendencia clara")
    print("• Puede tener drawdowns largos en mercados laterales")
    print("• Stop loss más amplio (5%) para evitar salidas prematuras")
    print("• Take profit ambicioso (15%) para capturar tendencias completas")
    print("• Presiona Ctrl+C para detener el sistema de forma segura")
    print("=" * 70)

    input("\nPresiona ENTER para iniciar el trading con MA200...")

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
