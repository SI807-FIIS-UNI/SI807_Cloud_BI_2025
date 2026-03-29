# Script PowerShell para visualizar el dashboard de Plotly
# Uso: .\view_dashboard.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Dashboard Supermarket Sales - Plotly" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Directorio del dashboard
$DashboardDir = "dashboard_plotly"
$IndexPath = Join-Path $DashboardDir "index.html"

# Verificar que existe el archivo
if (-not (Test-Path $IndexPath)) {
    Write-Host "ERROR: No se encuentra $IndexPath" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Dashboard encontrado: $IndexPath" -ForegroundColor Green
Write-Host ""

# Opción 1: Abrir directamente en el navegador predeterminado
Write-Host "Abriendo dashboard en el navegador..." -ForegroundColor Yellow
$FullPath = Resolve-Path $IndexPath
Start-Process $FullPath

Write-Host ""
Write-Host "✓ Dashboard abierto en navegador predeterminado" -ForegroundColor Green
Write-Host ""
Write-Host "Nota: Para mejor experiencia, usa un servidor HTTP local" -ForegroundColor Yellow
Write-Host "Ejecuta: .\start_server.ps1" -ForegroundColor Yellow
