variable "workspace_url" {
  description = "URL del workspace de Databricks."
  type        = string
}

variable "storage_account_name" {
  description = "Nombre de la cuenta de almacenamiento a conectar."
  type        = string
}

variable "storage_account_key" {
  description = "Clave de acceso de la cuenta de almacenamiento."
  type        = string
  sensitive   = true
}

variable "key_vault_id" {
  description = "ID del Key Vault donde se guardarán los secretos."
  type        = string
}