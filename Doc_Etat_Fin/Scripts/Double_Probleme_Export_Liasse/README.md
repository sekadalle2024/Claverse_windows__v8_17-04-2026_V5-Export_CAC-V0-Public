# Scripts - Double Problème Export Liasse

## 📋 Description

Scripts de test pour reproduire et diagnostiquer les deux problèmes identifiés dans l'export de la liasse fiscale.

---

## 🚀 Scripts Disponibles

### test-double-probleme.ps1

Script PowerShell qui:
- Charge une balance de test
- Génère les états financiers
- Tente l'export de la liasse
- Affiche le diagnostic des problèmes

**Usage:**
```powershell
.\test-double-probleme.ps1
```

---

## 📁 Scripts Python Associés

Les scripts Python sont situés dans `py_backend/`:

### test_export_double_probleme.py

Script Python qui reproduit les problèmes:
- Charge une balance de démonstration
- Génère les états financiers
- Tente l'export Excel
- Affiche les diagnostics détaillés

**Usage:**
```bash
cd ../../py_backend
python test_export_double_probleme.py
```

---

## 🔍 Ce Que Les Scripts Testent

### Problème 1: États de Contrôle
- Vérifie le nombre d'états générés (attendu: 16)
- Compare avec les états du frontend
- Identifie les états manquants

### Problème 2: Valeurs Non Renseignées
- Vérifie les cellules dans ACTIF
- Vérifie les cellules dans PASSIF
- Vérifie les cellules dans RESULTAT
- Identifie les cellules vides

---

## 📊 Résultats Attendus

Les scripts affichent:
- ✅ Nombre d'états de contrôle générés
- ✅ Liste des états présents/absents
- ✅ Nombre de cellules renseignées par onglet
- ✅ Liste des cellules vides
- ✅ Diagnostic des causes

---

## 🔗 Documentation Associée

Pour comprendre les résultats:
- `../../Documentation/Double_Probleme_Export_Liasse/00_COMMENCER_ICI.txt`
- `../../Documentation/Double_Probleme_Export_Liasse/00_DIAGNOSTIC_DOUBLE_PROBLEME_05_AVRIL_2026.txt`

Pour les corrections:
- `../../py_backend/CORRECTION_ETATS_CONTROLE_05_AVRIL_2026.md`
- `../../py_backend/CORRECTION_VALEURS_ETATS_FINANCIERS_05_AVRIL_2026.md`

---

## 💡 Notes

- Les scripts utilisent des données de test
- Aucune modification n'est apportée aux fichiers source
- Les résultats sont affichés dans la console
- Les fichiers Excel générés sont temporaires

---

**Dernière mise à jour:** 05 AVRIL 2026
