"""Loader centralizado para gestión de datos."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from loguru import logger

from .providers import CsvDataProvider, DataProvider, YahooFinanceProvider
from .validator import DataValidator


class DataLoader:
    """Gestor centralizado de datos con caché y validación."""

    def __init__(
        self,
        cache_dir: str | Path = "data/cache",
        use_cache: bool = True,
        validate_data: bool = True,
    ):
        """Inicializa el DataLoader.

        Args:
            cache_dir: Directorio para caché de datos
            use_cache: Si usar caché local
            validate_data: Si validar datos automáticamente
        """
        self.cache_dir = Path(cache_dir)
        self.use_cache = use_cache
        self.validate_data = validate_data

        if use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.csv_provider = CsvDataProvider(cache_dir)
        self.validator = DataValidator()

    def load_data(
        self,
        symbol: str,
        start_date: str | datetime,
        end_date: str | datetime,
        provider: str | DataProvider = "yahoo",
        force_download: bool = False,
        clean_data: bool = True,
        **kwargs,
    ) -> pd.DataFrame:
        """Carga datos desde caché o descarga si es necesario.

        Args:
            symbol: Símbolo del activo
            start_date: Fecha de inicio
            end_date: Fecha de fin
            provider: Proveedor de datos ('yahoo', 'csv') o instancia de DataProvider
            force_download: Forzar descarga aunque exista en caché
            clean_data: Limpiar datos automáticamente
            **kwargs: Parámetros adicionales para el proveedor

        Returns:
            DataFrame con datos históricos
        """
        # Verificar caché primero
        cache_file = self.cache_dir / f"{symbol}_{start_date}_{end_date}.csv"

        if self.use_cache and cache_file.exists() and not force_download:
            logger.info(f"Cargando datos desde caché: {cache_file}")
            try:
                data = pd.read_csv(cache_file)
                data["timestamp"] = pd.to_datetime(data["timestamp"])
                logger.success(f"Datos cargados desde caché: {len(data)} registros")
            except Exception as e:
                logger.warning(f"Error leyendo caché, descargando datos: {e}")
                data = self._download_data(symbol, start_date, end_date, provider, **kwargs)
                self._save_to_cache(data, cache_file)
        else:
            data = self._download_data(symbol, start_date, end_date, provider, **kwargs)
            if self.use_cache:
                self._save_to_cache(data, cache_file)

        # Validar datos
        if self.validate_data:
            try:
                self.validator.validate(data, strict=False)
            except Exception as e:
                logger.error(f"Error validando datos: {e}")

        # Limpiar datos
        if clean_data:
            data = self.validator.clean(data)

        return data

    def _download_data(
        self,
        symbol: str,
        start_date: str | datetime,
        end_date: str | datetime,
        provider: str | DataProvider,
        **kwargs,
    ) -> pd.DataFrame:
        """Descarga datos del proveedor.

        Args:
            symbol: Símbolo del activo
            start_date: Fecha de inicio
            end_date: Fecha de fin
            provider: Proveedor de datos
            **kwargs: Parámetros adicionales

        Returns:
            DataFrame con datos descargados
        """
        if isinstance(provider, str):
            if provider.lower() == "yahoo":
                provider = YahooFinanceProvider()
            elif provider.lower() == "csv":
                provider = CsvDataProvider()
            else:
                raise ValueError(f"Proveedor desconocido: {provider}")

        return provider.fetch_data(symbol, start_date, end_date, **kwargs)

    def _save_to_cache(self, data: pd.DataFrame, filepath: Path) -> None:
        """Guarda datos en caché.

        Args:
            data: DataFrame a guardar
            filepath: Ruta del archivo
        """
        try:
            data.to_csv(filepath, index=False)
            logger.info(f"Datos guardados en caché: {filepath}")
        except Exception as e:
            logger.warning(f"No se pudieron guardar datos en caché: {e}")

    def clear_cache(self, symbol: str | None = None) -> None:
        """Limpia caché de datos.

        Args:
            symbol: Si se especifica, solo limpia datos de ese símbolo
        """
        if not self.cache_dir.exists():
            return

        if symbol:
            pattern = f"{symbol}_*.csv"
            files = list(self.cache_dir.glob(pattern))
        else:
            files = list(self.cache_dir.glob("*.csv"))

        for file in files:
            file.unlink()
            logger.info(f"Eliminado de caché: {file}")

        logger.success(f"Caché limpiado: {len(files)} archivos eliminados")

    def download_and_save(
        self,
        symbol: str,
        start_date: str | datetime,
        end_date: str | datetime,
        output_file: str | Path,
        provider: str = "yahoo",
        **kwargs,
    ) -> Path:
        """Descarga datos y los guarda en archivo.

        Args:
            symbol: Símbolo del activo
            start_date: Fecha de inicio
            end_date: Fecha de fin
            output_file: Archivo de salida
            provider: Proveedor de datos
            **kwargs: Parámetros adicionales

        Returns:
            Path del archivo guardado
        """
        data = self.load_data(
            symbol,
            start_date,
            end_date,
            provider=provider,
            force_download=True,
            **kwargs,
        )

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data.to_csv(output_path, index=False)
        logger.success(f"Datos guardados en: {output_path}")

        return output_path
