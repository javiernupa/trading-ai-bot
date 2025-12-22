"""Trading Engine - Motor de backtesting y ejecución."""

from .backtest import Backtester
from .metrics import MetricsCalculator
from .models import (
    BacktestResult,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    Position,
    Trade,
)
from .portfolio import Portfolio
from .strategy_interface import Strategy
from .visualization import BacktestVisualizer

__version__ = "0.1.0"

__all__ = [
    "Backtester",
    "Strategy",
    "Portfolio",
    "MetricsCalculator",
    "BacktestVisualizer",
    "BacktestResult",
    "Order",
    "OrderSide",
    "OrderStatus",
    "OrderType",
    "Position",
    "Trade",
]
