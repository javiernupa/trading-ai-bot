"""Estrategia basada en Bandas de Bollinger."""

from __future__ import annotations

import pandas as pd

from .base import BaseStrategy


class BollingerBandsStrategy(BaseStrategy):
    """Estrategia de trading basada en Bandas de Bollinger.
    
    Compra cuando el precio toca la banda inferior (oversold),
    vende cuando toca la banda superior (overbought).
    """

    def __init__(
        self,
        period: int = 20,
        num_std: float = 2.0,
    ) -> None:
        """Inicializa la estrategia de Bandas de Bollinger.

        Args:
            period: Período para la media móvil (default: 20)
            num_std: Número de desviaciones estándar (default: 2.0)
        """
        self.period = period
        self.num_std = num_std

    def _calculate_bollinger_bands(
        self, data: pd.DataFrame
    ) -> tuple[pd.Series, pd.Series, pd.Series]:
        """Calcula las Bandas de Bollinger.

        Args:
            data: DataFrame con datos de precio

        Returns:
            Tupla con (upper_band, middle_band, lower_band)
        """
        close = data["close"]

        # Media móvil simple (banda media)
        middle_band = close.rolling(window=self.period).mean()

        # Desviación estándar
        std = close.rolling(window=self.period).std()

        # Bandas superior e inferior
        upper_band = middle_band + (std * self.num_std)
        lower_band = middle_band - (std * self.num_std)

        return upper_band, middle_band, lower_band

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading basadas en Bandas de Bollinger.

        Args:
            data: DataFrame con datos históricos

        Returns:
            DataFrame con columna 'signal' añadida (-1, 0, 1)
        """
        df = data.copy()

        # Calcular bandas
        upper_band, middle_band, lower_band = self._calculate_bollinger_bands(df)

        df["bb_upper"] = upper_band
        df["bb_middle"] = middle_band
        df["bb_lower"] = lower_band

        # Inicializar señales en 0
        df["signal"] = 0

        close = df["close"]

        # Señal de compra: precio toca o cruza la banda inferior
        df.loc[close <= lower_band, "signal"] = 1

        # Señal de venta: precio toca o cruza la banda superior
        df.loc[close >= upper_band, "signal"] = -1

        return df
