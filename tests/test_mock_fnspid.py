"""Tests for synthetic FNSPID-style data."""

import pandas as pd

from src.mock_fnspid import build_mock_fnspid_df


def test_build_mock_fnspid_df_columns_and_shape():
    df = build_mock_fnspid_df(n=100, seed=0)
    assert len(df) == 100
    assert set(df.columns) == {"headline", "url", "publisher", "date", "stock"}
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_build_mock_fnspid_df_weekday_heavier_than_weekend():
    df = build_mock_fnspid_df(n=8000, seed=1)
    dow = pd.to_datetime(df["date"]).dt.dayofweek
    weekday = (dow < 5).sum()
    weekend = (dow >= 5).sum()
    assert weekday > weekend
