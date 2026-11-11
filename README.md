# mlops-bike-sharing

API Flask qui prédit le nombre de vélos en location le lendemain à partir de la météo du jour, conteneurisée avec Docker et déployée sur Kubernetes (3 répliques).

Projet 2 de la formation Data Engineer de Datascientest (2022), remis à jour en 2026 : bugs de validation corrigés, catégories météo du jeu de données réalignées sur la source UCI, lancement en une commande.

## Ce que fait l'API

| Route | Méthode | Rôle |
| --- | --- | --- |
| `/status` | GET | Renvoie `1` si l'API répond |
| `/permissions` | POST | Vérifie l'identifiant et le mot de passe |
| `/biketomorrow/LR` | POST | Prédiction par régression linéaire (meilleur modèle) |
| `/biketomorrow/KNR` | POST | Prédiction par k plus proches voisins |
| `/biketomorrow/LOGR` | POST | Prédiction par régression logistique |
| `/metrics/LR` | POST | MSE, RMSE, MAE et R² de la régression linéaire |

Exemple de requête :

```json
{"username": "Quinlan", "password": 5210, "meteo": "rainy", "temp": 10, "bike": 3000, "day": "Wednesday"}
```

- `meteo` : `clear`, `cloudy`, `rainy` (pluie ou neige légère) ou `stormy` (fortes intempéries)
- `day` : `Monday` à `Sunday`
- `temp` : température ressentie en °C ; `bike` : nombre de vélos loués aujourd'hui

Données : jeu public [UCI Bike Sharing](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset), locations horaires à Washington, 2011-2012. Les identifiants de `credentials.csv` sont fictifs (données d'exercice).

**Résultats** (219 jours de test) : la régression linéaire obtient un R² de 0,69 et se trompe en moyenne de 779 vélos par jour. Elle fait à peine mieux que la règle « demain = aujourd'hui » (782) : sans la météo du lendemain, le modèle prévoit surtout que demain ressemblera à aujourd'hui.

## Lancer le projet sur Windows

### 1. Installer les outils (une seule fois)

1. **Git** : [git-scm.com/download/win](https://git-scm.com/download/win), installation par défaut.
2. **Docker Desktop** : [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/). Prendre la version **ARM64** si le PC a un processeur ARM (Snapdragon), sinon la version AMD64. Gratuit pour un usage personnel.
   - Si l'installateur le demande, ouvrir PowerShell en administrateur, taper `wsl --install`, puis redémarrer.
   - Lancer Docker Desktop et attendre que l'indicateur en bas à gauche soit vert (« Engine running »).

### 2. Récupérer le code

Dans PowerShell :

```powershell
cd $HOME\Documents
git clone https://github.com/qberengo/mlops-bike-sharing.git
cd mlops-bike-sharing
```

### 3. Lancer l'API et les tests avec Docker

```powershell
docker compose up --build
```

La première fois, le téléchargement et la construction prennent quelques minutes. Ensuite :

- les lignes `tests-1` affichent le résultat des 6 tests (`SUCCESS`, prédictions, métriques) ;
- l'API reste accessible sur http://localhost:5000/status (affiche `1`).

Pour tester une prédiction soi-même, dans une **deuxième** fenêtre PowerShell :

```powershell
$body = '{"username":"Quinlan","password":5210,"meteo":"rainy","temp":10,"bike":3000,"day":"Wednesday"}'
Invoke-RestMethod -Uri http://localhost:5000/biketomorrow/LR -Method Post -ContentType "application/json" -Body $body
```

Pour arrêter : `Ctrl+C`, puis `docker compose down`.

### 4. Déployer sur Kubernetes (3 répliques)

1. Dans Docker Desktop : menu **Kubernetes**, **Create cluster**, choisir **Kubeadm**, valider. Attendre que Kubernetes soit indiqué comme démarré. L'outil `kubectl` est fourni avec Docker Desktop.
2. Construire les images (si ce n'est pas déjà fait à l'étape 3) et déployer :

```powershell
docker compose build
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
kubectl get pods
```

Attendre que les 3 pods `bike-api-...` soient `Running` avec `1/1` (relancer `kubectl get pods` toutes les quelques secondes).

3. Vérifier l'API : http://localhost:5000/status doit afficher `1`. Les requêtes sont réparties entre les 3 répliques.
4. Jouer les tests depuis l'intérieur du cluster :

```powershell
kubectl apply -f k8s/tests-job.yaml
kubectl wait --for=condition=complete job/bike-tests --timeout=300s
kubectl logs job/bike-tests
```

5. Tout supprimer :

```powershell
kubectl delete -f k8s/tests-job.yaml -f k8s/service.yaml -f k8s/deployment.yaml
```

`k8s/ingress.yaml` reprend l'Ingress de 2022. Il n'est pas nécessaire sur Docker Desktop (le Service suffit) et demande d'installer un contrôleur Ingress pour fonctionner.

## Architecture

```
Client ──> Service bike-api (LoadBalancer, port 5000) ──> 3 répliques du pod API Flask
                                    ^
                     Job bike-tests (6 tests automatisés)
```

## Structure du dépôt

```
api/                 API Flask, données et Dockerfile
tests/               6 scripts de test, run_all.sh et Dockerfile
k8s/                 Deployment, Service, Job de tests, Ingress (optionnel)
docker-compose.yml   lancement local en une commande
Documentation.txt    documentation d'origine (2022)
```

## Limites connues

- Le modèle est réentraîné à chaque requête au lieu d'être chargé une fois ; la route `/biketomorrow/LOGR` est lente (plusieurs secondes).
- L'authentification est rudimentaire : mots de passe en clair dans un CSV, envoyés dans le corps de la requête.
- La régression logistique est un modèle de classification, peu adapté à la prédiction d'un nombre.
