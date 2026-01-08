"""Test de conexión y datos de criptomonedas con Alpaca."""

import os

from dotenv import load_dotenv

from trading_engine.data.crypto_provider import AlpacaCryptoProvider

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")


def test_crypto_data():
    """Test del proveedor de datos crypto."""
    print("=" * 70)
    print("TEST: PROVEEDOR DE DATOS CRYPTO")
    print("=" * 70)

    provider = AlpacaCryptoProvider(api_key=API_KEY, secret_key=SECRET_KEY)

    cryptos = ["BTC/USD", "ETH/USD", "SOL/USD"]

    for symbol in cryptos:
        print(f"\n📊 {symbol}")
        print("-" * 70)

        # Test 1: Última cotización
        try:
            quote = provider.fetch_latest_quote(symbol)
            print(f"  ✓ Bid: ${quote['bid']:,.2f} | Ask: ${quote['ask']:,.2f}")
            print(f"    Timestamp: {quote['timestamp']}")
        except Exception as e:
            print(f"  ✗ Error obteniendo quote: {e}")

        # Test 2: Última barra
        try:
            bar = provider.fetch_latest_bar(symbol)
            print(f"  ✓ Close: ${bar['close']:,.2f} | Volume: {bar['volume']:,.0f}")
            print(
                f"    OHLC: ${bar['open']:,.2f} / ${bar['high']:,.2f} / "
                f"${bar['low']:,.2f} / ${bar['close']:,.2f}"
            )
        except Exception as e:
            print(f"  ✗ Error obteniendo bar: {e}")

    # Test 3: Datos históricos
    print(f"\n📈 Datos históricos de BTC/USD (últimos 7 días)")
    print("-" * 70)
    try:
        data = provider.fetch_data(
            symbol="BTC/USD",
            start_date="2024-12-15",
            end_date="2024-12-22",
            timeframe="1Day",
        )

        print(f"  ✓ Descargados {len(data)} registros")
        print("\n  Últimas 3 barras:")
        print(data.tail(3).to_string())

    except Exception as e:
        print(f"  ✗ Error: {e}")


def main():
    """Función principal."""
    print("=" * 70)
    print("TEST DE CONEXIÓN A ALPACA CRYPTO")
    print("=" * 70)

    if not API_KEY or not SECRET_KEY:
        print("\n❌ ERROR: Faltan credenciales de Alpaca")
        print("   Configura ALPACA_API_KEY y ALPACA_SECRET_KEY en .env")
        return

    print(f"\nAPI Key: {API_KEY[:10]}...")
    print(f"Secret Key: {SECRET_KEY[:10]}...")

    test_crypto_data()

    print("\n" + "=" * 70)
    print("✅ ¡Tests completados!")
    print("=" * 70)
    print("\nPuedes ejecutar live_trading_crypto.py para trading de criptomonedas.")


if __name__ == "__main__":
    main()
