
#  Chatbot RAG – Clinique de l’Amitié

```bash
uvicorn main:app --reload
```

Ce projet vise à développer un **assistant virtuel intelligent** pour la **Clinique de l’Amitié à Dakar**, en s’appuyant sur l’approche **Retrieval-Augmented Generation (RAG)**. Il permet de répondre efficacement aux questions des patients et visiteurs en exploitant une base documentaire interne (documents `.txt`).

---

##  Objectifs

- Offrir un accès instantané et automatisé aux informations médicales et administratives
- Réduire la charge du personnel d’accueil
- Rendre les services de la Clinique plus accessibles, notamment en ligne
- Démontrer l’usage de l’IA générative dans un contexte de santé local

---

##  Fonctionnement

Le chatbot repose sur deux modules principaux :

### 1.  Module de récupération (Retriever)

- Utilise **FAISS** pour la recherche vectorielle
- Génère les embeddings avec `GoogleGenerativeAIEmbeddings`
- Recherche les passages les plus pertinents via `similarity_search_with_score()`

### 2.  Module de génération (LLM)

- Produit des réponses naturelles basées sur le contexte
- Utilise le modèle **Gemini 1.5 Flash**
- Structure le prompt avec un ton professionnel et informatif

---

##  Données sources

- Documents `.txt` dans `documents/`
- Informations internes sur les services, horaires, procédures
- Vectorisation après découpage par blocs de 500 caractères avec recouvrement

---

##  Stack technique

| Composant        | Technologie                  |
| ---------------- | ---------------------------- |
| API              | FastAPI                      |
| Vector DB        | FAISS                        |
| Embeddings       | GoogleGenerativeAIEmbeddings |
| LLM              | Gemini 1.5 Flash             |
| Langage          | Python 3.10+                 |
| Conteneurisation | Docker + Docker Compose      |

---

##  Déploiement local avec Docker

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

### 3. Lancer avec Docker Compose

```bash
docker-compose up --build
```

---

##  Déploiement depuis Docker Hub (optionnel)

Une image Docker pré-construite est disponible pour un déploiement rapide :

```bash
docker pull abdoulaye0diaw/chatbot-amitie-rag:latest
docker run -d -p 8000:8000 --env-file .env abdoulaye0diaw/chatbot-amitie-rag:latest
```

---

##  Accès à l’API

- Interface principale : [http://localhost:8000](http://localhost:8000)
- Interface Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)

---

##  Exemple de requête

### Via Swagger / Postman :

**POST** `/chat`

```json
{
  "question": "Quels sont les horaires d’ouverture ?"
}
```

### Via `curl` :

```bash
curl -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{"question": "Quels sont les horaires d’ouverture ?"}'
```

---

##  Mettre à jour les documents

Si vous modifiez les fichiers `.txt`, reconstruisez l’index FAISS :

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
├── build.py                  # Construction de l’index
├── requirements-dev.txt     # Dépendances Python
├── .env                      # Clé API Gemini (non versionné)
├── Dockerfile                # Image Docker
└── docker-compose.yml        # Orchestration Docker
```

---

##  Optimisations

- Nettoyage des réponses (suppression des phrases vagues)
- Structure des réponses améliorée (titres, paragraphes, listes)
- Prompt médical rassurant et adapté au public local
- Séparation claire entre récupération et génération

---

##  Auteur

**Abdoulaye DIAW**  
 [https://abdoulaye-diaw.vercel.app/](https://abdoulaye-diaw.vercel.app/)  
 Projet personnel autour de la RAG appliquée au secteur de la santé à Dakar.
