"""Gestión de configuración usando pydantic-settings."""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración global del sistema de trading."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Trading parameters
    initial_cash: float = Field(default=10000.0, description="Capital inicial para backtesting")
    commission: float = Field(default=0.001, description="Comisión por operación (0.1%)")
    slippage: float = Field(default=0.0005, description="Slippage esperado (0.05%)")

    # Data provider
    data_provider: Literal["yfinance", "alpaca", "binance"] = Field(
        default="yfinance", description="Proveedor de datos de mercado"
    )

    # API keys (opcional)
    alpaca_api_key: str | None = None
    alpaca_secret_key: str | None = None
    binance_api_key: str | None = None
    binance_secret_key: str | None = None

    # Database
    database_url: str = Field(
        default="sqlite:///./data/trading.db", description="URL de conexión a la base de datos"
    )

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Nivel de logging"
    )
    log_file: Path = Field(default=Path("logs/trading.log"), description="Archivo de logs")

    # Notifications
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    email_host: str | None = None
    email_port: int = 587
    email_user: str | None = None
    email_password: str | None = None

    # Backtesting
    backtest_start_date: str = Field(
        default="2020-01-01", description="Fecha inicio backtesting"
    )
    backtest_end_date: str = Field(default="2023-12-31", description="Fecha fin backtesting")


# Singleton para acceso global
_settings: Settings | None = None


def get_settings() -> Settings:
    """Obtener instancia única de Settings (singleton)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
