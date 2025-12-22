"""Tests para el motor de backtesting."""

import pandas as pd
import pytest

from trading_engine.backtest import Backtester
from trading_engine.models import OrderSide
from strategies.rsi import RsiStrategy


class TestBacktester:
    """Tests para la clase Backtester."""

    @pytest.fixture
    def sample_data(self) -> pd.DataFrame:
        """Fixture con datos de muestra."""
        return pd.DataFrame({
            "date": pd.date_range(start="2023-01-01", periods=50, freq="D"),
            "close": [100 + i * 0.5 for i in range(50)],  # Tendencia alcista
        })

    @pytest.fixture
    def strategy(self) -> RsiStrategy:
        """Fixture con estrategia RSI."""
        return RsiStrategy(period=10, lower=30, upper=70)

    def test_backtester_initialization(
        self, strategy: RsiStrategy, sample_data: pd.DataFrame
    ) -> None:
        """Test que el backtester se inicializa correctamente."""
        backtester = Backtester(strategy, sample_data, initial_cash=10000)
        
        assert backtester.initial_cash == 10000
        assert backtester.portfolio.cash == 10000
        assert len(backtester.data) == 50

    def test_backtester_requires_close_column(self, strategy: RsiStrategy) -> None:
        """Test que falla si no hay columna 'close'."""
        df = pd.DataFrame({"price": [100, 101, 102]})
        
        with pytest.raises(ValueError, match="must contain 'close' column"):
            Backtester(strategy, df)

    def test_backtester_run_basic(
        self, strategy: RsiStrategy, sample_data: pd.DataFrame
    ) -> None:
        """Test ejecución básica del backtest."""
        backtester = Backtester(strategy, sample_data, initial_cash=10000)
        result = backtester.run()
        
        assert result is not None
        assert result.initial_capital == 10000
        assert result.total_trades >= 0
        assert result.win_rate >= 0
        assert result.win_rate <= 100

    def test_backtester_generates_trades(
        self, strategy: RsiStrategy, sample_data: pd.DataFrame
    ) -> None:
        """Test que se generan trades durante el backtest."""
        # Datos oscilantes para generar señales
        import numpy as np
        
        np.random.seed(42)
        df = pd.DataFrame({
            "date": pd.date_range(start="2023-01-01", periods=100, freq="D"),
            "close": 100 + 10 * np.sin(np.linspace(0, 8 * np.pi, 100)) + np.random.normal(0, 1, 100),
        })
        
        backtester = Backtester(strategy, df, initial_cash=10000)
        result = backtester.run()
        
        # Con datos oscilantes, deberían generarse trades
        assert result.total_trades > 0
        assert len(result.trades) > 0

    def test_backtester_applies_commission(
        self, strategy: RsiStrategy, sample_data: pd.DataFrame
    ) -> None:
        """Test que se aplican comisiones."""
        backtester = Backtester(
            strategy, sample_data, initial_cash=10000, commission=0.01  # 1%
        )
        result = backtester.run()
        
        if result.total_trades > 0:
            assert result.total_commission > 0

    def test_backtester_metrics_consistency(
        self, strategy: RsiStrategy, sample_data: pd.DataFrame
    ) -> None:
        """Test que las métricas son consistentes."""
        backtester = Backtester(strategy, sample_data, initial_cash=10000)
        result = backtester.run()
        
        # Win rate debe ser consistente con trades
        if result.total_trades > 0:
            expected_win_rate = (result.winning_trades / result.total_trades) * 100
            assert abs(result.win_rate - expected_win_rate) < 0.01
        
        # Total trades = winning + losing
        assert result.total_trades == result.winning_trades + result.losing_trades
        
        # Final capital debe ser razonable
        assert result.final_capital > 0
