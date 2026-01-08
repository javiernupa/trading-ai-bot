"""Test rápido para verificar que la estrategia genera señales correctamente."""

import os
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv

from strategies import CombinedStrategy
from trading_engine.data.alpaca_provider import AlpacaDataProvider

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")


def test_strategy_signals():
    """Prueba que la estrategia genera señales con datos reales."""
    print("=" * 70)
    print("TEST: VERIFICACIÓN DE SEÑALES DE ESTRATEGIA")
    print("=" * 70)

    # Crear proveedor de datos
    provider = AlpacaDataProvider(api_key=API_KEY, secret_key=SECRET_KEY)

    # Descargar datos de AAPL (últimos 60 días)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)

    print(f"\nDescargando datos de AAPL desde {start_date.date()} hasta {end_date.date()}...")
    data = provider.fetch_data(
        symbol="AAPL",
        start_date=start_date,
        end_date=end_date,
        timeframe="1Day",
    )

    print(f"✓ Descargados {len(data)} registros\n")

    # Crear estrategia
    strategy = CombinedStrategy(
        rsi_period=14,
        rsi_lower=30,
        rsi_upper=70,
        macd_fast=12,
        macd_slow=26,
        macd_signal=9,
        bb_period=20,
        bb_std=2.0,
        consensus_threshold=2,
    )

    # Generar señales
    print("Generando señales con estrategia combinada...")
    data_with_signals = strategy.generate_signals(data)

    # Mostrar últimos 10 días
    print("\n" + "=" * 100)
    print("ÚLTIMOS 10 DÍAS - ANÁLISIS DETALLADO")
    print("=" * 100)

    last_10 = data_with_signals.tail(10)

    for idx, row in last_10.iterrows():
        date = row["timestamp"].strftime("%Y-%m-%d")
        close = row["close"]
        signal = row["signal"]

        print(f"\n📅 {date} - Cierre: ${close:.2f}")
        print(f"   RSI: {row['rsi']:.2f} (Señal: {row['rsi_signal']})")
        print(
            f"   MACD: {row['macd']:.4f} | Signal: {row['macd_signal']:.4f} | "
            f"Histogram: {row['macd_histogram']:.4f} (Señal: {row['macd_signal_ind']})"
        )
        print(
            f"   BB: Upper ${row['bb_upper']:.2f} | Lower ${row['bb_lower']:.2f} "
            f"(Señal: {row['bb_signal']})"
        )
        print(
            f"   Consenso: Compra {int(row['buy_votes'])} | Venta {int(row['sell_votes'])}"
        )

        if signal == 1:
            print(f"   ➡️  SEÑAL FINAL: 🟢 COMPRA")
        elif signal == -1:
            print(f"   ➡️  SEÑAL FINAL: 🔴 VENTA")
        else:
            print(f"   ➡️  SEÑAL FINAL: ⚪ MANTENER")

    # Resumen de señales
    print("\n" + "=" * 70)
    print("RESUMEN DE SEÑALES (todos los días)")
    print("=" * 70)

    buy_signals = (data_with_signals["signal"] == 1).sum()
    sell_signals = (data_with_signals["signal"] == -1).sum()
    hold_signals = (data_with_signals["signal"] == 0).sum()

    print(f"🟢 Señales de COMPRA: {buy_signals}")
    print(f"🔴 Señales de VENTA: {sell_signals}")
    print(f"⚪ Señales de MANTENER: {hold_signals}")
    print(f"📊 Total días analizados: {len(data_with_signals)}")

    # Validación
    print("\n" + "=" * 70)
    print("VALIDACIÓN")
    print("=" * 70)

    if buy_signals == 0 and sell_signals == 0:
        print("⚠️  ADVERTENCIA: No se generaron señales de compra/venta")
        print("   Esto puede suceder si:")
        print("   1. El mercado está en rango (sin tendencia clara)")
        print("   2. Los umbrales de consenso son muy estrictos")
        print("   3. Los indicadores no muestran condiciones extremas")
        print("\n   Sugerencia: Reduce consensus_threshold a 1 para señales más frecuentes")
    else:
        print("✅ La estrategia está generando señales correctamente")
        print(
            f"   Frecuencia de señales: {(buy_signals + sell_signals) / len(data_with_signals) * 100:.1f}%"
        )

    return data_with_signals


if __name__ == "__main__":
    test_strategy_signals()
