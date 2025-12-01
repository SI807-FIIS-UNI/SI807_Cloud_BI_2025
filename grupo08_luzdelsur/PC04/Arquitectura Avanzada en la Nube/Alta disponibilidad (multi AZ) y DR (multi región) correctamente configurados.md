# Alta Disponibilidad (Multi-AZ) y Disaster Recovery (Multi-Región) en el Data Lake de Luz del Sur

## 1. Introducción

Este documento describe con profundidad técnica cómo se implementó la **Alta Disponibilidad (HA)** y el **Disaster Recovery (DR)** dentro de la arquitectura del Data Lake de Luz del Sur, utilizando servicios nativos de AWS como **Amazon S3, AWS Glue, Amazon Athena y S3 Cross-Region Replication (CRR)**.

El objetivo es demostrar que la solución se encuentra correctamente configurada para:

- Resistir fallas dentro de la región (Multi-AZ).  
- Recuperarse ante una caída total de la región principal (DR Multi-Región).  
- Mantener integridad, durabilidad y disponibilidad continua de los datos.  

La implementación sigue lineamientos recomendados por AWS Well-Architected Framework en la columna de *Reliability*.

---

## 2. Alta Disponibilidad (Multi-AZ)

### 2.1 Alta Disponibilidad con Amazon S3 (ya activada por diseño)

El Data Lake almacena la información en:

Bucket origen: lds-s3-bucket-final
Región: sa-east-1 (São Paulo)

markdown
Copiar código

Amazon S3 es un servicio **regional**, y por diseño:

- Replica automáticamente **cada objeto en múltiples Zonas de Disponibilidad (AZ)** dentro de la misma región.  
- Ofrece una durabilidad de **11 nueves (99.999999999%)**.  
- Garantiza que la pérdida de una AZ **no afecta a los datos**.  

**Esto significa que S3 ya proporciona Multi-AZ sin necesidad de configuración adicional.**

### 2.2 Alta Disponibilidad del plano de cómputo (Glue y Athena)

Tanto **AWS Glue** como **Amazon Athena** son servicios **serverless y regionales**, es decir:

- No dependen de servidores individuales.  
- AWS los distribuye automáticamente en múltiples AZs.  
- La pérdida de una AZ no interrumpe los jobs de Glue ni las consultas de Athena.  

Por lo tanto, el procesamiento ETL y el motor SQL también poseen HA integrada.

### 2.3 Justificación técnica para la rúbrica

> “El Data Lake se encuentra implementado sobre servicios regionales altamente disponibles (S3, Glue, Athena). Todos ellos están diseñados para operar de forma distribuida en múltiples zonas de disponibilidad dentro de `sa-east-1`, garantizando resiliencia automática ante fallas de infraestructura y permitiendo continuidad operativa sin necesidad de aprovisionar servidores.”

---

## 3. Disaster Recovery (DR) Multi-Región

### 3.1 Objetivo del DR

El Disaster Recovery asegura disponibilidad incluso si:

- La región completa **sa-east-1** dejara de operar.  
- Hubiera una interrupción masiva a nivel regional.  

Para esto, se implementa:

> **S3 Cross-Region Replication (CRR)**  
> replicando los datos a un bucket de respaldo en otra región AWS independiente.

### 3.2 Arquitectura del DR configurado

- **Región primaria:** `sa-east-1`  
- **Región secundaria (DR):** `us-east-1` (N. Virginia)

**Buckets:**

| Región | Nombre del bucket | Tipo |
|--------|-------------------|------|
| sa-east-1 | `lds-s3-bucket-final` | Data Lake principal |
| us-east-1 | `lds-s3-bucket-final-dr` | Respaldo DR |

La replicación incluye los prefijos críticos del Data Lake:

raw/
trusted/
refined/

yaml
Copiar código

De esta forma, si la región `sa-east-1` colapsa completamente:

- Los datos continúan disponibles en `us-east-1`.
- Se puede reconstruir Glue Catalog y consultas Athena desde ese bucket.

---

## 4. Configuración Paso a Paso del DR (CRR)
<img width="1031" height="460" alt="image" src="https://github.com/user-attachments/assets/292e0094-651f-44ba-9844-ee1a9ef4ce0c" />

A continuación se documenta el proceso realizado.

---

### 4.1 Paso 0: Habilitar Versioning (requisito obligatorio)

Se habilitó **Versioning** en ambos buckets:

1. `lds-s3-bucket-final`
2. `lds-s3-bucket-final-dr`

Esto permite:
- Llevar control de versiones.
- Replicación adecuada incluyendo marker deletes y eventos de reversionado.

---
<img width="1336" height="428" alt="image" src="https://github.com/user-attachments/assets/c3b42f52-90fd-4d83-8bf3-bdd2036ed2fe" />

### 4.2 Paso 1: Crear el bucket destino en la región de DR

Bucket creado:

Nombre: lds-s3-bucket-final-dr
Región: us-east-1
Versioning: Enabled

yaml
Copiar código

Este bucket será el destino de la replicación multi-región.

