from __future__ import annotations

from typing import Iterable

import requests

from datapulse.config import WORLD_BANK_BASE_URL


def fetch_indicator(
    country_codes: Iterable[str],
    indicator_code: str,
    start_year: int,
    end_year: int,
    timeout: int = 30,
) -> list[dict]:
    """Fetch one World Bank indicator for multiple countries."""
    countries = ";".join(country_codes)
    url = f"{WORLD_BANK_BASE_URL}/country/{countries}/indicator/{indicator_code}"
    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 20000,
    }
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        return []

    return payload[1]


def fetch_many(
    country_codes: Iterable[str],
    indicator_codes: Iterable[str],
    start_year: int,
    end_year: int,
) -> list[dict]:
    rows: list[dict] = []
    for indicator_code in indicator_codes:
        rows.extend(
            fetch_indicator(
                country_codes=country_codes,
                indicator_code=indicator_code,
                start_year=start_year,
                end_year=end_year,
            )
        )
    return rows
