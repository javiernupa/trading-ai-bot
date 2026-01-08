"""Estrategia basada en el Oscilador Estocástico."""

from __future__ import annotations

import pandas as pd

from .base import BaseStrategy


class StochasticStrategy(BaseStrategy):
    """Estrategia de trading basada en el Oscilador Estocástico.
    
    Genera señales basadas en cruces de %K y %D en zonas de sobrecompra/sobreventa.
    - Señal de compra: %K cruza por encima de %D en zona de sobreventa
    - Señal de venta: %K cruza por debajo de %D en zona de sobrecompra
    """

    def __init__(
        self,
        period: int = 14,
        k_period: int = 3,
        d_period: int = 3,
        overbought: float = 80,
        oversold: float = 20,
    ) -> None:
        """Inicializa la estrategia Stochastic.

        Args:
            period: Período para el cálculo del estocástico (default: 14)
            k_period: Período de suavizado para %K (default: 3)
            d_period: Período de suavizado para %D (default: 3)
            overbought: Nivel de sobrecompra (default: 80)
            oversold: Nivel de sobreventa (default: 20)
        """
        self.period = period
        self.k_period = k_period
        self.d_period = d_period
        self.overbought = overbought
        self.oversold = oversold

    def _calculate_stochastic(self, data: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
        """Calcula el oscilador estocástico %K y %D.

        Args:
            data: DataFrame con datos de precio (high, low, close)

        Returns:
            Tupla con (%K, %D)
        """
        # Calcular el estocástico raw
        low_min = data["low"].rolling(window=self.period).min()
        high_max = data["high"].rolling(window=self.period).max()
        
        # %K = 100 * (Close - Low_min) / (High_max - Low_min)
        stoch_k_raw = 100 * (data["close"] - low_min) / (high_max - low_min)
        
        # Suavizar %K
        stoch_k = stoch_k_raw.rolling(window=self.k_period).mean()
        
        # %D es la media móvil de %K
        stoch_d = stoch_k.rolling(window=self.d_period).mean()
        
        return stoch_k, stoch_d

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading basadas en el oscilador estocástico.

        Args:
            data: DataFrame con datos históricos

        Returns:
            DataFrame con columna 'signal' añadida (-1, 0, 1)
        """
        df = data.copy()

        # Calcular estocástico
        stoch_k, stoch_d = self._calculate_stochastic(df)

        df["stoch_k"] = stoch_k
        df["stoch_d"] = stoch_d

        # Inicializar señales en 0
        df["signal"] = 0

        # Detectar cruces
        k_above_d = (stoch_k > stoch_d).fillna(False)
        k_below_d = (stoch_k < stoch_d).fillna(False)
        
        prev_k_above_d = k_above_d.shift(1, fill_value=False)
        prev_k_below_d = k_below_d.shift(1, fill_value=False)

        # Señal de compra: %K cruza por encima de %D en zona de sobreventa
        bullish_cross = (~prev_k_above_d) & k_above_d
        in_oversold = (stoch_k < self.oversold).fillna(False)
        
        df.loc[bullish_cross & in_oversold, "signal"] = 1

        # Señal de venta: %K cruza por debajo de %D en zona de sobrecompra
        bearish_cross = (~prev_k_below_d) & k_below_d
        in_overbought = (stoch_k > self.overbought).fillna(False)
        
        df.loc[bearish_cross & in_overbought, "signal"] = -1

        return df

    def __repr__(self) -> str:
        """Representación en string de la estrategia."""
        return (
            f"StochasticStrategy(period={self.period}, "
            f"k={self.k_period}, d={self.d_period}, "
            f"OB={self.overbought}, OS={self.oversold})"
        )