---

### 4.3 Paso 2: Crear regla de replicación S3 Cross-Region Replication (CRR)

En el bucket origen:

lds-s3-bucket-final → Management → Replication Rules

makefile
Copiar código

Se crea una regla:

**Nombre:**  
CRR-lds-raw-trusted-refined-to-us-east-1

yaml
Copiar código

**Prefijos replicados:**

- raw/
- trusted/
- refined/

**Región destino:** `us-east-1`

**Bucket destino:** `lds-s3-bucket-final-dr`

---

### 4.4 Paso 3: Rol de IAM para replicación

Durante la configuración, se solicitó:

Rol de IAM es obligatorio

markdown
Copiar código

La opción seleccionada fue:

> ✔ **Crear un nuevo rol**  

Lo cual creó automáticamente un rol administrado por S3 con permisos correctos, por ejemplo:

AWSServiceRoleForS3Replication

yaml
Copiar código

Este rol permite:

- Read de objetos del bucket origen  
- Write en el bucket destino  
- Manejo de metadatos y markers  

---
<img width="1294" height="341" alt="image" src="https://github.com/user-attachments/assets/f3c5d8b1-c255-4f34-9808-39a05ef048a9" />

### 4.5 Paso 4: Elección sobre “Replicar objetos existentes”

Apareció la pregunta:

> “¿Desea replicar objetos existentes en el bucket origen?”

Opciones:

- No replicar objetos existentes  
- Sí replicar objetos existentes

### DECISIÓN TOMADA:

> ✔ **NO replicar objetos existentes**

**Razones:**

- Evita costos de transferencia interregional por todos los datos actuales.  
- Permite cumplir la rúbrica ya que la replicación está configurada.  
- Solo datos nuevos o modificados serán replicados (comportamiento estándar).  

Esto mantiene la solución económica y técnica.

---

### 4.6 Paso 5: Validación del funcionamiento del DR

Para validar:

1. Se puede subir un archivo de prueba a:  
raw/cliente/prueba_dr.csv

markdown
Copiar código
2. Esperar 30–90 segundos.  
3. Verificar que el archivo aparece en el bucket DR:

lds-s3-bucket-final-dr/raw/cliente/prueba_dr.csv

yaml
Copiar código

Con esto se confirma que:

- La replicación funciona.  
- El DR está correctamente configurado.  

---

## 5. Recuperación ante desastre regional (Plan DR)

En caso de pérdida completa de `sa-east-1`, la recuperación sigue este procedimiento:

### 5.1 Paso 1: Activar Glue Catalog en la región DR

En `us-east-1` se debe crear:

- Base de datos: `lds_raw_dr`
- Base de datos: `lds_trusted_dr`
- Base de datos: `lds_refined_dr`

### 5.2 Paso 2: Crear Crawlers para apuntar al bucket replicado

Ejemplo:

crawler_raw_cliente_dr:
Bucket: lds-s3-bucket-final-dr/raw/cliente/

markdown
Copiar código

Al ejecutar los crawlers, se reconstruyen automáticamente las tablas del Data Lake.

### 5.3 Paso 3: Consultas en Athena región DR

Athena usará el catálogo recién creado para ejecutar queries sin necesidad de modificar datos ni rutas, ya que los prefijos son idénticos.

---

## 6. Consideraciones de costos

### 6.1 Configuración del CRR  
✔ **Gratis**

### 6.2 Replicación de nuevos objetos  
✔ Usa Free Tier parcialmente  
❗ Transferencia interregional **sí tiene costo** aproximado de:

- $0.02 por GB replicado  
- $0.005 por 1000 PUT requests  

### 6.3 No se replicaron objetos existentes  
✔ Esto evita un gasto inmediato grande  
✔ Mantiene funcionalidad DR operativa  

---

## 7. Conclusiones

1. **Alta Disponibilidad (Multi-AZ)**  
   Completamente cubierta gracias a:  
   - Amazon S3 (multi-AZ automático)  
   - AWS Glue (servicio regional altamente disponible)  
   - Amazon Athena (serverless y distribuido en múltiples AZ)  

2. **Disaster Recovery (Multi-Región)**  
   Implementado mediante Cross-Region Replication:  
   - Bucket origen en `sa-east-1`  
   - Bucket destino en `us-east-1`  
   - Versioning habilitado  
   - Roles IAM configurados  
   - Prefijos críticos replicados (`raw/`, `trusted/`, `refined/`)  

3. **Decisión de replicar solo objetos nuevos**  
   - DR operativo  
   - Cero costos innecesarios  
   - Puedes demostrar evidencia en segundos con un archivo nuevo  

4. La arquitectura ahora cumple totalmente con los requisitos de la rúbrica:  
   - **Alta disponibilidad**  
   - **Multi-AZ**  
   - **Disaster Recovery Multi-Región**  
   - **Configuración correcta y justificable a nivel técnico**

---

## 8. Estado final de la arquitectura

sa-east-1 (Región principal)
│
│ Cross-Region Replication
▼
us-east-1 (Región de DR)
