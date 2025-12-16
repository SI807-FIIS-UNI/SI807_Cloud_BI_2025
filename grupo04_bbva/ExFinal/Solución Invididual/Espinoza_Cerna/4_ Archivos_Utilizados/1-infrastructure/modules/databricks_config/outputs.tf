output "token" {
  description = "Databricks token"
  value       = databricks_token.main.token_value
  sensitive   = true
}