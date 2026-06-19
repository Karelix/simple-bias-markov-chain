import pandas as pd
import numpy as np


class MarkovChain:
    """
    Simple Markov Chain model for classifying market regimes
    and calculating transition probabilities.
    """

    def __init__(
        self,
        return_threshold=0.003,
        close_location_upper=0.60,
        close_location_lower=0.40,
        volatility_multiplier=1.5,
    ):
        self.return_threshold = return_threshold
        self.close_location_upper = close_location_upper
        self.close_location_lower = close_location_lower
        self.volatility_multiplier = volatility_multiplier

        self.transition_counts = None
        self.transition_probs = None

    def classify_day(self, row: pd.Series) -> str:
        strong_up = (
            row["return"] > self.return_threshold
            and row["close_location"] > self.close_location_upper
        )

        strong_down = (
            row["return"] < -self.return_threshold
            and row["close_location"] < self.close_location_lower
        )

        volatile = row["true_range_pct"] > self.volatility_multiplier * row["atr_14_pct"]

        if volatile and not strong_up and not strong_down:
            return "VOLATILE"
        elif strong_up:
            return "UP_TREND"
        elif strong_down:
            return "DOWN_TREND"
        else:
            return "BALANCE"

    def classify_states(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["state"] = df.apply(self.classify_day, axis=1)
        return df
    
    def build_transition_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "state" not in df.columns:
            df = self.classify_states(df)

        df["next_state"] = df["state"].shift(-1)


        self.transition_counts = pd.crosstab(
            df["state"],
            df["next_state"]
        )

        self.transition_probs = self.transition_counts.div(
            self.transition_counts.sum(axis=1),
            axis=0
        )

        return self.transition_probs
    
    def fit(self, df: pd.DataFrame) -> None:
        df = self.classify_states(df)
        baseline = df["state"].value_counts(normalize=True)
        self.build_transition_matrix(df)
        edge = self.transition_probs.subtract(baseline, axis=1)