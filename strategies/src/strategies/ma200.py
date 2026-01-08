"""Estrategia basada en Media Móvil de 200 períodos (MA200).

La MA200 es uno de los indicadores más seguidos en trading:
- Precio por encima de MA200 → Tendencia alcista → COMPRAR
- Precio por debajo de MA200 → Tendencia bajista → VENDER
- MA200 actúa como soporte/resistencia dinámica

Esta estrategia es ideal para:
- Trading de tendencias a largo plazo
- Evitar mercados laterales
- Filtrar ruido del mercado
"""

from __future__ import annotations

import pandas as pd

from .base import Strategy


class Ma200Strategy(Strategy):
    """Estrategia de Media Móvil de 200 períodos.

    Señales:
    - COMPRA (1): Precio cruza por encima de MA200
    - VENTA (-1): Precio cruza por debajo de MA200
    - MANTENER (0): Sin cruce

    Además, opcionalmente puede usar:
    - Filtro de tendencia: Solo operar cuando precio está por encima/debajo de MA200
    - Confirmación de volumen: Solo señales con volumen superior a la media
    """

    def __init__(
        self,
        period: int = 200,
        use_crossover: bool = True,
        volume_confirmation: bool = False,
        volume_period: int = 20,
    ):
        """Inicializa la estrategia MA200.

        Args:
            period: Período de la media móvil (default: 200)
            use_crossover: Si True, solo genera señales en cruces (más conservador)
                          Si False, genera señales según posición relativa
            volume_confirmation: Si True, requiere volumen superior a la media
            volume_period: Período para calcular media de volumen
        """
        super().__init__()
        self.period = period
        self.use_crossover = use_crossover
        self.volume_confirmation = volume_confirmation
        self.volume_period = volume_period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading basadas en MA200.

        Args:
            data: DataFrame con columnas ['timestamp', 'open', 'high', 'low', 'close', 'volume']

        Returns:
            DataFrame con columna 'signal' añadida:
            - 1: Señal de compra
            - -1: Señal de venta
            - 0: Mantener posición
        """
        df = data.copy()

        # Validar datos mínimos
        if len(df) < self.period:
            raise ValueError(
                f"Datos insuficientes: {len(df)} barras, "
                f"se requieren al menos {self.period}"
            )

        # Calcular MA200
        df["ma200"] = df["close"].rolling(window=self.period).mean()

        # Calcular posición relativa del precio vs MA200
        df["price_above_ma"] = (df["close"] > df["ma200"]).astype(bool)

        if self.use_crossover:
            # Estrategia conservadora: Solo señales en cruces
            df["prev_above_ma"] = df["price_above_ma"].shift(1, fill_value=False)

            # Detectar cruces
            df["bullish_cross"] = (~df["prev_above_ma"]) & df["price_above_ma"]
            df["bearish_cross"] = df["prev_above_ma"] & (~df["price_above_ma"])

            # Generar señales en cruces
            df["signal"] = 0
            df.loc[df["bullish_cross"], "signal"] = 1  # Compra en cruce alcista
            df.loc[df["bearish_cross"], "signal"] = -1  # Venta en cruce bajista

        else:
            # Estrategia agresiva: Señal continua según posición
            df["signal"] = 0
            df.loc[df["price_above_ma"], "signal"] = 1  # Compra si está arriba
            df.loc[~df["price_above_ma"], "signal"] = -1  # Venta si está abajo

        # Confirmación de volumen (opcional)
        if self.volume_confirmation:
            df["volume_ma"] = df["volume"].rolling(window=self.volume_period).mean()
            df["high_volume"] = df["volume"] > df["volume_ma"]

            # Solo mantener señales con volumen alto
            df.loc[~df["high_volume"], "signal"] = 0

        # Eliminar señales donde MA200 no está calculada aún
        df.loc[df["ma200"].isna(), "signal"] = 0

        return df

    def get_indicator_values(self, data: pd.DataFrame) -> dict:
        """Obtiene los valores actuales de los indicadores.

        Args:
            data: DataFrame con señales generadas

        Returns:
            Diccionario con valores de indicadores
        """
        if len(data) == 0:
            return {}

        latest = data.iloc[-1]

        result = {
            "ma200": latest.get("ma200", None),
            "current_price": latest.get("close", None),
            "price_above_ma": latest.get("price_above_ma", None),
        }

        # Calcular distancia porcentual
        if result["ma200"] and result["current_price"]:
            distance = (
                (result["current_price"] - result["ma200"]) / result["ma200"] * 100
            )
            result["distance_pct"] = distance

        if self.use_crossover:
            result["bullish_cross"] = latest.get("bullish_cross", False)
            result["bearish_cross"] = latest.get("bearish_cross", False)

        if self.volume_confirmation:
            result["volume"] = latest.get("volume", None)
            result["volume_ma"] = latest.get("volume_ma", None)
            result["high_volume"] = latest.get("high_volume", None)

        return result

    def __str__(self) -> str:
        """Representación en string de la estrategia."""
        mode = "Crossover" if self.use_crossover else "Position"
        volume = " + Volume" if self.volume_confirmation else ""
        return f"MA200Strategy(period={self.period}, mode={mode}{volume})"
