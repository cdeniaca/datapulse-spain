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
    "NY.GDP.PCAP.CD": {"name": "PIB per cápita", "unit": "USD", "allow_negative": False, "format": "currency"},
    "NY.GDP.MKTP.KD.ZG": {"name": "Crecimiento del PIB", "unit": "% anual", "allow_negative": True, "format": "percent"},
    "SL.UEM.TOTL.ZS": {"name": "Desempleo", "unit": "% población activa", "allow_negative": False, "format": "percent"},
    "SL.UEM.1524.ZS": {"name": "Desempleo juvenil", "unit": "% población activa 15-24", "allow_negative": False, "format": "percent"},
    "SL.TLF.CACT.ZS": {"name": "Participación laboral", "unit": "% población 15+", "allow_negative": False, "format": "percent"},
    "FP.CPI.TOTL.ZG": {"name": "Inflación", "unit": "% anual", "allow_negative": True, "format": "percent"},
    "NE.EXP.GNFS.ZS": {"name": "Exportaciones", "unit": "% del PIB", "allow_negative": False, "format": "percent"},
    "SP.POP.TOTL": {"name": "Población", "unit": "personas", "allow_negative": False, "format": "integer"},
}

START_YEAR = 2010
END_YEAR = 2025
WORLD_BANK_BASE_URL = "https://api.worldbank.org/v2"