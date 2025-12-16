# Tabla de Hechos ...


| Campo | Descripción |
|------|------------|
| `metricas_id` (PK) | Identificador único de la medición. |
| `tiempo_id` (FK) | Clave foránea que relaciona el registro con la dimensión de tiempo. |
| `geografia_id` (FK) | Clave foránea que vincula la medición con la localización geográfica. |
| `servicio_n1_id` (FK) | Clave foránea que asocia la medición al servicio N1 correspondiente. |
| `nro_fichas_rfo` | Número total de fichas de RFO registradas para los servicios N2 asociados al N1. |
| `nro_fichas_rfo_ok` | Cantidad de fichas RFO cuyo estado fue validado como **OK**. |
| `nro_sn2_sn1_dependencias` | Número de servicios N2 con dependencias definidas para un servicio N1. |
| `nro_sn2_sn1` | Total de servicios N2 asociados a un servicio N1. |
| `nro_features_desplegadas_calidad` | Features desplegadas que cumplen con los criterios de calidad. |
| `nro_features_desplegadas` | Total de features desplegadas consideradas. |
| `puntaje_total_adopcion_sn2` | Puntaje agregado de adopción de los servicios N2. |
| `sn2_sn1_medidos` | Total de servicios N2 medidos del servicio N1. |
| `total_vulnerabilidades_high` | Cantidad total de vulnerabilidades de alto riesgo detectadas. |
| `total_lineas_codigo` | Total de líneas de código analizadas. |

---

