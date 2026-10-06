# 📊 DataPulse Spain

Proyecto end-to-end de **Data Analytics y automatización** para extraer, validar, modelar y visualizar indicadores macroeconómicos de España y países comparables.

La primera versión utiliza la **World Bank Indicators API** como fuente pública y no necesita API key.

## Objetivo

Construir un pipeline reproducible que conecte una fuente pública real con una capa de calidad de datos, almacenamiento SQL y un dashboard orientado a análisis.

El proyecto está pensado como pieza de portfolio: no solo muestra visualizaciones, sino también cómo se estructura un flujo de datos mantenible.

## Qué incluye

- extracción automática desde API pública
- normalización con Pandas
- controles de calidad de datos
- almacenamiento en SQLite
- KPIs y variación interanual
- consultas SQL analíticas
- dashboard con Streamlit
- tests automatizados con Pytest
- CI con GitHub Actions

## Indicadores iniciales

| Indicador | Código |
|---|---|
| PIB per cápita | `NY.GDP.PCAP.CD` |
| Desempleo | `SL.UEM.TOTL.ZS` |
| Inflación | `FP.CPI.TOTL.ZG` |
| Población | `SP.POP.TOTL` |

Países de comparación: España, Portugal, Francia, Italia y Alemania.

## Arquitectura

```text
World Bank API
      │
      ▼
  Extract
      │
      ▼
 Transform ──► Data Quality
      │             │
      └──────┬──────┘
             ▼
          SQLite
             │
       ┌─────┴─────┐
       ▼           ▼
      SQL       Streamlit
```

## Estructura

```text
src/datapulse/
├── extract/      # consumo de APIs
├── transform/    # normalización
├── quality/      # reglas de calidad
├── load/         # persistencia SQLite
├── analytics/    # KPIs y lógica analítica
└── pipeline.py   # orquestación

dashboard/        # aplicación Streamlit
sql/              # consultas analíticas
tests/            # tests unitarios
data/sample/      # muestra reproducible
.github/workflows # CI
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
```

## Ejecutar el pipeline real

```bash
python -m datapulse.pipeline
```

Esto consulta la API, ejecuta los controles de calidad y genera `data/datapulse.sqlite`.

## Ejecutar sin conexión usando la muestra

```bash
python scripts/seed_sample.py
```

## Dashboard

```bash
streamlit run dashboard/app.py
```

## Tests

```bash
pytest -q
```

## Calidad de datos

La primera versión controla:

- claves duplicadas por país/indicador/año
- valores ausentes
- años inválidos
- valores negativos donde no son válidos
- tasas de desempleo fuera de 0–100

La ausencia de algunos valores publicados se registra como `warning`, no como error de pipeline.

## Próximas iteraciones

- añadir indicadores de productividad, empleo y energía
- generar un score de calidad por carga
- registrar histórico de ejecuciones del pipeline
- desplegar el dashboard
- añadir visualizaciones de benchmarking frente a Europa
- incorporar una segunda fuente pública para reconciliación de datos

## Fuente

World Bank Indicators API v2: https://api.worldbank.org/v2/

La API permite consultar series temporales de indicadores en JSON y no requiere autenticación.
