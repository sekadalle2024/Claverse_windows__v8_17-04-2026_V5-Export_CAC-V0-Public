# -*- coding: utf-8 -*-
"""
Module de génération des états de contrôle exhaustifs
- Un état de contrôle par document (Actif, Passif, Compte Résultat, TFT)
- Pour chaque exercice (N et N-1)
- Contrôle du sens des comptes pour chaque balance
"""

from typing import Dict, List, Any


def format_montant_controle(montant: float) -> str:
    """Formate un montant pour les contrôles"""
    if abs(montant) < 0.01:
        return "0"
    return f"{montant:,.0f}".replace(',', ' ')


def calculer_etat_controle_bilan_actif(bilan_actif_n: List[Dict], bilan_actif_n1: List[Dict]) -> Dict[str, Any]:
    """Calcule l'état de contrôle du bilan actif"""
    
    total_n = sum(p.get('montant_n', 0) for p in bilan_actif_n)
    total_n1 = sum(p.get('montant_n1', 0) for p in bilan_actif_n1)
    
    postes_n = len([p for p in bilan_actif_n if p.get('montant_n', 0) != 0])
    postes_n1 = len([p for p in bilan_actif_n1 if p.get('montant_n1', 0) != 0])
    
    return {
        'titre': 'Etat de contrôle Bilan Actif',
        'postes': [
            {'ref': 'CA', 'libelle': 'Total Actif', 'montant_n': total_n, 'montant_n1': total_n1},
            {'ref': 'CB', 'libelle': 'Nombre de postes (N)', 'montant_n': postes_n, 'montant_n1': 0},
            {'ref': 'CC', 'libelle': 'Nombre de postes (N-1)', 'montant_n': 0, 'montant_n1': postes_n1},
            {'ref': 'CD', 'libelle': 'Variation Total', 'montant_n': total_n - total_n1, 'montant_n1': 0},
        ]
    }


def calculer_etat_controle_bilan_passif(bilan_passif_n: List[Dict], bilan_passif_n1: List[Dict]) -> Dict[str, Any]:
    """Calcule l'état de contrôle du bilan passif"""
    
    total_n = sum(p.get('montant_n', 0) for p in bilan_passif_n)
    total_n1 = sum(p.get('montant_n1', 0) for p in bilan_passif_n1)
    
    postes_n = len([p for p in bilan_passif_n if p.get('montant_n', 0) != 0])
    postes_n1 = len([p for p in bilan_passif_n1 if p.get('montant_n1', 0) != 0])
    
    return {
        'titre': 'Etat de contrôle Bilan Passif',
        'postes': [
            {'ref': 'PA', 'libelle': 'Total Passif', 'montant_n': total_n, 'montant_n1': total_n1},
            {'ref': 'PB', 'libelle': 'Nombre de postes (N)', 'montant_n': postes_n, 'montant_n1': 0},
            {'ref': 'PC', 'libelle': 'Nombre de postes (N-1)', 'montant_n': 0, 'montant_n1': postes_n1},
            {'ref': 'PD', 'libelle': 'Variation Total', 'montant_n': total_n - total_n1, 'montant_n1': 0},
        ]
    }


def calculer_etat_controle_compte_resultat(compte_resultat_n: List[Dict], compte_resultat_n1: List[Dict]) -> Dict[str, Any]:
    """Calcule l'état de contrôle du compte de résultat"""
    
    total_n = sum(p.get('montant_n', 0) for p in compte_resultat_n)
    total_n1 = sum(p.get('montant_n1', 0) for p in compte_resultat_n1)
    
    # Résultat net (dernier poste)
    resultat_n = compte_resultat_n[-1].get('montant_n', 0) if compte_resultat_n else 0
    resultat_n1 = compte_resultat_n1[-1].get('montant_n1', 0) if compte_resultat_n1 else 0
    
    postes_n = len([p for p in compte_resultat_n if p.get('montant_n', 0) != 0])
    postes_n1 = len([p for p in compte_resultat_n1 if p.get('montant_n1', 0) != 0])
    
    return {
        'titre': 'Etat de contrôle Compte de Résultat',
        'postes': [
            {'ref': 'RA', 'libelle': 'Résultat Net (N)', 'montant_n': resultat_n, 'montant_n1': 0},
            {'ref': 'RB', 'libelle': 'Résultat Net (N-1)', 'montant_n': 0, 'montant_n1': resultat_n1},
            {'ref': 'RC', 'libelle': 'Nombre de postes (N)', 'montant_n': postes_n, 'montant_n1': 0},
            {'ref': 'RD', 'libelle': 'Nombre de postes (N-1)', 'montant_n': 0, 'montant_n1': postes_n1},
            {'ref': 'RE', 'libelle': 'Variation Résultat', 'montant_n': resultat_n - resultat_n1, 'montant_n1': 0},
        ]
    }


