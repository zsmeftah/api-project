
**API-Projet** est une application Fullstack (FastAPI + React) permettant de suivre et visualiser des indicateurs environnementaux locaux.

## 🚀 Fonctionnalités Techniques

### Backend (FastAPI)
* **Authentification :** Inscription et Connexion via JWT (JSON Web Tokens). Hachage des mots de passe via Argon2.
* **Rôles (RBAC) :**
    * *User* : Accès en lecture seule (Consultation du Dashboard).
    * *Admin* : Accès complet (Ajout de données, gestion).
* **Base de données :** SQLite avec l'ORM SQLAlchemy.
* **Filtres avancés :** Recherche par plage de dates, type d'indicateur et zone géographique.
* **Statistiques :** Endpoint dédié calculant la moyenne journalière des indicateurs.

### Frontend (React)
* **Dashboard :** Visualisation graphique (Librairie Recharts) et tableau de données.
* **Administration :** Interface protégée pour l'ajout manuel de données.
* **UX :** Gestion des chargements et des erreurs API.

---

## 🛠️ Installation et Démarrage

### Prérequis
* Python 3.10+
* Node.js (LTS)

### 1. Lancer le Backend

Ouvrez un terminal à la racine du projet :

# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement
# Windows :
.\venv\Scripts\activate
# Mac/Linux :
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Démarrer le serveur
python -m uvicorn backend.app.main:app --reload

### 1. Lancer le Frontend

Ouvrez un nouveau terminal dans le dossier `frontend` :

# 1. Installer les dépendances
npm install

# 2. Démarrer l'application
npm start

## ⚙️ Configuration Initiale
Une fois les serveurs lancés, exécutez ces commandes dans le terminal Backend (avec l'environnement virtuel activé) :

### 1. Peupler la Base de Données (Jeu de Test)
Ce script crée les zones (Paris, Lyon, Marseille) et récupère les dernières données météo/air.

python -m backend.scripts.ingest

### 2. Créer un compte Administrateur
Par défaut, l'inscription crée un utilisateur standard. Pour tester l'ajout de données :

1. Inscrivez-vous sur le site avec l'email `admin@gmail.com`.
2. Lancez ce script pour promouvoir cet utilisateur en Admin :
python -m backend.scripts.promote_admin

## ✅ Tests
Le projet contient les tests d'intégration Pytest couvrant l'auth, le CRUD et les stats :
python -m pytest

📂 Structure du Projet

api-proje/
backend/               # API FastAPI
    app/               # Code source API
    scripts/           # Scripts (Ingestion, Promot_Admin)
    tests/             # Tests automatisés
frontend/              # Client React
    src/               # Pages et composants
requirements.txt       # Dépendances
README.md              # Fichier démarrage