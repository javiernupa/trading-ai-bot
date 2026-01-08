"""Ejemplo de trading usando estrategias configuradas desde .env

Este ejemplo muestra cómo usar el sistema de configuración de estrategias
desde el archivo .env, permitiendo cambiar estrategias sin modificar código.

Pasos:
1. Configura tu archivo .env con las estrategias deseadas
2. Ejecuta este script
3. Las estrategias se cargarán automáticamente desde .env
"""

from dotenv import load_dotenv
from strategies import (
    load_strategies_from_env,
    print_strategy_config,
    CombinedStrategy,
)
from trading_engine import MultiSymbolLiveEngine
from trading_engine.data import AlpacaDataProvider
import os

# Cargar configuración desde .env
load_dotenv()


def main():
    """Ejecuta trading en vivo con estrategias configuradas desde .env."""
    
    print("\n" + "🚀 " * 35)
    print("TRADING CON ESTRATEGIAS DESDE .ENV")
    print("🚀 " * 35)
    
    # Mostrar configuración actual
    print_strategy_config()
    
    # Cargar estrategias desde .env
    print("\n📦 Cargando estrategias desde .env...")
    print("-" * 70)
    strategies, consensus = load_strategies_from_env()
    
    if not strategies:
        print("\n❌ No se pudieron cargar estrategias. Verifica tu archivo .env")
        return
    
    print(f"\n✅ {len(strategies)} estrategias cargadas correctamente")
    print()
    
    # Crear estrategia combinada
    combined_strategy = CombinedStrategy(strategies, consensus)
    print(f"🎯 Estrategia Combinada: {combined_strategy}")
    print()
    
    # Obtener parámetros de trading desde .env
    symbols = os.getenv('SYMBOLS', 'AAPL,MSFT,GOOGL').split(',')
    symbols = [s.strip() for s in symbols]
    
    capital_per_symbol = float(os.getenv('CAPITAL_PER_SYMBOL', '1000'))
    update_interval = int(os.getenv('UPDATE_INTERVAL', '300'))
    lookback_days = int(os.getenv('LOOKBACK_DAYS', '100'))
    stop_loss = float(os.getenv('STOP_LOSS_PCT', '0.02'))
    take_profit = float(os.getenv('TAKE_PROFIT_PCT', '0.05'))
    trading_mode = os.getenv('TRADING_MODE', 'paper')
    
    # Mostrar configuración de trading
    print("📋 CONFIGURACIÓN DE TRADING:")
    print("-" * 70)
    print(f"   Símbolos: {', '.join(symbols)}")
    print(f"   Capital por símbolo: ${capital_per_symbol:,.2f}")
    print(f"   Intervalo de actualización: {update_interval}s")
    print(f"   Días de historial: {lookback_days}")
    print(f"   Stop Loss: {stop_loss * 100:.1f}%")
    print(f"   Take Profit: {take_profit * 100:.1f}%")
    print(f"   Modo: {trading_mode.upper()}")
    print()
    
    # Validar API keys
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    base_url = os.getenv('ALPACA_BASE_URL')
    
    if not api_key or not secret_key:
        print("❌ Error: ALPACA_API_KEY y ALPACA_SECRET_KEY no configuradas en .env")
        return
    
    # Advertencia para modo live
    if trading_mode == 'live':
        print("⚠️  " + "=" * 68)
        print("⚠️  ADVERTENCIA: MODO LIVE TRADING ACTIVADO")
        print("⚠️  Se realizarán operaciones con DINERO REAL")
        print("⚠️  " + "=" * 68)
        response = input("\n¿Deseas continuar? (escribe 'SI' para confirmar): ")
        if response != 'SI':
            print("❌ Trading cancelado")
            return
        print()
    
    # Crear data provider
    print("🔌 Conectando con Alpaca...")
    data_provider = AlpacaDataProvider(
        api_key=api_key,
        secret_key=secret_key,
        base_url=base_url,
    )
    print("✓ Conexión establecida")
    print()
    
    # Crear motor de trading
    print("⚙️  Inicializando motor de trading...")
    engine = MultiSymbolLiveEngine(
        symbols=symbols,
        strategy=combined_strategy,
        data_provider=data_provider,
        capital_per_symbol=capital_per_symbol,
        lookback_days=lookback_days,
        update_interval=update_interval,
    )
    print("✓ Motor inicializado")
    print()
    
    # Iniciar trading
    print("=" * 70)
    print("🟢 INICIANDO TRADING EN VIVO")
    print("=" * 70)
    print()
    print("Presiona Ctrl+C para detener el trading de forma segura")
    print()
    
    try:
        engine.run()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("🛑 Deteniendo trading...")
        print("=" * 70)
        engine.stop()
        print("\n✅ Trading detenido de forma segura")
        print()


if __name__ == "__main__":
    main()
