"""Proveedor de datos de criptomonedas usando Alpaca Markets."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
from loguru import logger

try:
    from alpaca.data.historical import CryptoHistoricalDataClient
    from alpaca.data.requests import CryptoBarsRequest, CryptoLatestBarRequest, CryptoLatestQuoteRequest
    from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

    ALPACA_AVAILABLE = True
except ImportError:
    ALPACA_AVAILABLE = False
    logger.warning("alpaca-py no está instalado. Instala con: pip install alpaca-py")

from .providers import DataProvider


class AlpacaCryptoProvider(DataProvider):
    """Proveedor de datos de criptomonedas usando Alpaca Markets."""

    def __init__(self, api_key: str, secret_key: str):
        """Inicializa el proveedor de Alpaca Crypto.

        Args:
            api_key: API key de Alpaca
            secret_key: Secret key de Alpaca
        """
        if not ALPACA_AVAILABLE:
            raise ImportError("alpaca-py no está disponible")

        self.api_key = api_key
        self.secret_key = secret_key
        self.client = CryptoHistoricalDataClient(api_key, secret_key)

    def fetch_data(
        self,
        symbol: str,
        start_date: str | datetime,
        end_date: str | datetime,
        timeframe: str = "1Day",
        **kwargs,
    ) -> pd.DataFrame:
        """Obtiene datos históricos de criptomonedas de Alpaca.

        Args:
            symbol: Símbolo de la cripto (ej: "BTC/USD", "ETH/USD")
            start_date: Fecha de inicio
            end_date: Fecha de fin
            timeframe: Timeframe (1Min, 5Min, 15Min, 1Hour, 1Day)
            **kwargs: Parámetros adicionales

        Returns:
            DataFrame con datos históricos
        """
        logger.info(f"Descargando datos de {symbol} desde Alpaca Crypto...")

        # Convertir fechas
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)

        # Mapear timeframe
        timeframe_map = {
            "1Min": TimeFrame(1, TimeFrameUnit.Minute),
            "2Min": TimeFrame(2, TimeFrameUnit.Minute),
            "5Min": TimeFrame(5, TimeFrameUnit.Minute),
            "10Min": TimeFrame(10, TimeFrameUnit.Minute),
            "15Min": TimeFrame(15, TimeFrameUnit.Minute),
            "30Min": TimeFrame(30, TimeFrameUnit.Minute),
            "1Hour": TimeFrame(1, TimeFrameUnit.Hour),
            "2Hour": TimeFrame(2, TimeFrameUnit.Hour),
            "4Hour": TimeFrame(4, TimeFrameUnit.Hour),
            "6Hour": TimeFrame(6, TimeFrameUnit.Hour),
            "12Hour": TimeFrame(12, TimeFrameUnit.Hour),
            "1Day": TimeFrame(1, TimeFrameUnit.Day),
            "1Week": TimeFrame(1, TimeFrameUnit.Week),
            "1Month": TimeFrame(1, TimeFrameUnit.Month),
        }

        tf = timeframe_map.get(timeframe, TimeFrame(1, TimeFrameUnit.Day))

        try:
            request = CryptoBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=tf,
                start=start_date,
                end=end_date,
            )

            bars = self.client.get_crypto_bars(request)

            # Convertir a DataFrame
            df = bars.df

            if df.empty:
                raise ValueError(f"No se encontraron datos para {symbol}")

            # Resetear índice
            df = df.reset_index()

            # Renombrar columnas
            df = df.rename(
                columns={
                    "timestamp": "timestamp",
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "volume": "volume",
                }
            )

            # Seleccionar columnas necesarias
            df = df[["timestamp", "open", "high", "low", "close", "volume"]]

            # Asegurar que timestamp es datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            logger.success(f"Descargados {len(df)} registros de {symbol} desde Alpaca Crypto")
            return df

        except Exception as e:
            logger.error(f"Error descargando datos de {symbol}: {e}")
            raise

    def fetch_latest_quote(self, symbol: str) -> dict:
        """Obtiene la cotización más reciente de crypto.

        Args:
            symbol: Símbolo de la cripto (ej: "BTC/USD")

        Returns:
            Diccionario con bid, ask, last, etc.
        """
        try:
            request = CryptoLatestQuoteRequest(symbol_or_symbols=symbol)
            quote = self.client.get_crypto_latest_quote(request)

            return {
                "symbol": symbol,
                "bid": float(quote[symbol].bid_price),
                "ask": float(quote[symbol].ask_price),
                "bid_size": float(quote[symbol].bid_size),
                "ask_size": float(quote[symbol].ask_size),
                "timestamp": quote[symbol].timestamp,
            }

        except Exception as e:
            logger.error(f"Error obteniendo quote de {symbol}: {e}")
            raise

    def fetch_latest_bar(self, symbol: str) -> pd.Series:
        """Obtiene la barra más reciente de crypto.

        Args:
            symbol: Símbolo de la cripto (ej: "BTC/USD")

        Returns:
            Serie con OHLCV más reciente
        """
        try:
            request = CryptoLatestBarRequest(symbol_or_symbols=symbol)
            bar = self.client.get_crypto_latest_bar(request)

            return pd.Series(
                {
                    "timestamp": bar[symbol].timestamp,
                    "open": float(bar[symbol].open),
                    "high": float(bar[symbol].high),
                    "low": float(bar[symbol].low),
                    "close": float(bar[symbol].close),
                    "volume": float(bar[symbol].volume),
                }
            )

        except Exception as e:
            logger.error(f"Error obteniendo bar de {symbol}: {e}")
            raise
