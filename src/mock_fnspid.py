"""Synthetic FNSPID-style rows for notebook / tests without real course data."""

from __future__ import annotations

import numpy as np
import pandas as pd


def build_mock_fnspid_df(n: int = 2500, seed: int = 42) -> pd.DataFrame:
    """
    Build a DataFrame with columns: headline, url, publisher, date, stock.
    Weekday-heavy dates and a mix of plain vs email-style publishers for EDA tests.
    """
    rng = np.random.default_rng(seed)
    tickers = np.array(["AAPL", "MSFT", "GOOGL", "AMZN", "META"])
    publishers = np.array(
        [
            "Reuters",
            "analyst1@reuters.com",
            "Bloomberg",
            "tips@bloomberg.com",
            "MarketWatch",
            "Seeking Alpha",
            "Benzinga Staff",
        ]
    )
    templates = [
        "{sym} shares surge after earnings beat expectations",
        "{sym} stock plummets on miss and weak guidance",
        "Analysts raise price target on {sym} ahead of Fed decision",
        "{sym} gains on FDA approval headline",
        "{sym} falls as revenue miss spooks investors",
        "Big tech {sym} rises with broader market rally",
        "Options volume spikes on {sym} before the close",
        "{sym} drops on macro fears; bonds rally",
    ]

    end = pd.Timestamp.now(tz="UTC").normalize()
    day_index = pd.date_range(end=end, periods=180, freq="D", tz="UTC")
    weekday_bias = np.array([1.25 if d.dayofweek < 5 else 0.3 for d in day_index], dtype=float)
    weekday_bias /= weekday_bias.sum()
    day_pick = rng.choice(len(day_index), size=n, p=weekday_bias)
    hours = rng.integers(7, 21, size=n)
    minutes = rng.integers(0, 60, size=n)

    base = day_index[day_pick]
    delta = pd.to_timedelta(hours, unit="h") + pd.to_timedelta(minutes, unit="min")
    dates = pd.DatetimeIndex(base + delta)

    syms = tickers[rng.integers(0, len(tickers), size=n)]
    pubs = publishers[rng.integers(0, len(publishers), size=n)]
    headlines = [
        templates[int(t)].format(sym=str(s)) for t, s in zip(rng.integers(0, len(templates), size=n), syms)
    ]

    return pd.DataFrame(
        {
            "headline": headlines,
            "url": [f"https://mock.example/article/{i}" for i in range(n)],
            "publisher": pubs,
            "date": dates,
            "stock": syms,
        }
    )
