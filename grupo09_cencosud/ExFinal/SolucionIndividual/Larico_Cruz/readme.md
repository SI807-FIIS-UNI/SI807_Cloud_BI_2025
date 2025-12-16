# 🛒 Retail Analytics Data Lakehouse (GCP)

## 📂 Estructura del Proyecto
```
├── data/          # Dataset fuente (SuperMarket Analysis.csv)
├── etl/           # Script de limpieza y transformación (etl_supermarket.py)
├── sql/           # Scripts DDL para crear el Modelo Estrella (Dimensiones y Hechos)
└── docs/          # Documentación técnica y diagramas
```

---

## 📊 Modelo de Datos (Star Schema)

El Data Warehouse (`retail_dw`) utiliza un esquema de estrella para optimizar el rendimiento de las consultas:

### Fact Table
- **`fact_ventas`**: Métricas (Ventas, Margen, Cantidad, Impuestos)

### Dimensions
- **`dim_sucursal`**: Geografía (Ciudad, Rama)
- **`dim_producto`**: Catálogo (Línea de producto)
- **`dim_cliente`**: Perfil (Tipo, Género)
- **`dim_pago`**: Financiero (Ewallet, Cash, Credit Card)

![MODELO ER](https://github.com/user-attachments/assets/cc55980a-7b3e-4e79-a8a0-10d6f039efe2)


---

## 🚀 Despliegue Rápido

1. **Configuración**: Definir `PROJECT_ID`, Región y crear Bucket/Dataset
2. **Ingesta**: Subir archivo `.csv` y script `.py` a Google Cloud Storage
3. **Procesamiento**: Ejecutar Job de Dataproc para limpiar los datos crudos
4. **Modelado**: Ejecutar queries SQL en BigQuery para generar las tablas `fact_` y `dim_`
5. **Visualización**: Conectar las tablas en Looker Studio 


---

## 👤 Autor
Diego Larico Cruz
