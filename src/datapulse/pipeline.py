from __future__ import annotations

import argparse
import json
from pathlib import Path

from datapulse.config import COUNTRIES, DB_PATH, END_YEAR, INDICATORS, START_YEAR
from datapulse.extract.world_bank import fetch_many
from datapulse.load.sqlite import replace_indicators
from datapulse.quality.checks import run_quality_checks
from datapulse.transform.normalize import normalize_world_bank


def run_pipeline(db_path: str | Path = DB_PATH) -> dict:
    raw = fetch_many(
        country_codes=COUNTRIES.keys(),
        indicator_codes=INDICATORS.keys(),
        start_year=START_YEAR,
        end_year=END_YEAR,
    )
    frame = normalize_world_bank(raw)
    issues = run_quality_checks(frame)

    critical = [issue for issue in issues if issue.severity == "error"]
    if critical:
        raise RuntimeError(
            "Controles de calidad fallidos: "
            + json.dumps([issue.to_dict() for issue in critical], ensure_ascii=False)
        )

    replace_indicators(frame, db_path)
    return {
        "rows": len(frame),
        "database": str(db_path),
        "quality": [issue.to_dict() for issue in issues],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta el pipeline de DataPulse Spain")
    parser.add_argument("--db", default=str(DB_PATH), help="Ruta de la base SQLite")
    args = parser.parse_args()
    result = run_pipeline(args.db)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
