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
from datapulse.pipeline import run_pipeline
from datapulse.quality.checks import run_quality_checks

st.set_page_config(
    page_title="DataPulse Spain",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
[data-testid="stMetric"] {
  background: linear-gradient(145deg, rgba(111,66,193,.12), rgba(255,255,255,.03));
  border: 1px solid rgba(125,125,125,.18);
  padding: 1rem;
  border-radius: 16px;
}
.hero {
  padding: 1.35rem 1.5rem;
  border-radius: 22px;
  background: linear-gradient(135deg, #24143d 0%, #6f42c1 58%, #9b59b6 100%);
  color: white;
  margin-bottom: 1.4rem;
}
.hero h1 {margin: 0; font-size: 2.2rem;}
.hero p {margin: .35rem 0 0; opacity: .86;}
.small-note {opacity: .7; font-size: .85rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>DataPulse Spain</h1>
<p>Benchmark macroeconómico de España y Europa · extracción, calidad, SQL y visualización</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def ensure_database() -> None:
    if Path(DB_PATH).exists():
        return
    run_pipeline(DB_PATH)

if not Path(DB_PATH).exists():
    with st.spinner("Preparando los datos desde World Bank Indicators API..."):
        try:
            ensure_database()
        except Exception as exc:
            st.error("No se pudo preparar la base de datos automáticamente.")
            st.exception(exc)
            st.stop()

frame = read_indicators(DB_PATH)
if frame.empty:
    st.warning("La base de datos está vacía. Intenta reiniciar la aplicación.")
    st.stop()

yoy = add_year_over_year(frame)

with st.sidebar:
    st.header("Filtros")
    country = st.selectbox(
        "País principal",
        options=list(COUNTRIES.keys()),
        format_func=lambda code: COUNTRIES[code],
        index=list(COUNTRIES.keys()).index("ESP"),
    )
    indicator = st.selectbox(
        "Indicador",
        options=list(INDICATORS.keys()),
        format_func=lambda code: INDICATORS[code]["name"],
    )
    available_years = sorted(
        frame.loc[frame["indicator_code"] == indicator, "year"]
        .dropna()
        .astype(int)
        .unique(),
        reverse=True,
    )
    comparison_year = st.selectbox("Año de comparación", options=available_years)
    st.divider()
    st.caption("Fuente: World Bank Indicators API")
    st.caption("Persistencia: SQLite · Capa analítica: Pandas")

def format_value(value: float, indicator_code: str) -> str:
    kind = INDICATORS.get(indicator_code, {}).get("format", "number")
    if pd.isna(value):
        return "—"
    if kind == "currency":
        return "$" + format(value, ",.0f")
    if kind == "percent":
        return f"{value:,.2f}%"
    if kind == "integer":
        return f"{value:,.0f}"
    return f"{value:,.2f}"

st.subheader(f"Resumen ejecutivo · {COUNTRIES[country]}")
snapshot = latest_snapshot(yoy, country)
preferred = [
    "NY.GDP.PCAP.CD",
    "NY.GDP.MKTP.KD.ZG",
    "SL.UEM.TOTL.ZS",
    "FP.CPI.TOTL.ZG",
]
summary = snapshot[snapshot["indicator_code"].isin(preferred)].copy()
summary["order"] = summary["indicator_code"].map(
    {code: i for i, code in enumerate(preferred)}
)
summary = summary.sort_values("order")

cols = st.columns(4)
for col, code in zip(cols, preferred):
    row = summary[summary["indicator_code"] == code]
    if row.empty:
        col.metric(INDICATORS[code]["name"], "—")
        continue
    item = row.iloc[0]
    delta = None
    current = yoy[
        (yoy["country_code"] == country)
        & (yoy["indicator_code"] == code)
        & (yoy["year"] == item["year"])
    ]
    if not current.empty and pd.notna(current.iloc[0]["yoy_abs"]):
        delta = f"{current.iloc[0]['yoy_abs']:+,.2f} vs. año anterior"
    col.metric(
        label=f"{item['indicator_name']} · {int(item['year'])}",
        value=format_value(item["value"], code),
        delta=delta,
    )

tab_trend, tab_compare, tab_quality, tab_data = st.tabs(
    ["📈 Evolución", "🌍 Comparativa", "✅ Calidad", "🧾 Datos"]
)

with tab_trend:
    st.subheader(INDICATORS[indicator]["name"])
    selected = frame[frame["indicator_code"] == indicator].copy()
    chart = selected.pivot(index="year", columns="country_name", values="value")
    st.line_chart(chart, use_container_width=True)
    st.caption(
        f"Unidad: {INDICATORS[indicator]['unit']}. "
        "Cada país puede publicar el último dato disponible en un año distinto."
    )

with tab_compare:
    st.subheader(f"Comparativa europea · {comparison_year}")
    compare = frame[
        (frame["indicator_code"] == indicator)
        & (frame["year"] == comparison_year)
        & frame["value"].notna()
    ][["country_name", "value"]].sort_values("value", ascending=False)

    if compare.empty:
        st.info("No hay datos para ese indicador y año.")
    else:
        st.bar_chart(compare.set_index("country_name"), use_container_width=True)
        st.dataframe(
            compare.rename(columns={"country_name": "País", "value": "Valor"}),
            use_container_width=True,
            hide_index=True,
        )

with tab_quality:
    st.subheader("Estado de calidad de la carga")
    issues = run_quality_checks(frame)
    errors = sum(issue.count for issue in issues if issue.severity == "error")
    warnings = sum(issue.count for issue in issues if issue.severity == "warning")
    missing = int(frame["value"].isna().sum())
    total = len(frame)

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Filas", f"{total:,}")
    q2.metric("Valores ausentes", f"{missing:,}")
    q3.metric("Warnings", f"{warnings:,}")
    q4.metric("Errores críticos", f"{errors:,}")

    quality_table = pd.DataFrame([issue.to_dict() for issue in issues])
    st.dataframe(quality_table, use_container_width=True, hide_index=True)

with tab_data:
    st.subheader(f"Detalle · {COUNTRIES[country]}")
    detail = yoy[
        (yoy["country_code"] == country)
        & (yoy["indicator_code"] == indicator)
    ][["year", "value", "yoy_abs", "yoy_pct"]].sort_values(
        "year", ascending=False
    )
    st.dataframe(detail, use_container_width=True, hide_index=True)

st.markdown(
    '<p class="small-note">DataPulse Spain · proyecto de portfolio de Data Analytics, automatización y calidad de datos.</p>',
    unsafe_allow_html=True,
)
