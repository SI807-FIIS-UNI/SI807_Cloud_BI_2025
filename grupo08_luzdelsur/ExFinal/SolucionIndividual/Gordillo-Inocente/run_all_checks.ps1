# Script PowerShell para ejecutar todas las validaciones del proyecto
# Uso: .\run_all_checks.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  VERIFICACIÓN COMPLETA DEL PROYECTO    ║" -ForegroundColor Cyan
Write-Host "║  Supermarket Sales - Análisis Final    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. Validar estructura del proyecto
Write-Host "[1/4] Validando estructura del proyecto..." -ForegroundColor Yellow
Write-Host ""
.\validate_project.ps1
Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Gray
Read-Host

# 2. Verificar dashboard
Write-Host ""
Write-Host "[2/4] Verificando componentes del dashboard..." -ForegroundColor Yellow
Write-Host ""

$DashboardFiles = @(
    @{Path="dashboard_plotly\index.html"; Name="HTML Principal"},
    @{Path="dashboard_plotly\styles.css"; Name="Estilos CSS"},
    @{Path="dashboard_plotly\app.js"; Name="JavaScript"}
)

foreach ($File in $DashboardFiles) {
    if (Test-Path $File.Path) {
        $Size = (Get-Item $File.Path).Length
        $Lines = (Get-Content $File.Path).Count
        Write-Host "  ✓ $($File.Name): $Lines líneas, $Size bytes" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $($File.Name): NO ENCONTRADO" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Gray
Read-Host

# 3. Verificar documentación
Write-Host ""
Write-Host "[3/4] Verificando documentación..." -ForegroundColor Yellow
Write-Host ""

$DocPath = "docs\DOCUMENTACION_FINAL_PARTE1.md"
if (Test-Path $DocPath) {
    $DocLines = (Get-Content $DocPath).Count
    $DocSize = (Get-Item $DocPath).Length
    
    Write-Host "  ✓ Documentación Final encontrada" -ForegroundColor Green
    Write-Host "    - Líneas: $DocLines" -ForegroundColor White
    Write-Host "    - Tamaño: $([math]::Round($DocSize/1024, 2)) KB" -ForegroundColor White
    
    # Buscar las 4 partes
    $Content = Get-Content $DocPath -Raw
    
    $Parte1 = $Content -match "Parte 1.*Ingesta"
    $Parte2 = $Content -match "Parte 2.*Medallion"
    $Parte3 = $Content -match "Parte 3.*Star"
    $Parte4 = $Content -match "Parte 4.*Dashboard"
    
    Write-Host ""
    Write-Host "  Partes encontradas:" -ForegroundColor Cyan
    Write-Host "    - Parte 1 (Ingesta/EDA): $(if($Parte1){'✓'}else{'✗'})" -ForegroundColor $(if($Parte1){'Green'}else{'Red'})
    Write-Host "    - Parte 2 (Medallion): $(if($Parte2){'✓'}else{'✗'})" -ForegroundColor $(if($Parte2){'Green'}else{'Red'})
    Write-Host "    - Parte 3 (Star/KPIs): $(if($Parte3){'✓'}else{'✗'})" -ForegroundColor $(if($Parte3){'Green'}else{'Red'})
    Write-Host "    - Parte 4 (Dashboard): $(if($Parte4){'✓'}else{'✗'})" -ForegroundColor $(if($Parte4){'Green'}else{'Red'})
    
    # Contar imágenes referenciadas
    $ImageRefs = ([regex]::Matches($Content, '!\[.*?\]\(imagenes/.*?\)')).Count
    Write-Host ""
    Write-Host "  Imágenes referenciadas: $ImageRefs" -ForegroundColor Cyan
} else {
    Write-Host "  ✗ Documentación NO encontrada" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Gray
Read-Host

# 4. Resumen final
Write-Host ""
Write-Host "[4/4] Resumen de Scripts Disponibles..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Scripts de utilidad creados:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  PowerShell (Windows):" -ForegroundColor White
Write-Host "    .\view_dashboard.ps1      - Abrir dashboard en navegador" -ForegroundColor Gray
Write-Host "    .\start_server.ps1        - Iniciar servidor HTTP local" -ForegroundColor Gray
Write-Host "    .\open_docs.ps1           - Abrir documentación" -ForegroundColor Gray
Write-Host "    .\validate_project.ps1    - Validar estructura" -ForegroundColor Gray
Write-Host "    .\run_all_checks.ps1      - Este script (verificación completa)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Bash/Git Bash (Linux/WSL):" -ForegroundColor White
Write-Host "    ./view_dashboard.sh       - Ver dashboard con servidor HTTP" -ForegroundColor Gray
Write-Host ""

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✓ VERIFICACIÓN COMPLETADA             ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Siguiente paso: Ejecuta .\view_dashboard.ps1 o .\start_server.ps1" -ForegroundColor Yellow
Write-Host ""
