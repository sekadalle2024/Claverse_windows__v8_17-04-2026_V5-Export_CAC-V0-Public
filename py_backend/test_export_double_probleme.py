# -*- coding: utf-8 -*-
"""
Script de test pour diagnostiquer le double problème:
1. États de contrôle incorrects
2. Valeurs non renseignées dans les états financiers
"""

import pandas as pd
import json
from etats_financiers_v2 import process_balance_to_liasse_format, load_structure_liasse_complete
from export_liasse import remplir_liasse_officielle
from generer_onglet_controle_coherence import generer_etats_controle_pour_export

# Charger une balance de test
balance_file = "Balance_demo.xlsx"
balance_df = pd.read_excel(balance_file, sheet_name=0)

print("=" * 80)
print("TEST 1: GÉNÉRATION DES ÉTATS FINANCIERS")
print("=" * 80)

# Charger structure liasse
structure = load_structure_liasse_complete()

# Générer les états financiers
results = process_balance_to_liasse_format(balance_df, None, None, structure)

print(f"\n✅ États générés:")
print(f"   - Bilan Actif: {len(results['bilan_actif'])} postes")
print(f"   - Bilan Passif: {len(results['bilan_passif'])} postes")
print(f"   - Compte Résultat: {len(results['compte_resultat'])} postes")

# Afficher quelques postes du bilan actif
print(f"\n📊 Premiers postes Bilan Actif:")
for poste in results['bilan_actif'][:5]:
    print(f"   {poste['ref']}: {poste['libelle']} = {poste['montant_n']:,.0f}")

print("\n" + "=" * 80)
print("TEST 2: GÉNÉRATION DES ÉTATS DE CONTRÔLE")
print("=" * 80)

# Ajouter les balances brutes pour les contrôles
results['balance_n'] = balance_df.to_dict('records')
results['balance_n1'] = []

# Générer les états de contrôle
etats_controle = generer_etats_controle_pour_export(results)

print(f"\n✅ {len(etats_controle)} états de contrôle générés")
for i, etat in enumerate(etats_controle, 1):
    print(f"   {i}. {etat['titre']} - {len(etat['postes'])} postes")

print("\n" + "=" * 80)
print("TEST 3: EXPORT LIASSE (DIAGNOSTIC)")
print("=" * 80)

# Tester l'export
try:
    file_content = remplir_liasse_officielle(results, "TEST ENTREPRISE", "2024")
    print(f"\n✅ Export réussi: {len(file_content)} bytes")
except Exception as e:
    print(f"\n❌ Erreur export: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("DIAGNOSTIC TERMINÉ")
print("=" * 80)
