"""Test de conexión a Alpaca (sin realizar operaciones)."""

import os

from dotenv import load_dotenv

from trading_engine.brokers.alpaca_broker import AlpacaBroker
from trading_engine.data.alpaca_provider import AlpacaDataProvider

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")


def test_broker_connection():
    """Test de conexión al broker."""
    print("\n" + "=" * 60)
    print("TEST 1: Conexión al Broker")
    print("=" * 60)

    broker = AlpacaBroker(
        api_key=API_KEY,
        secret_key=SECRET_KEY,
        paper=True,  # Siempre paper para tests
    )

    # Conectar
    if broker.connect():
        print("✓ Conexión exitosa\n")

        # Obtener info de cuenta
        account = broker.get_account_info()
        print("Información de la cuenta:")
        print(f"  - Número: {account['account_number']}")
        print(f"  - Status: {account['status']}")
        print(f"  - Capital: ${account['equity']:,.2f}")
        print(f"  - Cash: ${account['cash']:,.2f}")
        print(f"  - Poder de compra: ${account['buying_power']:,.2f}")

        # Obtener posiciones
        positions = broker.get_positions()
        print(f"\nPosiciones abiertas: {len(positions)}")
        if positions:
            for symbol, pos in positions.items():
                print(
                    f"  - {symbol}: {pos.quantity:.2f} @ ${pos.entry_price:.2f} "
                    f"(Current: ${pos.current_price:.2f})"
                )

        broker.disconnect()
        return True
    else:
        print("✗ Error de conexión")
        return False


def test_data_provider():
    """Test del proveedor de datos."""
    print("\n" + "=" * 60)
    print("TEST 2: Proveedor de Datos")
    print("=" * 60)

    provider = AlpacaDataProvider(api_key=API_KEY, secret_key=SECRET_KEY)

    # Test 1: Datos históricos
    print("\nDescargando datos históricos de AAPL (últimos 10 días)...")
    try:
        data = provider.fetch_data(
            symbol="AAPL",
            start_date="2024-12-01",
            end_date="2024-12-12",
            timeframe="1Day",
        )

        print(f"✓ Descargados {len(data)} registros")
        print("\nÚltimas 3 barras:")
        print(data.tail(3).to_string())

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    # Test 2: Última cotización
    print("\nObteniendo cotización actual de AAPL...")
    try:
        quote = provider.fetch_latest_quote("AAPL")
        print(f"✓ Bid: ${quote['bid']:.2f} | Ask: ${quote['ask']:.2f}")
        print(f"  Timestamp: {quote['timestamp']}")

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    # Test 3: Última barra
    print("\nObteniendo última barra de AAPL...")
    try:
        bar = provider.fetch_latest_bar("AAPL")
        print(f"✓ Close: ${bar['close']:.2f} | Volume: {bar['volume']:,}")
        print(f"  OHLC: ${bar['open']:.2f} / ${bar['high']:.2f} / "
              f"${bar['low']:.2f} / ${bar['close']:.2f}")

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    return True


def main():
    """Función principal."""
    print("=" * 60)
    print("TEST DE CONEXIÓN A ALPACA")
    print("=" * 60)

    # Validar credenciales
    if not API_KEY or not SECRET_KEY:
        print("\n❌ ERROR: Faltan credenciales de Alpaca")
        print("   Configura ALPACA_API_KEY y ALPACA_SECRET_KEY en .env")
        return

    print(f"\nAPI Key: {API_KEY[:10]}...")
    print(f"Secret Key: {SECRET_KEY[:10]}...")

    # Ejecutar tests
    broker_ok = test_broker_connection()
    data_ok = test_data_provider()

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"Broker: {'✓ OK' if broker_ok else '✗ FALLÓ'}")
    print(f"Data Provider: {'✓ OK' if data_ok else '✗ FALLÓ'}")

    if broker_ok and data_ok:
        print("\n✅ ¡Todos los tests pasaron!")
        print("\nPuedes ejecutar live_trading_alpaca.py para iniciar trading en vivo.")
    else:
        print("\n❌ Algunos tests fallaron. Revisa la configuración.")


if __name__ == "__main__":
    main()
