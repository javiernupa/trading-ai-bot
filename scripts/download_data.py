"""Script para descargar datos históricos."""

from datetime import datetime, timedelta

from trading_engine.data import DataLoader

# Configuración
SYMBOLS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "BTC-USD", "ETH-USD"]
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365 * 2)  # 2 años de datos

OUTPUT_DIR = "data/historical"


def main():
    """Descarga datos históricos para múltiples símbolos."""
    loader = DataLoader(cache_dir="data/cache", use_cache=True)

    print(f"Descargando datos desde {START_DATE.date()} hasta {END_DATE.date()}\n")

    for symbol in SYMBOLS:
        try:
            print(f"Procesando {symbol}...")

            # Descargar y guardar datos
            output_file = f"{OUTPUT_DIR}/{symbol}.csv"
            filepath = loader.download_and_save(
                symbol=symbol,
                start_date=START_DATE,
                end_date=END_DATE,
                output_file=output_file,
                provider="yahoo",
            )

            print(f"✓ {symbol} guardado en: {filepath}\n")

        except Exception as e:
            print(f"✗ Error con {symbol}: {e}\n")
            continue

    print(f"\n{'=' * 60}")
    print("Descarga completada")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
