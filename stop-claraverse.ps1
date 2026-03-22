# ============================================================================
# Script d'Arrêt Claraverse - Backend + Frontend
# ============================================================================
# Description: Arrête proprement le backend Python et le frontend React
# Version: 1.0.0
# Date: 2026-03-22
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🛑 ARRÊT CLARAVERSE - Backend Python + Frontend React" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# ARRÊT DES JOBS POWERSHELL
# ============================================================================

Write-Host "🔍 Recherche des jobs PowerShell actifs..." -ForegroundColor Yellow
Write-Host ""

# Essayer de charger les IDs depuis le fichier
$jobFile = ".claraverse-jobs.json"
$savedJobs = $null

if (Test-Path $jobFile) {
    Write-Host "📄 Fichier de jobs trouvé: $jobFile" -ForegroundColor Green
    try {
        $savedJobs = Get-Content $jobFile | ConvertFrom-Json
        Write-Host "   Backend Job ID: $($savedJobs.Backend)" -ForegroundColor White
        Write-Host "   Frontend Job ID: $($savedJobs.Frontend)" -ForegroundColor White
        Write-Host ""
    } catch {
        Write-Host "⚠️  Impossible de lire le fichier de jobs" -ForegroundColor Yellow
    }
}

# Arrêter les jobs sauvegardés
if ($savedJobs) {
    Write-Host "🛑 Arrêt des jobs sauvegardés..." -ForegroundColor Yellow
    
    $jobsToStop = @()
    
    if ($savedJobs.Backend) {
        $backendJob = Get-Job -Id $savedJobs.Backend -ErrorAction SilentlyContinue
        if ($backendJob) {
            $jobsToStop += $backendJob
            Write-Host "   Backend (Job $($savedJobs.Backend)): Trouvé" -ForegroundColor White
        }
    }
    
    if ($savedJobs.Frontend) {
        $frontendJob = Get-Job -Id $savedJobs.Frontend -ErrorAction SilentlyContinue
        if ($frontendJob) {
            $jobsToStop += $frontendJob
            Write-Host "   Frontend (Job $($savedJobs.Frontend)): Trouvé" -ForegroundColor White
        }
    }
    
    if ($jobsToStop.Count -gt 0) {
        Stop-Job -Job $jobsToStop -ErrorAction SilentlyContinue
        Remove-Job -Job $jobsToStop -ErrorAction SilentlyContinue
        Write-Host "✅ Jobs arrêtés: $($jobsToStop.Count)" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Aucun job actif trouvé" -ForegroundColor Gray
    }
    
    # Supprimer le fichier de jobs
    Remove-Item $jobFile -ErrorAction SilentlyContinue
    Write-Host ""
}

# Arrêter tous les autres jobs actifs
$jobs = Get-Job | Where-Object { $_.State -eq "Running" }

if ($jobs.Count -eq 0) {
    Write-Host "ℹ️  Aucun autre job PowerShell actif" -ForegroundColor Gray
} else {
    Write-Host "📋 Autres jobs actifs trouvés: $($jobs.Count)" -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($job in $jobs) {
        Write-Host "   Job ID: $($job.Id) - État: $($job.State)" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "🛑 Arrêt des autres jobs..." -ForegroundColor Yellow
    
    Stop-Job -Job $jobs -ErrorAction SilentlyContinue
    Remove-Job -Job $jobs -ErrorAction SilentlyContinue
    
    Write-Host "✅ Autres jobs arrêtés" -ForegroundColor Green
}

Write-Host ""

# ============================================================================
# ARRÊT DES PROCESSUS PAR PORT
# ============================================================================

Write-Host "🔍 Recherche des processus sur les ports 5000 et 5173..." -ForegroundColor Yellow
Write-Host ""

$ports = @(5000, 5173)
$processesKilled = 0

foreach ($port in $ports) {
    Write-Host "🔌 Port $port..." -NoNewline
    
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    
    if ($connections) {
        Write-Host " ⚠️  Utilisé" -ForegroundColor Yellow
        
        foreach ($conn in $connections) {
            $processId = $conn.OwningProcess
            $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
            
            if ($process) {
                Write-Host "   Arrêt du processus: $($process.Name) (PID: $processId)" -ForegroundColor White
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                $processesKilled++
            }
        }
    } else {
        Write-Host " ✅ Libre" -ForegroundColor Green
    }
}

Write-Host ""

if ($processesKilled -gt 0) {
    Write-Host "✅ $processesKilled processus arrêté(s)" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Aucun processus à arrêter" -ForegroundColor Gray
}

Write-Host ""

# ============================================================================
# VÉRIFICATION FINALE
# ============================================================================

Write-Host "🔍 Vérification finale..." -ForegroundColor Yellow
Write-Host ""

Start-Sleep -Seconds 2

$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
$port5173 = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue

Write-Host "   Port 5000 (Backend)..." -NoNewline
if ($port5000) {
    Write-Host " ⚠️  Toujours utilisé" -ForegroundColor Yellow
} else {
    Write-Host " ✅ Libre" -ForegroundColor Green
}

Write-Host "   Port 5173 (Frontend)..." -NoNewline
if ($port5173) {
    Write-Host " ⚠️  Toujours utilisé" -ForegroundColor Yellow
} else {
    Write-Host " ✅ Libre" -ForegroundColor Green
}

Write-Host ""

# ============================================================================
# RÉSUMÉ
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "✅ ARRÊT TERMINÉ" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

if (-not $port5000 -and -not $port5173) {
    Write-Host "✅ Tous les services sont arrêtés" -ForegroundColor Green
} else {
    Write-Host "⚠️  Certains services sont peut-être encore actifs" -ForegroundColor Yellow
    Write-Host "   Redémarrez votre ordinateur si nécessaire" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Pour redémarrer Claraverse:" -ForegroundColor Gray
Write-Host ".\start-claraverse.ps1" -ForegroundColor White
Write-Host ""
