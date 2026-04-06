# CORRECTION VALEURS ÉTATS FINANCIERS - 05 AVRIL 2026

## PROBLÈME IDENTIFIÉ

Aucune valeur n'est renseignée dans les onglets ACTIF, PASSIF, RESULTAT de l'export Excel, même pour le bilan actif.

## CAUSE

Les mappings de cellules dans `export_liasse.py` (MAPPING_BILAN_ACTIF, etc.) ne correspondent PAS aux références réelles des postes générés par `etats_financiers_v2.py`.

### Exemple du problème:

**Mapping actuel** (export_liasse.py):
```python
MAPPING_BILAN_ACTIF = {
    'AD': 'C10',   # Charges immobilisées
    'AE': 'C11',   # Frais de recherche
    ...
}
```

**Références réelles** (etats_financiers_v2.py):
Les postes utilisent les références SYSCOHADA standard comme:
- 'AA', 'AB', 'AC', 'AD', 'AE', etc. pour le bilan actif
- 'TA', 'TB', 'TC', etc. pour les charges
- 'RA', 'RB', 'RC', etc. pour les produits

## SOLUTION

### Option 1: Corriger les mappings
Mettre à jour les mappings pour qu'ils correspondent aux références réelles.

### Option 2: Utiliser la structure liasse complète
Charger `structure_liasse_complete.json` et utiliser les références de ce fichier.

### Option 3: Mapping dynamique
Au lieu de mappings statiques, parcourir les postes et les écrire dans l'ordre.

## FICHIER À MODIFIER

`py_backend/export_liasse.py`

Fonction: `remplir_liasse_officielle()`

## PRINCIPE FONDAMENTAL

**"Utiliser strictement nos propres formules et valeurs qui en découlent pour TOUTES les cellules concernées"**

- NE PAS utiliser les formules Excel du template
- Remplir TOUS les onglets avec NOS valeurs calculées
- Les valeurs doivent être identiques au menu accordéon frontend
