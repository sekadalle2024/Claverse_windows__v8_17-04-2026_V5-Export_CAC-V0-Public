# Script de Demarrage Claraverse avec Conda
# Version: 1.0.0

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "DEMARRAGE CLARAVERSE - Backend Conda + Frontend React" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

$ENV_NAME = "claraverse_backend"
$BACKEND_DIR = "py_backend"
$BACKEND_PORT = 5000
$FRONTEND_PORT = 5173

# Verifications
Write-Host "Verifications prealables..." -ForegroundColor Yellow
Write-Host ""

# Verifier conda
Write-Host "Verification de conda..." -NoNewline
try {
    $condaVersion = & conda --version 2>&1
    Write-Host " OK $condaVersion" -ForegroundColor Green
} catch {
    Write-Host " ERREUR conda non trouve!" -ForegroundColor Red
    exit 1
}

# Verifier environnement
Write-Host "Verification de l'environnement '$ENV_NAME'..." -NoNewline
$envExists = conda env list | Select-String -Pattern $ENV_NAME -Quiet

if (-not $envExists) {
    Write-Host " NON TROUVE!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Executez d'abord: .\setup-backend-env.ps1" -ForegroundColor Yellow
    exit 1
}
Write-Host " OK" -ForegroundColor Green

# Verifier Node.js
Write-Host "Verification de Node.js..." -NoNewline
try {
    $nodeVersion = & node --version 2>&1
    Write-Host " OK $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host " ERREUR Node.js non trouve!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Toutes les verifications sont passees!" -ForegroundColor Green
Write-Host ""

# Demarrage Backend avec conda
Write-Host "Demarrage du Backend Python (conda env: $ENV_NAME)..." -ForegroundColor Yellow
Write-Host "   Dossier: $BACKEND_DIR" -ForegroundColor Gray
Write-Host "   Port: $BACKEND_PORT" -ForegroundColor Gray
Write-Host ""

$backendJob = Start-Job -ScriptBlock {
    param($envName, $dir)
    Set-Location $dir
    conda run -n $envName python main.py
} -ArgumentList $ENV_NAME, (Resolve-Path $BACKEND_DIR)

Write-Host "Backend demarre (Job ID: $($backendJob.Id))" -ForegroundColor Green
Write-Host ""

# Attendre le backend
Write-Host "Attente du demarrage du backend (10 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verifier le backend
Write-Host "Verification du backend..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:$BACKEND_PORT/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host " Backend operationnel!" -ForegroundColor Green
} catch {
    Write-Host " Backend en cours de demarrage..." -ForegroundColor Yellow
    Write-Host "Verifiez les logs: Receive-Job -Id $($backendJob.Id) -Keep" -ForegroundColor Gray
}

Write-Host ""

# Demarrage Frontend
Write-Host "Demarrage du Frontend React..." -ForegroundColor Yellow
Write-Host "   Port: $FRONTEND_PORT" -ForegroundColor Gray
Write-Host ""

$frontendJob = Start-Job -ScriptBlock {
    param($workDir)
    Set-Location $workDir
    npm run dev
} -ArgumentList (Get-Location).Path

Write-Host "Frontend demarre (Job ID: $($frontendJob.Id))" -ForegroundColor Green
Write-Host ""

# Informations
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "CLARAVERSE DEMARRE AVEC SUCCES!" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "SERVICES ACTIFS:" -ForegroundColor Green
Write-Host ""
Write-Host "   Backend Python (Conda: $ENV_NAME)" -ForegroundColor Yellow
Write-Host "      URL: http://127.0.0.1:$BACKEND_PORT" -ForegroundColor White
Write-Host "      Job ID: $($backendJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "   Frontend React" -ForegroundColor Yellow
Write-Host "      URL: http://localhost:$FRONTEND_PORT" -ForegroundColor White
Write-Host "      Job ID: $($frontendJob.Id)" -ForegroundColor Gray
Write-Host ""

Write-Host "COMMANDES UTILES:" -ForegroundColor Cyan
Write-Host "   Logs backend: Receive-Job -Id $($backendJob.Id) -Keep" -ForegroundColor White
Write-Host "   Logs frontend: Receive-Job -Id $($frontendJob.Id) -Keep" -ForegroundColor White
Write-Host "   Arreter: .\stop-claraverse.ps1" -ForegroundColor White
Write-Host ""

# Sauvegarder les IDs
$jobIds = @{
    Backend = $backendJob.Id
    Frontend = $frontendJob.Id
}
$jobIds | ConvertTo-Json | Out-File -FilePath ".claraverse-jobs.json" -Encoding UTF8

Write-Host "Pret a utiliser! Ouvrez http://localhost:$FRONTEND_PORT" -ForegroundColor Green
Write-Host ""
