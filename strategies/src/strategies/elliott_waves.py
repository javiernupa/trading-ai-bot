"""
Estrategia Elliott Waves

Detecta patrones de ondas de Elliott para generar señales de trading.
La teoría de Elliott Waves identifica patrones de ondas impulsivas (1, 3, 5)
y correctivas (2, 4, A, B, C) en los movimientos de precios.

Esta implementación simplificada:
- Identifica pivotes (máximos y mínimos locales)
- Detecta ondas impulsivas y correctivas
- Genera señales basadas en patrones de ondas
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from .base import Strategy


class ElliottWavesStrategy(Strategy):
    """
    Estrategia basada en la teoría de Elliott Waves.
    
    Detecta patrones de ondas para identificar:
    - Ondas impulsivas (1, 3, 5): movimientos en la dirección de la tendencia principal
    - Ondas correctivas (2, 4): correcciones contra la tendencia
    - Ondas ABC: patrones correctivos más amplios
    
    Señales:
    - COMPRA: Inicio de onda 3 o onda 5 (las ondas impulsivas más fuertes)
    - VENTA: Final de onda 5 o inicio de onda A correctiva
    
    Parámetros:
    - pivot_window (int): Ventana para identificar pivotes (default: 5)
    - min_wave_size (float): Tamaño mínimo de onda en % (default: 2.0)
    - use_volume (bool): Confirmar con volumen (default: True)
    - wave_count (int): Número de ondas para análisis (default: 5)
    """
    
    def __init__(
        self,
        pivot_window: int = 5,
        min_wave_size: float = 2.0,
        use_volume: bool = True,
        wave_count: int = 5
    ):
        """
        Inicializa la estrategia Elliott Waves.
        
        Args:
            pivot_window: Ventana para identificar pivotes (máximos/mínimos locales)
            min_wave_size: Tamaño mínimo de onda en porcentaje
            use_volume: Si True, confirma señales con volumen
            wave_count: Número de ondas a considerar en el análisis
        """
        super().__init__()
        self.pivot_window = pivot_window
        self.min_wave_size = min_wave_size / 100.0  # Convertir a decimal
        self.use_volume = use_volume
        self.wave_count = wave_count
        
    def __str__(self):
        return (f"ElliottWavesStrategy(pivot_window={self.pivot_window}, "
                f"min_wave_size={self.min_wave_size*100:.1f}%, "
                f"use_volume={self.use_volume}, wave_count={self.wave_count})")
    
    def __repr__(self):
        return self.__str__()
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Genera señales de trading basadas en patrones de Elliott Waves.
        
        Args:
            data: DataFrame con columnas OHLCV
            
        Returns:
            DataFrame con señales y columnas adicionales:
            - signal: 1 (compra), -1 (venta), 0 (neutral)
            - pivot_high: Pivotes altos identificados
            - pivot_low: Pivotes bajos identificados
            - wave_number: Número de onda actual (1-5)
            - wave_type: Tipo de onda ('impulse' o 'corrective')
        """
        df = data.copy()
        
        # Inicializar columnas
        df["signal"] = 0
        df["pivot_high"] = False
        df["pivot_low"] = False
        df["wave_number"] = 0
        df["wave_type"] = "neutral"
        
        # Validar datos suficientes
        if len(df) < self.pivot_window * 2 + 1:
            return df
        
        # 1. Identificar pivotes (máximos y mínimos locales)
        df = self._identify_pivots(df)
        
        # 2. Detectar ondas
        df = self._detect_waves(df)
        
        # 3. Generar señales basadas en patrones de ondas
        df = self._generate_wave_signals(df)
        
        # 4. Confirmar con volumen si está habilitado
        if self.use_volume and "volume" in df.columns:
            df = self._confirm_with_volume(df)
        
        return df
    
    def _identify_pivots(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Identifica pivotes (máximos y mínimos locales) usando una ventana móvil.
        
        Un pivot alto es un máximo local donde el precio es mayor que
        los precios en la ventana antes y después.
        
        Un pivot bajo es un mínimo local donde el precio es menor que
        los precios en la ventana antes y después.
        """
        df = df.copy()
        
        for i in range(self.pivot_window, len(df) - self.pivot_window):
            # Ventana de precios alrededor del punto actual
            window_high = df["high"].iloc[i - self.pivot_window:i + self.pivot_window + 1]
            window_low = df["low"].iloc[i - self.pivot_window:i + self.pivot_window + 1]
            
            current_high = df["high"].iloc[i]
            current_low = df["low"].iloc[i]
            
            # Pivot alto: máximo en la ventana
            if current_high == window_high.max():
                df.loc[df.index[i], "pivot_high"] = True
            
            # Pivot bajo: mínimo en la ventana
            if current_low == window_low.min():
                df.loc[df.index[i], "pivot_low"] = True
        
        return df
    
    def _detect_waves(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detecta ondas de Elliott basándose en los pivotes identificados.
        
        Clasifica las ondas como:
        - Impulsivas: Ondas 1, 3, 5 (movimiento en dirección de la tendencia)
        - Correctivas: Ondas 2, 4 (correcciones contra la tendencia)
        """
        df = df.copy()
        
        # Obtener índices de pivotes
        pivot_highs = df[df["pivot_high"]].index.tolist()
        pivot_lows = df[df["pivot_low"]].index.tolist()
        
        # Combinar y ordenar todos los pivotes
        all_pivots = sorted(
            [(idx, "high", df.loc[idx, "high"]) for idx in pivot_highs] +
            [(idx, "low", df.loc[idx, "low"]) for idx in pivot_lows]
        )
        
        if len(all_pivots) < 3:
            return df
        
        # Analizar secuencia de ondas
        wave_num = 1
        trend = "up"  # Comenzar asumiendo tendencia alcista
        
        for i in range(1, len(all_pivots)):
            prev_idx, prev_type, prev_price = all_pivots[i - 1]
            curr_idx, curr_type, curr_price = all_pivots[i]
            
            # Calcular tamaño de la onda
            wave_size = abs(curr_price - prev_price) / prev_price
            
            # Solo considerar ondas significativas
            if wave_size >= self.min_wave_size:
                # Determinar tipo de onda
                if prev_type == "low" and curr_type == "high":
                    # Movimiento alcista
                    if trend == "up":
                        wave_type = "impulse"
                    else:
                        wave_type = "corrective"
                        trend = "up"
                        wave_num = 1
                elif prev_type == "high" and curr_type == "low":
                    # Movimiento bajista
                    if trend == "down":
                        wave_type = "impulse"
                    else:
                        wave_type = "corrective"
                        trend = "down"
                        wave_num = 1
                else:
                    continue
                
                # Asignar número y tipo de onda al rango
                mask = (df.index >= prev_idx) & (df.index <= curr_idx)
                df.loc[mask, "wave_number"] = wave_num
                df.loc[mask, "wave_type"] = wave_type
                
                # Incrementar número de onda (ciclo 1-5)
                wave_num = (wave_num % 5) + 1
        
        return df
    
    def _generate_wave_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Genera señales de trading basadas en los patrones de ondas detectados.
        
        Reglas:
        - COMPRA: Inicio de onda 3 (la más fuerte) o onda 5
        - VENTA: Final de onda 5 (fin del ciclo impulsivo)
        """
        df = df.copy()
        
        for i in range(1, len(df)):
            prev_wave = df["wave_number"].iloc[i - 1]
            curr_wave = df["wave_number"].iloc[i]
            curr_type = df["wave_type"].iloc[i]
            
            # Señal de COMPRA: Inicio de onda 3 o onda 5 (impulsivas)
            if curr_type == "impulse":
                if prev_wave != curr_wave and curr_wave in [3, 5]:
                    # Verificar que sea movimiento alcista
                    if df["close"].iloc[i] > df["close"].iloc[i - 1]:
                        df.loc[df.index[i], "signal"] = 1
            
            # Señal de VENTA: Final de onda 5 o inicio de onda correctiva bajista
            if curr_type == "corrective" or (curr_type == "impulse" and prev_wave == 5):
                if df["close"].iloc[i] < df["close"].iloc[i - 1]:
                    df.loc[df.index[i], "signal"] = -1
        
        return df
    
    def _confirm_with_volume(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Confirma señales con análisis de volumen.
        
        Las ondas impulsivas (1, 3, 5) deben tener mayor volumen.
        Las ondas correctivas (2, 4) suelen tener menor volumen.
        """
        df = df.copy()
        
        # Calcular volumen promedio
        volume_ma = df["volume"].rolling(window=20, min_periods=1).mean()
        
        for i in range(len(df)):
            if df["signal"].iloc[i] != 0:
                curr_volume = df["volume"].iloc[i]
                avg_volume = volume_ma.iloc[i]
                wave_type = df["wave_type"].iloc[i]
                
                # Las ondas impulsivas deben tener volumen superior al promedio
                if wave_type == "impulse" and curr_volume < avg_volume * 1.2:
                    df.loc[df.index[i], "signal"] = 0
                
                # Las señales de venta deben tener volumen decente
                if df["signal"].iloc[i] == -1 and curr_volume < avg_volume * 0.8:
                    df.loc[df.index[i], "signal"] = 0
        
        return df
    
    def get_parameters(self) -> Dict[str, Any]:
        """Retorna los parámetros de la estrategia."""
        return {
            "pivot_window": self.pivot_window,
            "min_wave_size": self.min_wave_size * 100,
            "use_volume": self.use_volume,
            "wave_count": self.wave_count
        }
