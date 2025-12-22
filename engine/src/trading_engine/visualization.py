"""Utilidades para visualización de resultados de backtesting."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from trading_engine.models import BacktestResult

plt.style.use("seaborn-v0_8-darkgrid")


class BacktestVisualizer:
    """Clase para visualizar resultados de backtesting."""

    @staticmethod
    def plot_equity_curve(result: BacktestResult, save_path: str | None = None) -> None:
        """Grafica la curva de equity.

        Args:
            result: Resultados del backtesting
            save_path: Ruta opcional para guardar la imagen
        """
        if result.equity_curve is None or len(result.equity_curve) == 0:
            print("No hay datos de equity curve disponibles")
            return

        plt.figure(figsize=(14, 7))

        # Equity curve
        plt.plot(
            result.equity_curve.index,
            result.equity_curve["equity"],
            label="Equity",
            linewidth=2,
            color="green",
        )

        # Línea de capital inicial
        plt.axhline(
            y=result.initial_capital,
            color="gray",
            linestyle="--",
            label="Capital Inicial",
            alpha=0.7,
        )

        # Área sombreada de profit
        if result.final_capital > result.initial_capital:
            plt.fill_between(
                result.equity_curve.index,
                result.initial_capital,
                result.equity_curve["equity"],
                where=(result.equity_curve["equity"] > result.initial_capital),
                color="green",
                alpha=0.2,
            )
        else:
            plt.fill_between(
                result.equity_curve.index,
                result.initial_capital,
                result.equity_curve["equity"],
                where=(result.equity_curve["equity"] < result.initial_capital),
                color="red",
                alpha=0.2,
            )

        plt.title("Curva de Equity", fontsize=16, fontweight="bold")
        plt.xlabel("Fecha", fontsize=12)
        plt.ylabel("Equity ($)", fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Gráfica guardada en: {save_path}")

        plt.show()

    @staticmethod
    def plot_returns_distribution(
        result: BacktestResult, save_path: str | None = None
    ) -> None:
        """Grafica la distribución de retornos.

        Args:
            result: Resultados del backtesting
            save_path: Ruta opcional para guardar la imagen
        """
        if not result.trades:
            print("No hay trades para visualizar")
            return

        pnl_values = [trade.pnl for trade in result.trades]
        pnl_percent = [trade.pnl_percent for trade in result.trades]

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Histograma de PnL absoluto
        axes[0].hist(pnl_values, bins=30, color="steelblue", alpha=0.7, edgecolor="black")
        axes[0].axvline(x=0, color="red", linestyle="--", linewidth=2, label="Break-even")
        axes[0].set_title("Distribución de PnL", fontsize=14, fontweight="bold")
        axes[0].set_xlabel("PnL ($)", fontsize=11)
        axes[0].set_ylabel("Frecuencia", fontsize=11)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Histograma de PnL porcentual
        axes[1].hist(pnl_percent, bins=30, color="coral", alpha=0.7, edgecolor="black")
        axes[1].axvline(x=0, color="red", linestyle="--", linewidth=2, label="Break-even")
        axes[1].set_title("Distribución de Retorno %", fontsize=14, fontweight="bold")
        axes[1].set_xlabel("Retorno (%)", fontsize=11)
        axes[1].set_ylabel("Frecuencia", fontsize=11)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Gráfica guardada en: {save_path}")

        plt.show()

    @staticmethod
    def plot_drawdown(result: BacktestResult, save_path: str | None = None) -> None:
        """Grafica el drawdown a lo largo del tiempo.

        Args:
            result: Resultados del backtesting
            save_path: Ruta opcional para guardar la imagen
        """
        if result.equity_curve is None or len(result.equity_curve) == 0:
            print("No hay datos de equity curve disponibles")
            return

        equity = result.equity_curve["equity"]
        running_max = equity.expanding().max()
        drawdown = (equity - running_max) / running_max * 100

        plt.figure(figsize=(14, 7))

        plt.fill_between(drawdown.index, 0, drawdown, color="red", alpha=0.4)
        plt.plot(drawdown.index, drawdown, color="darkred", linewidth=2, label="Drawdown")

        plt.title("Drawdown a lo largo del tiempo", fontsize=16, fontweight="bold")
        plt.xlabel("Fecha", fontsize=12)
        plt.ylabel("Drawdown (%)", fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Gráfica guardada en: {save_path}")

        plt.show()

    @staticmethod
    def plot_monthly_returns(result: BacktestResult, save_path: str | None = None) -> None:
        """Grafica retornos mensuales.

        Args:
            result: Resultados del backtesting
            save_path: Ruta opcional para guardar la imagen
        """
        if not result.trades:
            print("No hay trades para visualizar")
            return

        # Crear DataFrame de trades
        trades_df = pd.DataFrame(
            [
                {
                    "entry_time": trade.entry_time,
                    "pnl": trade.pnl,
                }
                for trade in result.trades
            ]
        )

        trades_df["month"] = pd.to_datetime(trades_df["entry_time"]).dt.to_period("M")
        monthly_pnl = trades_df.groupby("month")["pnl"].sum().reset_index()
        monthly_pnl["month"] = monthly_pnl["month"].astype(str)

        plt.figure(figsize=(14, 7))

        colors = ["green" if x > 0 else "red" for x in monthly_pnl["pnl"]]
        plt.bar(
            monthly_pnl["month"], monthly_pnl["pnl"], color=colors, alpha=0.7, edgecolor="black"
        )

        plt.axhline(y=0, color="black", linestyle="-", linewidth=1)
        plt.title("PnL Mensual", fontsize=16, fontweight="bold")
        plt.xlabel("Mes", fontsize=12)
        plt.ylabel("PnL ($)", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Gráfica guardada en: {save_path}")

        plt.show()

    @staticmethod
    def create_full_report(
        result: BacktestResult, output_dir: str = "reports"
    ) -> None:
        """Crea un reporte completo con todas las visualizaciones.

        Args:
            result: Resultados del backtesting
            output_dir: Directorio donde guardar las imágenes
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*60}")
        print("Generando reporte completo de visualizaciones...")
        print(f"{'='*60}\n")

        BacktestVisualizer.plot_equity_curve(
            result, save_path=str(output_path / "equity_curve.png")
        )

        BacktestVisualizer.plot_returns_distribution(
            result, save_path=str(output_path / "returns_distribution.png")
        )

        BacktestVisualizer.plot_drawdown(result, save_path=str(output_path / "drawdown.png"))

        BacktestVisualizer.plot_monthly_returns(
            result, save_path=str(output_path / "monthly_returns.png")
        )

        print(f"\n{'='*60}")
        print(f"✓ Reporte completo generado en: {output_path}")
        print(f"{'='*60}\n")
