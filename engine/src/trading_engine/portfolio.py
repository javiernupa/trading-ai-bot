"""Gestión de portfolio y posiciones."""

from __future__ import annotations

from datetime import datetime

from loguru import logger

from .models import Order, OrderSide, OrderStatus, Position, Trade


class Portfolio:
    """Gestiona el capital, posiciones y trades del portfolio."""

    def __init__(
        self,
        initial_cash: float,
        commission_rate: float = 0.001,
        slippage_rate: float = 0.0005,
    ) -> None:
        """Inicializa el portfolio.

        Args:
            initial_cash: Capital inicial disponible
            commission_rate: Tasa de comisión por operación (default: 0.1%)
            slippage_rate: Tasa de slippage estimado (default: 0.05%)
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.commission_rate = commission_rate
        self.slippage_rate = slippage_rate

        self._positions: dict[str, Position] = {}
        self._closed_trades: list[Trade] = []
        self._equity_history: list[tuple[datetime, float]] = []
        self._total_commission = 0.0

        logger.info(
            f"Portfolio initialized: ${initial_cash:,.2f} | "
            f"Commission: {commission_rate*100:.2f}% | "
            f"Slippage: {slippage_rate*100:.3f}%"
        )

    @property
    def positions(self) -> dict[str, Position]:
        """Retorna las posiciones actuales."""
        return self._positions

    @property
    def closed_trades(self) -> list[Trade]:
        """Retorna los trades cerrados."""
        return self._closed_trades

    @property
    def total_commission(self) -> float:
        """Retorna la comisión total pagada."""
        return self._total_commission

    @property
    def market_value(self) -> float:
        """Valor de mercado total de las posiciones abiertas."""
        return sum(pos.market_value for pos in self._positions.values())

    @property
    def equity(self) -> float:
        """Equity total (cash + valor posiciones)."""
        return self.cash + self.market_value

    @property
    def total_pnl(self) -> float:
        """PnL total (realizado + no realizado)."""
        realized_pnl = sum(trade.pnl for trade in self._closed_trades)
        unrealized_pnl = sum(pos.pnl for pos in self._positions.values())
        return realized_pnl + unrealized_pnl

    def execute_order(self, order: Order, current_price: float, timestamp: datetime) -> bool:
        """Ejecuta una orden en el portfolio.

        Args:
            order: Orden a ejecutar
            current_price: Precio actual del mercado
            timestamp: Timestamp de la ejecución

        Returns:
            True si la orden se ejecutó exitosamente
        """
        # Aplicar slippage
        if order.side == OrderSide.BUY:
            execution_price = current_price * (1 + self.slippage_rate)
        else:
            execution_price = current_price * (1 - self.slippage_rate)

        # Calcular comisión
        trade_value = execution_price * order.quantity
        commission = trade_value * self.commission_rate

        # Verificar si hay posición existente
        existing_position = self._positions.get(order.symbol)

        if order.side == OrderSide.BUY:
            return self._execute_buy(order, execution_price, commission, timestamp, existing_position)
        else:
            return self._execute_sell(order, execution_price, commission, timestamp, existing_position)

    def _execute_buy(
        self,
        order: Order,
        execution_price: float,
        commission: float,
        timestamp: datetime,
        existing_position: Position | None,
    ) -> bool:
        """Ejecuta una orden de compra."""
        cost = execution_price * order.quantity + commission

        if cost > self.cash:
            logger.warning(
                f"Insufficient funds for {order.symbol}: "
                f"Need ${cost:,.2f}, have ${self.cash:,.2f}"
            )
            order.status = OrderStatus.REJECTED
            return False

        # Deducir del cash
        self.cash -= cost
        self._total_commission += commission

        if existing_position and existing_position.is_short:
            # Cerrar posición corta
            self._close_position(existing_position, execution_price, timestamp, commission)
        elif existing_position and existing_position.is_long:
            # Añadir a posición larga existente (promedio de precio)
            total_quantity = existing_position.quantity + order.quantity
            avg_price = (
                existing_position.entry_price * existing_position.quantity
                + execution_price * order.quantity
            ) / total_quantity
            existing_position.quantity = total_quantity
            existing_position.entry_price = avg_price
        else:
            # Abrir nueva posición larga
            self._positions[order.symbol] = Position(
                symbol=order.symbol,
                quantity=order.quantity,
                entry_price=execution_price,
                entry_time=timestamp,
                current_price=execution_price,
            )

        order.status = OrderStatus.FILLED
        order.filled_price = execution_price
        order.commission = commission

        logger.info(
            f"BUY {order.quantity} {order.symbol} @ ${execution_price:.2f} | "
            f"Commission: ${commission:.2f} | Cash: ${self.cash:,.2f}"
        )
        return True

    def _execute_sell(
        self,
        order: Order,
        execution_price: float,
        commission: float,
        timestamp: datetime,
        existing_position: Position | None,
    ) -> bool:
        """Ejecuta una orden de venta."""
        if not existing_position or existing_position.quantity < order.quantity:
            logger.warning(
                f"Insufficient position for {order.symbol}: "
                f"Trying to sell {order.quantity}, have {existing_position.quantity if existing_position else 0}"
            )
            order.status = OrderStatus.REJECTED
            return False

        # Añadir al cash (menos comisión)
        proceeds = execution_price * order.quantity - commission
        self.cash += proceeds
        self._total_commission += commission

        # Cerrar posición (parcial o total)
        if existing_position.quantity == order.quantity:
            self._close_position(existing_position, execution_price, timestamp, commission)
        else:
            # Venta parcial
            existing_position.quantity -= order.quantity

        order.status = OrderStatus.FILLED
        order.filled_price = execution_price
        order.commission = commission

        logger.info(
            f"SELL {order.quantity} {order.symbol} @ ${execution_price:.2f} | "
            f"Commission: ${commission:.2f} | Cash: ${self.cash:,.2f}"
        )
        return True

    def _close_position(
        self, position: Position, exit_price: float, exit_time: datetime, commission: float
    ) -> None:
        """Cierra una posición y registra el trade."""
        position.exit_price = exit_price
        position.exit_time = exit_time
        position.current_price = exit_price

        # Calcular PnL
        if position.is_long:
            pnl = (exit_price - position.entry_price) * position.quantity - commission
        else:
            pnl = (position.entry_price - exit_price) * abs(position.quantity) - commission

        pnl_percent = (pnl / (position.entry_price * abs(position.quantity))) * 100
        duration = (exit_time - position.entry_time).total_seconds()

        trade = Trade(
            symbol=position.symbol,
            entry_time=position.entry_time,
            exit_time=exit_time,
            entry_price=position.entry_price,
            exit_price=exit_price,
            quantity=abs(position.quantity),
            side="long" if position.is_long else "short",
            pnl=pnl,
            pnl_percent=pnl_percent,
            commission=commission,
            duration_seconds=duration,
        )

        self._closed_trades.append(trade)
        del self._positions[position.symbol]

        logger.info(
            f"CLOSED {position.symbol}: PnL ${pnl:,.2f} ({pnl_percent:+.2f}%) | "
            f"Duration: {duration/3600:.1f}h"
        )

    def update_positions(self, symbol: str, current_price: float) -> None:
        """Actualiza el precio actual de una posición.

        Args:
            symbol: Símbolo del activo
            current_price: Precio actual del mercado
        """
        if symbol in self._positions:
            self._positions[symbol].current_price = current_price

    def record_equity(self, timestamp: datetime) -> None:
        """Registra el equity actual en el histórico.

        Args:
            timestamp: Timestamp del registro
        """
        self._equity_history.append((timestamp, self.equity))

    def get_equity_curve(self) -> list[tuple[datetime, float]]:
        """Retorna la curva de equity histórica."""
        return self._equity_history
