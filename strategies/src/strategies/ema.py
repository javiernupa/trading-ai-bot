"""
EMA Strategy

Estrategia basada en Media Móvil Exponencial (Exponential Moving Average).
La EMA da más peso a los precios recientes, siendo más sensible a cambios
de tendencia que la SMA.

Señales:
- BUY: Cuando el precio cruza por encima de la EMA (señal alcista)
- SELL: Cuando el precio cruza por debajo de la EMA (señal bajista)
- Opción de usar dos EMAs (rápida y lenta) para señales de cruce
"""

import pandas as pd
from .base import BaseStrategy


class EMAStrategy(BaseStrategy):
    """Estrategia basada en Media Móvil Exponencial."""

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
        Inicializa la estrategia EMA.

        Args:
            period: Período de la EMA principal (default: 20)
            fast_period: Período de EMA rápida para crossover (opcional)
            slow_period: Período de EMA lenta para crossover (opcional)
            use_crossover: Si True, usa cruce de EMAs en lugar de precio vs EMA
            use_volume_confirmation: Si True, requiere volumen alto para señales
        """
        super().__init__(**kwargs)
        self.period = period
        self.fast_period = fast_period or 12
        self.slow_period = slow_period or 26
        self.use_crossover = use_crossover
        self.use_volume_confirmation = use_volume_confirmation

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Genera señales de trading basadas en EMA.

        Args:
            df: DataFrame con datos de precio (close, volume)

        Returns:
            DataFrame con columna 'signal' (-1: sell, 0: hold, +1: buy)
        """
        df = df.copy()
        
        if self.use_crossover:
            # Estrategia de cruce de dos EMAs
            df['ema_fast'] = df['close'].ewm(span=self.fast_period, adjust=False).mean()
            df['ema_slow'] = df['close'].ewm(span=self.slow_period, adjust=False).mean()
            
            # Detectar cruces
            fast_above_slow = (df['ema_fast'] > df['ema_slow']).fillna(False)
            prev_fast_above = fast_above_slow.shift(1, fill_value=False)
            
            # Cruce alcista: EMA rápida cruza por encima de lenta
            bullish_cross = (~prev_fast_above) & fast_above_slow
            
            # Cruce bajista: EMA rápida cruza por debajo de lenta
            bearish_cross = prev_fast_above & (~fast_above_slow)
            
            df['signal'] = 0
            df.loc[bullish_cross, 'signal'] = 1
            df.loc[bearish_cross, 'signal'] = -1
            
        else:
            # Estrategia de precio vs EMA
            df['ema'] = df['close'].ewm(span=self.period, adjust=False).mean()
            
            # Detectar cruces de precio con EMA
            price_above_ema = (df['close'] > df['ema']).fillna(False)
            prev_above_ema = price_above_ema.shift(1, fill_value=False)
            
            bullish_cross = (~prev_above_ema) & price_above_ema
            bearish_cross = prev_above_ema & (~price_above_ema)
            
            # Inicializar señales
            df['signal'] = 0
            
            # Señales basadas en cruces
            df.loc[bullish_cross, 'signal'] = 1
            df.loc[bearish_cross, 'signal'] = -1
            
            # Alternativa: señal continua mientras está arriba/abajo
            # df.loc[price_above_ema, 'signal'] = 1
            # df.loc[~price_above_ema, 'signal'] = -1
        
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
            return f"EMAStrategy(fast={self.fast_period}, slow={self.slow_period}, crossover=True)"
        return f"EMAStrategy(period={self.period})"
