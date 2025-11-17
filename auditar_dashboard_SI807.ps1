# ============================================================
# Auditoría completa + Dashboard HTML
# Curso: SI807 - UNI
# Repositorio: SI807_Cloud_BI_2025
# Autor: WebConceptos (Fernando García Atuncar)
# ============================================================

$org = "SI807-FIIS-UNI"
$repo = "SI807_Cloud_BI_2025"
$token = "ghp_TU_TOKEN_AQUI"   # Reemplazar aquí

$baseUri = "https://api.github.com/repos/$org/$repo"
$headers = @{ Authorization = "token $token"; "User-Agent" = "PowerShell" }

# Función API
function Call-GitHubApi {
    param([string]$Url)
    try { return Invoke-RestMethod -Uri $Url -Headers $headers }
    catch {
        Write-Host "Error consultando $Url"
        return $null
    }
}

# Obtener ramas
$branches = Call-GitHubApi "$baseUri/branches"

if (-not $branches) {
    Write-Host "No se pudieron obtener ramas."
    exit
}

$resultados = @()

foreach ($b in $branches) {

    $branchName = $b.name
    Write-Host "Procesando rama: $branchName"

    # Último commit
    $lastCommitSha = $b.commit.sha
    $lastCommit = Call-GitHubApi "$baseUri/commits/$lastCommitSha"

    $lastAuthor = $lastCommit.commit.author.name
    $lastDate   = $lastCommit.commit.author.date

    # Todos los commits
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

    # PRs
    $prs = Call-GitHubApi "$baseUri/pulls?state=all&base=main"
    $prsBranch = $prs | Where-Object { $_.head.ref -eq $branchName }

    $prCount        = $prsBranch.Count
    $prMerged       = ($prsBranch | Where-Object { $_.merged_at }).Count
    $prClosedNoMerge= ($prsBranch | Where-Object { $_.state -eq "closed" -and $_.merged_at -eq $null }).Count

    # Líneas cambiadas
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

    # Armar objeto final
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

# Exportar CSV
$csvFile = "auditoria_completa.csv"
$resultados | Export-Csv -Path $csvFile -NoTypeInformation -Encoding UTF8
Write-Host "Archivo CSV generado: $csvFile"

# ===================
# Generar HTML
# ===================

$htmlFile = "dashboard_auditoria_SI807.html"

# Construcción del HTML
$htmlHeader = @"
<!DOCTYPE html>
<html>
<head>
<title>Dashboard de Auditoría SI807</title>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { padding: 30px; }
.table thead th { background-color: #343a40; color: white; }
.card { margin-bottom: 20px; }
</style>
</head>
<body>

<h1 class="text-center">Dashboard de Auditoría SI807</h1>
<p class="text-center">Repositorio: $repo</p>
<hr>
"@

$htmlBody = "<div class='container'>"

# Tabla general
$htmlBody += "<h3>Resumen General</h3>"
$htmlBody += "<table class='table table-bordered table-sm'>"
$htmlBody += "<thead><tr>
<th>Rama</th>
<th>Creada</th>
<th>Primer Autor</th>
<th>Último Commit</th>
<th>Último Autor</th>
<th>Commits</th>
<th>PR Creados</th>
<th>PR Aprobados</th>
<th>PR Rechazados</th>
<th>Archivos Modificados</th>
<th>Líneas +</th>
<th>Líneas -</th>
</tr></thead><tbody>"

foreach ($r in $resultados) {
    $htmlBody += "<tr>
<td>$($r.Rama)</td>
<td>$($r.Fecha_Creacion_Rama)</td>
<td>$($r.Autor_Primer_Commit)</td>
<td>$($r.Fecha_Ultimo_Commit)</td>
<td>$($r.Autor_Ultimo_Commit)</td>
<td>$($r.Total_Commits)</td>
<td>$($r.PullRequests_Creados)</td>
<td>$($r.PR_Aprobados_Merged)</td>
<td>$($r.PR_Cerrados_SinMerge)</td>
<td>$($r.Archivos_Modificados)</td>
<td>$($r.Lineas_Agregadas)</td>
<td>$($r.Lineas_Eliminadas)</td>
</tr>"
}

$htmlBody += "</tbody></table>"

# Gráfico con Chart.js
$ramas = ($resultados.Rama | ConvertTo-Json)
$commits = ($resultados.Total_Commits | ConvertTo-Json)

$htmlBody += @"
<h3>Gráfico: Commits por Rama</h3>
<canvas id="chartCommits"></canvas>
<script>
const ctx = document.getElementById('chartCommits');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: $ramas,
        datasets: [{
            label: 'Commits por Rama',
            data: $commits,
            backgroundColor: 'rgba(54, 162, 235, 0.7)'
        }]
    }
});
</script>
</div>
"@

$htmlFooter = "</body></html>"

# Escribir archivo HTML
$htmlFull = $htmlHeader + $htmlBody + $htmlFooter
Set-Content -Path $htmlFile -Value $htmlFull -Encoding UTF8

Write-Host "Dashboard HTML generado: $htmlFile"
