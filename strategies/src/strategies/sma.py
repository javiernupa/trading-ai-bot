"""
SMA Strategy

Estrategia basada en Media Móvil Simple (Simple Moving Average).
La SMA calcula el promedio de precios de cierre en un período específico,
proporcionando señales más suaves y menos sensibles al ruido del mercado.

Señales:
- BUY: Cuando el precio cruza por encima de la SMA (señal alcista)
- SELL: Cuando el precio cruza por debajo de la SMA (señal bajista)
- Opción de usar dos SMAs (rápida y lenta) para señales de cruce
"""

import pandas as pd
from .base import BaseStrategy


class SMAStrategy(BaseStrategy):
    """Estrategia basada en Media Móvil Simple."""

    def __init__(
        self,
        period: int = 20,
        fast_period: int = None,
        slow_period: int = None,
        use_crossover: bool = False,
        use_volume_confirmation: bool = False,
        **kwargs
    ):
        """
        Inicializa la estrategia SMA.

        Args:
            period: Período de la SMA principal (default: 20)
            fast_period: Período de SMA rápida para crossover (opcional)
            slow_period: Período de SMA lenta para crossover (opcional)
            use_crossover: Si True, usa cruce de SMAs en lugar de precio vs SMA
            use_volume_confirmation: Si True, requiere volumen alto para señales
        """
        super().__init__(**kwargs)
        self.period = period
        self.fast_period = fast_period or 10
        self.slow_period = slow_period or 30
        self.use_crossover = use_crossover
        self.use_volume_confirmation = use_volume_confirmation

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Genera señales de trading basadas en SMA.

        Args:
            df: DataFrame con datos de precio (close, volume)

        Returns:
            DataFrame con columna 'signal' (-1: sell, 0: hold, +1: buy)
        """
        df = df.copy()
        
        if self.use_crossover:
            # Estrategia de cruce de dos SMAs
            df['sma_fast'] = df['close'].rolling(window=self.fast_period).mean()
            df['sma_slow'] = df['close'].rolling(window=self.slow_period).mean()
            
            # Detectar cruces
            fast_above_slow = (df['sma_fast'] > df['sma_slow']).fillna(False)
            prev_fast_above = fast_above_slow.shift(1, fill_value=False)
            
            # Cruce alcista: SMA rápida cruza por encima de lenta
            bullish_cross = (~prev_fast_above) & fast_above_slow
            
            # Cruce bajista: SMA rápida cruza por debajo de lenta
            bearish_cross = prev_fast_above & (~fast_above_slow)
            
            df['signal'] = 0
            df.loc[bullish_cross, 'signal'] = 1
            df.loc[bearish_cross, 'signal'] = -1
            
        else:
            # Estrategia de precio vs SMA
            df['sma'] = df['close'].rolling(window=self.period).mean()
            
            # Detectar cruces de precio con SMA
            price_above_sma = (df['close'] > df['sma']).fillna(False)
            prev_above_sma = price_above_sma.shift(1, fill_value=False)
            
            bullish_cross = (~prev_above_sma) & price_above_sma
            bearish_cross = prev_above_sma & (~price_above_sma)
            
            # Inicializar señales
            df['signal'] = 0
            
            # Señales basadas en cruces
            df.loc[bullish_cross, 'signal'] = 1
            df.loc[bearish_cross, 'signal'] = -1
            
            # Alternativa: señal continua mientras está arriba/abajo
            # df.loc[price_above_sma, 'signal'] = 1
            # df.loc[~price_above_sma, 'signal'] = -1
        
        # Confirmación por volumen (opcional)
        if self.use_volume_confirmation and 'volume' in df.columns:
            volume_ma = df['volume'].rolling(window=20).mean()
            high_volume = (df['volume'] > volume_ma * 1.5).fillna(False)
            
            # Solo mantener señales con volumen alto
            df.loc[~high_volume, 'signal'] = 0
        
        return df

    def __repr__(self) -> str:
        """Representación en string de la estrategia."""
        if self.use_crossover:
            return f"SMAStrategy(fast={self.fast_period}, slow={self.slow_period}, crossover=True)"
        return f"SMAStrategy(period={self.period})"
