"""Estrategia combinada que usa múltiples estrategias independientes.

Esta estrategia permite combinar cualquier número de estrategias individuales
(RSI, MACD, MA50, MA100, MA200, etc.) y generar señales basadas en consenso.
"""

from __future__ import annotations

from typing import List

import pandas as pd

from .base import BaseStrategy, Strategy


class CombinedStrategy(BaseStrategy):
    """Estrategia que combina múltiples estrategias para señales más robustas.
    
    Acepta una lista de estrategias individuales y genera señales basadas en
    el consenso (número mínimo de estrategias que deben coincidir).
    
    Ejemplo:
        from strategies import RsiStrategy, MacdStrategy, Ma200Strategy
        
        strategies = [
            RsiStrategy(),
            MacdStrategy(),
            Ma200Strategy()
        ]
        
        combined = CombinedStrategy(strategies, consensus_threshold=2)
    """

    def __init__(
        self,
        strategies: List[Strategy],
        consensus_threshold: int = 2,
    ) -> None:
        """Inicializa la estrategia combinada.

        Args:
            strategies: Lista de estrategias a combinar
            consensus_threshold: Número mínimo de estrategias que deben coincidir
                                para generar una señal (default: 2)
        
        Raises:
            ValueError: Si no hay suficientes estrategias o threshold inválido
        """
        if not strategies:
            raise ValueError("Debe proporcionar al menos una estrategia")
        
        if consensus_threshold < 1:
            raise ValueError("consensus_threshold debe ser al menos 1")
        
        if consensus_threshold > len(strategies):
            raise ValueError(
                f"consensus_threshold ({consensus_threshold}) no puede ser mayor "
                f"que el número de estrategias ({len(strategies)})"
            )
        
        self.strategies = strategies
        self.consensus_threshold = consensus_threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales combinadas de múltiples estrategias.

        Args:
            data: DataFrame con datos históricos

        Returns:
            DataFrame con columna 'signal' añadida (-1, 0, 1) y señales individuales
        """
        df = data.copy()
        
        # Inicializar contadores de votos
        df["buy_votes"] = 0
        df["sell_votes"] = 0
        
        # Aplicar cada estrategia y contar votos
        for i, strategy in enumerate(self.strategies):
            # Generar señales de la estrategia individual
            strategy_result = strategy.generate_signals(data)
            
            # Obtener columna de señal (puede ser 'signal' o personalizada)
            signal_col = "signal"
            if signal_col not in strategy_result.columns:
                raise ValueError(
                    f"La estrategia {strategy.__class__.__name__} no generó "
                    "una columna 'signal'"
                )
            
            # Guardar señales individuales con nombre único
            strategy_name = f"{strategy.__class__.__name__.lower()}_{i}"
            df[f"{strategy_name}_signal"] = strategy_result[signal_col]
            
            # Contar votos
            df["buy_votes"] += (strategy_result[signal_col] == 1).astype(int)
            df["sell_votes"] += (strategy_result[signal_col] == -1).astype(int)
            
            # Copiar columnas de indicadores si existen
            for col in strategy_result.columns:
                if col not in ["signal", "timestamp", "open", "high", "low", "close", "volume"]:
                    # Agregar prefijo para evitar colisiones
                    new_col_name = f"{strategy_name}_{col}"
                    df[new_col_name] = strategy_result[col]
        
        # Señal final basada en consenso
        df["signal"] = 0
        df.loc[df["buy_votes"] >= self.consensus_threshold, "signal"] = 1
        df.loc[df["sell_votes"] >= self.consensus_threshold, "signal"] = -1

        return df
    
    def get_strategy_summary(self) -> dict:
        """Obtiene un resumen de las estrategias configuradas.
        
        Returns:
            Diccionario con información de configuración
        """
        return {
            "num_strategies": len(self.strategies),
            "strategies": [str(s) for s in self.strategies],
            "consensus_threshold": self.consensus_threshold,
            "consensus_percentage": (self.consensus_threshold / len(self.strategies)) * 100,
        }
    
    def __str__(self) -> str:
        """Representación en string de la estrategia."""
        strategy_names = ", ".join([s.__class__.__name__ for s in self.strategies])
        return (
            f"CombinedStrategy({len(self.strategies)} strategies: {strategy_names}, "
            f"threshold={self.consensus_threshold}/{len(self.strategies)})"
        )
