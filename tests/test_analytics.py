import pandas as pd

from datapulse.analytics.kpis import add_year_over_year, latest_snapshot


def test_yoy_and_latest_snapshot():
    df = pd.DataFrame(
        [
            {"country_code": "ESP", "indicator_code": "X", "indicator_name": "X", "year": 2022, "value": 100.0},
            {"country_code": "ESP", "indicator_code": "X", "indicator_name": "X", "year": 2023, "value": 110.0},
        ]
    )
    out = add_year_over_year(df)
    assert round(out.iloc[1]["yoy_pct"], 2) == 10.00
    latest = latest_snapshot(out, "ESP")
    assert int(latest.iloc[0]["year"]) == 2023
