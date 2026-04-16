# Guide de Déploiement sur Render.com

**Date:** 16 Avril 2026  
**Contexte:** Alternative à Railway (qui refuse les cartes prépayées)

---

## 🎯 Pourquoi Render.com ?

✅ **Accepte les cartes prépayées**  
✅ **Plan gratuit généreux** (750 heures/mois)  
✅ **Déploiement automatique** via GitHub  
✅ **Support Docker natif**  
✅ **Interface simple et intuitive**  
✅ **Pas de configuration CLI complexe**

---

## 📋 Prérequis

- Compte GitHub avec le repo: `Back-end-python-V0_03_03_2026`
- Navigateur web
- 10 minutes de temps

---

## 🚀 Étapes de Déploiement

### Étape 1: Créer un compte Render

1. Aller sur: https://render.com
2. Cliquer sur **"Get Started"**
3. Choisir **"Sign up with GitHub"**
4. Autoriser Render à accéder à vos repos

⏱️ Temps: 2 minutes

---

### Étape 2: Créer un nouveau Web Service

1. Dans le dashboard Render, cliquer sur **"New +"**
2. Sélectionner **"Web Service"**
3. Connecter votre repository GitHub:
   - Chercher: `Back-end-python-V0_03_03_2026`
   - Cliquer sur **"Connect"**

⏱️ Temps: 1 minute

---

### Étape 3: Configurer le service

#### Configuration de base:

| Paramètre | Valeur |
|-----------|--------|
| **Name** | `clara-backend-production` |
| **Region** | `Frankfurt (EU Central)` ou le plus proche |
| **Branch** | `main` |
| **Root Directory** | `py_backend` |
| **Runtime** | `Docker` (détecté automatiquement) |

#### Commandes (laisser vides):

| Paramètre | Valeur |
|-----------|--------|
| **Build Command** | *(vide - Docker gère)* |
| **Start Command** | *(vide - Docker gère)* |

#### Plan:

- Sélectionner: **Free** (0$/mois)

⏱️ Temps: 2 minutes

---

### Étape 4: Variables d'environnement

Cliquer sur **"Advanced"** puis ajouter:

```
HOST=0.0.0.0
PORT=5000
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
```

**Comment ajouter:**
1. Cliquer sur **"Add Environment Variable"**
2. Entrer le nom (ex: `HOST`)
3. Entrer la valeur (ex: `0.0.0.0`)
4. Répéter pour chaque variable

⏱️ Temps: 2 minutes

---

### Étape 5: Créer le service

1. Vérifier tous les paramètres
2. Cliquer sur **"Create Web Service"**
3. Attendre le déploiement (5-10 minutes)

**Vous verrez:**
- Logs de build en temps réel
- Progression du déploiement
- URL générée automatiquement

⏱️ Temps: 5-10 minutes

---

## 🔗 Récupérer l'URL du service

Une fois le déploiement terminé:

1. En haut de la page, vous verrez l'URL:
   ```
   https://clara-backend-production.onrender.com
   ```

2. Tester l'endpoint de santé:
   ```
   https://clara-backend-production.onrender.com/health
   ```

---

## ⚙️ Configuration du Frontend

Mettre à jour `src/services/claraApiService.ts`:

```typescript
// Remplacer
const API_BASE_URL = 'https://hkj0631c.rpcl.app';

// Par
const API_BASE_URL = 'https://clara-backend-production.onrender.com';
```

**Commande PowerShell:**
```powershell
$file = "src/services/claraApiService.ts"
$oldUrl = "hkj0631c.rpcl.app"
$newUrl = "clara-backend-production.onrender.com"
(Get-Content $file) -replace $oldUrl, $newUrl | Set-Content $file
```

---

## ⚠️ Limitations du Plan Gratuit

### Cold Start (15 minutes d'inactivité)

Le service s'endort après 15 minutes sans requête.

**Impact:**
- Première requête après inactivité: 30-60 secondes
- Requêtes suivantes: instantanées

**Solutions:**

1. **Ping automatique** (recommandé):
   - Utiliser un service comme UptimeRobot
   - Ping toutes les 10 minutes
   - Gratuit: https://uptimerobot.com

2. **Accepter le cold start**:
   - Informer les utilisateurs
   - Afficher un message de chargement

### Ressources

- **RAM:** 512 MB (suffisant pour votre backend)
- **CPU:** Partagé
- **Bande passante:** 100 GB/mois
- **Heures:** 750h/mois (suffisant pour 24/7)

---

## 🔄 Déploiement Automatique

Render redéploie automatiquement à chaque push sur `main`:

```bash
git add .
git commit -m "Update backend"
git push origin main
```

Render détecte le push et redéploie (5-10 minutes).

---

## 📊 Monitoring

### Logs en temps réel

1. Dashboard Render
2. Sélectionner votre service
3. Onglet **"Logs"**

### Métriques

1. Onglet **"Metrics"**
2. Voir:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🛠️ Commandes Utiles

### Redéployer manuellement

1. Dashboard Render
2. Sélectionner votre service
3. Cliquer sur **"Manual Deploy"** → **"Deploy latest commit"**

### Voir les variables d'environnement

1. Onglet **"Environment"**
2. Voir/Modifier les variables

### Suspendre le service

1. Settings
2. **"Suspend Service"**
3. Confirmer

---

## 🐛 Dépannage

### Le service ne démarre pas

**Vérifier:**
1. Logs de build (erreurs de dépendances?)
2. Dockerfile correct dans `py_backend/`
3. Variables d'environnement définies

### Erreur 502 Bad Gateway

**Causes:**
- Service en cours de démarrage (attendre 1-2 min)
- Cold start (première requête après inactivité)
- Erreur dans le code backend

**Solution:**
- Vérifier les logs
- Tester l'endpoint `/health`

### Timeout

**Render timeout:** 30 secondes par défaut

**Solution:**
- Optimiser les requêtes longues
- Utiliser des tâches asynchrones

---

## 💰 Upgrade vers un plan payant (optionnel)

Si vous avez besoin de plus de ressources:

### Starter Plan ($7/mois)

✅ Pas de cold start  
✅ 512 MB RAM  
✅ Domaine personnalisé  
✅ Support prioritaire

### Standard Plan ($25/mois)

✅ 2 GB RAM  
✅ Scaling automatique  
✅ Meilleure performance

---

## 📝 Checklist Finale

- [ ] Service créé sur Render
- [ ] Variables d'environnement configurées
- [ ] Déploiement réussi
- [ ] URL récupérée
- [ ] Frontend mis à jour avec la nouvelle URL
- [ ] Test de l'endpoint `/health`
- [ ] (Optionnel) UptimeRobot configuré pour éviter cold start

---

## 🎉 Félicitations !

Votre backend Clara est maintenant déployé sur Render.com !

**URL de production:**
```
https://clara-backend-production.onrender.com
```

**Prochaines étapes:**
1. Tester toutes les fonctionnalités
2. Configurer UptimeRobot (optionnel)
3. Mettre à jour la documentation

---

## 📚 Ressources

- Documentation Render: https://render.com/docs
- Support: https://render.com/support
- Status: https://status.render.com
- Community: https://community.render.com

---

**Créé le:** 16 Avril 2026  
**Auteur:** Clara Team  
**Version:** 1.0.0
