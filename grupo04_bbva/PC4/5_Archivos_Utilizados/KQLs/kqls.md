## Para Datalake

1. Últimos 20 eventos en bronze
```bash
StorageBlobLogs
| where ObjectKey contains "/bronze/"
| project TimeGenerated, OperationName, StatusCode, ObjectKey
| order by TimeGenerated desc
| take 20
```

2. Errores en bronze
```bash
StorageBlobLogs
| where ObjectKey contains "/bronze/"
| extend StatusCodeInt = toint(StatusCode)
| where StatusCodeInt >= 400
| project TimeGenerated, OperationName, StatusCodeInt, ObjectKey
| take 20
```

3. Últimos 20 eventos en silver
```bash
StorageBlobLogs
| where ObjectKey contains "/silver/"
| project TimeGenerated, OperationName, StatusCode, ObjectKey
| order by TimeGenerated desc
| take 20
```

4. Errores en silver
```bash
StorageBlobLogs
| where ObjectKey contains "/silver/"
| extend StatusCodeInt = toint(StatusCode)
| where StatusCodeInt >= 400
| project TimeGenerated, OperationName, StatusCodeInt, ObjectKey
| take 20
```

## Para el postgres

1. Últimos 20 logs
```bash
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DBFORPOSTGRESQL"
| project TimeGenerated, OperationName, errorLevel_s, sqlerrcode_s, Message
| order by TimeGenerated desc
| take 20
```

2. Conexiones recibidas
```bash
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DBFORPOSTGRESQL"
| where Message contains "connection received"
| project TimeGenerated, Message
| take 20
```

3. Autenticaciones
```bash
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DBFORPOSTGRESQL"
| where Message contains "authenticated"
| project TimeGenerated, Message
| take 20
```

4. Desconexiones
```bash
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.DBFORPOSTGRESQL"
| where Message contains "disconnection"
| project TimeGenerated, Message
| take 20
```

## Para el containerapps

1. Últimos logs del backend
```bash
ContainerAppSystemLogs_CL
| project TimeGenerated, Reason_s, ContainerAppName_s, ReplicaName_s, Log_s
| order by TimeGenerated desc
| take 20
```

2. Logs de errores del backend
```bash
ContainerAppSystemLogs_CL
| where Log_s contains "ERROR" or Log_s contains "Exception"
| project TimeGenerated, ContainerAppName_s, ReplicaName_s, Log_s
| order by TimeGenerated desc
| take 20
```

3. Resumen de eventos por tipo
```bash
ContainerAppSystemLogs_CL
| summarize Count = count() by Reason_s
| order by Count desc
```

4. Últimos logs de escalado / sistema
```bash
ContainerAppSystemLogs_CL
| where Reason_s contains "Scale" 
      or Reason_s contains "Revision" 
      or Reason_s contains "Health"
| project TimeGenerated, Reason_s, ContainerAppName_s, Log_s
| order by TimeGenerated desc
| take 20
```

