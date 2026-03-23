# -*- coding: utf-8 -*-
"""
Module de génération HTML pour les états de contrôle exhaustifs
"""

from typing import Dict, Any, List


def format_montant_controle(montant: float) -> str:
    """Formate un montant pour les contrôles"""
    if abs(montant) < 0.01:
        return "-"
    return f"{montant:,.0f}".replace(',', ' ')


def generate_etat_controle_html(etat_controle: Dict[str, Any], section_id: str) -> str:
    """Génère le HTML pour un état de contrôle"""
    
    if not etat_controle or 'postes' not in etat_controle:
        return ''
    
    titre = etat_controle.get('titre', 'État de contrôle')
    postes = etat_controle.get('postes', [])
    
    html = f"""
    <div class="etats-fin-section" data-section="{section_id}">
        <div class="section-header-ef">
            <span>🔍 {titre}</span>
            <span class="arrow">›</span>
        </div>
        <div class="section-content-ef">
            <table class="liasse-table">
                <thead>
                    <tr>
                        <th style="width: 60px;">REF</th>
                        <th style="width: auto;">LIBELLÉS</th>
                        <th style="width: 150px; text-align: right;">EXERCICE N</th>
                        <th style="width: 150px; text-align: right;">EXERCICE N-1</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for poste in postes:
        ref = poste.get('ref', '')
        libelle = poste.get('libelle', '')
        montant_n = poste.get('montant_n', 0)
        montant_n1 = poste.get('montant_n1', 0)
        
        # Déterminer si c'est un total
        is_total = 'Total' in libelle or 'Équilibre' in libelle or 'Variation' in libelle
        row_class = 'total-row' if is_total else ''
        
        html += f"""
                    <tr class="{row_class}">
                        <td class="ref-cell">{ref}</td>
                        <td class="libelle-cell">{libelle}</td>
                        <td class="montant-cell">{format_montant_controle(montant_n)}</td>
                        <td class="montant-cell">{format_montant_controle(montant_n1)}</td>
                    </tr>
        """
    
    html += """
                </tbody>
            </table>
        </div>
    </div>
    """
    
    return html


def generate_all_etats_controle_html(etats_controle: Dict[str, Dict[str, Any]]) -> str:
    """Génère le HTML pour tous les états de contrôle"""
    
    html = ""
    
    # Ordre des états de contrôle
    ordre = [
        ('etat_controle_bilan_actif', 'Etat de contrôle Bilan Actif Exercice N'),
        ('etat_controle_bilan_actif_n1', 'Etat de contrôle Bilan Actif Exercice N-1'),
        ('etat_controle_bilan_passif', 'Etat de contrôle Bilan Passif Exercice N'),
        ('etat_controle_bilan_passif_n1', 'Etat de contrôle Bilan Passif Exercice N-1'),
        ('etat_controle_compte_resultat', 'Etat de contrôle Compte de Résultat Exercice N'),
        ('etat_controle_compte_resultat_n1', 'Etat de contrôle Compte de Résultat Exercice N-1'),
        ('etat_controle_tft', 'Etat de contrôle TFT Exercice N'),
        ('etat_controle_tft_n1', 'Etat de contrôle TFT Exercice N-1'),
        ('etat_controle_sens_comptes', 'Etat de contrôle Sens des Comptes'),
        ('etat_equilibre_bilan', 'Etat d\'équilibre Bilan'),
    ]
    
    for key, _ in ordre:
        if key in etats_controle:
            html += generate_etat_controle_html(etats_controle[key], key)
    
    return html
