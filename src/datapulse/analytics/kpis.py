from __future__ import annotations

import pandas as pd


def latest_snapshot(df: pd.DataFrame, country_code: str = "ESP") -> pd.DataFrame:
    subset = df[(df["country_code"] == country_code) & df["value"].notna()].copy()
    if subset.empty:
        return subset
    idx = subset.groupby("indicator_code")["year"].idxmax()
    return subset.loc[idx].sort_values("indicator_name").reset_index(drop=True)


def add_year_over_year(df: pd.DataFrame) -> pd.DataFrame:
    out = df.sort_values(["country_code", "indicator_code", "year"]).copy()
    out["previous_value"] = out.groupby(["country_code", "indicator_code"])["value"].shift(1)
    out["yoy_abs"] = out["value"] - out["previous_value"]
    out["yoy_pct"] = (out["value"] / out["previous_value"] - 1) * 100
    return out


def ranking_for_year(df: pd.DataFrame, indicator_code: str, year: int) -> pd.DataFrame:
    subset = df[
        (df["indicator_code"] == indicator_code)
        & (df["year"] == year)
        & df["value"].notna()
    ].copy()
    return subset.sort_values("value", ascending=False).reset_index(drop=True)
