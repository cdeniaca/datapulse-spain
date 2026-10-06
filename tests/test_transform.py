from datapulse.transform.normalize import normalize_world_bank


def test_normalize_world_bank():
    records = [
        {
            "indicator": {"id": "SL.UEM.TOTL.ZS", "value": "Unemployment"},
            "country": {"id": "ES", "value": "Spain"},
            "countryiso3code": "ESP",
            "date": "2023",
            "value": 12.18,
            "lastupdated": "2025-01-01",
        }
    ]
    df = normalize_world_bank(records)
    assert len(df) == 1
    assert df.loc[0, "country_name"] == "España"
    assert df.loc[0, "indicator_name"] == "Desempleo"
    assert df.loc[0, "year"] == 2023
