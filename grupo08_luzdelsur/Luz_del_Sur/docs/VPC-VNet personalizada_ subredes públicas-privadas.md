# Informe Técnico: Diseño e Implementación de Arquitectura de Red (VPC)

**Proyecto:** Infraestructura Cloud AWS - Región São Paulo (sa-east-1)  
**ID de Recurso:** `vpc-0871b57b7e8109d21`  
**Elaborado por:** Equipo de Arquitectura Cloud

---

## 1. Resumen Ejecutivo

Este documento detalla la configuración de la Nube Virtual Privada (VPC) denominada **"proyecto-vpc"**. Se ha diseñado una arquitectura de red personalizada que cumple con los estándares de **Alta Disponibilidad (HA)** y **Seguridad en Capas**, distribuyendo recursos a través de múltiples Zonas de Disponibilidad (AZs) y segmentando el tráfico en subredes públicas y privadas.

El diseño asegura que los componentes expuestos a internet estén aislados de la lógica de negocio y bases de datos, las cuales residen en segmentos de red protegidos.

---

## 2. Configuración General de la VPC

Se ha establecido un bloque de direcciones IP lo suficientemente amplio para soportar la escalabilidad futura de la aplicación y servicios auxiliares.

| Parámetro | Valor Configurado | Descripción |
| :--- | :--- | :--- |
| **Nombre** | `proyecto-vpc` | Identificador del recurso. |
| **VPC ID** | `vpc-0871b57b7e8109d21` | ID único en AWS. |
| **Bloque CIDR IPv4** | `10.0.0.0/16` | Espacio total de direcciones (65,536 IPs disponibles). |
| **Región** | `sa-east-1` | América del Sur (São Paulo). |
| **Tenencia** | `Default` | Hardware compartido (estándar). |
| **DNS Hostnames** | `Habilitado` | Permite resolución de nombres DNS dentro de la red. |

---

## 3. Estrategia de Subredes (Subnetting)

La red se ha segmentado siguiendo una arquitectura **Multi-AZ (Zona de Disponibilidad Múltiple)** para garantizar redundancia. Si una zona de datos (ej. `sa-east-1a`) falla, la infraestructura en la segunda zona (`sa-east-1b`) mantiene el servicio activo.

### 3.1. Distribución por Zona y Tipo

Se han configurado **4 subredes en total**, divididas equitativamente:

#### Zona A (`sa-east-1a`)
* **Subred Pública:** `proyecto-subnet-public1-sa-east-1a`
    * **CIDR:** `10.0.0.0/20` (4,096 IPs)
    * **Uso:** Balanceadores de carga, Servidores Bastion, NAT Gateways.
* **Subred Privada:** `proyecto-subnet-private1-sa-east-1a`
    * **CIDR:** `10.0.128.0/20` (4,096 IPs)
    * **Uso:** Servidores de aplicaciones, Bases de datos, Servicios backend.

#### Zona B (`sa-east-1b`)
* **Subred Pública:** `proyecto-subnet-public2-sa-east-1b`
    * **CIDR:** `10.0.16.0/20` (4,096 IPs)
    * **Uso:** Redundancia para capa pública.
* **Subred Privada:** `proyecto-subnet-private2-sa-east-1b`
    * **CIDR:** `10.0.144.0/20` (4,096 IPs)
    * **Uso:** Redundancia para capa privada.

---

## 4. Enrutamiento y Conectividad

La diferenciación entre "Público" y "Privado" se define estrictamente mediante las Tablas de Enrutamiento asociadas.

### 4.1. Conectividad Pública (Internet Gateway)
Se ha desplegado un **Internet Gateway (IGW)** denominado `proyecto-igw` que actúa como la puerta de salida y entrada hacia internet.

* **Tabla de Rutas:** `proyecto-rtb-public`
* **Asociación:** Vinculada a las subredes `public1` y `public2`.
* **Ruta Clave:**
    * Destino: `0.0.0.0/0` (Todo el tráfico de internet).
    * Objetivo: `proyecto-igw`.

### 4.2. Conectividad Privada (Aislamiento)
Las subredes privadas tienen sus propias tablas de enrutamiento independientes para asegurar que **no sean accesibles directamente desde internet**.

* **Tablas de Rutas:** `proyecto-rtb-private1-sa-east-1a` y `proyecto-rtb-private2-sa-east-1b`.
* **Comportamiento:** No poseen ruta hacia el IGW (`0.0.0.0/0` -> `igw`). Esto protege las bases de datos de ataques directos externos.

### 4.3. Integración con Servicios AWS (VPC Endpoints)
Se observa en el mapa de recursos la implementación de un **Gateway Endpoint** para S3.

* **Recurso:** `proyecto-vpce-s3`
* **Función:** Permite que los servidores en las subredes privadas se comuniquen con **Amazon S3** de forma segura y directa a través de la red interna de AWS, sin necesidad de salir a internet pública ni usar NAT Gateways, optimizando costos y seguridad.

---

## 5. Diagrama Lógico de la Arquitectura

Basado en la configuración desplegada, la topología de red resultante es la siguiente:

1.  **Tráfico de Entrada:** Llega a través del `proyecto-igw`.
2.  **Capa Pública:** El tráfico es distribuido en las subredes `10.0.0.0/20` y `10.0.16.0/20`.
3.  **Capa Privada:** Los recursos en `10.0.128.0/20` y `10.0.144.0/20` operan aislados, recibiendo tráfico solo de la capa pública interna o accediendo a S3 vía el Endpoint.

---

## 6. Conclusión

La VPC `proyecto-vpc` ha sido provisionada exitosamente siguiendo las mejores prácticas del marco de trabajo "AWS Well-Architected Framework":

1.  **Seguridad:** Aislamiento estricto de cargas de trabajo mediante subredes privadas.
2.  **Fiabilidad:** Despliegue en dos zonas de disponibilidad físicas distintas.
3.  **Escalabilidad:** CIDR `/16` permite un crecimiento masivo de recursos IP.
4.  **Optimización:** Uso de Gateway Endpoint para acceso eficiente a almacenamiento S3.

Esta infraestructura está lista para el despliegue de aplicaciones y servicios.