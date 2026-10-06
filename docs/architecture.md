# Arquitectura

DataPulse Spain sigue un pipeline ETL sencillo y explícito para que cada responsabilidad sea testeable por separado.

1. **Extract** consulta la World Bank Indicators API.
2. **Transform** normaliza la respuesta a un esquema tabular estable.
3. **Quality** valida claves, rangos y valores ausentes.
4. **Load** persiste la capa analítica en SQLite.
5. **Analytics** calcula snapshots y variaciones interanuales.
6. **Dashboard** consume exclusivamente la capa SQLite.

## Decisiones

- SQLite mantiene el proyecto ejecutable sin infraestructura externa.
- El dashboard no consume la API directamente: separa ingestión de presentación.
- Los valores ausentes de la fuente son warnings, no errores, porque las series oficiales pueden publicarse con distinto calendario.
- Las reglas de calidad están aisladas para poder crecer hacia un score de calidad o alertas automáticas.
