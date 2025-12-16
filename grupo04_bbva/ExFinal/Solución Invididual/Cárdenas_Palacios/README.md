
# Nube Seleccionada: Azure

## 1. Justificación

Azure es una buena elección para este caso porque permite construir una solución BI end-to-end para analizar el **Retail Transactions Dataset** con escalabilidad y rapidez. En Azure puedes implementar un enfoque tipo *lakehouse* para manejar desde el CSV crudo hasta un **modelo estrella**: almacenar la data en **Azure Data Lake Storage (ADLS Gen2)** (bronce/plata/oro), transformar y preparar **fact_transacciones** y las dimensiones (**dim_tiempo, dim_producto, dim_tienda, dim_cliente**) usando **Azure Databricks** o **Synapse**, y orquestar cargas/actualizaciones con **Azure Data Factory**. Esto facilita calcular KPIs como **ticket promedio, top productos, frecuencia de compra, horas pico y combos frecuentes**, y dejar los datos listos para consumo analítico.

Además, Azure destaca por su integración nativa con **Power BI** (dashboards y actualización programada), y por su gobierno y seguridad empresarial: control de accesos con **Entra ID (Azure AD)**, secretos/credenciales en **Key Vault**, y monitoreo con **Azure Monitor/Log Analytics**. También es práctico en costos porque puedes empezar con servicios *pay-as-you-go* y escalar solo cuando el volumen crezca (por ejemplo, subir potencia de cómputo solo durante los jobs de transformación). En conjunto, Azure soporta un flujo ordenado, auditable y fácil de presentar para un proyecto de analítica retail orientado a promociones y optimización de stock.


## 2. Flujo de Implementación

En la carpeta respectiva.

## 3. Docs

En la carpeta respectiva.

## 4. Archivos Adicionales

En la carpeta respectiva.
