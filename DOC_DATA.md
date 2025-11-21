# 📄 Documentation des Données

## 1. Introduction
Dans le cadre du projet, nous avons choisi d'agréger des données environnementales pour trois grandes villes françaises : Paris, Lyon et Marseille.
L'objectif est de croiser la météo et la pollution pour voir, par exemple, si le vent a un impact sur la qualité de l'air.

Nous utilisons deux API externes gratuites et ouvertes proposé dans l'ennoncé.

---

## 2. Source 1 : Météo (Open-Meteo)

### C'est quoi ?
C'est une API open-source qui fournit la météo passée, présente et future.

### Pourquoi ce choix ? (Justification)
Nous avons choisi Open-Meteo pour trois raisons principales :
1.  **Pas de clé API (API Key) :** C'est le gros avantage. Contrairement à OpenWeatherMap, on peut l'utiliser tout de suite sans créer de compte ni attendre de validation. C'est idéal pour le développement et les tests.
2.  **Simplicité :** On envoie juste la latitude et la longitude, et on reçoit un JSON très propre.
3.  **Gratuité :** Elle est gratuite pour les projets non-commerciaux.

### Informations techniques
* **URL utilisée :** `https://api.open-meteo.com/`
* **Format :** JSON.
* **Données récupérées :** Température (`temperature`) et Vitesse du vent (`windspeed`).
* **Fréquence :** Nous récupérons les données à la demande via notre script.

---

## 3. Source 2 : Qualité de l'air (OpenAQ)

### C'est quoi ?
OpenAQ est une plateforme qui regroupe les données de milliers de stations de mesure de la qualité de l'air dans le monde.

### Pourquoi ce choix ? (Justification)
1.  **Données réelles :** Contrairement à la météo où l'on utilise des prévisions, ici ce sont de vrais capteurs physiques installés dans les villes.
2.  **Standardisation :** L'API nous renvoie toujours les unités standardisées (µg/m³), ce qui nous évite de faire des conversions mathématiques compliquées dans le code.
3.  **Documentation :** La documentation est claire et l'API est un standard dans l'Open Data.

### Informations techniques
* **URL utilisée :** `https://docs.openaq.org`
* **Format :** JSON.
* **Données récupérées :** Particules fines, PM10, NO2 (selon ce que la station capte).
* **Paramètres :** Recherche par coordonnées géographiques (celles de nos villes).


## 4. Stratégie d'import (Ingestion)

Comme les données changent tout le temps, nous ne les stockons pas toutes.
Nous avons créé un script Python (`ingest.py`) qui :
1.  Définit les coordonnées GPS de Paris, Lyon et Marseille.
2.  Interroge séquentiellement Open-Meteo puis OpenAQ.
3.  Nettoie les données reçues.
4.  Les sauvegarde dans notre base de données locale (SQLite) avec la date et l'heure de l'import.

Cela nous permet de construire notre propre historique de données pour générer des statistiques.