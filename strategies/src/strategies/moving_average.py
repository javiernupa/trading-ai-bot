"""Estrategia de cruce de medias móviles."""

from __future__ import annotations

import pandas as pd

from .base import BaseStrategy


class MovingAverageCrossStrategy(BaseStrategy):
    """Estrategia de cruce de medias móviles (Golden Cross / Death Cross).
    
    Compra cuando la media móvil rápida cruza por encima de la lenta,
    vende cuando cruza por debajo.
    """

    def __init__(
        self,
        fast_period: int = 50,
        slow_period: int = 200,
        ma_type: str = "sma",
    ) -> None:
        """Inicializa la estrategia de cruce de medias móviles.

        Args:
            fast_period: Período para MA rápida (default: 50)
            slow_period: Período para MA lenta (default: 200)
            ma_type: Tipo de media móvil: 'sma' o 'ema' (default: 'sma')
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.ma_type = ma_type.lower()

        if self.ma_type not in ["sma", "ema"]:
            raise ValueError("ma_type debe ser 'sma' o 'ema'")

    def _calculate_ma(self, series: pd.Series, period: int) -> pd.Series:
        """Calcula media móvil.

        Args:
            series: Serie de precios
            period: Período de la media móvil

        Returns:
            Serie con la media móvil calculada
        """
        if self.ma_type == "sma":
            return series.rolling(window=period).mean()
        else:  # ema
            return series.ewm(span=period, adjust=False).mean()

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading basadas en cruce de medias móviles.

        Args:
            data: DataFrame con datos históricos

        Returns:
            DataFrame con columna 'signal' añadida (-1, 0, 1)
        """
        df = data.copy()

        # Calcular medias móviles
        close = df["close"]
        df["ma_fast"] = self._calculate_ma(close, self.fast_period)
        df["ma_slow"] = self._calculate_ma(close, self.slow_period)

        # Inicializar señales en 0
        df["signal"] = 0

        ma_fast = df["ma_fast"]
        ma_slow = df["ma_slow"]

        # Señal de compra: MA rápida cruza por encima de MA lenta (Golden Cross)
        df.loc[
            (ma_fast > ma_slow) & (ma_fast.shift(1) <= ma_slow.shift(1)),
            "signal",
        ] = 1

        # Señal de venta: MA rápida cruza por debajo de MA lenta (Death Cross)
        df.loc[
            (ma_fast < ma_slow) & (ma_fast.shift(1) >= ma_slow.shift(1)),
            "signal",
        ] = -1

        return df
