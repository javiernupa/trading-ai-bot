"""Tests de importación del paquete strategies."""

import pytest


def test_import_strategies_module() -> None:
    """Test que se puede importar el módulo strategies."""
    import strategies
    
    assert strategies is not None


def test_import_rsi_strategy() -> None:
    """Test que se puede importar RsiStrategy."""
    from strategies.rsi import RsiStrategy
    
    assert RsiStrategy is not None


def test_import_base_strategy() -> None:
    """Test que se puede importar BaseStrategy."""
    from strategies.base import BaseStrategy
    
    assert BaseStrategy is not None


def test_rsi_strategy_instantiation() -> None:
    """Test que se puede instanciar RsiStrategy."""
    from strategies.rsi import RsiStrategy
    
    strategy = RsiStrategy(period=14, lower=30, upper=70)
    
    assert strategy.period == 14
    assert strategy.lower == 30
    assert strategy.upper == 70
