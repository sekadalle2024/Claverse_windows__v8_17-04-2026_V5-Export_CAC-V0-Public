"""
Test simple du module Balance_Reader

Ce script teste le chargement des balances avec le fichier de démonstration.
"""

import sys
import os

# Ajouter le chemin des modules au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Modules'))

from balance_reader import BalanceReader, BalanceNotFoundException, InvalidBalanceFormatException
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_balance_reader():
    """Test du chargement des balances"""
    print("=" * 70)
    print("TEST DU MODULE BALANCE_READER")
    print("=" * 70)
    
    try:
        # Chemin vers le fichier de test (absolu)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        fichier_test = os.path.join(base_dir, "P000 -BALANCE DEMO N_N-1_N-2.xls")
        
        print(f"\n📂 Fichier de test: {fichier_test}")
        print(f"   Existe: {os.path.exists(fichier_test)}")
        
        # Créer une instance du lecteur
        print("\n1️⃣ Création du BalanceReader...")
        reader = BalanceReader(fichier_test)
        print("   ✓ BalanceReader créé")
        
        # Charger les balances
        print("\n2️⃣ Chargement des balances...")
        balance_n, balance_n1, balance_n2 = reader.charger_balances()
        print("   ✓ Balances chargées avec succès")
        
        # Afficher les résultats
        print("\n3️⃣ Résultats du chargement:")
        print(f"   - Balance N:   {len(balance_n):>5} comptes")
        print(f"   - Balance N-1: {len(balance_n1):>5} comptes")
        print(f"   - Balance N-2: {len(balance_n2):>5} comptes")
        
        # Vérifier les colonnes
        print("\n4️⃣ Vérification des colonnes:")
        colonnes_attendues = [
            'Numéro', 'Intitulé', 
            'Ant Débit', 'Ant Crédit',
            'Débit', 'Crédit',
            'Solde Débit', 'Solde Crédit'
        ]
        
        for col in colonnes_attendues:
            if col in balance_n.columns:
                print(f"   ✓ {col}")
            else:
                print(f"   ✗ {col} MANQUANTE")
        
        # Afficher un échantillon de données
        print("\n5️⃣ Échantillon de données (Balance N - 3 premières lignes):")
        print("-" * 70)
        for idx, row in balance_n.head(3).iterrows():
            print(f"   Compte: {row['Numéro']} - {row['Intitulé'][:40]}")
            print(f"   Solde Débit: {row['Solde Débit']:>12,.2f} | Solde Crédit: {row['Solde Crédit']:>12,.2f}")
            print("-" * 70)
        
        # Test de conversion des montants
        print("\n6️⃣ Vérification de la conversion des montants:")
        montant_test = balance_n['Solde Débit'].iloc[0]
        print(f"   Type du montant: {type(montant_test)}")
        print(f"   Valeur: {montant_test}")
        
        if isinstance(montant_test, (int, float)):
            print("   ✓ Les montants sont bien convertis en numérique")
        else:
            print("   ✗ ERREUR: Les montants ne sont pas numériques")
        
        print("\n" + "=" * 70)
        print("✅ TEST RÉUSSI - Module Balance_Reader opérationnel")
        print("=" * 70)
        return True
        
    except BalanceNotFoundException as e:
        print(f"\n❌ ERREUR - Balance non trouvée: {str(e)}")
        print("=" * 70)
        return False
        
    except InvalidBalanceFormatException as e:
        print(f"\n❌ ERREUR - Format invalide: {str(e)}")
        print("=" * 70)
        return False
        
    except Exception as e:
        print(f"\n❌ ERREUR inattendue: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = test_balance_reader()
    sys.exit(0 if success else 1)
