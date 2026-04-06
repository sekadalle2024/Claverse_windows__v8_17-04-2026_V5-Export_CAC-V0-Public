# Script PowerShell pour tester le double problème
# 05 AVRIL 2026

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "TEST DOUBLE PROBLÈME - EXPORT LIASSE" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que Python est disponible
Write-Host "Vérification de Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Python OK" -ForegroundColor Green
Write-Host ""

# Aller dans le dossier py_backend
Write-Host "Navigation vers py_backend..." -ForegroundColor Yellow
cd py_backend
Write-Host "✅ Dossier py_backend" -ForegroundColor Green
Write-Host ""

# Exécuter le script de test
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "EXÉCUTION DU TEST" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

python test_export_double_probleme.py

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "TEST TERMINÉ" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Retour au dossier racine
cd ..

Write-Host "📋 Prochaines étapes:" -ForegroundColor Yellow
Write-Host "   1. Lire: 00_DIAGNOSTIC_DOUBLE_PROBLEME_05_AVRIL_2026.txt" -ForegroundColor White
Write-Host "   2. Lire: QUICK_START_CORRECTION_DOUBLE_PROBLEME.txt" -ForegroundColor White
Write-Host "   3. Appliquer les corrections dans:" -ForegroundColor White
Write-Host "      - py_backend/generer_onglet_controle_coherence.py" -ForegroundColor White
Write-Host "      - py_backend/export_liasse.py" -ForegroundColor White
Write-Host ""
