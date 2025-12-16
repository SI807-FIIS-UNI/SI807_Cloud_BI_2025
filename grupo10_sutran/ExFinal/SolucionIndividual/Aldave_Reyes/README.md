# SOLUCION EXAMEN FINAL 
## 3.1 Ingestión y Estructuración – BRONCE
### Seleccion de nube
- **Escalabilidad y Flexibilidad:** GCP ofrece servicios como Google Dataproc (para procesamiento de grandes volúmenes de datos) y BigQuery (para análisis de datos en tiempo real), lo cual es crucial para manejar y analizar grandes cantidades de datos de ventas, clientes y productos.

- **Integración de Herramientas:** GCP integra herramientas como Google Cloud Storage y BigQuery con otras plataformas, lo que facilita el manejo de grandes datasets, análisis y optimización de datos.

- **Seguridad y Fiabilidad:** GCP ofrece una infraestructura confiable, con múltiples niveles de seguridad y cumplimiento de normativas internacionales.

**Problema: Incrementar rentabilidad optimizando mix de productos, regiones y segmentos de clientes.**

Usando GCP, puedes realizar análisis avanzados en tiempo real, identificar patrones en ventas por región, segmento de cliente y tipo de producto, y luego optimizar el mix de productos y estrategias de ventas, lo que te ayudará a maximizar la rentabilidad.

### Carga de csv utilizando CLI Y Ejecucion de EDA

[Visualizacion del Jupyter](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/65345a3cdc57425c0a683e84fcb6c0925f4efbee/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/readstream.ipynb)


![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_1.png)

 ![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_2.png)

## 3.2 Transformación y Modelo Dimensional – PLATA y ORO
***Se hace una limpieza***
![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_10.png?raw=true)

***Creacion de Tablas***
![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_11.png?raw=true)

![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_12.png?raw=true)

![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_13.png?raw=true)


## 3.3 Visualización de KPIs – Dashboards

Este proyecto incluye un análisis detallado de las ventas utilizando Power BI. Puedes encontrar el archivo de Power BI con el análisis completo en el siguiente enlace:

[Descargar el archivo de Power BI](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/f9c04db1508bc5f00efd1c16fdadaf84abf08643/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/dashboardFinal.pbit)

Este análisis proporciona KPIs clave, incluyendo ventas totales, margen, top productos, top regiones, ventas por segmento, y tendencia mensual.

**Ventas Totales por Producto**

Este KPI muestra la distribución de las ventas totales entre los diferentes productos. En el gráfico, vemos que un pequeño número de productos genera la mayor parte de las ventas, lo que puede indicar que algunos productos están dominando el mercado. Es fundamental identificar estos productos para optimizar el inventario y las estrategias de ventas.

![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_15.png)

**Ventas Totales por Región**

El gráfico muestra cómo las ventas están distribuidas entre las diferentes regiones. De acuerdo con los resultados, algunas regiones como West y East tienen mayores ventas, lo que sugiere que podrían ser las áreas clave para enfocarse en estrategias de marketing y expansión. Optimizar la oferta de productos y las campañas en estas regiones puede incrementar la rentabilidad.

![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_16.png)

**Ventas Totales por Segmento**

Este KPI visualiza las ventas totales por segmento de cliente. La visualización indica que el segmento Consumer tiene la mayor participación en las ventas, lo que sugiere que este grupo representa la mayor fuente de ingresos. A través de este análisis, podemos enfocar los esfuerzos de ventas y personalizar las ofertas para maximizar los ingresos en este segmento.

![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_17.png)

**Ventas Mensuales por Mes**

El gráfico de ventas mensuales muestra cómo las ventas fluctúan a lo largo del año. Se observa una tendencia estacional, con picos de ventas en ciertos meses, como noviembre y diciembre. Esto puede estar relacionado con el comportamiento de compra de los consumidores, como las compras de fin de año. Identificar estos picos puede ayudar a mejorar la gestión del inventario y las promociones durante estos meses clave.

![](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/SOLUCION_EXAMEN_FINAL_ALDAVE_REYES/grupo10_sutran/ExFinal/SolucionIndividual/Aldave_Reyes/evidencias_practi_final/Screenshot_18.png)


![]()

