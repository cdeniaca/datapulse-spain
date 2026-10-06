from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

SCHEMA = """
CREATE TABLE IF NOT EXISTS indicators (
    country_code TEXT NOT NULL,
    country_name TEXT NOT NULL,
    indicator_code TEXT NOT NULL,
    indicator_name TEXT NOT NULL,
    unit TEXT,
    year INTEGER NOT NULL,
    value REAL,
    source TEXT,
    last_updated TEXT,
    loaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (country_code, indicator_code, year)
);

CREATE INDEX IF NOT EXISTS idx_indicators_indicator_year
ON indicators(indicator_code, year);
"""


def initialize_database(db_path: str | Path) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA)


def replace_indicators(df: pd.DataFrame, db_path: str | Path) -> None:
    initialize_database(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM indicators")
        df.to_sql("indicators", conn, if_exists="append", index=False)


def read_indicators(db_path: str | Path) -> pd.DataFrame:
    initialize_database(db_path)
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(
            "SELECT * FROM indicators ORDER BY indicator_code, country_code, year",
            conn,
        )
