"""Broker para Alpaca Markets."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from loguru import logger

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.enums import OrderSide as AlpacaOrderSide
    from alpaca.trading.enums import OrderType as AlpacaOrderType
    from alpaca.trading.enums import TimeInForce
    from alpaca.trading.requests import (
        MarketOrderRequest,
        StopLossRequest,
        TakeProfitRequest,
    )

    ALPACA_AVAILABLE = True
except ImportError:
    ALPACA_AVAILABLE = False
    logger.warning("alpaca-py no está instalado. Instala con: pip install alpaca-py")

from ..models import Order, OrderSide, OrderType, Position
from .base import BaseBroker


class AlpacaBroker(BaseBroker):
    """Broker para operar con Alpaca Markets."""

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        paper: bool = True,
    ):
        """Inicializa el broker de Alpaca.

        Args:
            api_key: API key de Alpaca
            secret_key: Secret key de Alpaca
            paper: Si usar paper trading (default: True)
        """
        if not ALPACA_AVAILABLE:
            raise ImportError("alpaca-py no está disponible")

        self.api_key = api_key
        self.secret_key = secret_key
        self.paper = paper
        self.client: TradingClient | None = None

    def connect(self) -> bool:
        """Conecta con Alpaca.

        Returns:
            True si la conexión fue exitosa
        """
        try:
            self.client = TradingClient(
                api_key=self.api_key,
                secret_key=self.secret_key,
                paper=self.paper,
            )

            # Verificar conexión obteniendo info de cuenta
            account = self.client.get_account()
            mode = "PAPER" if self.paper else "LIVE"
            logger.success(
                f"Conectado a Alpaca ({mode}) | "
                f"Capital: ${float(account.equity):,.2f} | "
                f"Poder de compra: ${float(account.buying_power):,.2f}"
            )
            return True

        except Exception as e:
            logger.error(f"Error conectando a Alpaca: {e}")
            return False

    def disconnect(self) -> None:
        """Desconecta de Alpaca."""
        self.client = None
        logger.info("Desconectado de Alpaca")

    def get_account_info(self) -> dict[str, Any]:
        """Obtiene información de la cuenta.

        Returns:
            Diccionario con información de la cuenta
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        account = self.client.get_account()

        return {
            "account_number": account.account_number,
            "status": account.status,
            "currency": account.currency,
            "cash": float(account.cash),
            "portfolio_value": float(account.portfolio_value),
            "equity": float(account.equity),
            "buying_power": float(account.buying_power),
            "pattern_day_trader": account.pattern_day_trader,
            "trading_blocked": account.trading_blocked,
            "transfers_blocked": account.transfers_blocked,
            "account_blocked": account.account_blocked,
        }

    def get_buying_power(self) -> float:
        """Obtiene el poder de compra disponible.

        Returns:
            Poder de compra en USD
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        account = self.client.get_account()
        return float(account.buying_power)

    def get_positions(self) -> dict[str, Position]:
        """Obtiene las posiciones actuales.

        Returns:
            Diccionario de posiciones por símbolo (con formato normalizado para crypto)
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        positions = {}
        alpaca_positions = self.client.get_all_positions()

        for pos in alpaca_positions:
            # Normalizar símbolo: si es crypto (BTCUSD, ETHUSD), añadir barra para consistencia
            # pero en realidad lo mejor es mantener el formato de Alpaca (sin barra) internamente
            symbol = pos.symbol
            position = Position(
                symbol=symbol,
                quantity=float(pos.qty),
                entry_price=float(pos.avg_entry_price),
                current_price=float(pos.current_price),
                entry_time=datetime.now(),  # Alpaca no proporciona esto directamente
            )
            positions[symbol] = position

        return positions

    def submit_order(
        self,
        order: Order,
        stop_loss_pct: float | None = None,
        take_profit_pct: float | None = None,
    ) -> str:
        """Envía una orden a Alpaca con stop loss y take profit opcionales.

        Args:
            order: Orden a enviar
            stop_loss_pct: Porcentaje de stop loss (e.g., 0.02 = 2%)
            take_profit_pct: Porcentaje de take profit (e.g., 0.05 = 5%)

        Returns:
            ID de la orden en Alpaca
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        # Normalizar símbolo de crypto: eliminar barra para Alpaca API
        normalized_symbol = order.symbol.replace("/", "")
        
        # Convertir OrderSide a Alpaca OrderSide
        side = (
            AlpacaOrderSide.BUY if order.side == OrderSide.BUY else AlpacaOrderSide.SELL
        )

        # Por ahora solo soportamos órdenes de mercado
        if order.order_type != OrderType.MARKET:
            logger.warning(
                f"Solo se soportan órdenes MARKET, convirtiendo {order.order_type}"
            )

        # Detectar si es criptomoneda (símbolo original contenía '/' o símbolo termina en USD/USDT)
        is_crypto = "/" in order.symbol or normalized_symbol.endswith(("USD", "USDT"))
        
        # Para crypto usar GTC (Good Till Cancel), para acciones usar DAY
        time_in_force = TimeInForce.GTC if is_crypto else TimeInForce.DAY

        # Configurar stop loss y take profit si se proporcionan
        stop_loss = None
        take_profit = None

        # Nota: Stop Loss y Take Profit no están soportados para crypto en Alpaca
        if not is_crypto:
            if stop_loss_pct and side == AlpacaOrderSide.BUY:
                # Para compras, stop loss está por debajo del precio
                stop_price = order.price * (1 - stop_loss_pct)
                stop_loss = StopLossRequest(stop_price=stop_price)
                logger.debug(f"Stop Loss configurado en ${stop_price:.2f} ({stop_loss_pct:.1%})")

            if take_profit_pct and side == AlpacaOrderSide.BUY:
                # Para compras, take profit está por encima del precio
                limit_price = order.price * (1 + take_profit_pct)
                take_profit = TakeProfitRequest(limit_price=limit_price)
                logger.debug(f"Take Profit configurado en ${limit_price:.2f} ({take_profit_pct:.1%})")
        elif stop_loss_pct or take_profit_pct:
            logger.warning(f"{order.symbol}: Stop Loss y Take Profit no soportados para crypto")

        order_request = MarketOrderRequest(
            symbol=normalized_symbol,  # Usar símbolo normalizado sin barra
            qty=order.quantity,
            side=side,
            time_in_force=time_in_force,
            stop_loss=stop_loss,
            take_profit=take_profit,
        )

        try:
            alpaca_order = self.client.submit_order(order_request)
            
            order_info = (
                f"Orden enviada a Alpaca: {side.value} {order.quantity} {order.symbol} "
                f"@ Market (${order.price:.2f})"
            )
            if stop_loss:
                order_info += f" | SL: ${stop_price:.2f}"
            if take_profit:
                order_info += f" | TP: ${limit_price:.2f}"
            order_info += f" | ID: {alpaca_order.id}"
            
            logger.info(order_info)
            
            # Verificar si hay órdenes de legs (stop loss y take profit)
            if hasattr(alpaca_order, 'legs') and alpaca_order.legs:
                logger.info(f"  📎 Órdenes asociadas (legs):")
                for leg in alpaca_order.legs:
                    leg_type = leg.order_type if hasattr(leg, 'order_type') else 'unknown'
                    leg_id = leg.id if hasattr(leg, 'id') else 'unknown'
                    logger.info(f"     • {leg_type}: ID {leg_id}")
            elif stop_loss or take_profit:
                logger.warning(f"  ⚠️ Stop Loss/Take Profit configurados pero no se crearon órdenes legs")
            
            return str(alpaca_order.id)

        except Exception as e:
            logger.error(f"Error enviando orden a Alpaca: {e}")
            raise

    def cancel_order(self, order_id: str) -> bool:
        """Cancela una orden en Alpaca.

        Args:
            order_id: ID de la orden a cancelar

        Returns:
            True si se canceló exitosamente
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        try:
            self.client.cancel_order_by_id(order_id)
            logger.info(f"Orden {order_id} cancelada")
            return True

        except Exception as e:
            logger.error(f"Error cancelando orden {order_id}: {e}")
            return False

    def get_order_status(self, order_id: str) -> dict[str, Any]:
        """Obtiene el estado de una orden.

        Args:
            order_id: ID de la orden

        Returns:
            Diccionario con información de la orden
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        try:
            order = self.client.get_order_by_id(order_id)

            return {
                "id": str(order.id),
                "symbol": order.symbol,
                "side": order.side.value,
                "type": order.type.value,
                "qty": float(order.qty),
                "filled_qty": float(order.filled_qty),
                "status": order.status.value,
                "created_at": order.created_at,
                "filled_at": order.filled_at,
                "filled_avg_price": float(order.filled_avg_price)
                if order.filled_avg_price
                else None,
            }

        except Exception as e:
            logger.error(f"Error obteniendo estado de orden {order_id}: {e}")
            raise

    def get_open_orders(self) -> dict[str, list[str]]:
        """Obtiene todas las órdenes abiertas organizadas por símbolo.

        Returns:
            Diccionario con símbolos como claves y listas de order IDs como valores
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        try:
            from alpaca.trading.requests import GetOrdersRequest
            from alpaca.trading.enums import QueryOrderStatus
            
            # Crear request para obtener solo órdenes abiertas
            request = GetOrdersRequest(
                status=QueryOrderStatus.OPEN,
                limit=100
            )
            
            orders = self.client.get_orders(filter=request)
            
            open_orders = {}
            for order in orders:
                symbol = order.symbol
                if symbol not in open_orders:
                    open_orders[symbol] = []
                open_orders[symbol].append(str(order.id))
            
            return open_orders

        except Exception as e:
            logger.error(f"Error obteniendo órdenes abiertas: {e}")
            return {}

    def close_all_positions(self) -> bool:
        """Cierra todas las posiciones abiertas.

        Returns:
            True si se cerraron todas exitosamente
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        try:
            self.client.close_all_positions(cancel_orders=True)
            logger.warning("Cerrando TODAS las posiciones en Alpaca")
            return True

        except Exception as e:
            logger.error(f"Error cerrando posiciones: {e}")
            return False

    def close_position(self, symbol: str) -> bool:
        """Cierra una posición específica.

        Args:
            symbol: Símbolo a cerrar

        Returns:
            True si se cerró exitosamente
        """
        if not self.client:
            raise RuntimeError("No conectado a Alpaca")

        try:
            self.client.close_position(symbol)
            logger.info(f"Cerrando posición de {symbol}")
            return True

        except Exception as e:
            logger.error(f"Error cerrando posición de {symbol}: {e}")
            return False
