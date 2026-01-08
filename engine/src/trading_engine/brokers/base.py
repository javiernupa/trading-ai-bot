"""Broker base para ejecución de órdenes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..models import Order, Position


class BaseBroker(ABC):
    """Interfaz base para brokers."""

    @abstractmethod
    def connect(self) -> bool:
        """Conecta con el broker.

        Returns:
            True si la conexión fue exitosa
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Desconecta del broker."""
        pass

    @abstractmethod
    def get_account_info(self) -> dict[str, Any]:
        """Obtiene información de la cuenta.

        Returns:
            Diccionario con información de la cuenta
        """
        pass

    @abstractmethod
    def get_buying_power(self) -> float:
        """Obtiene el poder de compra disponible.

        Returns:
            Poder de compra en USD
        """
        pass

    @abstractmethod
    def get_positions(self) -> dict[str, Position]:
        """Obtiene las posiciones actuales.

        Returns:
            Diccionario de posiciones por símbolo
        """
        pass

    @abstractmethod
    def submit_order(self, order: Order) -> str:
        """Envía una orden al broker.

        Args:
            order: Orden a enviar

        Returns:
            ID de la orden
        """
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancela una orden.

        Args:
            order_id: ID de la orden a cancelar

        Returns:
            True si se canceló exitosamente
        """
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> dict[str, Any]:
        """Obtiene el estado de una orden.

        Args:
            order_id: ID de la orden

        Returns:
            Diccionario con información de la orden
        """
        pass

    @abstractmethod
    def get_open_orders(self) -> dict[str, list[str]]:
        """Obtiene todas las órdenes abiertas organizadas por símbolo.

        Returns:
            Diccionario con símbolos como claves y listas de order IDs como valores
        """
        pass
