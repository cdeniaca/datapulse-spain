from __future__ import annotations

import pandas as pd

from datapulse.config import COUNTRIES, INDICATORS

COLUMNS = [
    "country_code",
    "country_name",
    "indicator_code",
    "indicator_name",
    "unit",
    "year",
    "value",
    "source",
    "last_updated",
]


def normalize_world_bank(records: list[dict]) -> pd.DataFrame:
    rows = []
    for item in records:
        indicator_code = item.get("indicator", {}).get("id")
        country_code = item.get("countryiso3code") or item.get("country", {}).get("id")
        year_raw = item.get("date")

        try:
            year = int(year_raw)
        except (TypeError, ValueError):
            continue

        indicator_meta = INDICATORS.get(indicator_code, {})
        rows.append(
            {
                "country_code": country_code,
                "country_name": COUNTRIES.get(country_code, item.get("country", {}).get("value")),
                "indicator_code": indicator_code,
                "indicator_name": indicator_meta.get(
                    "name", item.get("indicator", {}).get("value", indicator_code)
                ),
                "unit": indicator_meta.get("unit", ""),
                "year": year,
                "value": item.get("value"),
                "source": "World Bank Indicators API",
                "last_updated": item.get("lastupdated"),
            }
        )

    frame = pd.DataFrame(rows, columns=COLUMNS)
    if frame.empty:
        return frame

    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce").astype("Int64")
    frame = frame.sort_values(["country_code", "indicator_code", "year"]).reset_index(drop=True)
    return frame
