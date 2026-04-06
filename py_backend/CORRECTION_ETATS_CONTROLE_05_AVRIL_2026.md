# CORRECTION ÉTATS DE CONTRÔLE - 05 AVRIL 2026

## PROBLÈME IDENTIFIÉ

La fonction `generer_etats_controle_pour_export()` dans `generer_onglet_controle_coherence.py` génère seulement 8 états simplifiés au lieu des 16 états exhaustifs utilisés en frontend.

## SOLUTION

Remplacer la fonction `generer_etats_controle_pour_export()` pour qu'elle génère EXACTEMENT les 16 mêmes états que le frontend.

### Changements à apporter:

1. **Utiliser la même source**: `etats_controle_exhaustifs.py` (fonction `generer_controles_exhaustifs`)
2. **Générer les 16 états complets**:
   - États 1-8: Exercice N
   - États 9-16: Exercice N-1

3. **Structure identique au frontend**:
   - Même titres
   - Mêmes postes
   - Mêmes calculs

## FICHIER À MODIFIER

`py_backend/generer_onglet_controle_coherence.py`

Fonction: `generer_etats_controle_pour_export()`

## RÉFÉRENCE FRONTEND

Le frontend utilise:
- `etats_controle_exhaustifs.py` → `generer_controles_exhaustifs()`
- `etats_controle_exhaustifs_html.py` → `generate_all_16_etats_controle_html()`

L'export Excel doit utiliser LA MÊME SOURCE.
