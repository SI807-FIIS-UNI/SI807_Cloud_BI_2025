# Script PowerShell para validar la estructura del proyecto
# Uso: .\validate_project.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Validación del Proyecto Final" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0
$WarningCount = 0

# Función para verificar archivo
function Test-ProjectFile {
    param($Path, $Description)
    
    if (Test-Path $Path) {
        Write-Host "✓ $Description" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ $Description - NO ENCONTRADO" -ForegroundColor Red
        $script:ErrorCount++
        return $false
    }
}

# Función para verificar directorio
function Test-ProjectDir {
    param($Path, $Description)
    
    if (Test-Path $Path -PathType Container) {
        $FileCount = (Get-ChildItem $Path -File).Count
        Write-Host "✓ $Description ($FileCount archivos)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ $Description - NO ENCONTRADO" -ForegroundColor Red
        $script:ErrorCount++
        return $false
    }
}

Write-Host "1. Verificando Dashboard Plotly..." -ForegroundColor Yellow
Write-Host ""
Test-ProjectFile "dashboard_plotly\index.html" "  Dashboard HTML"
Test-ProjectFile "dashboard_plotly\styles.css" "  Estilos CSS"
Test-ProjectFile "dashboard_plotly\app.js" "  Lógica JavaScript"
Write-Host ""

Write-Host "2. Verificando Documentación..." -ForegroundColor Yellow
Write-Host ""
Test-ProjectDir "docs" "  Directorio de documentación"
Test-ProjectFile "docs\DOCUMENTACION_FINAL_PARTE1.md" "  Documentación Final (4 partes)"
Write-Host ""

Write-Host "3. Verificando Guías..." -ForegroundColor Yellow
Write-Host ""
Test-ProjectDir "guias" "  Directorio de guías"
Test-ProjectFile "guias\modelo_star_supermarket.puml" "  Modelo Star (PlantUML)"
Test-ProjectFile "guias\modelo_dimensiones_hechos.puml" "  Dimensiones/Hechos (PlantUML)"
Write-Host ""

Write-Host "4. Verificando Imágenes..." -ForegroundColor Yellow
Write-Host ""
if (Test-ProjectDir "imagenes" "  Directorio de imágenes") {
    $ImageCount = (Get-ChildItem "imagenes" -Filter "*.png","*.jpg" -File).Count
    if ($ImageCount -ge 19) {
        Write-Host "  ✓ $ImageCount imágenes encontradas (mínimo 19)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Solo $ImageCount imágenes (se esperan 19)" -ForegroundColor Yellow
        $script:WarningCount++
    }
}
Write-Host ""

Write-Host "5. Verificando Scripts..." -ForegroundColor Yellow
Write-Host ""
Test-ProjectFile "kaggle.py" "  Script principal Python"
Test-ProjectDir "scripts" "  Directorio de scripts"
Write-Host ""

Write-Host "6. Verificando Scripts de Utilidad..." -ForegroundColor Yellow
Write-Host ""
Test-ProjectFile "view_dashboard.ps1" "  Script para ver dashboard (PowerShell)"
Test-ProjectFile "start_server.ps1" "  Script servidor HTTP (PowerShell)"
Test-ProjectFile "view_dashboard.sh" "  Script para ver dashboard (Bash)"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resumen de Validación" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($ErrorCount -eq 0 -and $WarningCount -eq 0) {
    Write-Host "✓ Proyecto completamente validado" -ForegroundColor Green
    Write-Host "  Todos los componentes están presentes" -ForegroundColor Green
} elseif ($ErrorCount -eq 0) {
    Write-Host "⚠ Proyecto validado con advertencias" -ForegroundColor Yellow
    Write-Host "  Errores: $ErrorCount" -ForegroundColor Green
    Write-Host "  Advertencias: $WarningCount" -ForegroundColor Yellow
} else {
    Write-Host "✗ Validación fallida" -ForegroundColor Red
    Write-Host "  Errores: $ErrorCount" -ForegroundColor Red
    Write-Host "  Advertencias: $WarningCount" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Estructura esperada:" -ForegroundColor Cyan
Write-Host "  parte_final/" -ForegroundColor White
Write-Host "  ├── dashboard_plotly/    (3 archivos: HTML, CSS, JS)" -ForegroundColor White
Write-Host "  ├── docs/                (Documentación final)" -ForegroundColor White
Write-Host "  ├── guias/               (PlantUML y guías)" -ForegroundColor White
Write-Host "  ├── imagenes/            (19+ imágenes)" -ForegroundColor White
Write-Host "  ├── scripts/             (Scripts adicionales)" -ForegroundColor White
Write-Host "  └── *.ps1, *.sh          (Scripts de utilidad)" -ForegroundColor White
