# Wait for workspace to be fully provisioned before configuring it
resource "time_sleep" "wait_for_workspace" {
  depends_on = [var.workspace_url] # Depende de que la URL del workspace esté disponible
  create_duration = "60s"
}

# Create Databricks Token
resource "databricks_token" "main" {
  depends_on       = [time_sleep.wait_for_workspace]
  comment          = "Terraform generated token"
  lifetime_seconds = 7776000 # 90 days
}

# Store Databricks configuration in Key Vault
resource "azurerm_key_vault_secret" "databricks_token" {
  name         = "databricks-token"
  value        = databricks_token.main.token_value
  key_vault_id = var.key_vault_id
}

resource "azurerm_key_vault_secret" "datalake_key" {
  name         = "datalake-key"
  value        = var.storage_account_key
  key_vault_id = var.key_vault_id
}