# DropZone

Plateforme de **drops** de sneakers en édition limitée : un drop met en vente un nombre fixe de paires à une heure précise, et les acheteurs commandent jusqu'à épuisement du stock.

> Projet pédagogique (BTS SIO SLAM, cours « Introduction DevOps »). L'application fonctionne ; il lui manque tout ce qui permet de la livrer et de l'exploiter : conteneurs, intégration continue, déploiement, monitoring. C'est l'objet du TP. L'application n'a pas d'authentification.

## Fonctionnalités

- Liste des drops avec leur statut (`upcoming`, `live`, `sold_out`), un filtre par statut et un compte à rebours avant l'ouverture.
- Page détail d'un drop avec un bouton « Commander ».
- Une commande décrémente le stock, sans jamais vendre deux fois la dernière paire (décrément atomique en base).
- Données de démonstration insérées au premier démarrage.

## Stack

| Partie | Technologies |
|---|---|
| API (`backend/`) | Python 3.12, FastAPI, SQLAlchemy 2, SQLite en local ou PostgreSQL, pytest, Ruff |
| Front (`frontend/`) | React 19, Vite, TypeScript, ESLint, Vitest + Testing Library, Playwright |

## Lancer le projet en local (sans Docker)

Prérequis : Git, Python 3.12 ou plus récent, Node.js 22.12 ou plus récent.

**API**, dans un premier terminal :

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate              # Windows : .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

- L'API répond sur <http://localhost:8000> ; documentation interactive sur <http://localhost:8000/docs>.
- Par défaut, elle utilise une base SQLite locale (fichier `backend/dropzone.db`, ignoré par Git), créée et remplie au premier démarrage.
- Pour utiliser une base PostgreSQL existante, définir la variable `DATABASE_URL` avant de lancer uvicorn :
  `DATABASE_URL=postgresql+psycopg://utilisateur:motdepasse@localhost:5432/dropzone`.

**Front**, dans un second terminal :

```bash
cd frontend
npm ci
npm run dev
```

Le front est servi sur <http://localhost:5173> ; les appels à `/api` sont redirigés vers l'API sur le port 8000.

## Qualité et tests

```bash
# backend/ (venv activé)
ruff check .              # lint
ruff format --check .     # format
pytest                    # tests + couverture (minimum 85 %)

# frontend/
npm run lint              # ESLint
npm run typecheck         # TypeScript
npm test                  # Vitest
npm run build             # build de production (dossier dist/)
npm run test:e2e          # Playwright : nécessite l'application complète sur http://localhost:8080
```

Les tests Playwright visent l'adresse `http://localhost:8080` (variable `E2E_BASE_URL` pour en viser une autre). Avant le premier lancement : `npx playwright install chromium`.

## API

| Requête | Réponse |
|---|---|
| `GET /health` | `200` : le processus répond (liveness) |
| `GET /health/ready` | `200` si la base répond, `503` sinon (readiness) |
| `GET /drops?status=live` | `200` : la liste triée par id, filtre facultatif `upcoming`, `live` ou `sold_out` |
| `GET /drops/{id}` | `200` le drop · `404` |
| `POST /drops` | `201` le drop créé · `422` données invalides |
| `POST /drops/{id}/orders` | `201` la commande · `404` · `409` drop pas encore ouvert ou épuisé |

Un drop : `id`, `product`, `description`, `price_cents` (entier, en centimes), `stock`, `remaining`, `opens_at` (RFC 3339) et `status`, calculé à chaque lecture.

```bash
curl -X POST localhost:8000/drops -H 'Content-Type: application/json' \
  -d '{"product":"Air Max 1","price_cents":18000,"stock":100,"opens_at":"2026-01-01T09:00:00Z"}'
curl -X POST localhost:8000/drops/1/orders
```

## Configuration

La configuration passe par des variables d'environnement (ou un fichier `backend/.env`, jamais commité).

| Variable | Rôle | Défaut |
|---|---|---|
| `DATABASE_URL` | URL SQLAlchemy de la base | `sqlite:///./dropzone.db` |
| `LOG_LEVEL` | niveau des logs | `INFO` |
| `SEED_DEMO_DATA` | insérer les données de démo si la base est vide | `true` |
| `CORS_ORIGINS` | origines autorisées, séparées par des virgules (front servi depuis un autre domaine) | vide |
| `VITE_API_URL` | URL de l'API pour le front, fixée au build | `/api` |
| `API_PROXY_TARGET` | API vers laquelle `npm run dev` redirige `/api` | `http://localhost:8000` |

## Structure du projet

```text
.
├── backend/                 API FastAPI
│   ├── app/                 code (routes, services, domaine, modèles)
│   ├── tests/               tests pytest (SQLite en mémoire)
│   ├── pyproject.toml       configuration Ruff et pytest
│   └── requirements*.txt    dépendances épinglées
└── frontend/                application React
    ├── src/                 composants, pages et tests Vitest
    ├── e2e/                 tests Playwright
    ├── nginx.conf           configuration nginx pour servir le front dans un conteneur
    └── playwright.config.ts
```

## Ce qu'il reste à faire

Le détail des consignes est dans la fiche **« TP DropZone »**. En résumé :

1. Remettre le dépôt d'aplomb : README, branche `main` protégée, Conventional Commits, première version taguée.
2. Conteneuriser : images Docker de l'API et du front, `compose.yml` avec PostgreSQL, `.env.example`.
3. Intégration continue : workflow GitHub Actions (lint, tests, E2E), tests manquants, badge.
4. Déploiement continu : images publiées sur ghcr.io, front sur GitHub Pages, release à chaque tag.
5. Observer : health checks Docker, logs structurés, métriques `/metrics`, supervision avec Uptime Kuma.

## Licence

MIT.
