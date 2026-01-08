"""Estrategia basada en OBV (On-Balance Volume)."""

from __future__ import annotations

import pandas as pd

from .base import BaseStrategy


class OBVStrategy(BaseStrategy):
    """Estrategia basada en OBV (On-Balance Volume).
    
    El OBV es un indicador técnico de momentum que relaciona el volumen
    con los cambios de precio. Acumula volumen en días alcistas y lo
    resta en días bajistas.
    
    Señales:
    - Compra: OBV cruza por encima de su media móvil (tendencia alcista)
    - Venta: OBV cruza por debajo de su media móvil (tendencia bajista)
    """

    def __init__(
        self,
        period: int = 20,
        use_signal_line: bool = True,
        min_volume: float = 0.0,
    ):
        """Inicializa la estrategia OBV.

        Args:
            period: Periodo para la media móvil del OBV (default: 20)
            use_signal_line: Usar cruce con línea de señal (default: True)
            min_volume: Volumen mínimo para considerar señales (default: 0)
        """
        super().__init__()
        self.period = period
        self.use_signal_line = use_signal_line
        self.min_volume = min_volume

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading basadas en OBV.

        Args:
            data: DataFrame con columnas ['close', 'volume']

        Returns:
            DataFrame con columna 'signal' (1: compra, -1: venta, 0: mantener)
        """
        df = data.copy()

        # Calcular OBV
        df['obv'] = self._calculate_obv(df)

        if self.use_signal_line:
            # Usar cruce con media móvil como señal
            df['obv_signal'] = df['obv'].rolling(window=self.period).mean()

            # Señales de cruce
            # Compra: OBV cruza por encima de su señal
            # Venta: OBV cruza por debajo de su señal
            df['obv_above_signal'] = df['obv'] > df['obv_signal']
            df['obv_above_signal_prev'] = df['obv_above_signal'].shift(1, fill_value=False)

            # Cruce alcista (de abajo hacia arriba)
            buy_signal = (df['obv_above_signal']) & (~df['obv_above_signal_prev'])

            # Cruce bajista (de arriba hacia abajo)
            sell_signal = (~df['obv_above_signal']) & (df['obv_above_signal_prev'])

        else:
            # Usar tendencia del OBV directamente
            df['obv_sma'] = df['obv'].rolling(window=self.period).mean()
            df['obv_trend'] = df['obv'] - df['obv_sma']

            # Señales basadas en cambio de tendencia
            df['obv_trend_positive'] = df['obv_trend'] > 0
            df['obv_trend_positive_prev'] = df['obv_trend_positive'].shift(1, fill_value=False)

            buy_signal = (df['obv_trend_positive']) & (~df['obv_trend_positive_prev'])
            sell_signal = (~df['obv_trend_positive']) & (df['obv_trend_positive_prev'])

        # Filtrar por volumen mínimo si se especifica
        if self.min_volume > 0:
            low_volume = df['volume'] < self.min_volume
            buy_signal = buy_signal & (~low_volume)
            sell_signal = sell_signal & (~low_volume)

        # Generar señales
        df['signal'] = 0
        df.loc[buy_signal.fillna(False), 'signal'] = 1
        df.loc[sell_signal.fillna(False), 'signal'] = -1

        return df

    def _calculate_obv(self, df: pd.DataFrame) -> pd.Series:
        """Calcula el On-Balance Volume.

        Args:
            df: DataFrame con columnas ['close', 'volume']

        Returns:
            Serie con valores de OBV
        """
        obv = pd.Series(index=df.index, dtype=float)
        obv.iloc[0] = df['volume'].iloc[0]

        for i in range(1, len(df)):
            if df['close'].iloc[i] > df['close'].iloc[i - 1]:
                # Precio sube: sumar volumen
                obv.iloc[i] = obv.iloc[i - 1] + df['volume'].iloc[i]
            elif df['close'].iloc[i] < df['close'].iloc[i - 1]:
                # Precio baja: restar volumen
                obv.iloc[i] = obv.iloc[i - 1] - df['volume'].iloc[i]
            else:
                # Precio sin cambio: mantener OBV
                obv.iloc[i] = obv.iloc[i - 1]

        return obv

    def __str__(self) -> str:
        """Representación en string."""
        mode = "Signal Line" if self.use_signal_line else "Trend"
        return (
            f"OBVStrategy(period={self.period}, "
            f"mode={mode}, "
            f"min_volume={self.min_volume})"
        )
