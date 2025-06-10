import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Nouvelle importation
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS  
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

# Configuration
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("La clé API Google n'est pas définie dans les variables d'environnement.")
EMBEDDING_MODEL = "models/embedding-001"  
LLM_MODEL = "gemini-1.5-flash"
FAISS_PATH = "faiss_clinique_amitie"

# Chargement FAISS
embedding_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=API_KEY
)
vector_store = FAISS.load_local(
    FAISS_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

# FastAPI app
app = FastAPI(
    title="Chatbot Clinique de l'Amitié",
    description="API RAG pour répondre aux questions concernant la Clinique de l'Amitié à Dakar.",
    version="1.0.0",
    docs_url="/docs"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle pour la requête utilisateur
class UserMessage(BaseModel):
    question: str

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/chat")
async def chatbot_interaction(user_message: UserMessage):  # Changé en async
    query = user_message.question

    # Recherche dans les documents vectorisés
    retrieved_docs = vector_store.similarity_search(query, k=3)
    if not retrieved_docs:
        return {"reponse": "Je suis désolé, je ne dispose pas d'informations sur ce sujet pour le moment. "
                           "Vous pouvez contacter notre accueil au 33 000 00 00 pour plus d'assistance."}

    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    best_doc = retrieved_docs[0]
    document_source = best_doc.metadata.get("source", "Document interne")

    # Prompt de génération
    prompt = f"""
    Tu es AmiBot, l'assistant virtuel officiel de la Clinique de l'Amitié à Dakar.
    Ton rôle est de fournir des informations fiables, précises et rassurantes aux visiteurs,
    patients ou proches qui s'interrogent sur les services, les horaires, les spécialités, etc.

    **Document utilisé** : {document_source}

    **Règles à suivre** :
    - Réponds directement à la question si l'information est présente dans les documents.
    - Si tu ne sais pas, dis-le simplement et invite à contacter l'accueil.
    - Ne mentionne jamais que tu as lu des documents.
    - Adopte un ton humain, professionnel et bienveillant, comme un agent d'accueil de la clinique.

    **Contexte** :
    {context}

    **Question posée** :
    {query}

    **Réponse :**
    """

    # Appel à Gemini
    chat_model = ChatGoogleGenerativeAI(model=LLM_MODEL, api_key=API_KEY)
    messages = [
        SystemMessage(content="Tu es AmiBot, le chatbot de la Clinique de l'Amitié. Donne des réponses professionnelles, claires et rassurantes."),
        HumanMessage(content=prompt)
    ]
    response = chat_model.invoke(messages)

    return {"reponse": response.content}