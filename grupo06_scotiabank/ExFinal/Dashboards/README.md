# 📊 Visualización Analítica de Riesgos Financieros

**Proyecto:** Grupo6 – Scotiabank  

**Curso:** Sistema de Inteligencia de Negocios - SI807-U

**Capa Analítica:** Google BigQuery (Capa Oro) + Power BI  

---

## 1. Contexto del Negocio

Las entidades financieras operan en un entorno altamente regulado y expuesto a múltiples tipos de riesgo, lo que exige contar con información confiable, consolidada y oportuna para la toma de decisiones estratégicas y regulatorias.

En el caso del banco analizado, la información de riesgos y desempeño financiero se encuentra distribuida en múltiples fuentes, con altos niveles de procesamiento manual y dependencia de entidades externas.

Ante este escenario, se plantea el diseño de una **solución analítica centralizada** que permita integrar, procesar y visualizar indicadores clave de riesgo y gestión, facilitando el monitoreo continuo y reduciendo riesgos operativos.

---

## 2. Problemática Identificada

### 2.1. Dificultad para explicar las variaciones del capital requerido
El banco no cuenta con un mecanismo uniforme y robusto que permita calcular, validar y explicar las variaciones del capital económico y regulatorio frente a los distintos tipos de riesgo:
- Crédito  
- Mercado  
- Operativo  
- Liquidez  

### 2.2. Poco control sobre indicadores comparativos externos (SBS, BCR)
La evaluación del desempeño frente al sector depende de indicadores generados por entidades externas, sin acceso automatizado ni mecanismos de integración directa, incrementando:
- Riesgo operativo  
- Latencia en el análisis  

### 2.3. Múltiples fuentes de datos internas
Diversas áreas calculan y mantienen información similar o duplicada, generando:
- Inconsistencias en datos financieros y de riesgos  
- Dificultad en la trazabilidad de la información  

### 2.4. Falta de consolidación para el monitoreo y la toma de decisiones
No existe un sistema centralizado que integre indicadores críticos como:
- Morosidad  
- Liquidez  
- Participación de mercado  

Lo cual limita una visión integral del negocio.

### 2.5. Alto esfuerzo manual en la consolidación de información de riesgos
La recopilación de datos desde distintas unidades de riesgo se realiza de forma manual y poco automatizada, afectando:
- Eficiencia operativa  
- Confiabilidad de la información  

---

## 3. Objetivo de la Solución

Implementar una **plataforma de visualización analítica en la nube**, basada en **Google BigQuery y Power BI**, que permita:

- Centralizar la información de riesgos en la **Capa Oro del Data Lake**
- Calcular y visualizar **KPIs regulatorios y gerenciales**
- Facilitar el análisis histórico y comparativo
- Reducir la dependencia de procesos manuales y fuentes dispersas

---

## 4. KPIs Implementados en los Dashboards

| KPI | Descripción | Fórmula | Unidad | Frecuencia | Umbrales de Decisión |
|----|------------|---------|--------|------------|---------------------|
| **Loans to Deposits** | Relación entre fondos disponibles y créditos concedidos | Colocaciones Brutas / Depósitos | % | Mensual | 🟢 ≤ 100%<br>🟡 100% – 120%<br>🔴 > 120% |
| **Ratio de Capital Global** | Patrimonio efectivo respecto a activos ponderados por riesgo | Patrimonio Efectivo / Requerimiento Patrimonial | % | Mensual | 🟢 ≥ 11%<br>🟡 10% – 11%<br>🔴 < 10% |
| **Morosidad** | Nivel de créditos atrasados | Créditos Atrasados / Total Créditos Directos | % | Mensual | 🟢 ≤ 4%<br>🟡 4% – 8%<br>🔴 > 8% |
| **Crecimiento de Cartera** | Variación interanual de créditos | (Créditos actuales − Créditos año anterior) / Créditos año anterior | % | Mensual | 🟢 > 0%<br>🟡 0% a -5%<br>🔴 < -5% |
| **Sensibilidad al Tipo de Cambio** | Exposición a fluctuaciones cambiarias | (Activos ME − Pasivos ME) / Patrimonio × %ΔTC | Millones S/ | Mensual | 🟢 < 2%<br>🟡 2% – 5%<br>🔴 > 5% |
| **Ratio de Liquidez** | Cobertura de obligaciones de corto plazo | Activos Líquidos / Obligaciones CP | % | Mensual | 🟢 ≥ 100%<br>🟡 90% – 100%<br>🔴 < 90% |

