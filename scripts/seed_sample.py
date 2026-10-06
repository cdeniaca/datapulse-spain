from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from datapulse.config import DB_PATH
from datapulse.load.sqlite import replace_indicators

sample_path = ROOT / "data" / "sample" / "wdi_sample.csv"
frame = pd.read_csv(sample_path)
replace_indicators(frame, DB_PATH)
print(f"Cargadas {len(frame)} filas de ejemplo en {DB_PATH}")
