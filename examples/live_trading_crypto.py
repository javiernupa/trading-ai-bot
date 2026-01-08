"""Ejemplo de trading en vivo con criptomonedas en Alpaca.

Este ejemplo usa configuración desde .env para todos los parámetros.
Puedes cambiar las estrategias y parámetros editando el archivo .env.
"""

import os
from datetime import datetime

from dotenv import load_dotenv

from strategies import load_strategies_from_env, CombinedStrategy
from trading_engine.brokers.alpaca_broker import AlpacaBroker
from trading_engine.data.crypto_provider import AlpacaCryptoProvider
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

# Criptomonedas (por defecto las 5 principales)
SYMBOLS_STR = os.getenv("CRYPTO_SYMBOLS", "BTC/USD,ETH/USD,SOL/USD,AVAX/USD,DOGE/USD")
SYMBOLS = [s.strip() for s in SYMBOLS_STR.split(",")]

# Parámetros de trading para crypto
INITIAL_CAPITAL = float(os.getenv("INITIAL_CAPITAL", "100000"))
CAPITAL_PER_SYMBOL = float(os.getenv("CAPITAL_PER_SYMBOL", "5000"))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "60"))
LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", "3"))
TIMEFRAME = os.getenv("TIMEFRAME", "1Hour")

# Gestión de riesgo para crypto
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "0.05"))
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "0.10"))


def main():
    """Función principal."""
    print("=" * 70)
    print("SISTEMA DE TRADING EN VIVO - CRIPTOMONEDAS (ALPACA)")
    print("=" * 70)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Modo: {'PAPER TRADING' if PAPER_TRADING else '⚠️  LIVE TRADING ⚠️ '}")

    print(f"\n💰 Criptomonedas: {', '.join(SYMBOLS)}")
    print(f"Capital por crypto: ${CAPITAL_PER_SYMBOL:,}")
    print(f"Capital total: ${CAPITAL_PER_SYMBOL * len(SYMBOLS):,}")
    print(f"Timeframe de análisis: {TIMEFRAME} (barras de 1 hora)")
    print(f"Historial: {LOOKBACK_DAYS} días = {LOOKBACK_DAYS * 24} barras horarias")
    print(f"Intervalo de actualización: {UPDATE_INTERVAL}s")
    
    print(f"\n🛡️ Gestión de Riesgo (ajustada para volatilidad crypto):")
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
        print("⚠️  LAS CRIPTOMONEDAS SON EXTREMADAMENTE VOLÁTILES")
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
        
        print(f"✅ Estrategia cargada: {strategy}")
        print(f"   • {len(strategies)} estrategias activas")
        print(f"   • Consenso: {consensus}/{len(strategies)}")
        
        print("\n📋 Estrategias configuradas:")
        for i, s in enumerate(strategies, 1):
            print(f"   {i}. {s}")
            
    except Exception as e:
        print(f"❌ Error cargando estrategias desde .env: {e}")
        print("\n💡 Consejo: Verifica tu archivo .env")
        print("Ejemplo de configuración:")
        print("  ACTIVE_STRATEGIES=RSI,MACD,BOLLINGER")
        print("  CONSENSUS_THRESHOLD=2")
        print("  STRATEGY_RSI=period:14,lower:30,upper:70")
        return

    # Crear broker (mismo para stocks y crypto)
    print("\n🔗 Conectando a Alpaca...")
    broker = AlpacaBroker(
        api_key=API_KEY,
        secret_key=SECRET_KEY,
        paper=PAPER_TRADING,
    )

    # Crear proveedor de datos para CRYPTO
    data_provider = AlpacaCryptoProvider(
        api_key=API_KEY,
        secret_key=SECRET_KEY,
    )

    # Crear motor de trading
    engine = MultiSymbolLiveEngine(
        symbols=SYMBOLS,
        strategy=strategy,
        broker=broker,
        data_provider=data_provider,
        initial_capital=INITIAL_CAPITAL,
        capital_per_symbol=CAPITAL_PER_SYMBOL,
        update_interval=UPDATE_INTERVAL,
        lookback_days=LOOKBACK_DAYS,
        timeframe=TIMEFRAME,  # Usar barras de 1 hora para crypto
        stop_loss_pct=STOP_LOSS_PCT,
        take_profit_pct=TAKE_PROFIT_PCT,
    )

    # Mostrar información importante
    print("\n" + "=" * 70)
    print("⚠️  CONSIDERACIONES ESPECIALES PARA CRIPTOMONEDAS")
    print("=" * 70)
    print("• Las criptomonedas operan 24/7 (sin horario de mercado)")
    print("• Volatilidad MUCHO mayor que acciones tradicionales")
    print("• Stop loss más amplio (5%) para evitar salidas prematuras")
    print("• Take profit más ambicioso (10%) aprovechando movimientos grandes")
    print("• Actualización más frecuente (60s) por cambios rápidos de precio")
    print("• Presiona Ctrl+C para detener el sistema de forma segura")
    print("=" * 70)

    input("\nPresiona ENTER para iniciar el trading de CRIPTOMONEDAS...")

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