def calculer_etat_controle_tft(tft_n: List[Dict], tft_n1: List[Dict]) -> Dict[str, Any]:
    """Calcule l'état de contrôle du TFT"""
    
    # Trésorerie finale (ZF)
    tresorerie_fin_n = next((p['montant_n'] for p in tft_n if p['ref'] == 'ZF'), 0) if tft_n else 0
    tresorerie_fin_n1 = next((p['montant_n1'] for p in tft_n1 if p['ref'] == 'ZF'), 0) if tft_n1 else 0
    
    # Variation de trésorerie (ZE)
    variation_n = next((p['montant_n'] for p in tft_n if p['ref'] == 'ZE'), 0) if tft_n else 0
    variation_n1 = next((p['montant_n1'] for p in tft_n1 if p['ref'] == 'ZE'), 0) if tft_n1 else 0
    
    # Flux opérationnels (ZB)
    flux_op_n = next((p['montant_n'] for p in tft_n if p['ref'] == 'ZB'), 0) if tft_n else 0
    flux_op_n1 = next((p['montant_n1'] for p in tft_n1 if p['ref'] == 'ZB'), 0) if tft_n1 else 0
    
    return {
        'titre': 'Etat de contrôle Tableau des Flux de Trésorerie',
        'postes': [
            {'ref': 'TA', 'libelle': 'Trésorerie finale (N)', 'montant_n': tresorerie_fin_n, 'montant_n1': 0},
            {'ref': 'TB', 'libelle': 'Trésorerie finale (N-1)', 'montant_n': 0, 'montant_n1': tresorerie_fin_n1},
            {'ref': 'TC', 'libelle': 'Variation trésorerie (N)', 'montant_n': variation_n, 'montant_n1': 0},
            {'ref': 'TD', 'libelle': 'Variation trésorerie (N-1)', 'montant_n': 0, 'montant_n1': variation_n1},
            {'ref': 'TE', 'libelle': 'Flux opérationnels (N)', 'montant_n': flux_op_n, 'montant_n1': 0},
            {'ref': 'TF', 'libelle': 'Flux opérationnels (N-1)', 'montant_n': 0, 'montant_n1': flux_op_n1},
        ]
    }


