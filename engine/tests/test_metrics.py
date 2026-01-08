"""Tests para el cálculo de métricas."""

from datetime import datetime, timedelta

import pandas as pd
import pytest

from trading_engine.metrics import MetricsCalculator
from trading_engine.models import Trade


class TestMetricsCalculator:
    """Tests para MetricsCalculator."""

    @pytest.fixture
    def winning_trades(self) -> list[Trade]:
        """Fixture con trades ganadores."""
        base_time = datetime(2023, 1, 1)
        return [
            Trade(
                symbol="TEST",
                entry_time=base_time,
                exit_time=base_time + timedelta(hours=1),
                entry_price=100.0,
                exit_price=105.0,
                quantity=10,
                side="long",
                pnl=50.0,
                pnl_percent=5.0,
                commission=1.0,
                duration_seconds=3600,
            ),
            Trade(
                symbol="TEST",
                entry_time=base_time + timedelta(hours=2),
                exit_time=base_time + timedelta(hours=3),
                entry_price=105.0,
                exit_price=110.0,
                quantity=10,
                side="long",
                pnl=50.0,
                pnl_percent=4.76,
                commission=1.0,
                duration_seconds=3600,
            ),
        ]

    @pytest.fixture
    def losing_trades(self) -> list[Trade]:
        """Fixture con trades perdedores."""
        base_time = datetime(2023, 1, 1)
        return [
            Trade(
                symbol="TEST",
                entry_time=base_time,
                exit_time=base_time + timedelta(hours=1),
                entry_price=100.0,
                exit_price=95.0,
                quantity=10,
                side="long",
                pnl=-50.0,
                pnl_percent=-5.0,
                commission=1.0,
                duration_seconds=3600,
            ),
        ]

    @pytest.fixture
    def equity_curve(self) -> list[tuple[pd.Timestamp, float]]:
        """Fixture con curva de equity."""
        base_time = pd.Timestamp("2023-01-01")
        return [
            (base_time + pd.Timedelta(hours=i), 10000 + i * 100)
            for i in range(10)
        ]

    def test_calculate_metrics_no_trades(self) -> None:
        """Test métricas con cero trades."""
        result = MetricsCalculator.calculate_metrics(
            trades=[],
            equity_curve=[(pd.Timestamp("2023-01-01"), 10000)],
            initial_capital=10000,
            total_commission=0,
        )
        
        assert result.total_trades == 0
        assert result.total_pnl == 0
        assert result.win_rate == 0

    def test_calculate_metrics_with_trades(
        self, winning_trades: list[Trade], equity_curve: list[tuple[pd.Timestamp, float]]
    ) -> None:
        """Test cálculo de métricas con trades."""
        result = MetricsCalculator.calculate_metrics(
            trades=winning_trades,
            equity_curve=equity_curve,
            initial_capital=10000,
            total_commission=2.0,
        )
        
        assert result.total_trades == 2
        assert result.winning_trades == 2
        assert result.losing_trades == 0
        assert result.win_rate == 100.0
        assert result.total_pnl == 100.0

    def test_win_rate_calculation(
        self,
        winning_trades: list[Trade],
        losing_trades: list[Trade],
        equity_curve: list[tuple[pd.Timestamp, float]],
    ) -> None:
        """Test cálculo de win rate."""
        all_trades = winning_trades + losing_trades
        result = MetricsCalculator.calculate_metrics(
            trades=all_trades,
            equity_curve=equity_curve,
            initial_capital=10000,
            total_commission=3.0,
        )
        
        expected_win_rate = (2 / 3) * 100  # 2 ganadores de 3 total
        assert abs(result.win_rate - expected_win_rate) < 0.01

    def test_profit_factor_calculation(
        self,
        winning_trades: list[Trade],
        losing_trades: list[Trade],
        equity_curve: list[tuple[pd.Timestamp, float]],
    ) -> None:
        """Test cálculo de profit factor."""
        all_trades = winning_trades + losing_trades
        result = MetricsCalculator.calculate_metrics(
            trades=all_trades,
            equity_curve=equity_curve,
            initial_capital=10000,
            total_commission=3.0,
        )
        
        # Profit factor = total wins / total losses
        # 100 / 50 = 2.0
        assert abs(result.profit_factor - 2.0) < 0.01

    def test_sharpe_ratio_calculation(self, equity_curve: list[tuple[pd.Timestamp, float]]) -> None:
        """Test cálculo de Sharpe ratio."""
        trades = [
            Trade(
                symbol="TEST",
                entry_time=datetime(2023, 1, 1),
                exit_time=datetime(2023, 1, 2),
                entry_price=100.0,
                exit_price=105.0,
                quantity=10,
                side="long",
                pnl=50.0,
                pnl_percent=5.0,
                commission=1.0,
                duration_seconds=86400,
            )
        ]
        
        result = MetricsCalculator.calculate_metrics(
            trades=trades,
            equity_curve=equity_curve,
            initial_capital=10000,
            total_commission=1.0,
        )
        
        # Sharpe ratio debe estar calculado
        assert isinstance(result.sharpe_ratio, float)
        assert not pd.isna(result.sharpe_ratio)

    def test_max_drawdown_calculation(self) -> None:
        """Test cálculo de máximo drawdown."""
        # Equity curve con drawdown conocido
        equity_curve = [
            (pd.Timestamp("2023-01-01"), 10000),
            (pd.Timestamp("2023-01-02"), 11000),  # Peak
            (pd.Timestamp("2023-01-03"), 9000),   # Drawdown del 18.18%
            (pd.Timestamp("2023-01-04"), 9500),
        ]
        
        trades = [
            Trade(
                symbol="TEST",
                entry_time=datetime(2023, 1, 1),
                exit_time=datetime(2023, 1, 4),
                entry_price=100.0,
                exit_price=95.0,
                quantity=10,
                side="long",
                pnl=-50.0,
                pnl_percent=-5.0,
                commission=1.0,
                duration_seconds=259200,
            )
        ]
        
        result = MetricsCalculator.calculate_metrics(
            trades=trades,
            equity_curve=equity_curve,
            initial_capital=10000,
            total_commission=1.0,
        )
        
        # Drawdown debería ser aproximadamente 18%
        assert result.max_drawdown_percent > 15.0
        assert result.max_drawdown_percent < 20.0
