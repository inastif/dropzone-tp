# Audit du dépôt DropZone

- **Projet audité** : DropZone (plateforme de drops de sneakers en édition limitée)
- **Dépôt** : https://github.com/inastif/dropzone-tp
- **Stack** : API Python 3.12+ (FastAPI, SQLAlchemy 2, SQLite ou PostgreSQL) et front React 19 (Vite, TypeScript)
- **Date de l'audit** : 9 novembre 2026
- **Poste de test** : Windows 11, Git 2.52, Python 3.14.0, Node 24.13.1, npm 11.8.0

Légende : ✅ OK, ⚠ partiel, ❌ absent.

## Git

| Point vérifié | ✅ | ⚠ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| Dépôt GitHub existant et accessible | ✅ | | | Dépôt public `inastif/dropzone-tp`, créé depuis le modèle du cours. |
| `.gitignore` adapté à la stack | ✅ | | | Il exclut `.env`, `*.db`, `.venv/`, `node_modules/`, `dist/` et les caches. `.env.example` est explicitement autorisé. Vérifié : après installation et lancement, `git status` reste propre. |
| Historique de commits lisible | | ⚠ | | Les messages ne sont pas du type « wip » ou « aaaa », mais l'historique est très court et aucune convention n'est imposée (« Initial commit »). |
| Branche `main` protégée | | | ❌ | Aucune règle dans Settings → Rules. Un push direct est accepté, y compris un `push --force`. |

## Build et lancement

| Point vérifié | ✅ | ⚠ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| L'application démarre en une seule commande documentée | | ⚠ | | Le README décrit le lancement, mais il faut deux terminaux : `uvicorn app.main:app --reload` pour l'API et `npm run dev` pour le front, après les installations. Testé en local sous Windows : `/health` et `/health/ready` répondent `{"status":"ok"}` sur le port 8000, `/docs` s'affiche, et le front affiche les 4 drops sur le port 5173. Piège rencontré : sous Windows, `python` pointait vers l'alias du Microsoft Store ; il a fallu utiliser `py`. |
| Les dépendances sont listées | ✅ | | | `requirements.txt` et `requirements-dev.txt` pour l'API, `package.json` et `package-lock.json` pour le front. |
| Aucun chemin absolu codé en dur | ✅ | | | Recherche faite dans le code : aucun chemin de type `C:\Users\...` ou `/home/...`. La configuration passe par des variables d'environnement. |

## Tests

| Point vérifié | ✅ | ⚠ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| Des tests existent | ✅ | | | Testé en local : `pytest` (26 tests réussis, couverture de 93 %, seuil exigé 85 %), Vitest (9 tests réussis dans 3 fichiers) et Playwright pour les tests E2E (non lancés). |
| Les tests s'exécutent en une seule commande | | ⚠ | | Il faut une commande par partie : `pytest` dans `backend/` et `npm test` dans `frontend/`. Les tests E2E exigent en plus l'application complète sur le port 8080. |

## Déploiement

| Point vérifié | ✅ | ⚠ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| La méthode de déploiement actuelle est connue et documentée | | | ❌ | Ni Dockerfile, ni `compose.yml`, ni workflow GitHub Actions. Seul un `nginx.conf` est présent, et le README ne décrit aucun déploiement. |
| Un environnement de staging existe | | | ❌ | Aucun environnement de test distinct de la production. |

## Monitoring

| Point vérifié | ✅ | ⚠ | ❌ | Constat |
|---|:-:|:-:|:-:|---|
| L'URL de production est surveillée | | | ❌ | Pas d'URL de production ni de supervision. Les routes `/health` et `/health/ready` existent et fonctionnent, mais personne ne les interroge. |
| Les logs sont accessibles | | ⚠ | | L'API écrit ses logs en texte sur la sortie standard, avec un niveau réglable (`LOG_LEVEL`). Ils ne sont ni structurés ni centralisés. |

## Bilan

**Total : 5 ✅, 4 ⚠, 4 ❌ (sur 13 points).**

## Mes 3 priorités d'amélioration

1. **Protéger `main`** : pull request obligatoire et push direct refusé, pour qu'aucun code cassé n'arrive sur la branche principale.
2. **Rendre le déploiement reproductible** : conteneuriser l'API et le front (Dockerfile, `compose.yml`), puis automatiser la livraison avec une intégration continue.
3. **Mettre en place la surveillance** : health checks Docker, logs structurés et supervision de l'URL de production.
