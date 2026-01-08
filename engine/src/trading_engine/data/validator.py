"""Validador de datos para asegurar calidad."""

from __future__ import annotations

import pandas as pd
from loguru import logger


class DataValidator:
    """Valida datos de mercado para asegurar calidad."""

    REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]

    @staticmethod
    def validate(data: pd.DataFrame, strict: bool = True) -> tuple[bool, list[str]]:
        """Valida un DataFrame de datos de mercado.

        Args:
            data: DataFrame a validar
            strict: Si es True, lanza excepciones. Si es False, solo retorna warnings

        Returns:
            Tupla (is_valid, warnings)
        """
        warnings = []

        # Check 1: DataFrame no vacío
        if data.empty:
            error = "DataFrame está vacío"
            if strict:
                raise ValueError(error)
            warnings.append(error)
            return False, warnings

        # Check 2: Columnas requeridas
        missing_cols = set(DataValidator.REQUIRED_COLUMNS) - set(data.columns)
        if missing_cols:
            error = f"Faltan columnas requeridas: {missing_cols}"
            if strict:
                raise ValueError(error)
            warnings.append(error)
            return False, warnings

        # Check 3: Timestamp es datetime
        if not pd.api.types.is_datetime64_any_dtype(data["timestamp"]):
            try:
                data["timestamp"] = pd.to_datetime(data["timestamp"])
            except Exception:
                error = "Columna 'timestamp' no se puede convertir a datetime"
                if strict:
                    raise ValueError(error)
                warnings.append(error)
                return False, warnings

        # Check 4: Datos numéricos
        numeric_cols = ["open", "high", "low", "close", "volume"]
        for col in numeric_cols:
            if not pd.api.types.is_numeric_dtype(data[col]):
                error = f"Columna '{col}' no es numérica"
                if strict:
                    raise ValueError(error)
                warnings.append(error)

        # Check 5: Valores nulos
        null_counts = data[DataValidator.REQUIRED_COLUMNS].isnull().sum()
        if null_counts.any():
            warning = f"Se encontraron valores nulos: {null_counts[null_counts > 0].to_dict()}"
            logger.warning(warning)
            warnings.append(warning)

        # Check 6: Valores negativos en precios
        price_cols = ["open", "high", "low", "close"]
        for col in price_cols:
            if (data[col] < 0).any():
                warning = f"Columna '{col}' contiene valores negativos"
                logger.warning(warning)
                warnings.append(warning)

        # Check 7: High >= Low
        if (data["high"] < data["low"]).any():
            warning = "Hay registros donde high < low"
            logger.warning(warning)
            warnings.append(warning)

        # Check 8: Close entre Low y High
        invalid_close = (data["close"] < data["low"]) | (data["close"] > data["high"])
        if invalid_close.any():
            count = invalid_close.sum()
            warning = f"{count} registros tienen close fuera del rango [low, high]"
            logger.warning(warning)
            warnings.append(warning)

        # Check 9: Datos ordenados por timestamp
        if not data["timestamp"].is_monotonic_increasing:
            warning = "Los datos no están ordenados por timestamp"
            logger.warning(warning)
            warnings.append(warning)

        # Check 10: Duplicados en timestamp
        duplicates = data["timestamp"].duplicated().sum()
        if duplicates > 0:
            warning = f"Se encontraron {duplicates} timestamps duplicados"
            logger.warning(warning)
            warnings.append(warning)

        is_valid = len(warnings) == 0
        if is_valid:
            logger.success("Validación completada: datos correctos")
        else:
            logger.warning(f"Validación completada con {len(warnings)} warnings")

        return is_valid, warnings

    @staticmethod
    def clean(data: pd.DataFrame) -> pd.DataFrame:
        """Limpia y prepara datos de mercado.

        Args:
            data: DataFrame a limpiar

        Returns:
            DataFrame limpio
        """
        df = data.copy()

        logger.info("Limpiando datos...")

        # Convertir timestamp (con soporte para timezones)
        if "timestamp" in df.columns and not pd.api.types.is_datetime64_any_dtype(
            df["timestamp"]
        ):
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            # Eliminar timezone para simplificar
            df["timestamp"] = df["timestamp"].dt.tz_localize(None)

        # Eliminar duplicados
        duplicates_before = df["timestamp"].duplicated().sum()
        if duplicates_before > 0:
            df = df.drop_duplicates(subset=["timestamp"], keep="first")
            logger.info(f"Eliminados {duplicates_before} timestamps duplicados")

        # Ordenar por timestamp
        df = df.sort_values("timestamp").reset_index(drop=True)

        # Rellenar valores nulos con forward fill
        null_before = df.isnull().sum().sum()
        if null_before > 0:
            df = df.ffill().bfill()
            logger.info(f"Rellenados {null_before} valores nulos")

        # Eliminar filas con precios negativos
        negative_mask = (
            (df["open"] < 0)
            | (df["high"] < 0)
            | (df["low"] < 0)
            | (df["close"] < 0)
        )
        negative_count = negative_mask.sum()
        if negative_count > 0:
            df = df[~negative_mask]
            logger.info(f"Eliminadas {negative_count} filas con precios negativos")

        # Corregir relaciones high/low
        df["high"] = df[["high", "low"]].max(axis=1)
        df["low"] = df[["high", "low"]].min(axis=1)

        logger.success(f"Datos limpios: {len(df)} registros")
        return df
