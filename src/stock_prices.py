"""Helpers for loading and cleaning OHLCV-style stock price data (Task 2)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

NUMERIC_OHLCV = ("Open", "High", "Low", "Close", "Volume")

_CANON = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
    "adj close": "Adj Close",
    "adj_close": "Adj Close",
    "adjclose": "Adj Close",
    "date": "Date",
}


def _normalize_column_name(name: str) -> str:
    key = str(name).strip().lower().replace(" ", "_")
    return _CANON.get(key, str(name).strip())


def load_ohlcv_csv(path: str | Path) -> pd.DataFrame:
    """
    Load a course-style daily OHLCV CSV: normalize column names and parse Date index.
    Expects columns like Open, High, Low, Close, Volume (Adj Close optional).
    """
    p = Path(path)
    df = pd.read_csv(p, low_memory=False)
    df = df.rename(columns=lambda c: _normalize_column_name(c))
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
        df = df.set_index("Date")
    elif not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("CSV must include a 'Date' column or a DatetimeIndex.")
    return df.sort_index()


def ensure_adj_close(df: pd.DataFrame) -> pd.DataFrame:
    """yfinance often omits Adj Close when auto_adjust=True; duplicate Close for PyNance."""
    out = df.copy()
    if "Adj Close" not in out.columns and "Close" in out.columns:
        out["Adj Close"] = out["Close"]
    return out


def prepare_price_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize a Yahoo-style history DataFrame:
    - ensure Adj Close exists
    - numeric OHLCV columns coerced to float
    - sort index, drop duplicate dates
    """
    out = ensure_adj_close(df)
    for col in NUMERIC_OHLCV:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").astype("float64")
    if "Adj Close" in out.columns:
        out["Adj Close"] = pd.to_numeric(out["Adj Close"], errors="coerce").astype("float64")
    out = out.sort_index()
    out = out[~out.index.duplicated(keep="last")]
    return out


def ohlcv_missing_report(df: pd.DataFrame) -> pd.Series:
    """Return per-column NaN counts for OHLCV + Adj Close."""
    cols = [c for c in list(NUMERIC_OHLCV) + ["Adj Close"] if c in df.columns]
    return df[cols].isna().sum()
