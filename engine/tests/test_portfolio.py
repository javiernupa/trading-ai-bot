"""Tests para el módulo de portfolio."""

from datetime import datetime

import pytest

from trading_engine.models import Order, OrderSide, OrderStatus, OrderType
from trading_engine.portfolio import Portfolio


class TestPortfolio:
    """Tests para la clase Portfolio."""

    @pytest.fixture
    def portfolio(self) -> Portfolio:
        """Fixture con portfolio de $10k."""
        return Portfolio(initial_cash=10000, commission_rate=0.001, slippage_rate=0.0005)

    def test_portfolio_initialization(self, portfolio: Portfolio) -> None:
        """Test inicialización del portfolio."""
        assert portfolio.initial_cash == 10000
        assert portfolio.cash == 10000
        assert portfolio.commission_rate == 0.001
        assert portfolio.slippage_rate == 0.0005
        assert len(portfolio.positions) == 0
        assert len(portfolio.closed_trades) == 0

    def test_execute_buy_order(self, portfolio: Portfolio) -> None:
        """Test ejecución de orden de compra."""
        order = Order(
            symbol="TEST",
            side=OrderSide.BUY,
            quantity=10,
            order_type=OrderType.MARKET,
        )
        
        success = portfolio.execute_order(order, current_price=100.0, timestamp=datetime.now())
        
        assert success is True
        assert order.status == OrderStatus.FILLED
        assert "TEST" in portfolio.positions
        assert portfolio.positions["TEST"].quantity == 10
        assert portfolio.cash < 10000  # Se dedujo el costo

    def test_execute_sell_order(self, portfolio: Portfolio) -> None:
        """Test ejecución de orden de venta."""
        # Primero comprar
        buy_order = Order(symbol="TEST", side=OrderSide.BUY, quantity=10)
        portfolio.execute_order(buy_order, current_price=100.0, timestamp=datetime.now())
        
        cash_after_buy = portfolio.cash
        
        # Luego vender
        sell_order = Order(symbol="TEST", side=OrderSide.SELL, quantity=10)
        success = portfolio.execute_order(
            sell_order, current_price=105.0, timestamp=datetime.now()
        )
        
        assert success is True
        assert sell_order.status == OrderStatus.FILLED
        assert "TEST" not in portfolio.positions  # Posición cerrada
        assert len(portfolio.closed_trades) == 1
        assert portfolio.cash > cash_after_buy  # Ganancia

    def test_insufficient_funds_rejection(self, portfolio: Portfolio) -> None:
        """Test rechazo de orden por fondos insuficientes."""
        order = Order(
            symbol="TEST",
            side=OrderSide.BUY,
            quantity=1000,  # Muy grande
        )
        
        success = portfolio.execute_order(order, current_price=100.0, timestamp=datetime.now())
        
        assert success is False
        assert order.status == OrderStatus.REJECTED
        assert len(portfolio.positions) == 0

    def test_insufficient_position_rejection(self, portfolio: Portfolio) -> None:
        """Test rechazo de venta sin posición."""
        order = Order(symbol="TEST", side=OrderSide.SELL, quantity=10)
        
        success = portfolio.execute_order(order, current_price=100.0, timestamp=datetime.now())
        
        assert success is False
        assert order.status == OrderStatus.REJECTED

    def test_commission_calculation(self, portfolio: Portfolio) -> None:
        """Test cálculo de comisiones."""
        order = Order(symbol="TEST", side=OrderSide.BUY, quantity=10)
        portfolio.execute_order(order, current_price=100.0, timestamp=datetime.now())
        
        expected_commission = 1000 * (1 + 0.0005) * 0.001  # price * (1+slippage) * commission
        
        assert portfolio.total_commission > 0
        assert abs(portfolio.total_commission - expected_commission) < 0.01

    def test_equity_calculation(self, portfolio: Portfolio) -> None:
        """Test cálculo de equity."""
        # Comprar
        order = Order(symbol="TEST", side=OrderSide.BUY, quantity=10)
        portfolio.execute_order(order, current_price=100.0, timestamp=datetime.now())
        
        # Actualizar precio
        portfolio.update_positions("TEST", current_price=110.0)
        
        expected_equity = portfolio.cash + (10 * 110.0)
        assert abs(portfolio.equity - expected_equity) < 0.01

    def test_pnl_calculation(self, portfolio: Portfolio) -> None:
        """Test cálculo de PnL."""
        # Comprar a 100
        buy_order = Order(symbol="TEST", side=OrderSide.BUY, quantity=10)
        portfolio.execute_order(buy_order, current_price=100.0, timestamp=datetime.now())
        
        # Vender a 110
        sell_order = Order(symbol="TEST", side=OrderSide.SELL, quantity=10)
        portfolio.execute_order(sell_order, current_price=110.0, timestamp=datetime.now())
        
        # PnL debería ser positivo (ganancia de $10 por acción menos comisiones)
        trade = portfolio.closed_trades[0]
        assert trade.pnl > 0
        assert trade.is_winner is True
