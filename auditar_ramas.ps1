# ============================================================
# Auditoría de ramas para evaluación de alumnos
# Repositorio: SI807_Cloud_BI_2025
# Organización: SI807-FIIS-UNI
# Autor: WebConceptos (Fernando García Atuncar)
# ============================================================

# CONFIGURACIÓN
$org = "SI807-FIIS-UNI"
$repo = "SI807_Cloud_BI_2025"
$token = "ghp_TU_TOKEN"   # Reemplazar por tu token personal

$baseUri = "https://api.github.com/repos/$org/$repo"
$headers = @{ Authorization = "token $token"; "User-Agent" = "PowerShell" }

# FUNCIÓN PARA LLAMAR A API DE GITHUB
function Call-GitHubApi {
    param(
        [string]$Url
    )
    try {
        return Invoke-RestMethod -Uri $Url -Headers $headers
    }
    catch {
        Write-Host "Error consultando: $Url" -ForegroundColor Yellow
        return $null
    }
}

# CONSULTAR TODAS LAS RAMAS
$branches = Call-GitHubApi "$baseUri/branches"

if (-not $branches) {
    Write-Host "No se pudieron obtener las ramas." -ForegroundColor Red
    exit
}

# RESULTADOS
$resultados = @()

foreach ($b in $branches) {

    $branchName = $b.name
    Write-Host "Procesando rama: $branchName"

    # OBTENER ÚLTIMO COMMIT
    $lastCommitSha = $b.commit.sha
    $lastCommit = Call-GitHubApi "$baseUri/commits/$lastCommitSha"

    $lastAuthor = $lastCommit.commit.author.name
    $lastDate   = $lastCommit.commit.author.date

    # OBTENER TODOS LOS COMMITS DE ESA RAMA
    $allCommits = Call-GitHubApi "$baseUri/commits?sha=$branchName"

    if ($allCommits -and $allCommits.Count -gt 0) {
        # PRIMER COMMIT (CREACIÓN DE RAMA)
        $firstCommit = $allCommits[$allCommits.Count - 1]
        $firstAuthor = $firstCommit.commit.author.name
        $firstDate   = $firstCommit.commit.author.date
        $totalCommits = $allCommits.Count
    }
    else {
        $firstAuthor = "No disponible"
        $firstDate   = "No disponible"
        $totalCommits = 0
    }

    # ARMAR RESULTADO
    $result = [PSCustomObject]@{
        Rama                 = $branchName
        Autor_Primer_Commit  = $firstAuthor
        Fecha_Creacion_Rama  = $firstDate
        Autor_Ultimo_Commit  = $lastAuthor
        Fecha_Ultimo_Commit  = $lastDate
        Total_Commits        = $totalCommits
    }

    $resultados += $result
}

# MOSTRAR EN CONSOLA
$resultados | Format-Table -AutoSize

# EXPORTAR A CSV (para tu evaluación)
$csvPath = "auditoria_ramas.csv"
$resultados | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

Write-Host ""
Write-Host "Auditoría completada. Archivo generado: $csvPath" -ForegroundColor Green
