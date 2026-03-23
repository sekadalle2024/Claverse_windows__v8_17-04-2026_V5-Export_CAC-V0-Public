# Correction de la Cohérence des Balances N, N-1, N-2

## Problème Identifié

Les balances générées précédemment avaient des variations **aléatoires indépendantes** pour chaque année, ce qui créait des incohérences :

- **Année N (2024)**: Variation aléatoire de -15% à +15%
- **Année N-1 (2023)**: Variation aléatoire de -10% à +10%
- **Année N-2 (2022)**: Variation aléatoire de -20% à +20%

Résultat : Un compte pouvait avoir une croissance de +50% entre N-2 et N-1, puis une baisse de -30% entre N-1 et N, ce qui n'est pas réaliste.

## Solution Implémentée

### 1. Variations Cohérentes par Compte

Chaque compte reçoit maintenant un **taux de croissance unique et stable** appliqué de manière cohérente :

```
Taux de croissance par compte: entre -5% et +15% par an
Formule: Valeur_N-X = Valeur_N / (1 + taux_croissance)^X
```

**Exemple:**
- Compte 101 avec taux de croissance +8% par an:
  - N-2 (2022): 100 000
  - N-1 (2023): 100 000 × 1.08 = 108 000
  - N (2024): 108 000 × 1.08 = 116 640

### 2. Avantages de cette Approche

✓ **Cohérence logique**: Chaque compte suit une trajectoire réaliste
✓ **Traçabilité**: On peut recalculer les valeurs précédentes
✓ **Réalisme**: Les taux de croissance sont constants par compte
✓ **Validabilité**: Les états financiers sont cohérents sur 3 ans

### 3. Fichiers Modifiés

#### `py_backend/create_balances_multi_exercices.py`
- Remplacé la fonction `apply_variation()` par `apply_coherent_variation()`
- Génère un facteur de croissance unique par compte
- Applique ce facteur de manière cohérente pour les 3 années

#### `py_backend/verify_balance_coherence.py` (NOUVEAU)
- Vérifie la cohérence des balances générées
- Calcule les taux de croissance réels
- Détecte les incohérences (écart > 50% entre deux périodes)
- Affiche un résumé de la cohérence

#### `test-verify-balances.ps1` (NOUVEAU)
- Script de test complet
- Génère les balances
- Vérifie la cohérence
- Affiche les résultats

## Utilisation

### Générer les balances cohérentes:
```powershell
python py_backend/create_balances_multi_exercices.py
```

### Vérifier la cohérence:
```powershell
python py_backend/verify_balance_coherence.py
```

### Test complet:
```powershell
.\test-verify-balances.ps1
```

## Résultats Attendus

Après exécution, vous devriez voir:

1. **Fichier généré**: `BALANCES_N_N1_N2.xlsx`
   - Onglet 1: Balance N (2024)
   - Onglet 2: Balance N-1 (2023)
   - Onglet 3: Balance N-2 (2022)

2. **Vérification**: Affichage des taux de croissance par compte
   - Croissance moyenne N-2 → N-1: ~X%
   - Croissance moyenne N-1 → N: ~X%
   - Aucun problème de cohérence majeur

## Validation

Les balances sont maintenant **cohérentes et réalistes** pour une entité sur 3 années consécutives.
