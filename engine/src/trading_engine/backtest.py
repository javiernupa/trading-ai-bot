"""Motor de backtesting para estrategias de trading."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
from loguru import logger

from .metrics import MetricsCalculator
from .models import BacktestResult, Order, OrderSide, OrderType
from .portfolio import Portfolio
from .strategy_interface import Strategy


class Backtester:
    """Motor de backtesting para simular estrategias sobre datos históricos."""

    def __init__(
        self,
        strategy: Strategy,
        data: pd.DataFrame,
        initial_cash: float = 10000,
        commission: float = 0.001,
        slippage: float = 0.0005,
    ) -> None:
        """Inicializa el backtester.

        Args:
            strategy: Estrategia a testear
            data: DataFrame con datos históricos (requiere columnas: date/timestamp, close)
            initial_cash: Capital inicial
            commission: Tasa de comisión por operación
            slippage: Tasa de slippage estimado
        """
        self.strategy = strategy
        self.data = data.copy()
        self.initial_cash = initial_cash

        # Validar datos
        if "close" not in self.data.columns:
            raise ValueError("Data must contain 'close' column")

        # Asegurar que haya un índice temporal
        if not isinstance(self.data.index, pd.DatetimeIndex):
            if "date" in self.data.columns:
                self.data["date"] = pd.to_datetime(self.data["date"])
                self.data.set_index("date", inplace=True)
            elif "timestamp" in self.data.columns:
                self.data["timestamp"] = pd.to_datetime(self.data["timestamp"])
                self.data.set_index("timestamp", inplace=True)
            else:
                # Crear índice temporal genérico
                self.data.index = pd.date_range(
                    start="2020-01-01", periods=len(self.data), freq="D"
                )

        self.portfolio = Portfolio(
            initial_cash=initial_cash,
            commission_rate=commission,
            slippage_rate=slippage,
        )

        logger.info(f"Backtester initialized with {len(self.data)} data points")

    def run(self) -> BacktestResult:
        """Ejecuta el backtest de la estrategia.

        Returns:
            BacktestResult con métricas completas del backtest
        """
        logger.info("Starting backtest...")

        # Generar señales de la estrategia
        df = self.strategy.generate_signals(self.data)

        if "signal" not in df.columns:
            raise ValueError("Strategy must generate 'signal' column")

        # Iterar sobre los datos
        symbol = "ASSET"  # Símbolo genérico para single-asset
        position_size = 0  # Tracking de posición actual

        for idx, row in df.iterrows():
            timestamp = idx if isinstance(idx, datetime) else pd.to_datetime(idx)
            current_price = row["close"]
            signal = row.get("signal", 0)

            # Actualizar precio de posiciones existentes
            self.portfolio.update_positions(symbol, current_price)

            # Ejecutar órdenes basadas en señales
            if signal == 1 and position_size == 0:
                # Señal de compra - abrir posición larga
                quantity = (self.portfolio.cash * 0.95) / current_price  # Usar 95% del cash
                order = Order(
                    symbol=symbol,
                    side=OrderSide.BUY,
                    quantity=quantity,
                    order_type=OrderType.MARKET,
                    timestamp=timestamp,
                )
                if self.portfolio.execute_order(order, current_price, timestamp):
                    position_size = quantity

            elif signal == -1 and position_size > 0:
                # Señal de venta - cerrar posición larga
                order = Order(
                    symbol=symbol,
                    side=OrderSide.SELL,
                    quantity=position_size,
                    order_type=OrderType.MARKET,
                    timestamp=timestamp,
                )
                if self.portfolio.execute_order(order, current_price, timestamp):
                    position_size = 0

            # Registrar equity
            self.portfolio.record_equity(timestamp)

        # Cerrar posiciones abiertas al final
        if symbol in self.portfolio.positions:
            final_price = df["close"].iloc[-1]
            final_timestamp = df.index[-1]
            remaining_position = self.portfolio.positions[symbol]

            order = Order(
                symbol=symbol,
                side=OrderSide.SELL,
                quantity=remaining_position.quantity,
                order_type=OrderType.MARKET,
                timestamp=final_timestamp,
            )
            self.portfolio.execute_order(order, final_price, final_timestamp)

        # Calcular métricas
        logger.info("Calculating metrics...")
        result = MetricsCalculator.calculate_metrics(
            trades=self.portfolio.closed_trades,
            equity_curve=self.portfolio.get_equity_curve(),
            initial_capital=self.initial_cash,
            total_commission=self.portfolio.total_commission,
        )

        logger.success(
            f"Backtest completed: {result.total_trades} trades, "
            f"PnL: ${result.total_pnl:,.2f} ({result.total_return_percent:.2f}%)"
        )

        return result