def calculer_etat_controle_sens_comptes(balance_n: List[Dict], balance_n1: List[Dict]) -> Dict[str, Any]:
    """Calcule l'état de contrôle du sens des comptes"""
    
    # Compter les comptes par sens
    comptes_debit_n = len([c for c in balance_n if c.get('solde_debit', 0) > 0])
    comptes_credit_n = len([c for c in balance_n if c.get('solde_credit', 0) > 0])
    
    comptes_debit_n1 = len([c for c in balance_n1 if c.get('solde_debit', 0) > 0])
    comptes_credit_n1 = len([c for c in balance_n1 if c.get('solde_credit', 0) > 0])
    
    # Totaux
    total_debit_n = sum(c.get('solde_debit', 0) for c in balance_n)
    total_credit_n = sum(c.get('solde_credit', 0) for c in balance_n)
    
    total_debit_n1 = sum(c.get('solde_debit', 0) for c in balance_n1)
    total_credit_n1 = sum(c.get('solde_credit', 0) for c in balance_n1)
    
    return {
        'titre': 'Etat de contrôle Sens des Comptes',
        'postes': [
            {'ref': 'SA', 'libelle': 'Comptes en débit (N)', 'montant_n': comptes_debit_n, 'montant_n1': 0},
            {'ref': 'SB', 'libelle': 'Comptes en crédit (N)', 'montant_n': comptes_credit_n, 'montant_n1': 0},
            {'ref': 'SC', 'libelle': 'Comptes en débit (N-1)', 'montant_n': 0, 'montant_n1': comptes_debit_n1},
            {'ref': 'SD', 'libelle': 'Comptes en crédit (N-1)', 'montant_n': 0, 'montant_n1': comptes_credit_n1},
            {'ref': 'SE', 'libelle': 'Total débit (N)', 'montant_n': total_debit_n, 'montant_n1': 0},
            {'ref': 'SF', 'libelle': 'Total crédit (N)', 'montant_n': total_credit_n, 'montant_n1': 0},
            {'ref': 'SG', 'libelle': 'Total débit (N-1)', 'montant_n': 0, 'montant_n1': total_debit_n1},
            {'ref': 'SH', 'libelle': 'Total crédit (N-1)', 'montant_n': 0, 'montant_n1': total_credit_n1},
            {'ref': 'SI', 'libelle': 'Équilibre (N)', 'montant_n': total_debit_n - total_credit_n, 'montant_n1': 0},
            {'ref': 'SJ', 'libelle': 'Équilibre (N-1)', 'montant_n': 0, 'montant_n1': total_debit_n1 - total_credit_n1},
        ]
    }


def calculer_etat_equilibre_bilan(bilan_actif_n: List[Dict], bilan_passif_n: List[Dict], 
                                   resultat_net_n: float, bilan_actif_n1: List[Dict], 
                                   bilan_passif_n1: List[Dict], resultat_net_n1: float) -> Dict[str, Any]:
    """Calcule l'état d'équilibre du bilan"""
    
    total_actif_n = sum(p.get('montant_n', 0) for p in bilan_actif_n)
    total_passif_n = sum(p.get('montant_n', 0) for p in bilan_passif_n)
    
    total_actif_n1 = sum(p.get('montant_n1', 0) for p in bilan_actif_n1)
    total_passif_n1 = sum(p.get('montant_n1', 0) for p in bilan_passif_n1)
    
    # Équilibre: Actif = Passif + Résultat Net
    equilibre_n = total_actif_n - (total_passif_n + resultat_net_n)
    equilibre_n1 = total_actif_n1 - (total_passif_n1 + resultat_net_n1)
    
    return {
        'titre': 'Etat d\'équilibre Bilan',
        'postes': [
            {'ref': 'EA', 'libelle': 'Total Actif (N)', 'montant_n': total_actif_n, 'montant_n1': 0},
            {'ref': 'EB', 'libelle': 'Total Passif (N)', 'montant_n': total_passif_n, 'montant_n1': 0},
            {'ref': 'EC', 'libelle': 'Résultat Net (N)', 'montant_n': resultat_net_n, 'montant_n1': 0},
            {'ref': 'ED', 'libelle': 'Passif + Résultat (N)', 'montant_n': total_passif_n + resultat_net_n, 'montant_n1': 0},
            {'ref': 'EE', 'libelle': 'Équilibre (N)', 'montant_n': equilibre_n, 'montant_n1': 0},
            {'ref': 'EF', 'libelle': 'Total Actif (N-1)', 'montant_n': 0, 'montant_n1': total_actif_n1},
            {'ref': 'EG', 'libelle': 'Total Passif (N-1)', 'montant_n': 0, 'montant_n1': total_passif_n1},
            {'ref': 'EH', 'libelle': 'Résultat Net (N-1)', 'montant_n': 0, 'montant_n1': resultat_net_n1},
            {'ref': 'EI', 'libelle': 'Passif + Résultat (N-1)', 'montant_n': 0, 'montant_n1': total_passif_n1 + resultat_net_n1},
            {'ref': 'EJ', 'libelle': 'Équilibre (N-1)', 'montant_n': 0, 'montant_n1': equilibre_n1},
        ]
    }
