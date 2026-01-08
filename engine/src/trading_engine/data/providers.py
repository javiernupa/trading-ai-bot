"""Proveedores de datos para diferentes fuentes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import pandas as pd
from loguru import logger

try:
    import yfinance as yf

    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    logger.warning("yfinance no está instalado. Instala con: pip install yfinance")


class DataProvider(ABC):
    """Clase base para proveedores de datos."""

    @abstractmethod
    def fetch_data(
        self,
        symbol: str,
        start_date: str | datetime,
        end_date: str | datetime,
        **kwargs,
    ) -> pd.DataFrame:
        """Obtiene datos históricos.

        Args:
            symbol: Símbolo del activo
            start_date: Fecha de inicio
            end_date: Fecha de fin
            **kwargs: Parámetros adicionales

        Returns:
            DataFrame con datos históricos
        """
        pass


class YahooFinanceProvider(DataProvider):
    """Proveedor de datos usando Yahoo Finance."""

    def __init__(self):
        """Inicializa el proveedor de Yahoo Finance."""
        if not YFINANCE_AVAILABLE:
            raise ImportError(
                "yfinance no está disponible. Instala con: pip install yfinance"
            )

    def fetch_data(
        self,
        symbol: str,
        start_date: str | datetime,
        end_date: str | datetime,
        interval: str = "1d",
        **kwargs,
    ) -> pd.DataFrame:
        """Obtiene datos de Yahoo Finance.

        Args:
            symbol: Ticker del activo (ej: 'AAPL', 'BTC-USD')
            start_date: Fecha de inicio
            end_date: Fecha de fin
            interval: Intervalo de tiempo (1d, 1h, etc.)
            **kwargs: Parámetros adicionales para yfinance

        Returns:
            DataFrame con columnas: open, high, low, close, volume
        """
        logger.info(f"Descargando datos de {symbol} desde Yahoo Finance...")

        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval,
                **kwargs,
            )

            if df.empty:
                raise ValueError(f"No se encontraron datos para {symbol}")

            # Resetear índice para tener la fecha como columna
            df = df.reset_index()
            
            # Normalizar nombres de columnas DESPUÉS del reset_index
            df.columns = df.columns.str.lower()

            # Crear columna timestamp
            if "date" in df.columns:
                df["timestamp"] = pd.to_datetime(df["date"])
            elif "datetime" in df.columns:
                df["timestamp"] = pd.to_datetime(df["datetime"])
            else:
                # Si no hay columna de fecha, usar el índice
                df["timestamp"] = df.index

            # Seleccionar columnas necesarias
            required_cols = ["timestamp", "open", "high", "low", "close", "volume"]
            df = df[required_cols]

            logger.success(f"Descargados {len(df)} registros de {symbol}")
            return df

        except Exception as e:
            logger.error(f"Error descargando datos de {symbol}: {e}")
            raise


class CsvDataProvider(DataProvider):
    """Proveedor de datos desde archivos CSV."""

    def __init__(self, data_dir: str | Path = "data"):
        """Inicializa el proveedor CSV.

        Args:
            data_dir: Directorio donde se encuentran los archivos CSV
        """
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            logger.warning(f"Directorio {data_dir} no existe. Se creará al guardar datos.")

    def fetch_data(
        self,
        symbol: str,
        start_date: str | datetime,
        end_date: str | datetime,
        filename: str | None = None,
        **kwargs,
    ) -> pd.DataFrame:
        """Lee datos desde archivo CSV.

        Args:
            symbol: Símbolo del activo (usado para nombre de archivo)
            start_date: Fecha de inicio para filtrar
            end_date: Fecha de fin para filtrar
            filename: Nombre del archivo (opcional, por defecto usa symbol.csv)
            **kwargs: Parámetros adicionales para pd.read_csv

        Returns:
            DataFrame con datos filtrados por fechas
        """
        if filename is None:
            filename = f"{symbol}.csv"

        filepath = self.data_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

        logger.info(f"Leyendo datos desde {filepath}")

        try:
            df = pd.read_csv(filepath, **kwargs)

            # Convertir timestamp a datetime si existe
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
            elif "date" in df.columns:
                df["timestamp"] = pd.to_datetime(df["date"])
                df = df.drop(columns=["date"])

            # Filtrar por fechas
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            df = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]

            logger.success(f"Leídos {len(df)} registros desde {filepath}")
            return df

        except Exception as e:
            logger.error(f"Error leyendo archivo {filepath}: {e}")
            raise

    def save_data(
        self,
        data: pd.DataFrame,
        symbol: str,
        filename: str | None = None,
    ) -> Path:
        """Guarda datos en archivo CSV.

        Args:
            data: DataFrame con datos a guardar
            symbol: Símbolo del activo
            filename: Nombre del archivo (opcional)

        Returns:
            Path del archivo guardado
        """
        if filename is None:
            filename = f"{symbol}.csv"

        # Crear directorio si no existe
        self.data_dir.mkdir(parents=True, exist_ok=True)

        filepath = self.data_dir / filename

        logger.info(f"Guardando datos en {filepath}")

        try:
            data.to_csv(filepath, index=False)
            logger.success(f"Datos guardados en {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error guardando archivo {filepath}: {e}")
            raise
