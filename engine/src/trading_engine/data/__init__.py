"""Sistema de gestión de datos para el motor de backtesting."""

from .loader import DataLoader
from .providers import CsvDataProvider, YahooFinanceProvider
from .validator import DataValidator

__all__ = [
    "DataLoader",
    "DataValidator",
    "YahooFinanceProvider",
    "CsvDataProvider",
]
