from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd

from datapulse.config import INDICATORS


@dataclass(frozen=True)
class QualityIssue:
    check: str
    severity: str
    count: int
    detail: str

    def to_dict(self) -> dict:
        return asdict(self)


def run_quality_checks(df: pd.DataFrame) -> list[QualityIssue]:
    issues: list[QualityIssue] = []

    if df.empty:
        return [QualityIssue("dataset_empty", "error", 1, "El dataset no contiene filas.")]

    key_cols = ["country_code", "indicator_code", "year"]
    duplicate_count = int(df.duplicated(subset=key_cols).sum())
    if duplicate_count:
        issues.append(
            QualityIssue(
                "duplicate_keys",
                "error",
                duplicate_count,
                "Hay combinaciones país/indicador/año duplicadas.",
            )
        )

    missing_values = int(df["value"].isna().sum())
    if missing_values:
        issues.append(
            QualityIssue(
                "missing_values",
                "warning",
                missing_values,
                "Existen observaciones sin valor publicado por la fuente.",
            )
        )

    invalid_years = int((df["year"].isna() | (df["year"] < 1960) | (df["year"] > 2100)).sum())
    if invalid_years:
        issues.append(
            QualityIssue(
                "invalid_years",
                "error",
                invalid_years,
                "Se detectaron años fuera de un rango razonable.",
            )
        )

    negative_mask = pd.Series(False, index=df.index)
    for code, meta in INDICATORS.items():
        if not meta.get("allow_negative", False):
            negative_mask |= (df["indicator_code"] == code) & (df["value"] < 0)
    negative_count = int(negative_mask.fillna(False).sum())
    if negative_count:
        issues.append(
            QualityIssue(
                "unexpected_negative_values",
                "error",
                negative_count,
                "Hay valores negativos en indicadores que no deberían ser negativos.",
            )
        )

    unemployment_out_of_range = int(
        (
            (df["indicator_code"] == "SL.UEM.TOTL.ZS")
            & df["value"].notna()
            & ((df["value"] < 0) | (df["value"] > 100))
        ).sum()
    )
    if unemployment_out_of_range:
        issues.append(
            QualityIssue(
                "unemployment_range",
                "error",
                unemployment_out_of_range,
                "La tasa de desempleo debe estar entre 0 y 100.",
            )
        )

    if not issues:
        issues.append(
            QualityIssue(
                "all_checks_passed",
                "info",
                0,
                "No se detectaron incidencias críticas.",
            )
        )

    return issues
