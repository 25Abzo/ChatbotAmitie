# Utilise une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY . .

# Installer les dépendances
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt

# Exposer le port utilisé par FastAPI/Uvicorn
EXPOSE 8000

# Lancer l'app FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
