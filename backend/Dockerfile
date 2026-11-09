# Image de l'API DropZone, en deux étapes.

# --- Étape 1 : installer les dépendances dans un environnement virtuel ---
FROM python:3.12-slim AS deps

WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# On copie seulement la liste des dépendances : tant qu'elle ne change pas,
# Docker réutilise cette couche en cache, même si le code change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Étape 2 : l'image finale, avec seulement le nécessaire ---
FROM python:3.12-slim

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Utilisateur sans droits root.
RUN useradd --create-home --uid 10001 app

WORKDIR /app
COPY --from=deps /opt/venv /opt/venv
COPY app ./app
# Sans PostgreSQL, l'API crée un fichier SQLite dans /app : l'utilisateur doit pouvoir y écrire.
RUN chown app:app /app

USER app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
