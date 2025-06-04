#  Chatbot RAG – Clinique de l’Amitié

```
uvicorn main:app --reload
```

Ce projet vise à développer un **assistant virtuel intelligent** pour la **Clinique de l’Amitié à Dakar**, en s’appuyant sur l’approche **Retrieval-Augmented Generation (RAG)**. Il permet de répondre efficacement aux questions des patients et visiteurs en exploitant une base documentaire interne (documents `.txt`).

---

##  Objectifs

* Offrir un accès instantané et automatisé aux informations médicales et administratives
* Réduire la charge du personnel d’accueil et administratif
* Rendre les services de la Clinique plus accessibles, notamment en ligne
* Démontrer l'usage de l’IA générative dans un contexte de santé local

---

##  Fonctionnement général

Le chatbot repose sur **deux modules principaux** :

### 1. **Module de récupération (Retriever)**

* Utilise **FAISS** comme base vectorielle
* Génère les **embeddings** avec `GoogleGenerativeAIEmbeddings`
* Recherche les **passages les plus pertinents** via `similarity_search_with_score()`

### 2. **Module de génération (LLM)**

* Génère des **réponses naturelles** à partir du contexte extrait
* Utilise le modèle **Gemini 1.5 Flash**
* Structure le prompt pour un **ton professionnel et informatif**

---

##  Données et sources

Les documents indexés sont issus de :

* Informations internes de la clinique
* Documents `.txt` déposés dans le dossier `documents/`
* Données structurées (horaires, services, procédures)

Les fichiers sont segmentés avec `RecursiveCharacterTextSplitter` en blocs de 500 caractères avec recouvrement, puis vectorisés.

---

##  Stack technique

| Composant        | Technologie                  |
| ---------------- | ---------------------------- |
| Framework API    | FastAPI                      |
| Vector DB        | FAISS                        |
| Embeddings       | GoogleGenerativeAIEmbeddings |
| Modèle LLM       | Gemini 1.5 Flash (Google)    |
| Langage          | Python 3.10+                 |
| Conteneurisation | Docker + Docker Compose      |

---

##  Déploiement rapide avec Docker

### 1. Cloner le dépôt

```bash
git clone https://github.com/25Abzo/ChatbotAmitie.git
cd ChatbotAmitie
```

### 2. Configurer vos clés API

Créer un fichier `.env` à la racine :

```env
GOOGLE_API_KEY="VOTRE_CLE_API_GEMINI"
```

### 3. Lancer le projet avec Docker Compose

```bash
docker-compose up --build
```

---

##  Accès au chatbot

* Interface principale : [http://localhost:8000](http://localhost:8000)
* Interface Swagger (API docs) : [http://localhost:8000/docs](http://localhost:8000/docs)

---

##  Exemples de requêtes

### Requête via Swagger ou Postman

**POST** `/chat`

```json
{
  "question": "Quels sont les horaires d’ouverture ?"
}
```

### Requête via `curl`

```bash
curl -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{"question": "Quels sont les horaires d’ouverture ?"}'
```

---

##  Mise à jour des documents

Si vous ajoutez ou modifiez des fichiers `.txt` dans le dossier `documents/`, vous devez **reconstruire l’index FAISS** :

```bash
python build.py
```

---

##  Structure du projet

```
.
├── documents/                # Textes sources (.txt)
├── faiss_clinique_amitie/   # Index vectoriel FAISS (auto-généré)
├── main.py                   # API FastAPI principale
├── build.py                  # Construction de l’index vectoriel
├── requirements-dev.txt      # Dépendances Python
├── .env                      # Clé API Gemini (non versionné)
├── Dockerfile                # Image Docker
└── docker-compose.yml        # Orchestration Docker
```

---

##  Optimisations apportées

* Nettoyage des réponses générées (suppression des phrases vagues)
* Structuration des réponses (titres, paragraphes, listes)
* Prompt adapté au domaine médical avec un ton informatif et rassurant
* Séparation claire entre récupération et génération

---

##  Auteur

**Abdoulaye DIAW**
 [https://abdoulaye-diaw.vercel.app/](https://abdoulaye-diaw.vercel.app/)
 Projet personnel autour de la RAG appliquée au secteur de la santé à Dakar.

---



