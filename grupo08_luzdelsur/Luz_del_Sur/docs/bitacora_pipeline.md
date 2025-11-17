# 🧾 Bitácora Corporativa – Proyecto Cloud BI Luz del Sur

## 1. Información General del Proyecto
**Nombre del proyecto:** Sistema Analítico para Detección de Facturación Atípica  
**Organización simulada:** Luz del Sur S.A.A.  
**Objetivo corporativo:** Implementar un pipeline analítico basado en arquitectura Medallion para identificar comportamientos anómalos de facturación eléctrica en la concesión Lima Metropolitana.  
**Tecnologías principales:** AWS S3, AWS Glue, Athena, Parquet, Power BI.

---

## 2. Arquitectura e Infraestructura AWS
Se diseñó un Data Lake alineado al estándar Medallion:

```
lds-s3-bucket-demo/
├── raw/
├── bronze/
├── silver/
├── gold/
└── athena_results/
```

Servicios empleados:
- **Amazon S3:** almacenamiento centralizado por capas.
- **AWS Glue:** catalogación y ETL (Data Catalog, Crawlers, Jobs).
- **Amazon Athena:** motor de consulta serverless y generación de vistas KPI.
- **IAM:** gestión de accesos y credenciales.
- **Power BI:** capa analítica corporativa conectada vía ODBC Athena.

Control de costos realizado mediante:
- Uso de Parquet + Snappy.
- Workgroup Athena con limitación de gastos.
- Data sample simulada del 0.1% del universo real de clientes (1,500 clientes).

---

## 3. Capa RAW – Ingesta
Carga de datasets sintéticos basados en la lógica real de operación:
- Cliente, suministro, medidor, sector, tarifas, asignación tarifaria.
- Consumos agregados mensuales 2022–2025.

Cada carpeta fue catalogada mediante Glue Crawlers en `raw_db`.

---

## 4. Capa BRONZE – Limpieza y Estandarización
Transformaciones realizadas mediante Jobs visuales en Glue Studio:

- Estandarización de tipos y normalización de columnas.
- Validación de calidad de datos.
- Conversión de CSV a **Parquet**.
- Creación de tablas en `bronze_db`.

Tablas clave:
- bronze_cliente  
- bronze_suministro  
- bronze_medidor  
- bronze_sector  
- bronze_tarifa  
- bronze_asignacion_tarifa  
- bronze_acumulado  

---

## 5. Capa SILVER – Modelo normalizado de consumo mensual
Se construyó la tabla:

**`silver_db.silver_consumo_mensual`**

Incluye:
- kWh mensual
- demanda KW
- registros esperados vs error
- % error por medidor y mes

Creada vía CTAS desde Bronze para optimización.

---

## 6. Capa GOLD – Facturación Teórica y Análisis de Atipicidad
Se consolidaron todas las dimensiones en:

**`gold_db.gold_facturacion_teorica_mes`**

Transformaciones clave:
- Cálculo de facturación teórica.
- Integración con cliente, suministro, tarifas y zonas.
- Segmentación por tipo_cliente, nivel_tension y anio_mes.
- Detección de outliers usando **IQR**:
  - Cálculo de Q1, Q3 e IQR.
  - Umbral: `Q3 + 1.5 × IQR`.
  - Segmentos mínimos: ≥ 30 observaciones.

Resultados:
- Tasa estable de atípicos entre **1% y 2%**, alineado a modelos reales.

---

## 7. Vistas KPI en Athena
Se crearon vistas corporativas para análisis:

- vw_facturacion_atipica_detalle  
- vw_kpi_atipicos_mes  
- vw_kpi_atipicos_distrito_mes  
- vw_kpi_atipicos_zona_mes  
- vw_kpi_atipicos_zona_anual  
- vw_kpi_atipicos_distrito_anual  

---

## 8. Integración con Power BI (ODBC Athena)
Se configuró un DSN corporativo:

- **Driver:** Simba Athena ODBC 2.x  
- **DSN:** athena_luzdelsur  
- **Output Location:** `s3://lds-s3-bucket-demo/athena_results/`  
- **Auth:** AWS Access Key / Secret Key  

Power BI consumió directamente las vistas GOLD, permitiendo:
- KPIs ejecutivos.
- Tendencias mensualizadas.
- Segmentación por zona (cono), distrito, tipo de cliente.
- Mapa geográfico de Lima Metropolitana.
- Semáforos de riesgo.

---

## 9. Dashboard Ejecutivo
El tablero presenta:

- Indicadores principales: total de suministros, total de atípicos, % de atípicos.
- Evolución mensual 2022–2025.
- Ranking por distrito y zona.
- Mapa con distribución geográfica.
- Tabla analítica de casos críticos.

El dashboard permite identificar rápidamente:
- Distorsiones en facturación.
- Sectores geográficos sensibles.
- Riesgos operativos.
- Análisis comparativo interanual.

---

## 10. Conclusiones Corporativas
- La arquitectura implementada es **escalable, modular y de bajo costo**.
- El modelo IQR permite detectar **anomalías robustas** sin falsos positivos masivos.
- Athena + Parquet optimiza costos operativos y velocidad de consulta.
- Power BI proporciona una capa ejecutiva confiable y flexible.
- El proyecto puede escalarse fácilmente al universo completo de clientes (1.3M).

---

## 11. Próximos pasos sugeridos
- Migración del GOLD a Redshift para cargas mayores.
- Implementación de alertas automáticas de atipicidad.
- Incorporación de datos horarios y eventos de medidor.
- Integración de inspecciones comerciales para validación de casos.
