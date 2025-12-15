# ============================================================
# Auditoría completa de repositorio SI807
# Incluye ramas, commits, PRs, autores, líneas modificadas.
# Repositorio: SI807_Cloud_BI_2025
# Organización: SI807-FIIS-UNI
# Autor: WebConceptos (Fernando García Atuncar)
# ============================================================

$org = "SI807-FIIS-UNI"
$repo = "SI807_Cloud_BI_2025"

# Reemplazar por tu token personal
$token = "ghp_TU_TOKEN_AQUI"

# Configuración general
$baseUri = "https://api.github.com/repos/$org/$repo"
$headers = @{ Authorization = "token $token"; "User-Agent" = "PowerShell" }

# Función API
function Call-GitHubApi {
    param([string]$Url)
    try {
        return Invoke-RestMethod -Uri $Url -Headers $headers
    }
    catch {
        Write-Host "Error consultando $Url"
        return $null
    }
}

# Obtener todas las ramas
$branches = Call-GitHubApi "$baseUri/branches"

if (-not $branches) {
    Write-Host "No se pudieron obtener ramas."
    exit
}

# Lista donde se guardarán los resultados finales
$resultados = @()

foreach ($b in $branches) {

    $branchName = $b.name
    Write-Host ""
    Write-Host "Procesando rama: $branchName"

    # Último commit
    $lastCommitSha = $b.commit.sha
    $lastCommit = Call-GitHubApi "$baseUri/commits/$lastCommitSha"

    $lastAuthor = $lastCommit.commit.author.name
    $lastDate   = $lastCommit.commit.author.date

    # Obtener commits de la rama
    $allCommits = Call-GitHubApi "$baseUri/commits?sha=$branchName"

    if ($allCommits -and $allCommits.Count -gt 0) {
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

    # Obtener Pull Requests relacionados a la rama
    $prs = Call-GitHubApi "$baseUri/pulls?state=all&base=main"
    $prsBranch = $prs | Where-Object { $_.head.ref -eq $branchName }

    $prCount        = $prsBranch.Count
    $prMerged       = ($prsBranch | Where-Object { $_.merged_at }).Count
    $prClosedNoMerge= ($prsBranch | Where-Object { $_.state -eq "closed" -and $_.merged_at -eq $null }).Count

    # Variables para líneas agregadas/eliminadas
    $totalAdditions = 0
    $totalDeletions = 0
    $totalFilesChanged = 0

    foreach ($pr in $prsBranch) {
        $prDetails = Call-GitHubApi $pr.url
        if ($prDetails) {
            $totalAdditions += $prDetails.additions
            $totalDeletions += $prDetails.deletions
            $totalFilesChanged += $prDetails.changed_files
        }
    }

    # Construcción del objeto de resultado
    $result = [PSCustomObject]@{
        Rama                   = $branchName
        Fecha_Creacion_Rama    = $firstDate
        Autor_Primer_Commit    = $firstAuthor
        Fecha_Ultimo_Commit    = $lastDate
        Autor_Ultimo_Commit    = $lastAuthor
        Total_Commits          = $totalCommits
        PullRequests_Creados   = $prCount
        PR_Aprobados_Merged    = $prMerged
        PR_Cerrados_SinMerge   = $prClosedNoMerge
        Archivos_Modificados   = $totalFilesChanged
        Lineas_Agregadas       = $totalAdditions
        Lineas_Eliminadas      = $totalDeletions
    }

    $resultados += $result
}

# Mostrar resumen en consola
$resultados | Format-Table -AutoSize

# Guardar CSV
$csvPath = "auditoria_completa.csv"
$resultados | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

Write-Host ""
Write-Host "Auditoría completa finalizada. Archivo generado: $csvPath"
