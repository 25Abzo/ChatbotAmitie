import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

# Configuration
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("La clé API Google n'est pas définie dans les variables d'environnement.")
EMBEDDING_MODEL = "models/embedding-001"  
DOCUMENTS_DIR = "documents"
FAISS_SAVE_PATH = "faiss_clinique_amitie"

# Étape 1 : Chargement des fichiers texte depuis le dossier documents/
documents = []
for filename in os.listdir(DOCUMENTS_DIR):
    if filename.endswith(".txt"):
        path = os.path.join(DOCUMENTS_DIR, filename)
        loader = TextLoader(path)
        doc = loader.load()
        for d in doc:
            d.metadata["source"] = filename
        documents.extend(doc)

print(f"{len(documents)} documents chargés.")

# Étape 2 : Découpage en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs_split = text_splitter.split_documents(documents)
print(f"{len(docs_split)} chunks générés.")

# Étape 3 : Génération des embeddings avec Gemini
embedding_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=API_KEY
)

# Étape 4 : Création de l’index FAISS
vector_store = FAISS.from_documents(docs_split, embedding_model)

# Étape 5 : Création du dossier FAISS s'il n'existe pas et sauvegarde
os.makedirs(FAISS_SAVE_PATH, exist_ok=True)
vector_store.save_local(FAISS_SAVE_PATH)
print(f"✅ Index FAISS sauvegardé dans : {FAISS_SAVE_PATH}")
