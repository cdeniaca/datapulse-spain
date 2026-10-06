# Controles de calidad

| Regla | Severidad | Motivo |
|---|---|---|
| Dataset vacío | Error | Una carga sin datos no es publicable |
| Clave país/indicador/año duplicada | Error | Rompe la granularidad esperada |
| Valor ausente | Warning | Puede ser normal en series oficiales |
| Año fuera de rango | Error | Probable problema de esquema o parseo |
| Negativo no permitido | Error | Inconsistencia semántica |
| Desempleo fuera de 0–100 | Error | Valor imposible para una tasa porcentual |
