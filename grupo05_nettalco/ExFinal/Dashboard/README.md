# 🔐 Acceso Temporal a BigQuery mediante Service Account

## 1. Objetivo

Con el fin de permitir la reproducibilidad de los dashboards analíticos desarrollados para el proyecto **NETTALCO**, se habilitó un mecanismo de acceso temporal a los datos almacenados en **Google BigQuery**, orientado a herramientas externas de visualización como **Power BI** o **Looker Studio**.

Este acceso se implementa siguiendo buenas prácticas de seguridad en entornos Cloud, utilizando una **Service Account** con permisos mínimos y una **clave JSON temporal**.

---

## 2. Arquitectura de Autenticación

El esquema de acceso se define de la siguiente manera:

```
Herramienta BI (Power BI / Looker Studio)
            ↓
     Service Account (GCP)
            ↓
     IAM Roles (BigQuery)
            ↓
   Datasets Analíticos (BigQuery)
```

La clave JSON se utiliza únicamente como mecanismo de autenticación, mientras que la autorización se controla mediante políticas **IAM** a nivel de proyecto.

---

## 3. Service Account Configurada

**Nombre de la Service Account:**
```
powerbi-bigquery-temp
```

**Alcance del acceso:**
- Nivel: Proyecto GCP
- Recursos: Todos los datasets analíticos en BigQuery

**Roles asignados:**
- `roles/bigquery.dataViewer.ventas_netallco`  
  Permite lectura de tablas y vistas solo del conjunto de datos ventas_nettalco.
- `roles/bigquery.jobUser`  
  Permite la ejecución de consultas SQL.

> ⚠️ La Service Account no posee permisos de escritura ni administración.

---

## 4. Clave de Acceso (JSON Key)

La autenticación se realiza mediante una **JSON Key**, generada desde **Cloud Shell**, asociada exclusivamente a la Service Account definida.

**Características de la clave:**
- Tipo: Service Account JSON Key
- Uso: Autenticación desde herramientas BI
- Alcance: Solo lectura
- **Vigencia: 5 días**

La clave será revocada o eliminada una vez concluido el período de evaluación, reduciendo la superficie de exposición de credenciales.

---

## 5. Uso en Herramientas de Visualización

### Power BI
1. Abrir **Power BI Desktop**
2. Seleccionar **Get Data**
3. Elegir el conector **Google BigQuery**
4. Método de autenticación: **Service Account**
5. Cargar el archivo JSON proporcionado
6. Seleccionar el proyecto y dataset deseado

### Looker Studio
El acceso se realiza directamente mediante la configuración de credenciales de GCP o conexión autorizada al proyecto BigQuery correspondiente.

---

## 6. Buenas Prácticas de Seguridad

- La clave JSON **no se encuentra versionada** en el repositorio GitHub.
- El acceso se limita a operaciones de lectura y consulta.
- La Service Account y/o su clave serán eliminadas una vez finalizada la evaluación.
- Se sigue el principio de **mínimo privilegio** dentro del alcance definido para el proyecto.

---

## 7. Consideraciones Finales

Este mecanismo de acceso garantiza:
- Reproducibilidad de dashboards
- Seguridad de los datos
- Separación entre cuentas personales y acceso técnico
- Cumplimiento de estándares Cloud para proyectos analíticos
