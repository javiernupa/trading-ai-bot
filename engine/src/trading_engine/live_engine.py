"""Motor de trading en vivo para múltiples símbolos."""

from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from loguru import logger

from .brokers.alpaca_broker import AlpacaBroker
from .data.alpaca_provider import AlpacaDataProvider
from .models import Order, OrderSide, OrderStatus, OrderType
from .strategy_interface import Strategy


class MultiSymbolLiveEngine:
    """Motor de trading en vivo para múltiples símbolos."""

    def __init__(
        self,
        symbols: list[str],
        strategy: Strategy,
        broker: AlpacaBroker,
        data_provider: AlpacaDataProvider,
        initial_capital: float = 100000,
        capital_per_symbol: float = 10000,
        update_interval: int = 60,
        lookback_days: int = 100,
        timeframe: str = "1Day",  # Timeframe para descarga de datos
        stop_loss_pct: float | None = 0.02,  # 2% por defecto
        take_profit_pct: float | None = 0.05,  # 5% por defecto
    ):
        """Inicializa el motor de trading en vivo.

        Args:
            symbols: Lista de símbolos a operar
            strategy: Estrategia a usar
            broker: Broker para ejecutar órdenes
            data_provider: Proveedor de datos
            initial_capital: Capital inicial para calcular rendimiento
            capital_per_symbol: Capital asignado por símbolo
            update_interval: Intervalo de actualización en segundos
            lookback_days: Días de historial para calcular indicadores
            timeframe: Timeframe de las barras (1Min, 5Min, 1Hour, 1Day)
            stop_loss_pct: Porcentaje de stop loss (None para desactivar)
            take_profit_pct: Porcentaje de take profit (None para desactivar)
        """
        self.symbols = symbols
        self.strategy = strategy
        self.broker = broker
        self.data_provider = data_provider
        self.initial_capital = initial_capital
        self.capital_per_symbol = capital_per_symbol
        self.update_interval = update_interval
        self.lookback_days = lookback_days
        self.timeframe = timeframe
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct

        self.running = False
        self.historical_data: dict[str, pd.DataFrame] = {}
        self.positions: dict[str, Any] = {}
        self.pending_orders: dict[str, list[str]] = {}  # symbol -> [order_ids]
        self.stop_loss_sales: dict[str, datetime] = {}  # symbol -> timestamp de última venta por SL
        
        # Leer orden de estrategias desde .env para display ordenado
        active_str = os.getenv('ACTIVE_STRATEGIES', '')
        self.active_strategies_order = [s.strip().upper() for s in active_str.split(',') if s.strip()]
        
        # Calcular número de barras a mantener según timeframe
        self._bars_to_keep = self._calculate_bars_to_keep()

        risk_info = ""
        if stop_loss_pct:
            risk_info += f", SL: {stop_loss_pct:.1%}"
        if take_profit_pct:
            risk_info += f", TP: {take_profit_pct:.1%}"

        logger.info(
            f"Motor en vivo inicializado: {len(symbols)} símbolos, "
            f"Capital inicial: ${initial_capital:,.2f}, "
            f"${capital_per_symbol:,.0f} por símbolo{risk_info}"
        )

    def _calculate_bars_to_keep(self) -> int:
        """Calcula el número de barras a mantener según el timeframe.
        
        Returns:
            Número de barras que cubren el lookback_days configurado
        """
        # Mapear timeframe a barras por día
        bars_per_day = {
            "1Min": 390,    # 6.5 horas de mercado (stocks) / 1440 para crypto 24/7
            "2Min": 195,
            "5Min": 78,
            "10Min": 39,
            "15Min": 26,
            "30Min": 13,
            "1Hour": 24,    # 24 horas para crypto
            "2Hour": 12,
            "4Hour": 6,
            "6Hour": 4,
            "12Hour": 2,
            "1Day": 1,
            "1Week": 1/7,   # ~0.14 barras por día
            "1Month": 1/30, # ~0.03 barras por día
        }
        
        multiplier = bars_per_day.get(self.timeframe, 1)
        total_bars = self.lookback_days * multiplier
        
        # Asegurar mínimo de barras necesarias para indicadores
        min_required = 50  # Mínimo razonable para cualquier estrategia
        
        return max(total_bars, min_required)

    def start(self) -> None:
        """Inicia el motor de trading en vivo."""
        logger.info("=" * 60)
        logger.info("INICIANDO MOTOR DE TRADING EN VIVO")
        logger.info("=" * 60)

        # Conectar al broker
        if not self.broker.connect():
            logger.error("No se pudo conectar al broker. Abortando.")
            return

        # Verificar cuenta
        account = self.broker.get_account_info()
        logger.info(f"Cuenta: {account['account_number']}")
        logger.info(f"Capital disponible: ${account['buying_power']:,.2f}")
        logger.info(f"Símbolos a operar: {', '.join(self.symbols)}")

        # Cargar datos históricos iniciales
        logger.info("\nCargando datos históricos iniciales...")
        self._load_historical_data()

        # Obtener posiciones actuales
        self.positions = self.broker.get_positions()
        if self.positions:
            logger.info(f"\nPosiciones actuales: {len(self.positions)}")
            for symbol, pos in self.positions.items():
                logger.info(
                    f"  {symbol}: {pos.quantity:.2f} @ ${pos.entry_price:.2f} "
                    f"(Current: ${pos.current_price:.2f})"
                )

        self.running = True
        logger.success("\n✓ Motor iniciado correctamente\n")

        # Loop principal
        try:
            self._run_loop()
        except KeyboardInterrupt:
            logger.warning("\n⚠ Interrupción detectada, deteniendo...")
        finally:
            self.stop()

    def stop(self) -> None:
        """Detiene el motor de trading."""
        logger.info("\nDeteniendo motor de trading...")
        self.running = False

        # Mostrar resumen final
        self._show_summary()

        self.broker.disconnect()
        logger.success("Motor detenido correctamente")

    def _load_historical_data(self) -> None:
        """Carga datos históricos para todos los símbolos."""
        end_date = datetime.now()
        start_date = end_date - pd.Timedelta(days=self.lookback_days)

        for symbol in self.symbols:
            try:
                data = self.data_provider.fetch_data(
                    symbol=symbol,
                    start_date=start_date,
                    end_date=end_date,
                    timeframe=self.timeframe,  # Usar el timeframe configurado
                )
                self.historical_data[symbol] = data
                logger.info(f"  ✓ {symbol}: {len(data)} barras cargadas")

            except Exception as e:
                logger.error(f"  ✗ {symbol}: Error cargando datos - {e}")
                self.symbols.remove(symbol)  # Remover símbolo problemático

    def _run_loop(self) -> None:
        """Loop principal de trading."""
        iteration = 0

        while self.running:
            iteration += 1
            logger.info(f"\n{'=' * 60}")
            logger.info(f"ITERACIÓN {iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"{'=' * 60}")

            # Actualizar posiciones desde el broker al inicio de cada iteración
            try:
                self.positions = self.broker.get_positions()
                logger.debug(f"Posiciones actualizadas: {len(self.positions)} abiertas")
            except Exception as e:
                logger.error(f"Error actualizando posiciones: {e}")

            # Sincronizar órdenes pendientes desde Alpaca
            try:
                self.pending_orders = self.broker.get_open_orders()
                if self.pending_orders:
                    total_pending = sum(len(orders) for orders in self.pending_orders.values())
                    logger.info(f"⏳ Órdenes pendientes: {total_pending} órdenes en {len(self.pending_orders)} símbolos")
                    for sym, orders in self.pending_orders.items():
                        logger.info(f"   • {sym}: {len(orders)} orden(es) - IDs: {orders}")
            except Exception as e:
                logger.error(f"Error sincronizando órdenes pendientes: {e}")

            # Actualizar datos y generar señales
            for symbol in self.symbols:
                try:
                    self._process_symbol(symbol)
                except Exception as e:
                    logger.error(f"Error procesando {symbol}: {e}")

            # Verificar órdenes pendientes
            self._check_pending_orders()

            # Mostrar estado actual
            self._show_status()

            # Esperar hasta la próxima iteración
            if self.running:
                logger.info(f"\nEsperando {self.update_interval} segundos...")
                time.sleep(self.update_interval)

    def _process_symbol(self, symbol: str) -> None:
        """Procesa un símbolo: actualiza datos y genera señales.

        Args:
            symbol: Símbolo a procesar
        """
        # Normalizar símbolo para crypto (sin barra) para coincidir con Alpaca
        normalized_symbol = symbol.replace("/", "")
        
        # Obtener barra más reciente
        try:
            latest_bar = self.data_provider.fetch_latest_bar(symbol)

            # Añadir a datos históricos
            new_row = pd.DataFrame([latest_bar])
            self.historical_data[symbol] = pd.concat(
                [self.historical_data[symbol], new_row], ignore_index=True
            )

            # Mantener solo las últimas barras según timeframe
            self.historical_data[symbol] = self.historical_data[symbol].tail(
                self._bars_to_keep
            )

        except Exception as e:
            logger.warning(f"{symbol}: No se pudo actualizar datos - {e}")
            return

        # Verificar que tenemos suficientes datos para los indicadores
        min_data_required = max(
            self.strategy.rsi_period if hasattr(self.strategy, 'rsi_period') else 14,
            self.strategy.macd_slow if hasattr(self.strategy, 'macd_slow') else 26,
            self.strategy.bb_period if hasattr(self.strategy, 'bb_period') else 20,
        ) + 10  # Buffer adicional para cálculos
        
        if len(self.historical_data[symbol]) < min_data_required:
            logger.warning(
                f"{symbol}: Datos insuficientes ({len(self.historical_data[symbol])} / {min_data_required} requeridos). "
                "Esperando más datos históricos..."
            )
            return

        # Generar señales con la estrategia
        data_with_signals = self.strategy.generate_signals(self.historical_data[symbol])
        latest_signal = data_with_signals.iloc[-1]["signal"]

        current_price = float(latest_bar["close"])

        # Logging detallado de indicadores
        last_row = data_with_signals.iloc[-1]
        logger.info(f"{symbol}: Analizando @ ${current_price:.2f}")
        
        # Mostrar señales individuales de cada estrategia
        strategy_signals = []
        signal_symbols = {1: "⬆️ +1", 0: "➡️  0", -1: "⬇️ -1"}
        
        for col in last_row.index:
            # Solo procesar columnas que son señales de estrategia con formato exacto: *strategy_N_signal
            # Debe cumplir: terminar en _signal Y tener el patrón strategy_[número]_signal
            if col.endswith("_signal") and "strategy_" in col:
                # Verificar que el formato es correcto: debe ser *strategy_{numero}_signal
                # No debe tener nada después de _signal (como macdstrategy_1_macd_signal)
                parts = col.split("_")
                # El formato correcto es: ...strategy_N_signal (al menos 3 partes y penúltima es número)
                if len(parts) >= 3 and parts[-1] == "signal" and parts[-2].isdigit():
                    # Extraer nombre de estrategia (ej: macdstrategy_0_signal -> MACDSTRATEGY_0)
                    strategy_full_name = col.replace("_signal", "").upper()
                    
                    # Simplificar nombre base
                    strategy_base = strategy_full_name
                    if "RSISTRATEGY" in strategy_base:
                        strategy_base = "RSI"
                    elif "MACDSTRATEGY" in strategy_base:
                        strategy_base = "MACD"
                    elif "BOLLINGERBANDSSTRATEGY" in strategy_base:
                        strategy_base = "BB"
                    elif "ELLIOTTWAVESSTRATEGY" in strategy_base:
                        strategy_base = "EW"
                    elif "ICHIMOKUSTRATEGY" in strategy_base:
                        strategy_base = "ICHIMOKU"
                    elif "MA50STRATEGY" in strategy_base:
                        strategy_base = "MA50"
                    elif "MA200STRATEGY" in strategy_base:
                        strategy_base = "MA200"
                    elif "STOCHASTICSTRATEGY" in strategy_base:
                        strategy_base = "STOCH"
                    elif "PARABOLICSARSTRATEGY" in strategy_base:
                        strategy_base = "PSAR"
                    elif "EMASTRATEGY" in strategy_base:
                        strategy_base = "EMA"
                    elif "SMASTRATEGY" in strategy_base:
                        strategy_base = "SMA"
                    elif "OBVSTRATEGY" in strategy_base:
                        strategy_base = "OBV"
                    else:
                        # Si no se reconoce, mantener el nombre completo
                        strategy_base = strategy_full_name
                    
                    signal_value = int(last_row[col])
                    signal_display = signal_symbols.get(signal_value, f"{signal_value}")
                    
                    # Si hay múltiples instancias, agregar el índice extraído del nombre original
                    if "_" in strategy_full_name:
                        # Extraer el índice (ej: MACDSTRATEGY_0 -> 0)
                        idx_parts = strategy_full_name.split("_")
                        if len(idx_parts) >= 2 and idx_parts[-1].isdigit():
                            idx = idx_parts[-1]
                            display_name = f"{strategy_base}_{idx}"
                        else:
                            display_name = strategy_base
                    else:
                        display_name = strategy_base
                    
                    strategy_signals.append((display_name, signal_display))
        
        # Ordenar señales según el orden de ACTIVE_STRATEGIES
        def get_strategy_order(signal_tuple):
            """Retorna el índice de orden según ACTIVE_STRATEGIES."""
            strategy_name = signal_tuple[0].split('_')[0]  # Extraer nombre base sin índice
            try:
                return self.active_strategies_order.index(strategy_name)
            except ValueError:
                # Si no está en la lista, ponerlo al final
                return len(self.active_strategies_order)
        
        strategy_signals.sort(key=get_strategy_order)
        
        # Verificar si hay duplicados y agregar índice solo cuando sea necesario
        final_signals = []
        for display_name, signal_display in strategy_signals:
            base = display_name.rsplit("_", 1)[0] if "_" in display_name else display_name
            count = sum(1 for name, _ in strategy_signals if name.startswith(base))
            
            # Si hay más de una instancia de esta estrategia, mantener el índice
            if count > 1:
                final_signals.append(f"{display_name}: {signal_display}")
            else:
                # Si solo hay una, quitar el índice
                final_signals.append(f"{base}: {signal_display}")
        
        if final_signals:
            logger.info("  📊 Señales individuales:")
            for signal in final_signals:
                logger.info(f"     {signal}")
        
        # Mostrar votos de consenso
        if "buy_votes" in last_row and "sell_votes" in last_row:
            logger.info(f"  💡 Consenso: Compra {int(last_row['buy_votes'])} | Venta {int(last_row['sell_votes'])} | Señal Final: {latest_signal}")

        # Verificar si tenemos posición (usar símbolo normalizado para crypto)
        has_position = normalized_symbol in self.positions or symbol in self.positions
        
        # Verificar si hay órdenes pendientes para este símbolo (usar normalizado)
        has_pending_orders = (normalized_symbol in self.pending_orders and len(self.pending_orders[normalized_symbol]) > 0) or \
                            (symbol in self.pending_orders and len(self.pending_orders[symbol]) > 0)
        
        if has_pending_orders:
            # Obtener IDs de órdenes pendientes (puede estar en cualquiera de los dos formatos)
            pending_ids = self.pending_orders.get(normalized_symbol, []) + self.pending_orders.get(symbol, [])
            logger.info(f"  ⏸️  {symbol}: Orden pendiente detectada - esperando ejecución (IDs: {pending_ids})")

        # Lógica de trading mejorada
        if has_position and not has_pending_orders:
            # Tenemos posición: verificar condiciones de venta
            position = self.positions.get(normalized_symbol) or self.positions.get(symbol)
            
            if position:
                # Usar el precio actual del broker (tiempo real) en lugar del histórico
                current_price = position.current_price if position.current_price else current_price
                
                # Calcular niveles de Stop Loss y Take Profit
                stop_loss_price = position.entry_price * (1 - self.stop_loss_pct) if self.stop_loss_pct else None
                take_profit_price = position.entry_price * (1 + self.take_profit_pct) if self.take_profit_pct else None
                
                # Condiciones de venta mejoradas:
                # 1. Stop Loss alcanzado → VENDE SIEMPRE (protección obligatoria)
                stop_loss_hit = stop_loss_price and current_price <= stop_loss_price
                
                # 2. Take Profit alcanzado → Solo si hay señal de venta (dejar correr ganancias)
                take_profit_hit = take_profit_price and current_price >= take_profit_price
                
                # 3. Señal de venta con confirmación
                signal_sell_valid = latest_signal == -1 and (stop_loss_hit or take_profit_hit)
                
                # Vender si:
                # - SL alcanzado (siempre, sin importar señal)
                # - Señal de venta + (SL o TP alcanzado)
                should_sell = stop_loss_hit or signal_sell_valid
                
                if should_sell:
                    reason = []
                    if stop_loss_hit:
                        reason.append(f"🛡️ Stop Loss (${stop_loss_price:.2f})")
                        # Registrar venta por SL para bloquear recompra por 1 hora
                        self.stop_loss_sales[symbol] = datetime.now()
                        self.stop_loss_sales[normalized_symbol] = datetime.now()
                    if take_profit_hit and latest_signal == -1:
                        reason.append(f"🎯 Take Profit (${take_profit_price:.2f})")
                    if latest_signal == -1:
                        # Mencionar señal
                        reason.append("📉 Señal de venta por consenso")
                    
                    logger.info(f"  🔴 {symbol}: Ejecutando VENTA - {' + '.join(reason)}")
                    self._execute_sell(symbol, current_price)
                elif latest_signal == -1:
                    # Señal de venta pero no se cumplen condiciones de SL/TP
                    pnl = (current_price - position.entry_price) * position.quantity
                    pnl_pct = (current_price / position.entry_price - 1) * 100
                    sl_display = f"${stop_loss_price:.2f}" if stop_loss_price else "N/A"
                    tp_display = f"${take_profit_price:.2f}" if take_profit_price else "N/A"
                    logger.warning(
                        f"  ⚠️  {symbol}: Señal de VENTA por consenso detectada pero IGNORADA | "
                        f"Precio actual: ${current_price:.2f} | "
                        f"SL: {sl_display} | "
                        f"TP: {tp_display} | "
                        f"PnL actual: ${pnl:,.2f} ({pnl_pct:+.2f}%)"
                    )
                elif take_profit_hit:
                    # TP alcanzado pero NO hay señal de venta → Dejar correr ganancias
                    pnl = (current_price - position.entry_price) * position.quantity
                    pnl_pct = (current_price / position.entry_price - 1) * 100
                    logger.success(
                        f"  🚀 {symbol}: TP ALCANZADO pero SIN señal de venta → Dejando correr ganancias | "
                        f"Precio actual: ${current_price:.2f} | "
                        f"TP objetivo: ${take_profit_price:.2f} | "
                        f"PnL actual: ${pnl:,.2f} ({pnl_pct:+.2f}%)"
                    )
        
        elif latest_signal == 1 and not has_position and not has_pending_orders:
            # Verificar si hubo venta por SL en la última hora
            sl_sale_time = self.stop_loss_sales.get(symbol) or self.stop_loss_sales.get(normalized_symbol)
            if sl_sale_time:
                hours_since_sl = (datetime.now() - sl_sale_time).total_seconds() / 3600
                if hours_since_sl < 1.0:
                    logger.warning(
                        f"  🚫 {symbol}: Compra BLOQUEADA - Venta por Stop Loss hace {hours_since_sl*60:.0f} minutos | "
                        f"Se requiere esperar {(1-hours_since_sl)*60:.0f} minutos más"
                    )
                    return
                else:
                    # Limpiar registro si ya pasó la hora
                    self.stop_loss_sales.pop(symbol, None)
                    self.stop_loss_sales.pop(normalized_symbol, None)
            
            # Señal de compra y no tenemos posición ni órdenes pendientes
            self._execute_buy(symbol, current_price)
        
        elif has_pending_orders:
            # Ya logueado arriba
            pass

        else:
            logger.debug(f"{symbol}: Sin acción (Signal: {latest_signal}, Position: {has_position})")

    def _execute_buy(self, symbol: str, price: float) -> None:
        """Ejecuta una orden de compra.

        Args:
            symbol: Símbolo a comprar
            price: Precio actual
        """
        # Normalizar símbolo para órdenes
        normalized_symbol = symbol.replace("/", "")
        
        # Detectar si es crypto (contiene barra o símbolo normalizado termina en USD/USDT)
        is_crypto = "/" in symbol or normalized_symbol.endswith(("USD", "USDT"))
        
        # Calcular cantidad basada en capital asignado
        if is_crypto:
            # Para crypto: permitir decimales (puedes comprar 0.05 BTC)
            quantity = round(self.capital_per_symbol / price, 8)  # 8 decimales para precisión
            min_quantity = 0.0001  # Cantidad mínima para crypto
        else:
            # Para acciones: solo enteros
            quantity = int(self.capital_per_symbol / price)
            min_quantity = 1

        if quantity < min_quantity:
            logger.warning(
                f"{symbol}: Capital insuficiente para comprar "
                f"(${self.capital_per_symbol} / ${price:.2f} = {quantity:.8f}, mínimo: {min_quantity})"
            )
            return

        # Crear orden
        order = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=quantity,
            price=price,
            timestamp=datetime.now(),
            status=OrderStatus.PENDING,
        )

        try:
            # Enviar orden al broker con stop loss y take profit
            order_id = self.broker.submit_order(
                order,
                stop_loss_pct=self.stop_loss_pct,
                take_profit_pct=self.take_profit_pct,
            )

            # Guardar como pendiente (usar símbolo normalizado para consistencia)
            if normalized_symbol not in self.pending_orders:
                self.pending_orders[normalized_symbol] = []
            self.pending_orders[normalized_symbol].append(order_id)

            # Calcular niveles
            stop_loss_price = price * (1 - self.stop_loss_pct) if self.stop_loss_pct else None
            take_profit_price = price * (1 + self.take_profit_pct) if self.take_profit_pct else None

            log_msg = (
                f"🟢 {symbol}: COMPRA {quantity} @ ${price:.2f} "
                f"(Total: ${quantity * price:,.2f})"
            )
            if stop_loss_price:
                log_msg += f" | 🛡️ SL: ${stop_loss_price:.2f}"
            if take_profit_price:
                log_msg += f" | 🎯 TP: ${take_profit_price:.2f}"
            log_msg += f" | Order ID: {order_id}"

            logger.info(log_msg)

        except Exception as e:
            logger.error(f"{symbol}: Error ejecutando compra - {e}")

    def _execute_sell(self, symbol: str, price: float) -> None:
        """Ejecuta una orden de venta.

        Args:
            symbol: Símbolo a vender
            price: Precio actual
        """
        # Normalizar símbolo para buscar posición
        normalized_symbol = symbol.replace("/", "")
        
        # Las posiciones ya están actualizadas al inicio del loop
        # Buscar en ambos formatos
        position = self.positions.get(normalized_symbol) or self.positions.get(symbol)
        if not position:
            logger.warning(f"{symbol}: No hay posición para vender")
            return

        quantity = position.quantity
        
        # Validar cantidad antes de enviar orden
        if quantity <= 0:
            logger.error(f"{symbol}: Cantidad inválida para venta: {quantity}")
            return

        # Crear orden
        order = Order(
            symbol=symbol,
            side=OrderSide.SELL,
            order_type=OrderType.MARKET,
            quantity=quantity,
            price=price,
            timestamp=datetime.now(),
            status=OrderStatus.PENDING,
        )

        try:
            # Enviar orden al broker
            order_id = self.broker.submit_order(order)

            # Guardar como pendiente (usar símbolo normalizado para consistencia)
            if normalized_symbol not in self.pending_orders:
                self.pending_orders[normalized_symbol] = []
            self.pending_orders[normalized_symbol].append(order_id)

            # Calcular PnL estimado
            pnl = (price - position.entry_price) * quantity
            pnl_pct = (price / position.entry_price - 1) * 100

            logger.info(
                f"🔴 {symbol}: VENTA {quantity:.2f} @ ${price:.2f} "
                f"(Entry: ${position.entry_price:.2f}) | "
                f"PnL: ${pnl:,.2f} ({pnl_pct:+.2f}%) | "
                f"Order ID: {order_id}"
            )
            
            # Eliminar posición ya que se vendió completamente
            del self.positions[symbol]

        except Exception as e:
            logger.error(f"{symbol}: Error ejecutando venta - {e}")

    def _check_pending_orders(self) -> None:
        """Verifica el estado de órdenes pendientes."""
        for symbol, order_ids in list(self.pending_orders.items()):
            for order_id in list(order_ids):
                try:
                    status = self.broker.get_order_status(order_id)

                    if status["status"] == "filled":
                        logger.success(
                            f"✓ {symbol}: Orden {order_id} ejecutada @ "
                            f"${status['filled_avg_price']:.2f}"
                        )
                        order_ids.remove(order_id)

                        # Actualizar posiciones
                        self.positions = self.broker.get_positions()

                    elif status["status"] in ["canceled", "expired", "rejected"]:
                        logger.warning(
                            f"✗ {symbol}: Orden {order_id} {status['status']}"
                        )
                        order_ids.remove(order_id)

                except Exception as e:
                    logger.error(f"Error verificando orden {order_id}: {e}")

            # Limpiar si no quedan órdenes
            if not order_ids:
                del self.pending_orders[symbol]

    def _show_status(self) -> None:
        """Muestra el estado actual del sistema."""
        account = self.broker.get_account_info()
        positions = self.broker.get_positions()
        
        # Calcular rendimiento desde el inicio
        current_capital = account['equity']
        total_gain_loss = current_capital - self.initial_capital
        total_gain_loss_pct = (current_capital / self.initial_capital - 1) * 100
        
        # Color para ganancia/pérdida total
        if total_gain_loss >= 0:
            performance_str = f"<green>+${total_gain_loss:,.2f} (+{total_gain_loss_pct:.2f}%)</green>"
        else:
            performance_str = f"<red>${total_gain_loss:,.2f} ({total_gain_loss_pct:.2f}%)</red>"

        logger.info("")
        logger.info("📊 ESTADO ACTUAL:")
        logger.info(f"  Capital Inicial: ${self.initial_capital:,.2f}")
        logger.opt(colors=True).info(f"  Capital Actual: ${current_capital:,.2f} | Rendimiento: {performance_str}")
        logger.info(f"  Cash disponible: ${account['cash']:,.2f}")
        logger.info(f"  Posiciones abiertas: {len(positions)}")

        if positions:
            logger.info("")
            logger.info("  💼 Detalle de posiciones:")
            logger.info(f"  {'─' * 135}")
            logger.info(f"  {'Símbolo':<10} {'Cant.':<10} {'Entrada':<12} {'SL':<12} {'TP':<12} {'Actual':<12} {'Valor Pos.':<16} {'PnL':<22}")
            logger.info(f"  {'─' * 135}")
            
            total_pnl = 0
            for symbol, pos in positions.items():
                pnl = (pos.current_price - pos.entry_price) * pos.quantity
                pnl_pct = (pos.current_price / pos.entry_price - 1) * 100
                total_pnl += pnl
                
                # Calcular valor total de la posición
                position_value = pos.current_price * pos.quantity
                
                # Calcular Stop Loss y Take Profit
                stop_loss = pos.entry_price * (1 - self.stop_loss_pct) if self.stop_loss_pct else None
                take_profit = pos.entry_price * (1 + self.take_profit_pct) if self.take_profit_pct else None
                
                # Formatear valores con anchos fijos
                symbol_str = f"{symbol:<10}"
                qty_str = f"{pos.quantity:<10.2f}"
                entry_str = f"${pos.entry_price:<11.2f}"
                sl_str = f"${stop_loss:<11.2f}" if stop_loss else f"{'N/A':<12}"
                tp_str = f"${take_profit:<11.2f}" if take_profit else f"{'N/A':<12}"
                current_str = f"${pos.current_price:<11.2f}"
                value_str = f"${position_value:>14,.2f}"
                
                # Colores para PnL: verde si ganancia, rojo si pérdida
                if pnl >= 0:
                    pnl_str = f"<green>+${pnl:>10,.2f} ({pnl_pct:+6.2f}%)</green>"
                else:
                    pnl_str = f"<red>${pnl:>11,.2f} ({pnl_pct:+6.2f}%)</red>"

                logger.opt(colors=True).info(
                    f"  {symbol_str} {qty_str} {entry_str} {sl_str} {tp_str} {current_str} {value_str}  {pnl_str}"
                )
            
            logger.info(f"  {'─' * 135}")
            
            # Color para PnL total
            if total_pnl >= 0:
                total_pnl_str = f"<green>+${total_pnl:>10,.2f}</green>"
            else:
                total_pnl_str = f"<red>${total_pnl:>11,.2f}</red>"
            
            logger.opt(colors=True).info(f"  {'Total PnL:':<106} {total_pnl_str}")

        if self.pending_orders:
            logger.info(f"  Órdenes pendientes: {sum(len(o) for o in self.pending_orders.values())}")

    def _show_summary(self) -> None:
        """Muestra resumen final."""
        logger.info("\n" + "=" * 60)
        logger.info("RESUMEN FINAL")
        logger.info("=" * 60)

        account = self.broker.get_account_info()
        positions = self.broker.get_positions()

        logger.info(f"Capital final: ${account['equity']:,.2f}")
        logger.info(f"Cash: ${account['cash']:,.2f}")
        logger.info(f"Posiciones abiertas: {len(positions)}")

        if positions:
            logger.warning("\n⚠ Hay posiciones abiertas:")
            for symbol, pos in positions.items():
                value = pos.quantity * pos.current_price
                logger.info(
                    f"  {symbol}: {pos.quantity:.2f} @ ${pos.current_price:.2f} "
                    f"(Valor: ${value:,.2f})"
                )
