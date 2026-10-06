from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from datapulse.analytics.kpis import add_year_over_year, latest_snapshot
from datapulse.config import COUNTRIES, DB_PATH, INDICATORS
from datapulse.load.sqlite import read_indicators

st.set_page_config(page_title="DataPulse Spain", page_icon="📊", layout="wide")

st.title("📊 DataPulse Spain")
st.caption("Indicadores macroeconómicos de España y países comparables · World Bank Indicators API")

if not Path(DB_PATH).exists():
    st.warning("No existe la base de datos. Ejecuta primero: `python -m datapulse.pipeline`")
    st.stop()

frame = read_indicators(DB_PATH)
if frame.empty:
    st.warning("La base de datos está vacía. Ejecuta de nuevo el pipeline.")
    st.stop()

yoy = add_year_over_year(frame)

country = st.sidebar.selectbox(
    "País principal",
    options=list(COUNTRIES.keys()),
    format_func=lambda code: COUNTRIES[code],
    index=list(COUNTRIES.keys()).index("ESP"),
)
indicator = st.sidebar.selectbox(
    "Indicador",
    options=list(INDICATORS.keys()),
    format_func=lambda code: INDICATORS[code]["name"],
)

st.subheader(f"Últimos datos · {COUNTRIES[country]}")
snapshot = latest_snapshot(yoy, country)
cols = st.columns(max(1, len(snapshot)))
for col, (_, row) in zip(cols, snapshot.iterrows()):
    delta = None
    previous = yoy[
        (yoy["country_code"] == country)
        & (yoy["indicator_code"] == row["indicator_code"])
        & (yoy["year"] == row["year"])
    ]
    if not previous.empty and pd.notna(previous.iloc[0]["yoy_abs"]):
        delta = f"{previous.iloc[0]['yoy_abs']:+,.2f} vs. año anterior"
    col.metric(
        label=f"{row['indicator_name']} ({int(row['year'])})",
        value=f"{row['value']:,.2f}",
        delta=delta,
    )

st.subheader(f"Evolución · {INDICATORS[indicator]['name']}")
chart = frame[frame["indicator_code"] == indicator].pivot(
    index="year", columns="country_name", values="value"
)
st.line_chart(chart)

st.subheader("Detalle")
detail = yoy[
    (yoy["country_code"] == country) & (yoy["indicator_code"] == indicator)
][["year", "value", "yoy_abs", "yoy_pct"]].sort_values("year", ascending=False)
st.dataframe(detail, use_container_width=True, hide_index=True)
