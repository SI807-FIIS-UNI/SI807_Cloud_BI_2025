# Script PowerShell para iniciar servidor HTTP local
# Uso: .\start_server.ps1 [puerto]

param(
    [int]$Port = 8000
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Servidor HTTP - Dashboard Plotly" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Directorio del dashboard
$DashboardDir = "dashboard_plotly"

# Verificar que existe el directorio
if (-not (Test-Path $DashboardDir)) {
    Write-Host "ERROR: No se encuentra el directorio $DashboardDir" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Dashboard encontrado en: $DashboardDir" -ForegroundColor Green
Write-Host ""

# Cambiar al directorio del dashboard
Set-Location $DashboardDir

Write-Host "Iniciando servidor HTTP en puerto $Port..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Dashboard disponible en:" -ForegroundColor Green
Write-Host "  http://localhost:$Port" -ForegroundColor Cyan
Write-Host "  http://127.0.0.1:$Port" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Intentar iniciar servidor con Python
try {
    # Intentar con python
    if (Get-Command python -ErrorAction SilentlyContinue) {
        python -m http.server $Port
    }
    # Si no, intentar con python3
    elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
        python3 -m http.server $Port
    }
    else {
        Write-Host "ERROR: Python no está instalado" -ForegroundColor Red
        Write-Host ""
        Write-Host "Alternativa: Abre directamente el archivo index.html" -ForegroundColor Yellow
        Write-Host "Ejecuta: .\view_dashboard.ps1" -ForegroundColor Yellow
        exit 1
    }
}
catch {
    Write-Host "ERROR al iniciar servidor: $_" -ForegroundColor Red
    exit 1
}
