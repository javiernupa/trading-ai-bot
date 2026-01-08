"""
Parabolic SAR Strategy

Estrategia basada en el indicador Parabolic SAR (Stop and Reverse) desarrollado
por J. Welles Wilder. Este indicador se utiliza para determinar la dirección de
la tendencia y posibles puntos de reversión.

Señales:
- BUY: Cuando el SAR cambia de estar por encima del precio a por debajo (inicio tendencia alcista)
- SELL: Cuando el SAR cambia de estar por debajo del precio a por encima (inicio tendencia bajista)
"""

import pandas as pd
import numpy as np
from .base import BaseStrategy


class ParabolicSARStrategy(BaseStrategy):
    """Estrategia basada en el indicador Parabolic SAR."""

    def __init__(
        self,
        af_start: float = 0.02,
        af_increment: float = 0.02,
        af_max: float = 0.20,
        **kwargs
    ):
        """
        Inicializa la estrategia Parabolic SAR.

        Args:
            af_start: Factor de aceleración inicial (default: 0.02)
            af_increment: Incremento del factor de aceleración (default: 0.02)
            af_max: Factor de aceleración máximo (default: 0.20)
        """
        super().__init__(**kwargs)
        self.af_start = af_start
        self.af_increment = af_increment
        self.af_max = af_max

    def _calculate_parabolic_sar(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula el indicador Parabolic SAR.

        Args:
            df: DataFrame con columnas 'high', 'low', 'close'

        Returns:
            DataFrame con columnas adicionales: 'sar', 'sar_trend'
        """
        df = df.copy()
        
        high = df['high'].values
        low = df['low'].values
        close = df['close'].values
        
        n = len(df)
        sar = np.zeros(n)
        ep = np.zeros(n)
        af = np.zeros(n)
        trend = np.zeros(n)  # 1 = alcista, -1 = bajista
        
        # Inicialización
        sar[0] = low[0]
        ep[0] = high[0]
        af[0] = self.af_start
        trend[0] = 1  # Empezamos en tendencia alcista
        
        for i in range(1, n):
            # SAR anterior
            prev_sar = sar[i-1]
            prev_ep = ep[i-1]
            prev_af = af[i-1]
            prev_trend = trend[i-1]
            
            # Calcular nuevo SAR
            sar[i] = prev_sar + prev_af * (prev_ep - prev_sar)
            
            # Determinar tendencia actual
            if prev_trend == 1:  # Tendencia alcista
                # Ajustar SAR para que no supere los mínimos de las últimas 2 velas
                if i >= 2:
                    sar[i] = min(sar[i], low[i-1], low[i-2])
                elif i >= 1:
                    sar[i] = min(sar[i], low[i-1])
                
                # Verificar si hay reversión
                if low[i] < sar[i]:
                    # Reversión a tendencia bajista
                    trend[i] = -1
                    sar[i] = prev_ep  # SAR se mueve al EP anterior
                    ep[i] = low[i]  # Nuevo EP es el mínimo actual
                    af[i] = self.af_start  # Resetear AF
                else:
                    # Continuar tendencia alcista
                    trend[i] = 1
                    # Actualizar EP si hay nuevo máximo
                    if high[i] > prev_ep:
                        ep[i] = high[i]
                        af[i] = min(prev_af + self.af_increment, self.af_max)
                    else:
                        ep[i] = prev_ep
                        af[i] = prev_af
            
            else:  # Tendencia bajista (prev_trend == -1)
                # Ajustar SAR para que no sea menor que los máximos de las últimas 2 velas
                if i >= 2:
                    sar[i] = max(sar[i], high[i-1], high[i-2])
                elif i >= 1:
                    sar[i] = max(sar[i], high[i-1])
                
                # Verificar si hay reversión
                if high[i] > sar[i]:
                    # Reversión a tendencia alcista
                    trend[i] = 1
                    sar[i] = prev_ep  # SAR se mueve al EP anterior
                    ep[i] = high[i]  # Nuevo EP es el máximo actual
                    af[i] = self.af_start  # Resetear AF
                else:
                    # Continuar tendencia bajista
                    trend[i] = -1
                    # Actualizar EP si hay nuevo mínimo
                    if low[i] < prev_ep:
                        ep[i] = low[i]
                        af[i] = min(prev_af + self.af_increment, self.af_max)
                    else:
                        ep[i] = prev_ep
                        af[i] = prev_af
        
        df['sar'] = sar
        df['sar_trend'] = trend
        
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Genera señales de trading basadas en el Parabolic SAR.

        Args:
            df: DataFrame con datos de precio (high, low, close)

        Returns:
            DataFrame con columna 'signal' (-1: sell, 0: hold, +1: buy)
        """
        df = self._calculate_parabolic_sar(df)
        
        # Inicializar señal en 0 (hold)
        df['signal'] = 0
        
        # Detectar cambios de tendencia
        df['trend_change'] = df['sar_trend'].diff()
        
        # Señal de compra: cambio de tendencia bajista a alcista
        df.loc[df['trend_change'] > 0, 'signal'] = 1
        
        # Señal de venta: cambio de tendencia alcista a bajista
        df.loc[df['trend_change'] < 0, 'signal'] = -1
        
        # Limpiar columnas auxiliares
        df = df.drop(columns=['trend_change'])
        
        return df
