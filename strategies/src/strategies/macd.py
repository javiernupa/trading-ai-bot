"""Estrategia basada en MACD (Moving Average Convergence Divergence)."""

from __future__ import annotations

import pandas as pd

from .base import BaseStrategy


class MacdStrategy(BaseStrategy):
    """Estrategia de trading basada en MACD.
    
    Genera señales de compra cuando MACD cruza por encima de la señal,
    y señales de venta cuando cruza por debajo.
    """

    def __init__(
        self,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> None:
        """Inicializa la estrategia MACD.

        Args:
            fast_period: Período para EMA rápida (default: 12)
            slow_period: Período para EMA lenta (default: 26)
            signal_period: Período para línea de señal (default: 9)
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def _calculate_macd(self, data: pd.DataFrame) -> tuple[pd.Series, pd.Series, pd.Series]:
        """Calcula MACD, señal e histograma.

        Args:
            data: DataFrame con datos de precio

        Returns:
            Tupla con (macd, signal, histogram)
        """
        close = data["close"]

        # Calcular EMAs
        ema_fast = close.ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = close.ewm(span=self.slow_period, adjust=False).mean()

        # MACD = EMA rápida - EMA lenta
        macd = ema_fast - ema_slow

        # Línea de señal = EMA del MACD
        signal = macd.ewm(span=self.signal_period, adjust=False).mean()

        # Histograma = MACD - Señal
        histogram = macd - signal

        return macd, signal, histogram

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading basadas en MACD.

        Args:
            data: DataFrame con datos históricos

        Returns:
            DataFrame con columna 'signal' añadida (-1, 0, 1)
        """
        df = data.copy()

        # Calcular MACD
        macd, signal, histogram = self._calculate_macd(df)

        df["macd"] = macd
        df["macd_signal"] = signal
        df["macd_histogram"] = histogram

        # Inicializar señales en 0
        df["signal"] = 0

        # Señal de compra: MACD cruza por encima de la señal
        # (histograma pasa de negativo a positivo)
        df.loc[
            (histogram > 0) & (histogram.shift(1) <= 0),
            "signal",
        ] = 1

        # Señal de venta: MACD cruza por debajo de la señal
        # (histograma pasa de positivo a negativo)
        df.loc[
            (histogram < 0) & (histogram.shift(1) >= 0),
            "signal",
        ] = -1

        return df
