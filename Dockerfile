# Dockerfile - SenSante

# Image Python légère
FROM python:3.11-slim

# Dossier de travail
WORKDIR /app

# Copier requirements.txt
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Copier tout le projet
COPY . .

# Port utilisé par Hugging Face Spaces
EXPOSE 7860

# Lancer FastAPI avec Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]