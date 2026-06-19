from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import warnings

import pandas as pd
import numpy as np
import yfinance as yf


@dataclass
class PriceDataHandler:
    symbol: str
    start_date: str
    end_date: str
    prices: pd.DataFrame | None = None

    def fetch_data(self, auto_adjust: bool = False) -> pd.DataFrame:
        self.prices = yf.download(
            self.symbol,
            start=self.start_date,
            end=self.end_date,
            auto_adjust=auto_adjust,
        )
        self.prices.columns = self.prices.columns.get_level_values(0)
        return self.prices

    def calculate_features(self):
        # Calculating previous close because I will need it
        self.prices["prev_close"] = self.prices["Close"].shift(1)

        self.prices["return"] = self.prices["Close"].pct_change()

        # Range percentage based on yesterday's close price
        self.prices["range_pct"] = (
            self.prices["High"] - self.prices["Low"]
        ) / self.prices["prev_close"]

        # Close localtion gets values in the range of [0,1]
        # Values close to 1.0 mean that price closed near the high
        # Values close to 0.5 mean that price closed near the middle
        # Values close to 0.0 mean that price closed near the low
        self.prices["close_location"] = (self.prices["Close"] - self.prices["Low"]) / (
            self.prices["High"] - self.prices["Low"]
        ).replace(
            [np.inf, -np.inf], np.nan
        )  # In the case that High Price = Low Price (Almost never)

        # ATR(14)
        self.prices["tr_1"] = self.prices["High"] - self.prices["Low"]
        self.prices["tr_2"] = (self.prices["High"] - self.prices["prev_close"]).abs()
        self.prices["tr_3"] = (self.prices["Low"] - self.prices["prev_close"]).abs()
        self.prices["true_range"] = self.prices[["tr_1", "tr_2", "tr_3"]].max(axis=1)
        self.prices["true_range_pct"] = self.prices["true_range"] / self.prices["prev_close"]
        self.prices["atr_14"] = self.prices["true_range"].rolling(14).mean()
        self.prices["atr_14_pct"] = self.prices["atr_14"] / self.prices["prev_close"]
        self.prices = self.prices.dropna()
        # breakpoint()