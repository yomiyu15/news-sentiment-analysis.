"""Tests for stock price preparation helpers."""

from pathlib import Path

import pandas as pd

from src.stock_prices import (
    ensure_adj_close,
    load_ohlcv_csv,
    ohlcv_missing_report,
    prepare_price_df,
)


def test_ensure_adj_close_adds_from_close():
    df = pd.DataFrame({"Open": [1.0], "High": [1.1], "Low": [0.9], "Close": [1.05], "Volume": [100]})
    out = ensure_adj_close(df)
    assert "Adj Close" in out.columns
    assert out["Adj Close"].iloc[0] == 1.05


def test_prepare_price_df_coerces_and_sorts():
    idx = pd.to_datetime(["2020-01-02", "2020-01-01"])
    df = pd.DataFrame(
        {
            "Open": ["10", "9"],
            "High": [11, 10],
            "Low": [9, 8],
            "Close": [10.5, 9.5],
            "Volume": [1000, 900],
        },
        index=idx,
    )
    out = prepare_price_df(df)
    assert out.index.is_monotonic_increasing
    assert out["Open"].dtype == "float64"
    assert "Adj Close" in out.columns


def test_ohlcv_missing_report():
    df = pd.DataFrame(
        {
            "Open": [1.0, float("nan")],
            "High": [1.1, 1.0],
            "Low": [0.9, 0.8],
            "Close": [1.0, 0.9],
            "Volume": [100, 100],
            "Adj Close": [1.0, 0.9],
        }
    )
    rep = ohlcv_missing_report(df)
    assert rep["Open"] == 1


def test_load_ohlcv_csv_parses_date_index(tmp_path: Path):
    p = tmp_path / "ohlcv.csv"
    p.write_text(
        "Date,Open,High,Low,Close,Volume\n"
        "2024-01-02,10,11,9,10.5,1000\n"
        "2024-01-03,10.5,12,10,11.2,1100\n",
        encoding="utf-8",
    )
    raw = load_ohlcv_csv(p)
    df = prepare_price_df(raw)
    assert isinstance(df.index, pd.DatetimeIndex)
    assert len(df) == 2
    assert df["Close"].iloc[-1] == 11.2
