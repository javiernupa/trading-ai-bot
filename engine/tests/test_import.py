"""Tests de importación del paquete trading_engine."""

import pytest


def test_import_backtester() -> None:
    """Test que se puede importar Backtester."""
    from trading_engine import Backtester
    
    assert Backtester is not None


def test_import_strategy() -> None:
    """Test que se puede importar Strategy."""
    from trading_engine import Strategy
    
    assert Strategy is not None


def test_import_portfolio() -> None:
    """Test que se puede importar Portfolio."""
    from trading_engine import Portfolio
    
    assert Portfolio is not None


def test_import_models() -> None:
    """Test que se pueden importar los modelos."""
    from trading_engine import (
        BacktestResult,
        Order,
        OrderSide,
        OrderStatus,
        OrderType,
        Position,
        Trade,
    )
    
    assert BacktestResult is not None
    assert Order is not None
    assert OrderSide is not None
    assert OrderStatus is not None
    assert OrderType is not None
    assert Position is not None
    assert Trade is not None


def test_import_metrics() -> None:
    """Test que se puede importar MetricsCalculator."""
    from trading_engine import MetricsCalculator
    
    assert MetricsCalculator is not None
