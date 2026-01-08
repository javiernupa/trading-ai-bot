from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """Interface mínima que debe implementar una estrategia."""

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Recibe price dataframe y devuelve dataframe con columna 'signal' (-1,0,1)."""
        ...
