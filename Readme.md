#  Chatbot Clinique de l'Amitié

Un chatbot intelligent basé sur LangChain et Gemini, capable de répondre aux questions liées aux services de la Clinique de l’Amitié à Dakar.

##  Lancement rapide avec Docker

1. **Configurer vos clés API**

   Créez un fichier `.env` à la racine avec :

   ```env
   GOOGLE_API_KEY="API_KEY" 
````

2. **Construire et démarrer l’application**

   ```bash
   docker-compose up --build
   ```

3. **Accéder à la documentation**

   Ouvrez [http://localhost:8000/docs](http://localhost:8000/docs)

##  Structure du projet

```
.
├── documents/                # Textes sources (.txt)
├── faiss_clinique_amitie/   # Index vectoriel FAISS (généré par build.py)
├── main.py               # API FastAPI principale
├── build.py                 # Script de construction de l’index FAISS
├── requirements-dev.txt     # Dépendances Python
├── .env                     # Clé API Google Gemini
├── Dockerfile               # Image Docker
└── docker-compose.yml       # Orchestration avec Docker Compose
```

##  Modèle utilisé

* **Embedding** : `models/embedding-001` (Google Generative AI)
* **LLM** : `gemini-1.5-flash`

## 🛠 Rebuild FAISS

Si tu ajoutes/modifies des documents `.txt` :

```bash
python build.py
```

##  Exemples de requêtes

```json
POST /chat
{
  "question": "Quels sont les horaires d’ouverture ?"
}
```


