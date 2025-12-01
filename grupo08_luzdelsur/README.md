
# Proyecto Cloud BI – Luz del Sur  
Arquitectura Medallion (RAW → BRONZE → SILVER → GOLD) + Dashboard Power BI

---

## 1. Descripción General  
Este proyecto implementa un sistema analítico completo para la detección de facturación atípica en clientes de Luz del Sur, utilizando tecnologías serverless de AWS y un enfoque moderno basado en arquitectura Medallion.  

Incluye:  
- Generación de datos realistas alineados al negocio eléctrico peruano.  
- Construcción del Data Lake en AWS S3.  
- Procesamiento en capas: RAW → BRONZE → SILVER → GOLD.  
- Modelado analítico final con detección de anomalías.  
- Dashboard ejecutivo en Power BI conectado a Athena vía ODBC.

---

## 2. Arquitectura General  
```
s3://lds-s3-bucket-final/
│── raw/
│── bronze/
│── silver/
│── gold/
└── athena_results/
```

Servicios AWS utilizados:
- **S3**: almacenamiento por capas.  
- **Glue**: crawler, ETL en Visual Studio, catalogación.  
- **Athena**: consultas SQL, creación de tablas Silver/Gold.  
- **IAM**: gestión de permisos.  
- **Power BI**: visualización.  

---

## 3. Capa RAW  
Archivos cargados:
- raw_cliente  
- raw_suministro  
- raw_medidor  
- raw_tarifa_simple  
- raw_asignacion_tarifa  
- raw_lectura_60m  
- consolidado_mensual (2021–2024)

Acciones:
- Validación de estructura.  
- EDA inicial (nulos, blancos, duplicados).  
- No se aplicaron transformaciones para mantener RAW intacto.

---

## 4. Capa BRONZE  
Acciones realizadas:
- Transformación de CSV a Parquet.  
- Estandarización de tipos.  
- Correcciones menores de esquema.  
- Limpieza de caracteres erróneos y blancos en consolidado.  
- Validación de relaciones entre tablas.

Tablas generadas:
- bronze_cliente  
- bronze_suministro  
- bronze_medidor  
- bronze_tarifa  
- bronze_asig_tarifa  
- bronze_consolidado  

---

## 5. Capa SILVER  
Procesos aplicados:
- Limpieza completa de nulos.  
- Normalización de columnas numéricas.  
- Conversión adecuada de fechas.  
- Separación de año y mes para análisis.  
- Enriquecimiento de relaciones entre dimensiones.

Tablas resultantes:
- silver_cliente  
- silver_suministro  
- silver_medidor  
- silver_ubicacion  
- silver_tarifa  
- silver_asignacion_tarifa  
- silver_consolidado_mensual  

---

## 6. Capa GOLD  
Procesos:
- Unión de todas las dimensiones Silver.  
- Consolidación de métricas mensuales.  
- Construcción de tabla analítica:
  - **gold_facturacion_mensual**

### Detección de facturación atípica:
Método aplicado: **IQR (Interquartile Range)**  
```
IQR = Q3 – Q1
Umbral superior = Q3 + 1.5 × IQR
```

### Vistas finales:
- **vw_facturacion_atipica_base**  
- **vw_facturacion_atipica_resumen**  

Resultados finales:
- Tasa global de atípicos: 2.8%–3.3%  
- Distritos más afectados: Punta Hermosa, Jesús María, Carabayllo, Lurigancho  

---

## 7. Conexión Power BI  
Configuración ODBC:
- DSN: athena_luzdelsur  
- Authentication: Access Key + Secret Key IAM  
- S3 Output: `s3://lds-s3-bucket-final/athena_results/`  
- Workgroup: primary  
- Base de datos: lds_gold  

Visuales generados:
- % atípicos por distrito  
- Línea temporal  
- Monto atípico promedio  
- Mapa geográfico (Distrito, Lima, Perú)  
- Ranking de distritos  

---

## 8. Resultados del Dashboard  
KPIs:
- Total registros analizados: 2,064  
- % atípicos general: 2.8%  
- Monto atípico promedio: 230–270 soles  

Las tendencias coinciden con patrones reales simulados del sector eléctrico.

---

## 9. Conclusiones  
- Arquitectura implementada correctamente en AWS.  
- Pipeline escalable y eficiente.  
- Modelo IQR adecuado para detección realista.  
- Dashboard listo para uso ejecutivo.  

---

## 10. Equipo  
Grupo 08 – Proyecto Final Luz del Sur
