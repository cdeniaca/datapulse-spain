import pandas as pd

from datapulse.quality.checks import run_quality_checks


def test_duplicate_detection():
    df = pd.DataFrame(
        [
            {"country_code": "ESP", "indicator_code": "SL.UEM.TOTL.ZS", "year": 2023, "value": 12.1},
            {"country_code": "ESP", "indicator_code": "SL.UEM.TOTL.ZS", "year": 2023, "value": 12.1},
        ]
    )
    issues = run_quality_checks(df)
    assert any(issue.check == "duplicate_keys" and issue.count == 1 for issue in issues)
