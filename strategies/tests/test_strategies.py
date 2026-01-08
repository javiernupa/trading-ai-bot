"""Tests para las nuevas estrategias."""

import numpy as np
import pandas as pd
import pytest

from strategies import (
    BollingerBandsStrategy,
    CombinedStrategy,
    MacdStrategy,
    MovingAverageCrossStrategy,
)


@pytest.fixture
def sample_data():
    """Crea datos de prueba."""
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    np.random.seed(42)

    # Crear precios con tendencia alcista
    close_prices = 100 + np.cumsum(np.random.randn(100) * 2)

    return pd.DataFrame(
        {
            "timestamp": dates,
            "open": close_prices + np.random.randn(100),
            "high": close_prices + np.abs(np.random.randn(100)),
            "low": close_prices - np.abs(np.random.randn(100)),
            "close": close_prices,
            "volume": np.random.randint(1000000, 5000000, 100),
        }
    )


class TestMacdStrategy:
    """Tests para MacdStrategy."""

    def test_initialization(self):
        """Test inicialización."""
        strategy = MacdStrategy(fast_period=12, slow_period=26, signal_period=9)
        assert strategy.fast_period == 12
        assert strategy.slow_period == 26
        assert strategy.signal_period == 9

    def test_generate_signals(self, sample_data):
        """Test generación de señales."""
        strategy = MacdStrategy()
        result = strategy.generate_signals(sample_data)

        assert "signal" in result.columns
        assert "macd" in result.columns
        assert "macd_signal" in result.columns
        assert "macd_histogram" in result.columns
        assert result["signal"].isin([-1, 0, 1]).all()

    def test_signal_logic(self, sample_data):
        """Test lógica de señales."""
        strategy = MacdStrategy(fast_period=5, slow_period=10, signal_period=3)
        result = strategy.generate_signals(sample_data)

        # Verificar que hay señales
        buy_signals = (result["signal"] == 1).sum()
        sell_signals = (result["signal"] == -1).sum()

        assert buy_signals > 0 or sell_signals > 0


class TestBollingerBandsStrategy:
    """Tests para BollingerBandsStrategy."""

    def test_initialization(self):
        """Test inicialización."""
        strategy = BollingerBandsStrategy(period=20, num_std=2.0)
        assert strategy.period == 20
        assert strategy.num_std == 2.0

    def test_generate_signals(self, sample_data):
        """Test generación de señales."""
        strategy = BollingerBandsStrategy()
        result = strategy.generate_signals(sample_data)

        assert "signal" in result.columns
        assert "bb_upper" in result.columns
        assert "bb_middle" in result.columns
        assert "bb_lower" in result.columns
        assert result["signal"].isin([-1, 0, 1]).all()

    def test_bands_relationship(self, sample_data):
        """Test relación entre bandas."""
        strategy = BollingerBandsStrategy()
        result = strategy.generate_signals(sample_data)

        # Verificar que upper >= middle >= lower
        valid_bands = result.dropna()
        assert (valid_bands["bb_upper"] >= valid_bands["bb_middle"]).all()
        assert (valid_bands["bb_middle"] >= valid_bands["bb_lower"]).all()


class TestMovingAverageCrossStrategy:
    """Tests para MovingAverageCrossStrategy."""

    def test_initialization_sma(self):
        """Test inicialización con SMA."""
        strategy = MovingAverageCrossStrategy(
            fast_period=50, slow_period=200, ma_type="sma"
        )
        assert strategy.fast_period == 50
        assert strategy.slow_period == 200
        assert strategy.ma_type == "sma"

    def test_initialization_ema(self):
        """Test inicialización con EMA."""
        strategy = MovingAverageCrossStrategy(
            fast_period=12, slow_period=26, ma_type="ema"
        )
        assert strategy.ma_type == "ema"

    def test_invalid_ma_type(self):
        """Test tipo de MA inválido."""
        with pytest.raises(ValueError):
            MovingAverageCrossStrategy(ma_type="invalid")

    def test_generate_signals(self, sample_data):
        """Test generación de señales."""
        strategy = MovingAverageCrossStrategy(fast_period=10, slow_period=20)
        result = strategy.generate_signals(sample_data)

        assert "signal" in result.columns
        assert "ma_fast" in result.columns
        assert "ma_slow" in result.columns
        assert result["signal"].isin([-1, 0, 1]).all()

    def test_golden_cross(self):
        """Test detección de Golden Cross."""
        # Crear datos con cruce alcista claro
        # Primero precios bajos, luego subida fuerte
        prices = [100] * 20 + list(range(100, 150))  # 20 días flat, luego sube

        data = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2023-01-01", periods=len(prices)),
                "close": prices,
                "open": prices,
                "high": [p + 1 for p in prices],
                "low": [p - 1 for p in prices],
                "volume": [1000000] * len(prices),
            }
        )

        strategy = MovingAverageCrossStrategy(fast_period=5, slow_period=15, ma_type="sma")
        result = strategy.generate_signals(data)

        # Debe haber al menos una señal de compra después del cruce
        buy_signals = result["signal"] == 1
        assert buy_signals.sum() > 0, "No se detectó Golden Cross"


class TestCombinedStrategy:
    """Tests para CombinedStrategy."""

    def test_initialization(self):
        """Test inicialización."""
        strategy = CombinedStrategy(
            rsi_period=14,
            rsi_lower=30,
            rsi_upper=70,
            consensus_threshold=2,
        )
        assert strategy.rsi_period == 14
        assert strategy.consensus_threshold == 2

    def test_generate_signals(self, sample_data):
        """Test generación de señales."""
        strategy = CombinedStrategy(consensus_threshold=2)
        result = strategy.generate_signals(sample_data)

        assert "signal" in result.columns
        assert "rsi" in result.columns
        assert "macd" in result.columns
        assert "bb_upper" in result.columns
        assert "buy_votes" in result.columns
        assert "sell_votes" in result.columns
        assert result["signal"].isin([-1, 0, 1]).all()

    def test_consensus_mechanism(self, sample_data):
        """Test mecanismo de consenso."""
        # Con threshold=3, necesita 3 indicadores de acuerdo
        strategy = CombinedStrategy(consensus_threshold=3)
        result = strategy.generate_signals(sample_data)

        # Verificar que las señales requieren consenso
        buy_signals = result[result["signal"] == 1]
        if len(buy_signals) > 0:
            assert (buy_signals["buy_votes"] >= 3).all()

        sell_signals = result[result["signal"] == -1]
        if len(sell_signals) > 0:
            assert (sell_signals["sell_votes"] >= 3).all()

    def test_individual_indicators(self, sample_data):
        """Test cálculo de indicadores individuales."""
        strategy = CombinedStrategy()
        result = strategy.generate_signals(sample_data)

        # Verificar que todos los indicadores están presentes
        assert "rsi_signal" in result.columns
        assert "macd_signal_ind" in result.columns
        assert "bb_signal" in result.columns

        # Verificar que las señales individuales son válidas
        assert result["rsi_signal"].isin([-1, 0, 1]).all()
        assert result["macd_signal_ind"].isin([-1, 0, 1]).all()
        assert result["bb_signal"].isin([-1, 0, 1]).all()
