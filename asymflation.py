"""
Asymflation: computational implementation for macroeconomics analysis.

Asymflation refers to asymmetric inflation dynamics where prices rise rapidly in response to cost shocks but decline slowly or incompletely when costs fall, creating persistent upward pressure on the aggregate price level through downward price rigidities and behavioral asymmetries in price adjustment. This module provides a reproducible calculator that validates the canonical channels, normalizes each series, computes a weighted index, and supports simple counterfactual policy simulation. The design is intentionally transparent so researchers can inspect how the concept moves from definition to code. Typical uses include comparative diagnostics, notebook-based scenario testing, and integration into empirical pipelines where consistent measurement matters as much as prediction.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# Asymflation channels track the observable anatomy of the canonical definition.
TERM_CHANNELS = [
    "input_cost_shock",  # Input cost shock captures a distinct economic channel.
    "price_increase_speed",  # Price increase speed captures a distinct economic channel.
    "price_decrease_speed",  # Price decrease speed mitigates exposure when it is high.
    "inflation_expectations",  # Inflation expectations captures a distinct economic channel.
    "market_power",  # Market power captures a distinct economic channel.
    "wage_rigidity",  # Wage rigidity captures a distinct economic channel.
    "pass_through_gap",  # Pass through gap captures a distinct economic channel.
]

# Weighted channels preserve the repository's existing score logic.
WEIGHTED_CHANNELS = [
    "input_cost_shock",
    "price_increase_speed",
    "price_decrease_speed",
    "inflation_expectations",
    "market_power",
    "wage_rigidity",
    "pass_through_gap",
]

# Default weights encode the relative economic importance of each weighted channel.
DEFAULT_WEIGHTS: dict[str, float] = {
    "input_cost_shock": 0.18,  # Input cost shock captures a distinct economic channel.
    "price_increase_speed": 0.2,  # Price increase speed captures a distinct economic channel.
    "price_decrease_speed": 0.14,  # Price decrease speed mitigates exposure when it is high.
    "inflation_expectations": 0.18,  # Inflation expectations captures a distinct economic channel.
    "market_power": 0.14,  # Market power captures a distinct economic channel.
    "wage_rigidity": 0.08,  # Wage rigidity captures a distinct economic channel.
    "pass_through_gap": 0.08,  # Pass through gap captures a distinct economic channel.
}


class AsymflationCalculator:
    """
    Compute Asymflation index scores from tabular data.

    Parameters
    ----------
    weights : dict[str, float] | None
        Optional weights overriding DEFAULT_WEIGHTS. Keys must match
        WEIGHTED_CHANNELS and values must sum to 1.0.
    """

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        # Alternative weights are useful for robustness checks across specifications.
        self.weights = weights or DEFAULT_WEIGHTS.copy()

        # Exact key matching prevents silent omission of economically relevant channels.
        if set(self.weights) != set(WEIGHTED_CHANNELS):
            raise ValueError(f"Weights must include exactly these channels: {WEIGHTED_CHANNELS}")

        # Unit-sum weights keep the index interpretable across datasets.
        if abs(sum(self.weights.values()) - 1.0) >= 1e-6:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def _normalise(series: pd.Series) -> pd.Series:
        """
        Return min-max normalized values on the unit interval.
        """
        lo = float(series.min())
        hi = float(series.max())
        if hi == lo:
            # Degenerate channels should not create spurious variation.
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - lo) / (hi - lo)

    def calculate_asymflation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute normalized channels, composite scores, and qualitative bands.
        """
        # Full channel validation keeps the score tied to the canonical definition.
        missing = [channel for channel in TERM_CHANNELS if channel not in df.columns]
        if missing:
            raise ValueError(f"Missing Asymflation channels: {missing}")

        out = df.copy()
        for channel in TERM_CHANNELS:
            out[f"{channel}_norm"] = self._normalise(out[channel])

        # Positive channels intensify the mechanism while negative channels offset it.
        out["asymflation_index"] = (
            + self.weights["input_cost_shock"] * out["input_cost_shock_norm"]
            + self.weights["price_increase_speed"] * out["price_increase_speed_norm"]
            + self.weights["inflation_expectations"] * out["inflation_expectations_norm"]
            + self.weights["market_power"] * out["market_power_norm"]
            + self.weights["wage_rigidity"] * out["wage_rigidity_norm"]
            + self.weights["pass_through_gap"] * out["pass_through_gap_norm"]
            + self.weights["price_decrease_speed"] * (1.0 - out["price_decrease_speed_norm"])
        )

        # Three bands keep the metric usable in audits, papers, and dashboards.
        out["asymflation_band"] = pd.cut(
            out["asymflation_index"],
            bins=[-np.inf, 0.33, 0.66, np.inf],
            labels=["low", "moderate", "high"],
        )
        return out

    def simulate_policy(self, df: pd.DataFrame, channel: str, reduction: float = 0.2) -> pd.DataFrame:
        """
        Simulate a policy shock that reduces one observed channel.
        """
        if channel not in TERM_CHANNELS:
            raise ValueError(f"Unknown Asymflation channel: {channel}")
        if reduction < 0.0 or reduction > 1.0:
            raise ValueError("reduction must be between 0.0 and 1.0")

        # Counterfactual shocks translate reforms into score movements.
        df_policy = df.copy()
        df_policy[channel] = df_policy[channel] * (1 - reduction)
        return self.calculate_asymflation(df_policy)


if __name__ == "__main__":
    sample = pd.read_csv("asymflation_dataset.csv")
    calc = AsymflationCalculator()
    print(calc.calculate_asymflation(sample)[["asymflation_index", "asymflation_band"]].head(10).to_string(index=False))

    scenario = calc.simulate_policy(sample, channel="input_cost_shock", reduction=0.15)
    print("\nPolicy Scenario Mean Index:")
    print(float(scenario["asymflation_index"].mean()))
