"""Tests para el sistema de gestión de datos."""

from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from trading_engine.data import CsvDataProvider, DataLoader, DataValidator


@pytest.fixture
def sample_data():
    """Crea datos de prueba válidos."""
    return pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2023-01-01", periods=10, freq="D"),
            "open": [100, 102, 101, 103, 105, 104, 106, 108, 107, 109],
            "high": [101, 103, 102, 104, 106, 105, 107, 109, 108, 110],
            "low": [99, 101, 100, 102, 104, 103, 105, 107, 106, 108],
            "close": [100.5, 102.5, 101.5, 103.5, 105.5, 104.5, 106.5, 108.5, 107.5, 109.5],
            "volume": [1000000, 1100000, 1050000, 1200000, 1150000, 1080000, 1250000, 1300000, 1220000, 1350000],
        }
    )


@pytest.fixture
def invalid_data():
    """Crea datos inválidos para testing."""
    return pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "open": [100, -10, 101, 103, 105],  # Valor negativo
            "high": [101, 103, 102, 104, 106],
            "low": [99, 105, 100, 102, 104],  # low > high en índice 1
            "close": [98, 102.5, 101.5, 103.5, 105.5],  # close < low en índice 0
            "volume": [1000000, 1100000, 1050000, 1200000, 1150000],
        }
    )


class TestDataValidator:
    """Tests para DataValidator."""

    def test_validate_valid_data(self, sample_data):
        """Test validación de datos válidos."""
        is_valid, warnings = DataValidator.validate(sample_data, strict=False)
        assert is_valid
        assert len(warnings) == 0

    def test_validate_empty_dataframe(self):
        """Test validación de DataFrame vacío."""
        with pytest.raises(ValueError):
            DataValidator.validate(pd.DataFrame(), strict=True)

    def test_validate_missing_columns(self):
        """Test validación con columnas faltantes."""
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2023-01-01", periods=5),
                "close": [100, 101, 102, 103, 104],
            }
        )

        with pytest.raises(ValueError):
            DataValidator.validate(df, strict=True)

    def test_validate_non_numeric_columns(self):
        """Test validación con columnas no numéricas."""
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2023-01-01", periods=5),
                "open": ["100", "101", "102", "103", "104"],  # Strings
                "high": [101, 102, 103, 104, 105],
                "low": [99, 100, 101, 102, 103],
                "close": [100, 101, 102, 103, 104],
                "volume": [1000, 1100, 1050, 1200, 1150],
            }
        )

        with pytest.raises(ValueError):
            DataValidator.validate(df, strict=True)

    def test_validate_with_null_values(self, sample_data):
        """Test validación con valores nulos."""
        df = sample_data.copy()
        df.loc[2, "close"] = None

        is_valid, warnings = DataValidator.validate(df, strict=False)
        assert not is_valid
        assert any("nulos" in w for w in warnings)

    def test_validate_negative_prices(self, invalid_data):
        """Test validación con precios negativos."""
        is_valid, warnings = DataValidator.validate(invalid_data, strict=False)
        assert not is_valid
        assert any("negativo" in w for w in warnings)

    def test_validate_high_low_relationship(self, invalid_data):
        """Test validación de relación high/low."""
        is_valid, warnings = DataValidator.validate(invalid_data, strict=False)
        assert not is_valid
        assert any("high < low" in w for w in warnings)

    def test_clean_data(self, invalid_data):
        """Test limpieza de datos."""
        cleaned = DataValidator.clean(invalid_data)

        # Verificar que no hay precios negativos
        assert (cleaned["open"] >= 0).all()
        assert (cleaned["high"] >= 0).all()
        assert (cleaned["low"] >= 0).all()
        assert (cleaned["close"] >= 0).all()

        # Verificar relación high/low
        assert (cleaned["high"] >= cleaned["low"]).all()

    def test_clean_removes_duplicates(self, sample_data):
        """Test que clean elimina duplicados."""
        df = pd.concat([sample_data, sample_data.iloc[[0]]])  # Agregar duplicado
        cleaned = DataValidator.clean(df)

        assert len(cleaned) == len(sample_data)

    def test_clean_fills_nulls(self, sample_data):
        """Test que clean rellena nulos."""
        df = sample_data.copy()
        df.loc[2, "close"] = None
        cleaned = DataValidator.clean(df)

        assert cleaned["close"].isnull().sum() == 0


class TestCsvDataProvider:
    """Tests para CsvDataProvider."""

    def test_initialization(self, tmp_path):
        """Test inicialización."""
        provider = CsvDataProvider(data_dir=tmp_path)
        assert provider.data_dir == tmp_path

    def test_save_and_load_data(self, sample_data, tmp_path):
        """Test guardar y cargar datos."""
        provider = CsvDataProvider(data_dir=tmp_path)

        # Guardar datos
        filepath = provider.save_data(sample_data, symbol="TEST")
        assert filepath.exists()

        # Cargar datos
        loaded = provider.fetch_data(
            symbol="TEST",
            start_date="2023-01-01",
            end_date="2023-01-10",
            filename="TEST.csv",
        )

        assert len(loaded) == len(sample_data)
        assert list(loaded.columns) == list(sample_data.columns)

    def test_fetch_nonexistent_file(self, tmp_path):
        """Test cargar archivo inexistente."""
        provider = CsvDataProvider(data_dir=tmp_path)

        with pytest.raises(FileNotFoundError):
            provider.fetch_data(
                symbol="NONEXISTENT",
                start_date="2023-01-01",
                end_date="2023-01-10",
            )

    def test_date_filtering(self, sample_data, tmp_path):
        """Test filtrado por fechas."""
        provider = CsvDataProvider(data_dir=tmp_path)
        provider.save_data(sample_data, symbol="TEST")

        # Cargar solo un subconjunto
        loaded = provider.fetch_data(
            symbol="TEST",
            start_date="2023-01-03",
            end_date="2023-01-07",
            filename="TEST.csv",
        )

        assert len(loaded) == 5  # 5 días entre 03 y 07 inclusive


class TestDataLoader:
    """Tests para DataLoader."""

    def test_initialization(self, tmp_path):
        """Test inicialización."""
        loader = DataLoader(cache_dir=tmp_path)
        assert loader.cache_dir == tmp_path
        assert loader.use_cache is True
        assert loader.validate_data is True

    def test_cache_creation(self, tmp_path):
        """Test que se crea directorio de caché."""
        cache_dir = tmp_path / "cache"
        loader = DataLoader(cache_dir=cache_dir)
        assert cache_dir.exists()

    def test_clear_cache(self, sample_data, tmp_path):
        """Test limpiar caché."""
        loader = DataLoader(cache_dir=tmp_path)

        # Guardar algunos archivos
        (tmp_path / "AAPL_2023-01-01_2023-12-31.csv").write_text("test")
        (tmp_path / "GOOGL_2023-01-01_2023-12-31.csv").write_text("test")

        # Limpiar todo
        loader.clear_cache()
        assert len(list(tmp_path.glob("*.csv"))) == 0

    def test_clear_cache_by_symbol(self, tmp_path):
        """Test limpiar caché por símbolo."""
        loader = DataLoader(cache_dir=tmp_path)

        # Guardar archivos
        (tmp_path / "AAPL_2023-01-01_2023-12-31.csv").write_text("test")
        (tmp_path / "GOOGL_2023-01-01_2023-12-31.csv").write_text("test")

        # Limpiar solo AAPL
        loader.clear_cache(symbol="AAPL")

        remaining = list(tmp_path.glob("*.csv"))
        assert len(remaining) == 1
        assert "GOOGL" in remaining[0].name
