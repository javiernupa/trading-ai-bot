import pandas as pd
from .base import BaseStrategy

class RsiStrategy(BaseStrategy):
    def __init__(self, period: int = 14, lower: int = 30, upper: int = 70):
        self.period = period
        self.lower = lower
        self.upper = upper

    def _rsi(self, series: pd.Series) -> pd.Series:
        delta = series.diff()
        up = delta.clip(lower=0).ewm(alpha=1/self.period).mean()
        down = -delta.clip(upper=0).ewm(alpha=1/self.period).mean()
        rs = up / down
        return 100 - (100 / (1 + rs))

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df["rsi"] = self._rsi(df["close"])
        df["signal"] = 0
        df.loc[df.rsi < self.lower, "signal"] = 1
        df.loc[df.rsi > self.upper, "signal"] = -1
        return df
