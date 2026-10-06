from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "datapulse.sqlite"

COUNTRIES = {
    "ESP": "España",
    "PRT": "Portugal",
    "FRA": "Francia",
    "ITA": "Italia",
    "DEU": "Alemania",
}

INDICATORS = {
    "NY.GDP.PCAP.CD": {
        "name": "PIB per cápita",
        "unit": "USD",
        "allow_negative": False,
    },
    "SL.UEM.TOTL.ZS": {
        "name": "Desempleo",
        "unit": "% población activa",
        "allow_negative": False,
    },
    "FP.CPI.TOTL.ZG": {
        "name": "Inflación",
        "unit": "% anual",
        "allow_negative": True,
    },
    "SP.POP.TOTL": {
        "name": "Población",
        "unit": "personas",
        "allow_negative": False,
    },
}

START_YEAR = 2010
END_YEAR = 2025
WORLD_BANK_BASE_URL = "https://api.worldbank.org/v2"
