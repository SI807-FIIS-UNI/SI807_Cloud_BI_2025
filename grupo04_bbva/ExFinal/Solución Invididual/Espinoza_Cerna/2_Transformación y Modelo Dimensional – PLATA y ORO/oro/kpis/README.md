# KPIs Analíticos (Capa Oro)

En esta carpeta se documentan los **KPIs** calculados a partir del modelo estrella en la **capa Oro (Gold)**.  
Estos indicadores permiten medir **puntualidad**, **retrasos**, **cancelaciones** y **causas de demora** por **aerolínea (carrier_code)**, facilitando la construcción de dashboards y análisis comparativos.

> **Nivel de agregación (granularidad):** por **aerolínea** (`carrier_code`) en la tabla `kpis_reporte_gold`.  
> **Fuente principal:** `fact_vuelos_gold` (derivada de `flight_delay_silver`).

---

## Resumen de KPIs

| Código | Nombre del KPI | Qué mide | Unidad | Tabla/Salida |
|------|------------------|---------|--------|--------------|
| KPI01 | Porcentaje de vuelos retrasados (> 15 min) | Proporción de vuelos con retraso significativo | % | `kpis_reporte_gold` |
| KPI02 | Retraso promedio de llegada | Promedio general del retraso de llegada | Minutos | `kpis_reporte_gold` |
| KPI03 | Tasa de cancelación | Porcentaje de vuelos cancelados | % | `kpis_reporte_gold` |
| KPI04 | Porcentaje de vuelos a tiempo | Proporción de vuelos con `arr_delay <= 0` | % | `kpis_reporte_gold` |
| KPI05 | Retraso promedio (solo vuelos retrasados) | Promedio del retraso considerando solo `arr_delay > 0` | Minutos | `kpis_reporte_gold` |
| KPI06 | Minutos de retraso por causa (Carrier) | Total de minutos perdidos por causa “Carrier” | Minutos | `kpis_reporte_gold` |
| KPI07 | Minutos de retraso por causa (Weather) | Total de minutos perdidos por clima | Minutos | `kpis_reporte_gold` |
| KPI08 | Minutos de retraso por causa (NAS) | Total de minutos perdidos por NAS | Minutos | `kpis_reporte_gold` |
| KPI09 | Minutos de retraso por causa (Security) | Total de minutos perdidos por seguridad | Minutos | `kpis_reporte_gold` |
| KPI10 | Minutos de retraso por causa (Late Aircraft) | Total de minutos perdidos por llegada tardía de aeronave | Minutos | `kpis_reporte_gold` |

---

# Fichas de KPIs (formato de documentación)

## KPI01 — Porcentaje de vuelos retrasados (> 15 min)

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI01 |
| Nombre del KPI | Porcentaje de vuelos retrasados (> 15 min) |
| Objetivo analítico | Identificar aerolíneas con mayor incidencia de retrasos relevantes. |
| Definición | Porcentaje de vuelos cuya demora de llegada es mayor a 15 minutos (`arr_delay > 15`). |
| Fórmula | (`# vuelos con arr_delay > 15` / `# vuelos totales`) × 100 |
| Unidad de medida | % |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.porcentaje_retrasos` |

---

## KPI02 — Retraso promedio de llegada

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI02 |
| Nombre del KPI | Retraso promedio de llegada |
| Objetivo analítico | Medir el comportamiento promedio del retraso por aerolínea. |
| Definición | Promedio del retraso de llegada (`arr_delay`) considerando todos los vuelos. |
| Fórmula | AVG(`arr_delay`) |
| Unidad de medida | Minutos |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.retraso_promedio_llegada` |

---

## KPI03 — Tasa de cancelación

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI03 |
| Nombre del KPI | Tasa de cancelación |
| Objetivo analítico | Evaluar el impacto de cancelaciones por aerolínea. |
| Definición | Porcentaje de vuelos con estado cancelado (`cancelled = 1`). |
| Fórmula | AVG(`cancelled`) × 100 |
| Unidad de medida | % |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.tasa_cancelacion_pct` |

---

## KPI04 — Porcentaje de vuelos a tiempo

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI04 |
| Nombre del KPI | Porcentaje de vuelos a tiempo |
| Objetivo analítico | Medir el nivel de puntualidad por aerolínea. |
| Definición | Porcentaje de vuelos con llegada a tiempo o anticipada (`arr_delay <= 0`). |
| Fórmula | (`# vuelos con arr_delay <= 0` / `# vuelos totales`) × 100 |
| Unidad de medida | % |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.porcentaje_a_tiempo_pct` |

---

## KPI05 — Retraso promedio (solo vuelos retrasados)

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI05 |
| Nombre del KPI | Retraso promedio (solo vuelos retrasados) |
| Objetivo analítico | Medir severidad del retraso cuando ocurre (excluye vuelos a tiempo/anticipados). |
| Definición | Promedio de `arr_delay` considerando únicamente vuelos con `arr_delay > 0`. |
| Fórmula | AVG( `arr_delay` | condición: `arr_delay > 0`) |
| Unidad de medida | Minutos |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.retraso_promedio_solo_retrasados` |

---

## KPI06 — Minutos de retraso por causa (Carrier)

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI06 |
| Nombre del KPI | Minutos de retraso por causa (Carrier) |
| Objetivo analítico | Identificar impacto de demoras atribuibles a la aerolínea (operación/mantenimiento/crew). |
| Definición | Suma total de minutos de retraso por causa Carrier. |
| Fórmula | SUM(`delay_carrier`) |
| Unidad de medida | Minutos |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.minutos_retraso_carrier` |

---

## KPI07 — Minutos de retraso por causa (Weather)

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI07 |
| Nombre del KPI | Minutos de retraso por causa (Weather) |
| Objetivo analítico | Medir el impacto del clima en la operación aérea por aerolínea. |
| Definición | Suma total de minutos de retraso por clima. |
| Fórmula | SUM(`delay_weather`) |
| Unidad de medida | Minutos |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.minutos_retraso_weather` |

---

## KPI08 — Minutos de retraso por causa (NAS)

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI08 |
| Nombre del KPI | Minutos de retraso por causa (NAS) |
| Objetivo analítico | Medir el impacto del National Airspace System (congestión/ATC). |
| Definición | Suma total de minutos de retraso por NAS. |
| Fórmula | SUM(`delay_nas`) |
| Unidad de medida | Minutos |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.minutos_retraso_nas` |

---

## KPI09 — Minutos de retraso por causa (Security)

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI09 |
| Nombre del KPI | Minutos de retraso por causa (Security) |
| Objetivo analítico | Medir impacto de eventos de seguridad en retrasos. |
| Definición | Suma total de minutos de retraso por seguridad. |
| Fórmula | SUM(`delay_security`) |
| Unidad de medida | Minutos |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.minutos_retraso_security` |

---

## KPI10 — Minutos de retraso por causa (Late Aircraft)

| CAMPO | DESCRIPCIÓN / EJEMPLO |
|------|------------------------|
| Código | KPI10 |
| Nombre del KPI | Minutos de retraso por causa (Late Aircraft) |
| Objetivo analítico | Medir retrasos por arrastre operacional (aeronave llega tarde y afecta siguiente vuelo). |
| Definición | Suma total de minutos de retraso por “Late Aircraft”. |
| Fórmula | SUM(`delay_late_aircraft`) |
| Unidad de medida | Minutos |
| Nivel de análisis | Aerolínea (`carrier_code`) |
| Fuente de datos | `fact_vuelos_gold` |
| Tabla resultante | `kpis_reporte_gold.minutos_retraso_late_aircraft` |

