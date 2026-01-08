"""Demo del sistema de stop loss y take profit."""

from datetime import datetime

# Simular una orden con stop loss y take profit


def demo_bracket_order():
    """Demuestra cómo funcionan las bracket orders."""
    print("=" * 70)
    print("DEMO: BRACKET ORDER CON STOP LOSS Y TAKE PROFIT")
    print("=" * 70)

    # Parámetros
    symbol = "AAPL"
    quantity = 100
    entry_price = 180.00
    capital = quantity * entry_price

    stop_loss_pct = 0.02  # 2%
    take_profit_pct = 0.05  # 5%

    # Cálculos
    stop_loss_price = entry_price * (1 - stop_loss_pct)
    take_profit_price = entry_price * (1 + take_profit_pct)

    max_loss = capital * stop_loss_pct
    target_profit = capital * take_profit_pct

    # Mostrar información
    print(f"\n📊 COMPRA INICIAL")
    print(f"   Símbolo: {symbol}")
    print(f"   Cantidad: {quantity}")
    print(f"   Precio de entrada: ${entry_price:.2f}")
    print(f"   Capital invertido: ${capital:,.2f}")

    print(f"\n🛡️ STOP LOSS (Protección)")
    print(f"   Nivel: {stop_loss_pct:.1%} por debajo")
    print(f"   Precio: ${stop_loss_price:.2f}")
    print(f"   Pérdida máxima: ${max_loss:,.2f}")
    print(f"   Si el precio baja a ${stop_loss_price:.2f}, se vende automáticamente")

    print(f"\n🎯 TAKE PROFIT (Objetivo)")
    print(f"   Nivel: {take_profit_pct:.1%} por encima")
    print(f"   Precio: ${take_profit_price:.2f}")
    print(f"   Ganancia objetivo: ${target_profit:,.2f}")
    print(f"   Si el precio sube a ${take_profit_price:.2f}, se vende automáticamente")

    print(f"\n📈 RATIO RIESGO:BENEFICIO")
    ratio = take_profit_pct / stop_loss_pct
    print(f"   1:{ratio:.1f} - Arriesgas $1 para ganar ${ratio:.1f}")

    print(f"\n⚖️ ESCENARIOS POSIBLES")
    print(f"   ✅ Mejor caso: +${target_profit:,.2f} ({take_profit_pct:+.1%})")
    print(f"   ❌ Peor caso: -${max_loss:,.2f} ({-stop_loss_pct:.1%})")
    print(
        f"   🔄 Neutral: La posición se mantiene entre ${stop_loss_price:.2f} y ${take_profit_price:.2f}"
    )

    # Simular movimientos de precio
    print(f"\n📉 SIMULACIÓN DE PRECIOS")
    price_scenarios = [
        (182.00, "📊 Normal"),
        (185.00, "📈 Subiendo"),
        (189.00, "🎯 TAKE PROFIT EJECUTADO!"),
        (178.00, "📉 Bajando"),
        (176.40, "🛡️ STOP LOSS EJECUTADO!"),
    ]

    for price, status in price_scenarios:
        pnl = (price - entry_price) * quantity
        pnl_pct = (price / entry_price - 1) * 100

        print(f"   Precio: ${price:6.2f} | PnL: ${pnl:7,.2f} ({pnl_pct:+5.1f}%) | {status}")


