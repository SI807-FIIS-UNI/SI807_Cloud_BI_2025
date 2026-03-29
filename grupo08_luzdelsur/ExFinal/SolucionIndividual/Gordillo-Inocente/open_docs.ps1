# Script PowerShell para abrir la documentación final
# Uso: .\open_docs.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Documentación Final del Proyecto" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Archivo de documentación
$DocPath = "docs\DOCUMENTACION_FINAL_PARTE1.md"

# Verificar que existe
if (-not (Test-Path $DocPath)) {
    Write-Host "ERROR: No se encuentra $DocPath" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Documentación encontrada: $DocPath" -ForegroundColor Green
Write-Host ""

# Abrir en VS Code si está disponible
if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "Abriendo en VS Code..." -ForegroundColor Yellow
    code $DocPath
    Write-Host "✓ Documentación abierta en VS Code" -ForegroundColor Green
}
# Si no, abrir con editor predeterminado
else {
    Write-Host "Abriendo con editor predeterminado..." -ForegroundColor Yellow
    $FullPath = Resolve-Path $DocPath
    Start-Process $FullPath
    Write-Host "✓ Documentación abierta" -ForegroundColor Green
}

Write-Host ""
Write-Host "Contenido de la documentación:" -ForegroundColor Cyan
Write-Host "  - Parte 1: Ingesta y EDA completo" -ForegroundColor White
Write-Host "  - Parte 2: Arquitectura Medallion" -ForegroundColor White
Write-Host "  - Parte 3: Modelo Star y KPIs" -ForegroundColor White
Write-Host "  - Parte 4: Dashboard y Reproducibilidad" -ForegroundColor White
