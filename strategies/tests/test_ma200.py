"""Tests para la estrategia MA200."""

import pandas as pd
import pytest

from strategies import Ma200Strategy


@pytest.fixture
def sample_data():
    """Crea datos de muestra para testing."""
    # Crear datos con tendencia alcista luego bajista
    dates = pd.date_range(start="2020-01-01", periods=250, freq="D")
    
    # Primera mitad: tendencia alcista (precio sube de 100 a 150)
    prices_up = list(range(100, 150))
    
    # Segunda mitad: tendencia bajista (precio baja de 150 a 125)
    prices_down = list(range(150, 125, -1))
    
    # Combinar
    all_prices = prices_up + prices_down + [125] * (250 - len(prices_up) - len(prices_down))
    
    return pd.DataFrame(
        {
            "timestamp": dates,
            "open": all_prices,
            "high": [p + 2 for p in all_prices],
            "low": [p - 2 for p in all_prices],
            "close": all_prices,
            "volume": [1000000] * 250,
        }
    )


def test_ma200_initialization():
    """Test de inicialización de la estrategia."""
    strategy = Ma200Strategy()
    assert strategy.period == 200
    assert strategy.use_crossover is True
    assert strategy.volume_confirmation is False


def test_ma200_custom_params():
    """Test con parámetros personalizados."""
    strategy = Ma200Strategy(
        period=50, use_crossover=False, volume_confirmation=True, volume_period=10
    )
    assert strategy.period == 50
    assert strategy.use_crossover is False
    assert strategy.volume_confirmation is True
    assert strategy.volume_period == 10


def test_ma200_insufficient_data():
    """Test con datos insuficientes."""
    strategy = Ma200Strategy(period=200)
    
    # Solo 100 barras (insuficiente para MA200)
    data = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2024-01-01", periods=100, freq="D"),
            "close": range(100, 200),
            "volume": [1000] * 100,
        }
    )
    
    with pytest.raises(ValueError, match="Datos insuficientes"):
        strategy.generate_signals(data)


def test_ma200_crossover_mode(sample_data):
    """Test modo crossover (solo cruces)."""
    strategy = Ma200Strategy(period=200, use_crossover=True)
    result = strategy.generate_signals(sample_data)
    
    # Verificar que tiene columna signal
    assert "signal" in result.columns
    assert "ma200" in result.columns
    assert "price_above_ma" in result.columns
    assert "bullish_cross" in result.columns
    assert "bearish_cross" in result.columns
    
    # Verificar que hay al menos una señal
    assert result["signal"].abs().sum() > 0
    
    # Verificar que señales son solo -1, 0, 1
    assert set(result["signal"].unique()).issubset({-1, 0, 1})


def test_ma200_position_mode(sample_data):
    """Test modo position (continuo)."""
    strategy = Ma200Strategy(period=200, use_crossover=False)
    result = strategy.generate_signals(sample_data)
    
    # Verificar columnas
    assert "signal" in result.columns
    assert "ma200" in result.columns
    
    # En modo position, debería haber más señales que en crossover
    crossover_strategy = Ma200Strategy(period=200, use_crossover=True)
    crossover_result = crossover_strategy.generate_signals(sample_data)
    
    # Position mode tiene más señales != 0
    assert (result["signal"] != 0).sum() >= (crossover_result["signal"] != 0).sum()


def test_ma200_volume_confirmation():
    """Test confirmación de volumen."""
    # Crear datos con variación de volumen
    data = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2020-01-01", periods=250, freq="D"),
            "close": list(range(100, 200)) + list(range(200, 150, -1)),
            "volume": [500] * 100 + [2000] * 100 + [500] * 50,  # Volumen alto en medio
        }
    )
    
    # Sin confirmación de volumen
    strategy_no_vol = Ma200Strategy(period=200, volume_confirmation=False)
    result_no_vol = strategy_no_vol.generate_signals(data)
    
    # Con confirmación de volumen
    strategy_vol = Ma200Strategy(period=200, volume_confirmation=True, volume_period=20)
    result_vol = strategy_vol.generate_signals(data)
    
    # Con volumen debería haber menos señales (filtradas)
    assert (result_vol["signal"] != 0).sum() <= (result_no_vol["signal"] != 0).sum()


def test_ma200_get_indicator_values(sample_data):
    """Test obtención de valores de indicadores."""
    strategy = Ma200Strategy(period=200)
    result = strategy.generate_signals(sample_data)
    
    indicators = strategy.get_indicator_values(result)
    
    # Verificar que tiene los campos esperados
    assert "ma200" in indicators
    assert "current_price" in indicators
    assert "price_above_ma" in indicators
    assert "distance_pct" in indicators
    
    # Verificar que los valores son numéricos
    assert isinstance(indicators["ma200"], (int, float))
    assert isinstance(indicators["current_price"], (int, float))
    assert isinstance(indicators["distance_pct"], (int, float))


def test_ma200_bullish_signal():
    """Test señal alcista (cruce hacia arriba)."""
    # Crear datos donde precio cruza MA200 hacia arriba
    data = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2020-01-01", periods=220, freq="D"),
            "close": [100] * 200 + list(range(100, 120)),  # Sube al final
            "volume": [1000] * 220,
        }
    )
    
    strategy = Ma200Strategy(period=200, use_crossover=True)
    result = strategy.generate_signals(data)
    
    # Debería haber señal de compra (1) al cruzar hacia arriba
    assert (result["signal"] == 1).any()


def test_ma200_bearish_signal():
    """Test señal bajista (cruce hacia abajo)."""
    # Crear datos donde precio cruza MA200 hacia abajo
    data = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2020-01-01", periods=220, freq="D"),
            "close": [100] * 200 + list(range(100, 80, -1)),  # Baja al final
            "volume": [1000] * 220,
        }
    )
    
    strategy = Ma200Strategy(period=200, use_crossover=True)
    result = strategy.generate_signals(data)
    
    # Debería haber señal de venta (-1) al cruzar hacia abajo
    assert (result["signal"] == -1).any()


def test_ma200_str_representation():
    """Test representación en string."""
    strategy = Ma200Strategy(period=200, use_crossover=True)
    assert "MA200Strategy" in str(strategy)
    assert "period=200" in str(strategy)
    assert "Crossover" in str(strategy)


def test_ma200_with_nan_values():
    """Test con valores NaN."""
    data = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2020-01-01", periods=250, freq="D"),
            "close": [100] * 100 + [float("nan")] * 50 + [110] * 100,
            "volume": [1000] * 250,
        }
    )
    
    strategy = Ma200Strategy(period=200)
    result = strategy.generate_signals(data)
    
    # No debería crashear, debería manejar NaN correctamente
    assert "signal" in result.columns
    # Las señales donde hay NaN deberían ser 0
    assert result.loc[result["close"].isna(), "signal"].eq(0).all()