---

## 5. Arquitectura de la Visualización

- **Fuente de datos:** Google BigQuery – *Capa Oro*
- **Modelo:** Esquema estrella (tabla de hechos + dimensiones)
- **Herramienta de visualización:** Power BI Desktop
- **Autenticación:** Cuenta de Servicio GCP

---

## 6. Creación de Cuenta de Servicio para Visualización (CLI)

### 6.1. Configuración del proyecto
```bash
gcloud config set project grupo6-scotiabank
```

### 6.1. Configuración del proyecto
```bash
gcloud config set project grupo6-scotiabank
```

### 6.2. Creación de la cuenta de servicio
```bash
gcloud iam service-accounts create sa-visualizacion-dashboard \
  --display-name="Cuenta de Servicio - Visualización Dashboards Power BI"
```
![1](Evidencias/1-Cuenta_servicio.png)


## 7. Asignación de Roles (Acceso Simplificado)

Para garantizar compatibilidad con datasets que utilizan ACL clásico y facilitar la conexión desde Power BI, se asignaron los siguientes roles a nivel proyecto:
```bash
gcloud projects add-iam-policy-binding grupo6-scotiabank \
  --member="serviceAccount:sa-visualizacion-dashboard@grupo6-scotiabank.iam.gserviceaccount.com" \
  --role="roles/bigquery.user"
```
![2](Evidencias/2-Creacion_rol.png)

### Roles implícitos habilitados:

- Ejecución de consultas

- Lectura de datasets

- Acceso a metadata

Compatibilidad con Power BI (ADBC)

## 8. Generación de Clave JSON (Credencial Temporal)
```bash
gcloud iam service-accounts keys create \
  sa-visualizacion-dashboard-key.json \
  --iam-account=sa-visualizacion-dashboard@grupo6-scotiabank.iam.gserviceaccount.com
```
![3](Evidencias/3-Generacion-clave-json.png)

La clave se genera en el directorio de ejecución de Cloud Shell.

Descarga a entorno local
```bash
cloudshell download sa-visualizacion-dashboard-key.json
```
![4.1](Evidencias/4.1-Descargar_json.png)
![4.2](Evidencias/4.2-Descargar_ubicacion.png)
![4.3](Evidencias/4.3-Archivo_json.png)
![5](Evidencias/5-Json.png)

**Nota:** Esta clave es de uso temporal (5 días). Finalizado el periodo de evaluación, la clave debe ser revocada.

## 9. Autenticación en Power BI con BigQuery

1) Abrir Power BI Desktop

2) Seleccionar Obtener datos → Google BigQuery

3) Elegir Cuenta de Servicio como método de autenticación

4) Ingresar el contenido del archivo JSON

![6.1](Evidencias/6.1-Big_query.png)
![6.2](Evidencias/6.2-Credenciales.png)

Seleccionar:

- Proyecto: grupo6-scotiabank

- Dataset: oro

- Tablas de hechos y dimensiones

Construir el modelo estrella en Power BI

![6.3](Evidencias/6.3-Tablas_oro.png)

## 10. Reproducibilidad

Para replicar los dashboards:

Descargar el archivo .pbix desde el repositorio.

1) Crear o reutilizar una cuenta de servicio con permisos equivalentes.

2) Generar una clave JSON.

3) Reconfigurar el origen de datos en Power BI.

4) Actualizar el modelo y visualizar los KPIs.