def demo_multiple_positions():
    """Demuestra gestión de riesgo en múltiples posiciones."""
    print("\n\n" + "=" * 70)
    print("DEMO: PORTFOLIO CON 5 POSICIONES")
    print("=" * 70)

    positions = [
        {"symbol": "AAPL", "capital": 20000, "entry": 180.00},
        {"symbol": "GOOGL", "capital": 20000, "entry": 140.00},
        {"symbol": "MSFT", "capital": 20000, "entry": 380.00},
        {"symbol": "TSLA", "capital": 20000, "entry": 250.00},
        {"symbol": "AMZN", "capital": 20000, "entry": 175.00},
    ]

    stop_loss_pct = 0.02  # 2%
    take_profit_pct = 0.05  # 5%

    total_capital = sum(p["capital"] for p in positions)
    total_max_loss = total_capital * stop_loss_pct
    total_target_profit = total_capital * take_profit_pct

    print(f"\n💰 CAPITAL TOTAL: ${total_capital:,.0f}")
    print(f"   Capital por posición: ${positions[0]['capital']:,.0f}")
    print(f"   Número de posiciones: {len(positions)}")

    print(f"\n🛡️ PROTECCIÓN DEL PORTFOLIO")
    print(f"   Stop Loss: {stop_loss_pct:.1%} por posición")
    print(f"   Pérdida máxima por posición: ${positions[0]['capital'] * stop_loss_pct:,.0f}")
    print(f"   Pérdida máxima total: ${total_max_loss:,.0f} ({stop_loss_pct:.1%} del total)")

    print(f"\n🎯 OBJETIVOS DEL PORTFOLIO")
    print(f"   Take Profit: {take_profit_pct:.1%} por posición")
    print(
        f"   Ganancia objetivo por posición: ${positions[0]['capital'] * take_profit_pct:,.0f}"
    )
    print(f"   Ganancia objetivo total: ${total_target_profit:,.0f} ({take_profit_pct:.1%} del total)")

    print(f"\n📊 DETALLE POR POSICIÓN:")
    print("-" * 70)
    print(f"{'Símbolo':<8} {'Precio':<10} {'Qty':<8} {'Stop Loss':<12} {'Take Profit':<12}")
    print("-" * 70)

    for pos in positions:
        qty = int(pos["capital"] / pos["entry"])
        stop_loss = pos["entry"] * (1 - stop_loss_pct)
        take_profit = pos["entry"] * (1 + take_profit_pct)

        print(
            f"{pos['symbol']:<8} ${pos['entry']:<9.2f} {qty:<8} ${stop_loss:<11.2f} ${take_profit:<11.2f}"
        )


def demo_risk_scenarios():
    """Demuestra diferentes escenarios de riesgo."""
    print("\n\n" + "=" * 70)
    print("DEMO: COMPARACIÓN DE CONFIGURACIONES DE RIESGO")
    print("=" * 70)

    capital = 20000
    entry_price = 180.00

    configs = [
        {
            "name": "Conservador",
            "sl": 0.01,
            "tp": 0.03,
            "desc": "Protección máxima, salidas rápidas",
        },
        {
            "name": "Moderado (Recomendado)",
            "sl": 0.02,
            "tp": 0.05,
            "desc": "Balance entre riesgo y oportunidad",
        },
        {
            "name": "Agresivo",
            "sl": 0.05,
            "tp": 0.15,
            "desc": "Mayor riesgo, mayores objetivos",
        },
    ]

    print(f"\nCapital por posición: ${capital:,.0f}")
    print(f"Precio de entrada: ${entry_price:.2f}\n")

    for config in configs:
        sl_pct = config["sl"]
        tp_pct = config["tp"]
        max_loss = capital * sl_pct
        target_profit = capital * tp_pct
        ratio = tp_pct / sl_pct

        print(f"{'=' * 70}")
        print(f"📌 {config['name'].upper()}")
        print(f"   {config['desc']}")
        print(f"{'=' * 70}")
        print(f"   Stop Loss: {sl_pct:.1%} → Max Loss: ${max_loss:,.0f}")
        print(f"   Take Profit: {tp_pct:.1%} → Target: ${target_profit:,.0f}")
        print(f"   Ratio: 1:{ratio:.1f}")
        print()


def main():
    """Función principal."""
    demo_bracket_order()
    demo_multiple_positions()
    demo_risk_scenarios()

    print("\n" + "=" * 70)
    print("💡 CONCLUSIONES")
    print("=" * 70)
    print("""
1. Stop Loss protege tu capital limitando pérdidas
2. Take Profit asegura ganancias al alcanzar objetivos
3. Ambos se ejecutan automáticamente sin intervención
4. Ratio riesgo:beneficio debe ser al menos 1:2
5. Configura según tu tolerancia al riesgo
6. SIEMPRE usa stop loss en trading en vivo

🛡️ Protege tu capital. Opera con disciplina.
    """)


if __name__ == "__main__":
    main()
