"""Cálculo de métricas de rendimiento."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .models import BacktestResult, Trade


class MetricsCalculator:
    """Calcula métricas de rendimiento del backtesting."""

    @staticmethod
    def calculate_metrics(
        trades: list[Trade],
        equity_curve: list[tuple[pd.Timestamp, float]],
        initial_capital: float,
        total_commission: float,
    ) -> BacktestResult:
        """Calcula todas las métricas del backtest.

        Args:
            trades: Lista de trades completados
            equity_curve: Curva de equity histórica
            initial_capital: Capital inicial
            total_commission: Comisión total pagada

        Returns:
            BacktestResult con todas las métricas calculadas
        """
        if not trades:
            return BacktestResult(
                total_pnl=0.0,
                total_return_percent=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0,
                max_drawdown_percent=0.0,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0.0,
                average_win=0.0,
                average_loss=0.0,
                profit_factor=0.0,
                initial_capital=initial_capital,
                final_capital=initial_capital,
                total_commission=0.0,
                trades=[],
            )

        # Convertir equity curve a DataFrame
        df_equity = pd.DataFrame(equity_curve, columns=["timestamp", "equity"])
        df_equity.set_index("timestamp", inplace=True)

        final_capital = df_equity["equity"].iloc[-1] if len(df_equity) > 0 else initial_capital

        # Métricas básicas
        total_pnl = sum(trade.pnl for trade in trades)
        total_return_percent = ((final_capital - initial_capital) / initial_capital) * 100

        # Trade statistics
        winning_trades = [t for t in trades if t.is_winner]
        losing_trades = [t for t in trades if not t.is_winner]

        win_rate = (len(winning_trades) / len(trades)) * 100 if trades else 0
        average_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        average_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0

        # Profit factor
        total_wins = sum(t.pnl for t in winning_trades)
        total_losses = abs(sum(t.pnl for t in losing_trades))
        profit_factor = total_wins / total_losses if total_losses > 0 else float("inf")

        # Sharpe ratio
        sharpe_ratio = MetricsCalculator._calculate_sharpe_ratio(df_equity)

        # Maximum drawdown
        max_drawdown, max_drawdown_percent = MetricsCalculator._calculate_max_drawdown(df_equity)

        return BacktestResult(
            total_pnl=total_pnl,
            total_return_percent=total_return_percent,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_percent=max_drawdown_percent,
            total_trades=len(trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            win_rate=win_rate,
            average_win=average_win,
            average_loss=average_loss,
            profit_factor=profit_factor,
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_commission=total_commission,
            trades=trades,
            equity_curve=df_equity,
        )

    @staticmethod
    def _calculate_sharpe_ratio(
        equity_curve: pd.DataFrame, risk_free_rate: float = 0.0, periods_per_year: int = 252
    ) -> float:
        """Calcula el Sharpe ratio.

        Args:
            equity_curve: DataFrame con la curva de equity
            risk_free_rate: Tasa libre de riesgo anualizada
            periods_per_year: Número de períodos por año (252 para días de trading)

        Returns:
            Sharpe ratio anualizado
        """
        if len(equity_curve) < 2:
            return 0.0

        # Calcular retornos
        returns = equity_curve["equity"].pct_change().dropna()

        if len(returns) == 0 or returns.std() == 0:
            return 0.0

        # Sharpe ratio = (retorno promedio - tasa libre riesgo) / desviación estándar
        excess_returns = returns - (risk_free_rate / periods_per_year)
        sharpe = excess_returns.mean() / returns.std()

        # Anualizar
        return sharpe * np.sqrt(periods_per_year)

    @staticmethod
    def _calculate_max_drawdown(equity_curve: pd.DataFrame) -> tuple[float, float]:
        """Calcula el maximum drawdown.

        Args:
            equity_curve: DataFrame con la curva de equity

        Returns:
            Tupla con (max_drawdown_absoluto, max_drawdown_porcentaje)
        """
        if len(equity_curve) == 0:
            return 0.0, 0.0

        equity = equity_curve["equity"]

        # Calcular running maximum
        running_max = equity.expanding().max()

        # Calcular drawdown
        drawdown = equity - running_max
        max_drawdown = drawdown.min()

        # Drawdown en porcentaje
        drawdown_percent = (drawdown / running_max) * 100
        max_drawdown_percent = drawdown_percent.min()

        return abs(max_drawdown), abs(max_drawdown_percent)

    @staticmethod
    def print_summary(result: BacktestResult) -> None:
        """Imprime un resumen formateado de los resultados.

        Args:
            result: Resultados del backtesting
        """
        print("\n" + "=" * 60)
        print("BACKTEST RESULTS SUMMARY".center(60))
        print("=" * 60)

        print("\n📊 PERFORMANCE METRICS")
        print("-" * 60)
        print(f"Initial Capital:        ${result.initial_capital:>15,.2f}")
        print(f"Final Capital:          ${result.final_capital:>15,.2f}")
        print(f"Total PnL:              ${result.total_pnl:>15,.2f}")
        print(f"Total Return:           {result.total_return_percent:>14.2f}%")
        print(f"Sharpe Ratio:           {result.sharpe_ratio:>18.2f}")
        print(f"Max Drawdown:           {result.max_drawdown_percent:>14.2f}%")
        print(f"Total Commission:       ${result.total_commission:>15,.2f}")

        print("\n📈 TRADE STATISTICS")
        print("-" * 60)
        print(f"Total Trades:           {result.total_trades:>18}")
        print(f"Winning Trades:         {result.winning_trades:>18}")
        print(f"Losing Trades:          {result.losing_trades:>18}")
        print(f"Win Rate:               {result.win_rate:>14.2f}%")
        print(f"Average Win:            ${result.average_win:>15,.2f}")
        print(f"Average Loss:           ${result.average_loss:>15,.2f}")
        print(f"Profit Factor:          {result.profit_factor:>18.2f}")

        print("\n" + "=" * 60 + "\n")
