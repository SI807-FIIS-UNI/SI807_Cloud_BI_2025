# Informe Técnico: Implementación de Cifrado (KMS/CMEK)

**Proyecto:** Seguridad de Datos y Cumplimiento Normativo  
**Región:** sa-east-1 (São Paulo)  
**Recurso:** AWS Key Management Service (KMS)  
**ID de Llave:** `mrk-27c0e9effd814c3ea91087a6fd6a723c`  

---

## 1. Resumen Ejecutivo

Se ha implementado una estrategia de seguridad de datos centrada en el uso de **Llaves Administradas por el Cliente (CMEK - Customer Managed Keys)**. A diferencia de las llaves gestionadas por AWS por defecto, esta implementación otorga control total sobre el ciclo de vida, la rotación y los permisos de acceso de las llaves criptográficas.

El recurso desplegado (`KMSKeyDemo`) servirá como la raíz de confianza para proteger la confidencialidad de la información tanto en reposo (bases de datos, buckets S3) como en los procesos de integración de datos.

---

## 2. Especificaciones Técnicas del Recurso

Se ha provisionado una llave simétrica de alta disponibilidad con capacidad multi-región, lo que permite futuras estrategias de recuperación ante desastres (DR) sin necesidad de re-encriptar los datos al replicarlos a otra región.

| Parámetro | Configuración Implementada | Detalles Técnicos |
| :--- | :--- | :--- |
| **Alias** | `KMSKeyDemo` | Nombre amigable para fácil identificación en código y consola. |
| **Key ID** | `mrk-27c0e9effd814c3ea91087a6fd6a723c` | Identificador único global (ARN). |
| **Tipo de Llave** | `Simétrico` | Cifrado de llave única (misma llave para cifrar y descifrar). |
| **Especificación** | `SYMMETRIC_DEFAULT` | Algoritmo estándar AES-256-GCM. |
| **Uso de Llave** | `Cifrado y descifrado` | Protección de volúmenes de datos y objetos. |
| **Regionalidad** | `Multi-Region (Primary)` | Llave maestra que puede ser replicada a otras regiones AWS. |

---

## 3. Modelo de Seguridad y Control de Acceso

La seguridad de la llave se ha definido bajo el principio de separación de privilegios, distinguiendo entre quién puede *administrar* la llave (configurarla/borrarla) y quién puede *usarla* (cifrar datos).

### 3.1. Administradores de la Llave (Key Admins)
Usuarios con permisos para editar las políticas de confianza, habilitar/deshabilitar la llave o programar su eliminación.

* `admin-Mikhael-1`
* `admin-Frey-1`

### 3.2. Usuarios de la Llave (Key Users)
Entidades autorizadas para realizar operaciones criptográficas (`kms:Encrypt`, `kms:Decrypt`, `kms:GenerateDataKey`) desde servicios integrados o vía SDK.

* `admin-Frey-1`
* `admin-Mikhael-1`
* *(Nota: Se recomienda añadir aquí los Roles de Servicio, como el de Glue o Lambda, para que las aplicaciones puedan usar esta llave).*

---

## 4. Estrategia de Cifrado Implementada

### 4.1. Cifrado en Reposo (Data at Rest)
Esta llave CMEK se utilizará para sustituir las llaves por defecto en los servicios de almacenamiento.
* **Funcionamiento:** Cuando se guarda un archivo en S3 o un dato en RDS, AWS utiliza esta llave (`mrk-27c0...`) para generar una "Data Key" única que cifra el contenido real (Cifrado de Sobre).
* **Beneficio:** Si un actor malintencionado obtiene acceso físico a los discos de AWS, no podrá leer la información sin acceso a esta llave maestra en KMS.

### 4.2. Cifrado en Tránsito y Uso
Aunque TLS (HTTPS) protege los datos mientras viajan por la red, KMS añade una capa de seguridad lógica.
* **Integridad:** Asegura que solo los servicios autorizados en la política de la llave puedan descifrar los datos una vez llegan a su destino.
* **Auditoría:** Cada vez que se descifra un dato en tránsito (por ejemplo, Glue leyendo de S3), CloudTrail registra la llamada a `kms:Decrypt`, permitiendo trazar exactamente quién y cuándo accedió a la información sensible.

---

## 5. Conclusión

La creación de la llave `KMSKeyDemo` establece una base sólida para el cumplimiento normativo (Compliance). Al utilizar una llave **Multi-Region (MRK)** y gestionada por el cliente, la organización asegura:

1.  **Soberanía del Dato:** Control total sobre quién puede acceder a la información, independiente de AWS.
2.  **Resiliencia:** Capacidad de extender la seguridad a otras regiones geográficas.
3.  **Auditoría:** Trazabilidad completa del acceso a datos sensibles.

El recurso se encuentra en estado **Habilitado** y listo para ser asociado a servicios como S3, EBS, RDS y Glue.