"""Estrategia basada en Ichimoku Cloud (Ichimoku Kinko Hyo)."""

from __future__ import annotations

import pandas as pd

from .base import BaseStrategy


class IchimokuStrategy(BaseStrategy):
    """Estrategia de trading basada en Ichimoku Cloud.
    
    Genera señales basadas en:
    - Cruces de Tenkan-sen y Kijun-sen
    - Posición del precio respecto a la nube (Kumo)
    - Compra: Tenkan cruza Kijun al alza Y precio sobre la nube
    - Venta: Tenkan cruza Kijun a la baja Y precio bajo la nube
    """

    def __init__(
        self,
        tenkan_period: int = 9,
        kijun_period: int = 26,
        senkou_b_period: int = 52,
    ) -> None:
        """Inicializa la estrategia Ichimoku.

        Args:
            tenkan_period: Período para Tenkan-sen/línea de conversión (default: 9)
            kijun_period: Período para Kijun-sen/línea base (default: 26)
            senkou_b_period: Período para Senkou Span B (default: 52)
        """
        self.tenkan_period = tenkan_period
        self.kijun_period = kijun_period
        self.senkou_b_period = senkou_b_period

    def _calculate_ichimoku(self, data: pd.DataFrame) -> dict[str, pd.Series]:
        """Calcula los componentes del Ichimoku.

        Args:
            data: DataFrame con datos de precio (high, low, close)

        Returns:
            Diccionario con los componentes del Ichimoku
        """
        high = data["high"]
        low = data["low"]
        close = data["close"]

        # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
        tenkan_high = high.rolling(window=self.tenkan_period).max()
        tenkan_low = low.rolling(window=self.tenkan_period).min()
        tenkan_sen = (tenkan_high + tenkan_low) / 2

        # Kijun-sen (Base Line): (26-period high + 26-period low)/2
        kijun_high = high.rolling(window=self.kijun_period).max()
        kijun_low = low.rolling(window=self.kijun_period).min()
        kijun_sen = (kijun_high + kijun_low) / 2

        # Senkou Span A (Leading Span A): (Tenkan-sen + Kijun-sen)/2, shifted 26 periods ahead
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(self.kijun_period)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2, shifted 26 periods ahead
        senkou_b_high = high.rolling(window=self.senkou_b_period).max()
        senkou_b_low = low.rolling(window=self.senkou_b_period).min()
        senkou_span_b = ((senkou_b_high + senkou_b_low) / 2).shift(self.kijun_period)

        return {
            "tenkan_sen": tenkan_sen,
            "kijun_sen": kijun_sen,
            "senkou_span_a": senkou_span_a,
            "senkou_span_b": senkou_span_b,
        }

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading basadas en Ichimoku Cloud.

        Args:
            data: DataFrame con datos históricos

        Returns:
            DataFrame con columna 'signal' añadida (-1, 0, 1)
        """
        df = data.copy()

        # Calcular componentes de Ichimoku
        ichimoku = self._calculate_ichimoku(df)
        
        df["tenkan_sen"] = ichimoku["tenkan_sen"]
        df["kijun_sen"] = ichimoku["kijun_sen"]
        df["senkou_span_a"] = ichimoku["senkou_span_a"]
        df["senkou_span_b"] = ichimoku["senkou_span_b"]

        # Calcular límites de la nube (kumo)
        df["kumo_top"] = df[["senkou_span_a", "senkou_span_b"]].max(axis=1)
        df["kumo_bottom"] = df[["senkou_span_a", "senkou_span_b"]].min(axis=1)

        # Inicializar señales en 0
        df["signal"] = 0

        # Detectar cruces de Tenkan y Kijun
        tenkan_above_kijun = (df["tenkan_sen"] > df["kijun_sen"]).fillna(False)
        tenkan_below_kijun = (df["tenkan_sen"] < df["kijun_sen"]).fillna(False)
        
        prev_tenkan_above = tenkan_above_kijun.shift(1, fill_value=False)
        prev_tenkan_below = tenkan_below_kijun.shift(1, fill_value=False)

        # Cruce alcista: Tenkan cruza Kijun al alza
        bullish_cross = (~prev_tenkan_above) & tenkan_above_kijun
        
        # Cruce bajista: Tenkan cruza Kijun a la baja
        bearish_cross = (~prev_tenkan_below) & tenkan_below_kijun

        # Posición del precio respecto a la nube
        price_above_cloud = (df["close"] > df["kumo_top"]).fillna(False)
        price_below_cloud = (df["close"] < df["kumo_bottom"]).fillna(False)

        # Señal de compra: cruce alcista Y precio sobre la nube
        df.loc[bullish_cross & price_above_cloud, "signal"] = 1

        # Señal de venta: cruce bajista Y precio bajo la nube
        df.loc[bearish_cross & price_below_cloud, "signal"] = -1

        return df

    def __repr__(self) -> str:
        """Representación en string de la estrategia."""
        return (
            f"IchimokuStrategy(tenkan={self.tenkan_period}, "
            f"kijun={self.kijun_period}, "
            f"senkou_b={self.senkou_b_period})"
        )
