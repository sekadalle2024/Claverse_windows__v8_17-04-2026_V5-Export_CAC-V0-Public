# Solutions Implémentées - Résolution du Double Problème (06 Avril 2026)

## Document de Reprise et Post-Mortem Technique

Ce document vise à détailler, pour toute reprise postérieure par un autre ingénieur ou agent, l'intégralité des problèmes trouvés concernant l'exportation de la Liasse Fiscale et les solutions fonctionnelles mises en place. 

---

## 1. Problème: Décalage des Valeurs et Liasse Excel Vide (ACTIF, PASSIF, RESULTAT, TFT, BILAN)

### 📌 Les Symptômes Initiaux
- Les montants numériques des onglets ACTIF, PASSIF et RESULTAT étaient soit vides au moment de l'export, soit venaient s'écraser visuellement sur les libellés de texte.
- L'onglet `TFT` (Tableau des Flux de Trésorerie) n’intégrait aucune valeur.
- L'onglet central `BILAN` demeurait totalement vide.

### 🔍 Les Causes Racines
L'export officiel défini par la DGI `Liasse_officielle_revise.xlsx` requiert le fonctionnement sur une structure extrêmement rigide contenant de nombreuses fusions de cellules (`MergedCells`). 
1. **L'approche initiale statique** (écrire en `'DA': 'E10'`) échouait silencieusement car `openpyxl` ne prend pas en charge l'écriture partielle dans des cellules fusionnées si on ne cible pas exactement la cellule dite "maîtresse".
2. **L'approche de scan dynamique des fusions** : Une tentative algorithmique de scanner dynamiquement la ligne Excel pour y trouver la "première cellule libre non-fusionnée" a échoué. En effet, l'immense titre "LIBELLÉS" dans les feuilles (ex: `PASSIF`, `RESULTAT`) englobait en réalité d'autres colonnes fusionnées de manière invisible (ex: Les colonnes B à E étaient fusionnées, faisant ressortir "F" ou "B" comme points de contacts maîtres). Ceci causait un décalage brutal des valeurs vers la gauche qui écrasait le texte originel au lieu de s'inscrire dans les cases `EXERCICE N`.
3.  **TFT & Bilan ignorés** : L'intégration originelle des montants du `TFT` n'était pas passée par la boucle de traitement de l'export (qui exige des marqueurs de correspondances formels de 2 lettres). L'onglet `BILAN` (qui affiche simultanément ACTIF à gauche et PASSIF à droite) n'était simplement pas implémenté dans le script de remplissage `export_liasse`.

### 🛡️ Solution Implémentée : Frappe Balistique et Alignement Strict (`export_liasse.py`)
La gestion flottante a été supprimée au profit d'une approche de ciblage explicite par rapport à l'architecture ferme fournie via l'inspection programmatique du document :

1. **Scanner R.E.F vertical intelligent** : Le système conserve la logique de boucler sur la **Colonne A** (`REF` ou index 1) à la recherche stricte des codes comptables à 2 lettres uppercase SYSCOHADA (ex: `AD`, `RA`, `ZA`).
2. **Ciblage Absolu (Frappe Balistique)** : Une fois la ligne trouvée via la R.E.F., le script injecte rigoureusement `montant_n` et `montant_n1` en ignorant totalement la logique de fusion latérale.
   Suite à l'analyse fine des grilles "EXERCICE N" dans le document certifié `Liasse_officielle_revise.xlsx`, le mappage adopté est le suivant :
   - **ACTIF** : `H` (N) & `I` (N-1)
   - **PASSIF** : `H` (N) & `I` (N-1)
   - **RESULTAT** : `H` (N) & `I` (N-1)
   - **TFT** : `H` (N) & `I` (N-1)
   - **BILAN** : Double passage sur `H/I` (pour l'Actif, ref=Col. A) et sur `M/N` (pour le Passif, ref=Col. J)
3. **Traducteur à la volée du TFT** : Extraire dynamiquement les 2 premières lettres majuscules d'un dictionnaire brut (ex: `ZA_ouverture` -> `ZA`) permet la compatibilité pleine de l'onglet TFT.

> **Résultat ✅** : La liasse officielle sort parfaitement alignée sous les marqueurs `EXERCICE N` préétablis. Plus aucun écrasement gauche n'est soulevé. Les onglets TFT et BILAN sont complets.

---

## 2. Problème: L'Onglet "Contrôle de Cohérence" (Erreurs & Obsolescences)

### 📌 Les Symptômes Initiaux
Les 16 règles de validation censées atterrir dans l'onglet `Contrôle de cohérence` produisaient un rapport erroné, sortaient des variations chiffrées à zéro (`0`) et provoquaient par moments des plantages Python fatals d'export si une balance n'était pas fournie au travers du Backend. Le format n'était parfois même que de 8 contrôles effectifs.

### 🔍 Les Causes Racines
Trois failles mathématiques ou algorithmiques provoquaient ce bris :
1. **La Variation N/N-1 Absente** : Les méthodes d'appel (comme `calculer_etat_controle_bilan_actif_variation(bilan_actif, bilan_actif)`) repassaient le même objet en doublon au processeur au lieu de l'exercice décalé. Tout delta devenait alors un `0` constant puisque A - A = 0.
2. **Format TFT Incompatible** : Le moteur comptable interne du projet expédiait le Tableau de Flux de Trésorerie en dict : `{ 'ZA_tresorerie_ouverture': 1800000 }`. Mais le framework central d'audit s'attendait formellement au "standard liasse" en liste à objets : `[{'ref': 'ZA', 'montant_n': 1800000}]`. Cette erreur silencieuse faisait échouer l'audit TFT.
3. **Instabilité Fallback (Liasse sans Balance N-1)** : L'algorithme se crashait lorsqu'une condition métier tentait d'appeler l'objet vide `balance_n1`, provoquant l'échec de la compilation complète avant même la genération du document.

### 🛡️ Solutions Implémentées (`generer_onglet_controle_coherence.py`)
1. **Extraction Intuitive du Delta** : Une procédure directe a été injectée dans l'évaluateur de section. Au lieu de compter sur un objet miroir externe, il extrait la base des composants internes natifs standard : `poste.get('montant_n')` confrontés au `poste.get('montant_n1')`. Le système génère donc de véritables écarts chiffrés.
2. **Pont "Dictionnaire-Liste" (TFT Bridge)** : Une simple passe récupère les index préfixés natifs (le `split` sur l'underscore ou les 2 premières lettres si pertinent) qui reformate et repackage formellement le composant mémoire avant l'entrée dans les fonctions du grand journal.
3. **Sécurisation par Fallback (Graceful Degradation)** : Ajout de conteneurs de sécurité. Si la requête Backend lance un export qui n'est pas assorti de l'intégralité des Balances, le contrôleur utilise alors des tableaux d'avertissement sûrs `[]` qui permettent de conclure et retourner l'export complet (et les autres audits validés) sans planter le document HTML ou Excel final.

> **Résultat ✅** : Les 16 états certifiés sont présents, précis (-1.5M€ Variation d'ACTIF bien évaluée), et les vérifications de trésoreries affichent un statut sain.

---

## Conclusion et Validation Finale
- Le système s'exécute aujourd'hui de manière fluide au travers de l'interface front et de `generer_etats_liasse.py`.
- Le pipeline de tests unitaires sur modèle physique (`test_corrections_export_v2.py`) réussit ses validations à 100%. `Export de cellules: ~40 montants détectés, placés en absolu dans H / I`.
- **Pret pour le staging.**
