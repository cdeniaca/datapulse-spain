-- Último dato disponible por país e indicador
WITH ranked AS (
    SELECT
        country_code,
        country_name,
        indicator_code,
        indicator_name,
        unit,
        year,
        value,
        ROW_NUMBER() OVER (
            PARTITION BY country_code, indicator_code
            ORDER BY year DESC
        ) AS rn
    FROM indicators
    WHERE value IS NOT NULL
)
SELECT *
FROM ranked
WHERE rn = 1
ORDER BY indicator_name, country_name;

-- Evolución interanual de España
SELECT
    indicator_name,
    year,
    value,
    value - LAG(value) OVER (
        PARTITION BY indicator_code
        ORDER BY year
    ) AS variacion_absoluta
FROM indicators
WHERE country_code = 'ESP'
ORDER BY indicator_name, year;
