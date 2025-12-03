
# Bitácora Corporativa – Proyecto Cloud BI Luz del Sur  

---

## 1. Definición del Proyecto  
Objetivo: Detectar facturación atípica a través de un pipeline moderno en AWS usando arquitectura Medallion.  
Alcance: Datos de 2021–2024 con análisis completo en Power BI.  

---

## 2. Diseño de Arquitectura  
Estructura implementada:
```
raw → bronze → silver → gold → Power BI
```

Servicios: S3, Glue, Athena, IAM, ODBC.

---

## 3. Ejecución por Capas  

### 🔹 RAW  
- Carga de datasets simulados realistas.  
- Validación de estructura y formatos.  
- EDA (nulos, duplicados, rangos).  

### 🔹 BRONZE  
- Conversión CSV → Parquet.  
- Limpieza mínima (blancos → NULL).  
- Reparación de tipos.  
- Mapeo de columnas en Glue Visual ETL.  

### 🔹 SILVER  
- Limpieza profunda.  
- Normalización de fechas.  
- Integración entre tablas.  
- Preparación para analítica final.  

### 🔹 GOLD  
- Integración total Cliente + Suministro + Medidor + Tarifas.  
- Cálculo de métricas por distrito/año/mes.  
- Aplicación de IQR para detectar anomalías.  
- Creación de vistas KPI.  

---

## 4. Validación de Calidad  
- Nulos controlados en consolidado.  
- llaves revisadas.  
- Coherencia temporal validada.  
- Formatos de fechas homologados.  

---

## 5. Power BI  
- Configuración de ODBC Athena.  
- Carga de vistas GOLD.  
- Creación de KPIs ejecutivos.  
- Mapa por distrito (Lima, Perú).  

---

## 6. Hallazgos Principales  
- % atípicos anual: 2%–3.5%.  
- Distritos con mayor incidencia: Punta Hermosa, Jesús María, Carabayllo.  
- Tendencia decreciente 2021–2023.  
- Incremento leve en 2024.  

---

## 7. Conclusiones  
- Medallion implementado correctamente.  
- Detección de anomalías estable.  
- Dashboard final listo para presentación.  

---

## 8. Próximos Pasos  
- Migración GOLD a Redshift.  
- Automatización con Step Functions.  
- Integrar datos horarios (15m / 60m).  

