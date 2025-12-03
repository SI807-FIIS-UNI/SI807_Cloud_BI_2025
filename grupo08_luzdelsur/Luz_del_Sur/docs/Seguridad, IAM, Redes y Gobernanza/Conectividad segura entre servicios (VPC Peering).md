# Informe Técnico: Conectividad Segura entre Servicios (VPC Peering)

## 1. Introducción
El objetivo de este documento es detallar la configuración de infraestructura de red implementada en AWS para establecer una conectividad privada y segura entre dos entornos aislados (VPC). La solución se basa en **VPC Peering**, permitiendo la comunicación directa entre instancias mediante direcciones IP privadas.

## 2. Inventario de Red (VPC)

Se han identificado dos Nubes Privadas Virtuales (VPC) en la región `sa-east-1` (São Paulo) que participan en esta arquitectura. Los bloques CIDR no se superponen, cumpliendo con el requisito fundamental para el emparejamiento.

### A. VPC Solicitante (Requester)
* **Nombre:** (VPC por defecto)
* **ID de VPC:** `vpc-011b2da7a917b3fac`
* **Bloque CIDR IPv4:** `172.31.0.0/16`
* **Estado:** `Available`
* **Rol:** Iniciador de la conexión.

### B. VPC Receptora (Accepter)
* **Nombre:** `proyecto-vpc`
* **ID de VPC:** `vpc-0871b57b7e8109d21`
* **Bloque CIDR IPv4:** `10.0.0.0/16`
* **Estado:** `Available`
* **Rol:** Red de destino para el proyecto.

## 3. Detalle de la Conexión de Emparejamiento (Peering)

Se ha establecido un recurso de interconexión para vincular ambas redes.

| Parámetro | Valor |
| :--- | :--- |
| **Nombre** | `Peering default-project` |
| **ID de Interconexión** | `pcx-0b31ecaa11841e90b` |
| **VPC Solicitante** | `vpc-011b2da7a917b3fac` |
| **VPC Receptora** | `vpc-0871b57b7e8109d21` |
| **Estado Actual** |  **Activo** |

> **Nota Crítica:** La conexión ha sido solicitada correctamente, pero el tráfico no puede fluir hasta que la solicitud sea explícitamente aceptada por la cuenta propietaria de la VPC receptora.

## 4. Recursos de Cómputo (EC2)

Las siguientes instancias se encuentran desplegadas y se beneficiarán de esta conectividad privada una vez finalizada la configuración:

* **Instancia:** `EC2 - project`
    * **ID:** `i-0be4dd7aa79463108`
    * **Estado:** `En ejecución`
    * **Tipo:** `t3.micro`
    * **Red:** Ubicada en `proyecto-vpc` (Rango 10.0.x.x)

* **Instancia:** `EC2 default` / `instance-in-vpc-default`
    * **Estado:** En ejecución / Terminada
    * **Red:** Ubicada en la VPC por defecto (Rango 172.31.x.x)

## 5. Diagnóstico y Próximos Pasos

Según la evidencia visual, la configuración está incompleta. Para lograr una conectividad funcional ("ping" exitoso o conexión TCP), se requieren las siguientes acciones:

1.  **Aceptar la Solicitud de Peering:**
    * Navegar a *VPC Dashboard* > *Peering Connections*.
    * Seleccionar `pcx-0b31ecaa11841e90b`.
    * Ejecutar: `Actions` > `Accept Request`.

2.  **Actualizar Tablas de Enrutamiento (Route Tables):**
    * **En la VPC Default:** Agregar ruta `10.0.0.0/16` -> Target: `pcx-0b31ecaa11841e90b`.
    * **En la VPC Proyecto:** Agregar ruta `172.31.0.0/16` -> Target: `pcx-0b31ecaa11841e90b`.

3.  **Configurar Security Groups:**
    * Permitir el tráfico entrante (ej. puerto 80, 443 o ICMP) en los grupos de seguridad de las instancias, especificando como origen el CIDR de la VPC opuesta.
