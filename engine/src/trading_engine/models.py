"""Modelos de datos para el motor de trading."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Literal

import pandas as pd


class OrderType(str, Enum):
    """Tipos de órdenes soportadas."""

    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


class OrderSide(str, Enum):
    """Lado de la orden (compra/venta)."""

    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, Enum):
    """Estados posibles de una orden."""

    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    """Representa una orden de trading."""

    symbol: str
    side: OrderSide
    quantity: float
    order_type: OrderType = OrderType.MARKET
    price: float | None = None
    timestamp: datetime | None = None
    status: OrderStatus = OrderStatus.PENDING
    filled_price: float | None = None
    commission: float = 0.0

    def __post_init__(self) -> None:
        """Validación post-inicialización."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class Position:
    """Representa una posición abierta."""

    symbol: str
    quantity: float
    entry_price: float
    entry_time: datetime
    current_price: float | None = None
    exit_price: float | None = None
    exit_time: datetime | None = None

    @property
    def is_long(self) -> bool:
        """Verifica si es posición larga."""
        return self.quantity > 0

    @property
    def is_short(self) -> bool:
        """Verifica si es posición corta."""
        return self.quantity < 0

    @property
    def market_value(self) -> float:
        """Valor de mercado actual de la posición."""
        price = self.current_price or self.entry_price
        return abs(self.quantity) * price

    @property
    def pnl(self) -> float:
        """Profit and Loss no realizado."""
        if self.current_price is None:
            return 0.0
        if self.is_long:
            return (self.current_price - self.entry_price) * self.quantity
        return (self.entry_price - self.current_price) * abs(self.quantity)

    @property
    def pnl_percent(self) -> float:
        """PnL en porcentaje."""
        if self.entry_price == 0:
            return 0.0
        return (self.pnl / (self.entry_price * abs(self.quantity))) * 100


@dataclass
class Trade:
    """Representa un trade completado (entrada + salida)."""

    symbol: str
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    quantity: float
    side: Literal["long", "short"]
    pnl: float
    pnl_percent: float
    commission: float
    duration_seconds: float

    @property
    def is_winner(self) -> bool:
        """Verifica si el trade fue ganador."""
        return self.pnl > 0


@dataclass
class BacktestResult:
    """Resultados del backtesting."""

    # Performance metrics
    total_pnl: float
    total_return_percent: float
    sharpe_ratio: float
    max_drawdown: float
    max_drawdown_percent: float

    # Trade statistics
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    average_win: float
    average_loss: float
    profit_factor: float

    # Additional metrics
    initial_capital: float
    final_capital: float
    total_commission: float
    trades: list[Trade] = field(default_factory=list)
    equity_curve: pd.DataFrame | None = None

    def summary(self) -> dict:
        """Retorna un resumen de las métricas principales."""
        return {
            "Total PnL": f"${self.total_pnl:,.2f}",
            "Total Return": f"{self.total_return_percent:.2f}%",
            "Sharpe Ratio": f"{self.sharpe_ratio:.2f}",
            "Max Drawdown": f"{self.max_drawdown_percent:.2f}%",
            "Total Trades": self.total_trades,
            "Win Rate": f"{self.win_rate:.2f}%",
            "Profit Factor": f"{self.profit_factor:.2f}",
            "Final Capital": f"${self.final_capital:,.2f}",
        }
